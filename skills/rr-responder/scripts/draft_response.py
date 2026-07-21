#!/usr/bin/env python3.11
"""
rr-responder / draft_response.py

Stage 3 of the rr-responder pipeline.

For each (critiqued) atomic sub-question, write a complete R&R response
block in three parts:
  (a) Restated question (1-2 sentences, neutralized) -- mirror for reviewer
  (b) Our response -- thank + address directly, reference paper section /
      table / figure / new experiment added
  (c) Changes made (in paper) -- bullet list, each entry is concrete
      (e.g., "Section 4.2, added 3rd paragraph explaining X")
  (d) Optional mini-Q&A table addressing the follow-ups from stage 2.

Inputs:
  --in PATH.jsonl     output from deep_critique.py
  --author-notes PATH    (optional) free-form text file: context the author
                          wants every response to draw from
                         (e.g., "We added a new ablation in §4.3").

Output:
  JSONL with one record per sub-question, each containing:
    qid, reviewer_id, atomic_question,
    restated_question, response_body, changes_in_paper (list[str]),
    followup_qa (list[{q, a}])

This stage can be chained into stage 4 (render_latex.py) which assembles
the record into a LaTeX appendix block.
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

# Fix 1 (7/11):共享 _json_safety 的 escape 容错
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _json_safety import _fix_invalid_escapes
from typing import Any

DEFAULT_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1").rstrip("/")
DEFAULT_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.environ.get("RR_MODEL", "deepseek-v4-flash")

SYSTEM_PROMPT = """你是论文作者,正在写 R&R(rebuttal)回应。要求非常严格:

1. 每条回复必须有 "We thank Reviewer X for..." 开头(中性化,不谄媚)。
2. 不能用 "future work" / "we will consider" / "out of scope" 这类搪塞式结尾。
3. 引用的章节/图/表必须明确(如 §4.2, Table 3, Figure 5)。
4. 给出的修改必须是**已发生**的(用 past tense),不是承诺。
5. 对 follow-up 必须一个个回答,不能回避。

读者会提供:
- 一条 reviewer 子问题
- reviewer 已假设的尖锐 follow-ups
- 一段「作者需要融合的全局上下文」(论文修改摘要)
- topic_hint + severity_hint + is_fatal(致命程度判定)

输出严格 JSON:
{
  "restated_question": "1-2 句中性复述,作为回应开头",
  "response_body": "2-4 段,平实学术语气;带 §X.Y / Table N 引用",
  "changes_in_paper": [
    "Section X: 增/改/删了... (1 句具体)",
    "Table N: 增/改了... (1 句)"
  ],
  "followup_qa": [
    {"q": "followup text", "a": "1-2 句简短回答"}
  ]
}

Fix 2 (7/11 打磨):followup_qa 字段规则——
- **若 is_fatal=true**:followup_qa 必须有 2-3 条最尖锐的追问回答(刻意收敛,不要无脑产出)
- **若 is_fatal=false**:followup_qa 必须为 **[] 空数组**(非致命问题不需要二次追问)
- 真实 R&R 不会每条都写 followup,过度生成会被审稿人认为是「话术填充」。

不要 markdown 包装,不要解释,只 JSON。"""


USER_TEMPLATE = """# 子问题原句
{raw}

# 中性复述
{atom}

# 锐化版
{sharp}

# Follow-ups(必须都答)
{followups}

# 作者上下文(可选;若有,则融入回答)
{notes}

# Topic / Severity
topic={topic}  severity={sev}

按要求输出 JSON。"""


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
                  max_tokens: int = 1200, retries: int = 3) -> dict[str, Any] | None:
    url = f"{DEFAULT_BASE}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": 0.3,
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
            # Fix 1 (7/11):用 _json_safety 的 escape 容错
            fixed = _fix_invalid_escapes(content)
            try:
                return json.loads(fixed, strict=False)
            except json.JSONDecodeError:
                extracted = _try_extract_json(content)
                if extracted is not None:
                    return json.loads(_fix_invalid_escapes(extracted), strict=False)
                raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
    print(f"[draft_response] call failed: {last_err}", file=sys.stderr)
    return None


def format_followups(followups: list[dict[str, Any]]) -> str:
    if not followups:
        return "(none)"
    lines = []
    for i, fu in enumerate(followups, 1):
        lines.append(f"F{i}: {fu.get('text','')}  [why_hard={fu.get('why_hard','')}]")
    return "\n".join(lines)


def process_item(item: dict[str, Any], model: str, notes: str) -> dict[str, Any]:
    user = USER_TEMPLATE.format(
        raw=item.get("raw_text", ""),
        atom=item.get("atomic_question", ""),
        sharp=item.get("sharpened_question", ""),
        followups=format_followups(item.get("followups", [])),
        notes=notes or "(none)",
        topic=item.get("topic_hint", "other"),
        sev=item.get("severity_hint", 3),
    )
    result = call_deepseek(model, SYSTEM_PROMPT, user)
    if result is None:
        return {**item,
                "restated_question": item.get("atomic_question", ""),
                "response_body": "[draft_generation_failed]",
                "changes_in_paper": [],
                "followup_qa": [],
                "_stage3_status": "failed"}
    out = {**item}
    out["restated_question"] = str(result.get("restated_question", ""))[:400]
    out["response_body"] = str(result.get("response_body", ""))[:2000]
    out["changes_in_paper"] = [str(x)[:300] for x in result.get("changes_in_paper", [])][:6]
    out["followup_qa"] = [
        {"q": str(x.get("q", ""))[:200], "a": str(x.get("a", ""))[:400]}
        for x in result.get("followup_qa", [])
    ][:6]
    out["_stage3_status"] = "ok"
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate R&R draft per sub-question.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    p.add_argument("--author-notes", dest="notes_path", default=None)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-workers", type=int, default=4)
    args = p.parse_args(argv)

    notes = ""
    if args.notes_path and os.path.exists(args.notes_path):
        with open(args.notes_path, "r", encoding="utf-8") as f:
            notes = f.read().strip()

    with open(args.in_path, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]
    if not items:
        print("[draft_response] no items; nothing to do.", file=sys.stderr)
        with open(args.out_path, "w", encoding="utf-8") as f:
            pass
        return 0

    if not DEFAULT_KEY:
        print("[draft_response] no OPENAI_API_KEY; passing items through with stubs.",
              file=sys.stderr)
        with open(args.out_path, "w", encoding="utf-8") as f:
            for it in items:
                f2 = {**it,
                      "response_body": "[no_api_key]",
                      "changes_in_paper": [],
                      "followup_qa": [],
                      "_stage3_status": "no_key"}
                f.write(json.dumps(f2, ensure_ascii=False) + "\n")
        return 0

    print(f"[draft_response] processing {len(items)} items with {args.model}, "
          f"workers={args.max_workers}", file=sys.stderr)

    out_items: list[dict[str, Any]] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = {ex.submit(process_item, it, args.model, notes): i
                   for i, it in enumerate(items)}
        done = 0
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                out_items[i] = fut.result()
            except Exception as e:
                print(f"[draft_response] item {i} failed: {e}", file=sys.stderr)
                out_items[i] = {**items[i],
                                "response_body": "[worker error]",
                                "_stage3_status": "worker_error"}
            done += 1
            if done % 5 == 0 or done == len(items):
                print(f"[draft_response] {done}/{len(items)} done", file=sys.stderr)

    with open(args.out_path, "w", encoding="utf-8") as f:
        for it in out_items:
            if it is not None:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"[draft_response] wrote {len(out_items)} drafts to {args.out_path}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())