#!/usr/bin/env python3.11
"""
rr-responder / review2queries.py

Stage 1 of the rr-responder pipeline.

Read a paragraph-level review (one or more reviewer comments pasted as plain
text or markdown) and split it into atomic, addressable sub-questions.

Why split? Because R&R drafts work item-by-item. A 4-paragraph reviewer
comment yields ~4 draft paragraphs. Each atomic sub-question becomes one
response block in the final R&R document.

Output: JSONL, one record per sub-question:
{
  "qid": "R1.3",                 # synthetic id, will be re-stamped in stage 4
  "reviewer_id": "R1",           # detected from headings like "Reviewer 1" or "## R1"
  "raw_text": "...original review sentence span...",
  "atomic_question": "...the question restated neutrally...",
  "topic_hint": "experimental|methodology|writing|ablation|limitation|other",
  "severity_hint": 1..5,         # LLM guess, can be edited later
  "evidence_required": "..."     # what extra experiment/analysis is needed
}

CLI:
  python review2queries.py --in PATH.txt|md --out PATH.jsonl
                           [--reviewer-id R1] [--model deepseek-v4-flash]
                           [--max-workers 4]

If OPENAI_API_KEY is missing, the script falls back to a heuristic
paragraph-level split (still useful, just less precise).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

DEFAULT_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1").rstrip("/")
DEFAULT_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.environ.get("RR_MODEL", "deepseek-v4-flash")

SYSTEM_PROMPT = """你是顶级 ML 会议(TMLR / NeurIPS / ICLR)的程序主席。
读者会贴给你一段审稿人的意见(可能合并自多条原始意见)。
你的任务:把这段意见拆分成「原子问题列表」——每个问题必须:
1. 可以独立回答(Y/N + 改论文哪一章/图/表,或加实验)
2. 不要丢失原意
3. 措辞中性化,去掉情绪化表达
4. 给出 1-5 分 severity(1=小修改,5=拒稿级)和 topic hint

