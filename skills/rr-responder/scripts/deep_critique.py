#!/usr/bin/env python3.11
"""
rr-responder / deep_critique.py

Stage 2 of the rr-responder pipeline (this is the "+B" half).

For each atomic sub-question produced by review2queries.py, run one LLM call
in reviewer role to:
  - restate the question even more sharply,
  - surface 2-3 "tough follow-ups" the reviewer might raise next round,
  - flag if the question is actually fatal (would justify rejection) or
    negotiable.

Input:  JSONL from stage 1.
Output: JSONL, same records enriched with:
  - sharpened_question
  - followups: [{followup_id, text, is_fatal, why}]
  - pivot_suggestion:    # brief hint for stage-3 author to address
  - _stage2_status: ok|fallback|failed

CLI:
  python deep_critique.py --in PATH.jsonl --out PATH.jsonl
                          [--model deepseek-v4-flash] [--max-workers 4]

If OPENAI_API_KEY is missing, pass-through with empty followups (so
stage 3 can still produce a draft, just without the extra rigor pass).
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

# Fix 1 (7/11 打磨):import _json_safety 共享 escape 容错 + bracketed extract
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _json_safety
from typing import Any

DEFAULT_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com/v1").rstrip("/")
DEFAULT_KEY = os.environ.get("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.environ.get("RR_MODEL", "deepseek-v4-flash")

SYSTEM_PROMPT = """你是 TMLR 的资深 reviewer,极度严厉,你见过太多作者用模糊回复敷衍。
读者会给你一条论文中的子问题。

你的任务:
1. 把问题「锐化」成可证伪的形式(使作者无法用"我们会在未来工作中考虑"糊弄)。
2. 列出 2-3 条最可能的追问(follow-ups),每条说明追问什么、为什么这条难回答。
3. 判断该问题是否「致命」(is_fatal=true 表示这条不解,paper 应拒)。
4. 给一条「pivot_suggestion」:建议作者从哪个角度回答最有力(<=40字)。

严格只输出合法 JSON:
{
  "sharpened_question": "...",
  "followups": [
    {"followup_id": "F1", "text": "...", "why_hard": "..."}
  ],
  "is_fatal": false,
  "fatal_reason": "" | "...",
  "pivot_suggestion": "..."
}

不要输出其它文字,不要 markdown 包装。"""

USER_TEMPLATE = """原子问题原句: {raw}
中性复述: {atom}
主题: {topic}
严重度(1-5): {sev}

按要求生成 critique JSON。"""


def call_deepseek(model: str, system: str, user: str,
                  max_tokens: int = 800, retries: int = 3) -> dict[str, Any] | None:
    url = f"{DEFAULT_BASE}/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
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
            # Fix 1 (7/11):用 _json_safety 的 escape 容错 + bracketed extract fallback
            fixed = _json_safety._fix_invalid_escapes(content)
            try:
                return json.loads(fixed, strict=False)
            except json.JSONDecodeError:
                extracted = _json_safety._try_extract_json(content)
                if extracted is not None:
                    return json.loads(
                        _json_safety._fix_invalid_escapes(extracted), strict=False
                    )
                raise
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
    print(f"[deep_critique] call failed: {last_err}", file=sys.stderr)
    return None


def process_item(item: dict[str, Any], model: str) -> dict[str, Any]:
    user = USER_TEMPLATE.format(
        raw=item.get("raw_text", ""),
        atom=item.get("atomic_question", ""),
        topic=item.get("topic_hint", "other"),
        sev=item.get("severity_hint", 3),
    )
    result = call_deepseek(model, SYSTEM_PROMPT, user)
    if result is None:
        return {**item,
                "sharpened_question": item.get("atomic_question", ""),
                "followups": [],
                "is_fatal": False,
                "fatal_reason": "",
                "pivot_suggestion": "",
                "_stage2_status": "failed"}
    out = {**item}
    out["sharpened_question"] = str(result.get("sharpened_question", ""))[:400]
    out["followups"] = result.get("followups", [])[:5]
    out["is_fatal"] = bool(result.get("is_fatal", False))
    out["fatal_reason"] = str(result.get("fatal_reason", ""))[:200]
    out["pivot_suggestion"] = str(result.get("pivot_suggestion", ""))[:200]
    out["_stage2_status"] = "ok"
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Critique each atomic sub-question.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-workers", type=int, default=4)
    args = p.parse_args(argv)

    with open(args.in_path, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]
    if not items:
        print("[deep_critique] no items; nothing to do.", file=sys.stderr)
        with open(args.out_path, "w", encoding="utf-8") as f:
            pass
        return 0

    if not DEFAULT_KEY:
        print("[deep_critique] no OPENAI_API_KEY; passing items through.",
              file=sys.stderr)
        with open(args.out_path, "w", encoding="utf-8") as f:
            for it in items:
                f2 = {**it, "followups": [], "_stage2_status": "no_key"}
                f.write(json.dumps(f2, ensure_ascii=False) + "\n")
        return 0

    print(f"[deep_critique] processing {len(items)} items with {args.model}",
          file=sys.stderr)

    out_items: list[dict[str, Any]] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = {ex.submit(process_item, it, args.model): i
                   for i, it in enumerate(items)}
        done = 0
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                out_items[i] = fut.result()
            except Exception as e:
                print(f"[deep_critique] item {i} failed: {e}", file=sys.stderr)
                out_items[i] = {**items[i],
                                "followups": [],
                                "_stage2_status": "worker_error"}
            done += 1
            if done % 5 == 0 or done == len(items):
                print(f"[deep_critique] {done}/{len(items)} done", file=sys.stderr)

    with open(args.out_path, "w", encoding="utf-8") as f:
        for it in out_items:
            if it is not None:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"[deep_critique] wrote {len(out_items)} items to {args.out_path}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())