严格只输出合法 JSON,格式:
{
  "reviewer_id": "R1",
  "items": [
    {"qid": "R1.1", "raw_text": "原句/原段摘录(50字内)",
     "atomic_question": "中性化复述(20字内)",
     "topic_hint": "experimental|methodology|writing|ablation|limitation|clarification|other",
     "severity_hint": 3,
     "evidence_required": "需要的实验/分析/章节修改(30字内,no evidence=no)}
  ]
}

不要输出其它文字。不要 markdown 包装。"""

USER_TEMPLATE = """reviewer 编号: {rid}
原始意见段落:
\"\"\"
{body}
\"\"\"

按要求拆分成原子问题列表并输出 JSON。"""


def _try_extract_json(text: str) -> str | None:
    """Return the first balanced {...} substring, else None."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == "\\" and in_string:
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def call_deepseek(model: str, system: str, user: str,
                  max_tokens: int = 1500, retries: int = 3) -> dict[str, Any] | None:
    url = f"{DEFAULT_BASE}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {DEFAULT_KEY}"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"].get("content", "")
            content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback: extract first balanced {...}
                extracted = _try_extract_json(content)
                if extracted is not None:
                    return json.loads(extracted)
                raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
    print(f"[review2queries] call failed after {retries} retries: {last_err}",
          file=sys.stderr)
    return None


def detect_reviewer_hint(text: str) -> str:
    """Heuristic for default reviewer id if user didn't pass --reviewer-id."""
    patterns = [
        r"Reviewer\s*([1-9])",   # "Reviewer 1"
        r"##\s*R([1-9])\b",      # "## R1"
        r"\*\*R([1-9])\*\*",     # "**R1**"
    ]
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return f"R{m.group(1)}"
    return "R1"


def fallback_paragraphs(text: str, reviewer_id: str) -> list[dict[str, Any]]:
    """No-LLM path: split review into atomic sub-questions.

    Fix 3 (7/11 打磨):升级拆分粒度——
    - 旧版:整篇 review 当 1 个 item(测试 1 暴露的坑)
    - 新版:依次尝试 markdown heading / numbered list / 段落 / 句群 4 种粒度拆

    设计意图:即使 LLM 不可用,fallback 至少拆出 3-5 个 item,而不是整篇当 1 个。
    """
    items = []
    sections = []

    # 1. 优先按 markdown heading 拆(## / ### / numbered)
    heading_sections = re.split(r"\n(?=#{1,4}\s|\d+\.|-\s\*\*[A-Z]|\*\*)", text)
    if len(heading_sections) > 1 and any("" in s for s in heading_sections):
        sections = [s.strip() for s in heading_sections if s.strip()]
    else:
        # 2. 退到段落拆(空行分隔)
        sections = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        # 3. 如果段落还是 1 个,按句号拆(中文 / 英文)
        if len(sections) == 1 and len(text) > 200:
            sentences = re.split(r"(?<=[.!?。！？])\s+|\n[•·]\s*", sections[0])
            sections = [s.strip() for s in sentences if len(s.strip()) > 30]
            # 4. 再退,按行拆(列表项)
            if len(sections) == 1:
                sections = [line.strip() for line in sections[0].split("\n") if len(line.strip()) > 30]

    # 兜底:实在拆不出来,整篇当 1 个
    if not sections:
        sections = [text]

    # 限制 item 数(避免过拆)
    MAX_ITEMS = 12
    if len(sections) > MAX_ITEMS:
        # 合并相邻的短 sections
        merged = []
        cur = ""
        for s in sections:
            if len(cur) + len(s) < 300:
                cur = (cur + "\n" + s).strip()
            else:
                if cur:
                    merged.append(cur)
                cur = s
        if cur:
            merged.append(cur)
        sections = merged[:MAX_ITEMS]

    for i, p in enumerate(sections, 1):
        items.append({
            "qid": f"{reviewer_id}.{i}",
            "reviewer_id": reviewer_id,
            "raw_text": p[:200],
            "atomic_question": p[:80] + ("..." if len(p) > 80 else ""),
            "topic_hint": "other",
            "severity_hint": 3,
            "evidence_required": "no",
            "_fallback_strategy": "markdown_heading_or_paragraph_or_sentence",
        })
    return items


def process_one(idx: int, body: str, reviewer_id: str, model: str,
                max_chars: int) -> dict[str, Any]:
    body_trim = body[:max_chars]
    user = USER_TEMPLATE.format(rid=reviewer_id, body=body_trim)
    result = call_deepseek(model, SYSTEM_PROMPT, user)
    if result is None or "items" not in result:
        return {
            "batch_idx": idx,
            "reviewer_id": reviewer_id,
            "raw_text": body_trim[:200],
            "items": fallback_paragraphs(body_trim, reviewer_id),
            "_status": "fallback" if result is None else "malformed",
        }
    return {
        "batch_idx": idx,
        "reviewer_id": reviewer_id,
        "raw_text": body_trim[:200],
        "items": result["items"],
        "_status": "ok",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Split a review into atomic sub-questions.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    p.add_argument("--reviewer-id", default=None,
                   help="Default R1 if omitted; auto-detected from text if possible.")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-workers", type=int, default=3)
    p.add_argument("--max-chars", type=int, default=6000,
                   help="Hard cap per batch; truncate long reviews to this.")
    args = p.parse_args(argv)

    with open(args.in_path, "r", encoding="utf-8") as f:
        text = f.read()

    reviewer_id = args.reviewer_id or detect_reviewer_hint(text)
    print(f"[review2queries] reviewer_id={reviewer_id}, model={args.model}, "
          f"len={len(text)}", file=sys.stderr)

    if not DEFAULT_KEY:
        print("[review2queries] no OPENAI_API_KEY; using paragraph fallback.",
              file=sys.stderr)
        items = fallback_paragraphs(text, reviewer_id)
        with open(args.out_path, "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
        print(f"[review2queries] wrote {len(items)} items to {args.out_path}",
              file=sys.stderr)
        return 0

    # Run a single LLM call on the full text (cap at max_chars).
    out = process_one(0, text, reviewer_id, args.model, args.max_chars)

    flat_items = out["items"]
    seen_qids = set()
    for i, it in enumerate(flat_items):
        qid = it.get("qid") or f"{reviewer_id}.{i+1}"
        if qid in seen_qids:
            qid = f"{reviewer_id}.{i+1}"
        it["qid"] = qid
        it["reviewer_id"] = reviewer_id
        seen_qids.add(qid)

    with open(args.out_path, "w", encoding="utf-8") as f:
        for it in flat_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    print(f"[review2queries] wrote {len(flat_items)} atomic items "
          f"(status={out.get('_status', 'ok')}) to {args.out_path}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())