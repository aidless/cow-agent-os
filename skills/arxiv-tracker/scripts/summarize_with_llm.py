#!/usr/bin/env python3.11
"""
arxiv-tracker / summarize_with_llm.py

Read JSONL from fetch_arxiv.py, ask DeepSeek to:
1. Write a 1-2 sentence Chinese summary.
2. Judge relevance to researcher's stated interests (1-5 stars).
3. Identify the most relevant paper in the batch as "anchor" for context.

Output: same JSONL, one row per input, with added fields:
  zh_summary, relevance, relevance_reason, anchor_arxiv_id (only on anchors).

CLI:
  python summarize_with_llm.py --in PATH.jsonl --out PATH.jsonl
                              [--model deepseek-v4-flash] [--batch-size 8]
                              [--max-concurrent 4]

If API key is missing, prints warning to stderr and writes input unchanged.
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
DEFAULT_MODEL = os.environ.get("ARXIV_TRACKER_MODEL", "deepseek-v4-flash")

SYSTEM_PROMPT = """你是刘泽文的研究助理。他的研究方向是多智能体 LLM 系统中的
通信 / 校准 / 偏好耦合。具体兴趣:多 agent 协作是否引发策略共识与校准传染,
校准能否抵消通信噪声,agent 之间偏好差异如何放大或缩小。

你的任务:
1. 用 1-2 句中文写一段「论文做了什么 + 与刘泽文主线的相关性」。
2. 给出 1-5 星的 relevance 评分(1=无关,5=高度相关到他的研究主线)。
3. 简述评分理由(中文,<=30 字)。

严格只输出合法 JSON:
{"zh_summary": "...", "relevance": 4, "relevance_reason": "..."}

不要输出其它文字、不要 markdown、不要代码块。"""

USER_TEMPLATE = """标题: {title}
作者: {authors}
分类: {cats}
摘要: {abstract}
命中关键词: {kw}
"""


def call_deepseek(model: str, system: str, user: str,
                  max_tokens: int = 400, retries: int = 3) -> dict[str, Any] | None:
    url = f"{DEFAULT_BASE}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
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
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {DEFAULT_KEY}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            content = body["choices"][0]["message"].get("content", "")
            # Strip markdown fences just in case
            content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
            return json.loads(content)
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                break
    print(f"[summarize] call failed after {retries} retries: {last_err}", file=sys.stderr)
    return None


def summarize_one(row: dict[str, Any], model: str) -> dict[str, Any]:
    user = USER_TEMPLATE.format(
        title=row.get("title", ""),
        authors=", ".join(row.get("authors", [])[:6]) + (" et al." if len(row.get("authors", [])) > 6 else ""),
        cats=", ".join(row.get("categories", [])),
        abstract=(row.get("abstract", "") or "")[:2500],
        kw=", ".join(row.get("matched_keywords", [])),
    )
    result = call_deepseek(model, SYSTEM_PROMPT, user)
    if result is None:
        return {**row,
                "zh_summary": "[LLM call failed]",
                "relevance": 0,
                "relevance_reason": "call_failed"}
    out = {**row}
    out["zh_summary"] = str(result.get("zh_summary", "")).strip()[:500]
    try:
        out["relevance"] = max(0, min(5, int(result.get("relevance", 0))))
    except (ValueError, TypeError):
        out["relevance"] = 0
    out["relevance_reason"] = str(result.get("relevance_reason", "")).strip()[:200]
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Summarize arxiv rows with DeepSeek.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-workers", type=int, default=4)
    args = p.parse_args(argv)

    if not DEFAULT_KEY:
        print("[summarize] OPENAI_API_KEY not set; copying input to output unchanged.",
              file=sys.stderr)
        with open(args.in_path, "r", encoding="utf-8") as f:
            data = f.read()
        with open(args.out_path, "w", encoding="utf-8") as f:
            f.write(data)
        return 0

    with open(args.in_path, "r", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]

    if not rows:
        with open(args.out_path, "w", encoding="utf-8") as f:
            pass
        print("[summarize] no rows to process.", file=sys.stderr)
        return 0

    print(f"[summarize] processing {len(rows)} rows with {args.model}, "
          f"workers={args.max_workers}", file=sys.stderr)

    out_rows: list[dict[str, Any] | None] = [None] * len(rows)
    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futures = {
            ex.submit(summarize_one, row, args.model): i
            for i, row in enumerate(rows)
        }
        done = 0
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                out_rows[i] = fut.result()
            except Exception as e:
                print(f"[summarize] row {i} failed: {e}", file=sys.stderr)
                out_rows[i] = {**rows[i],
                               "zh_summary": "[worker error]",
                               "relevance": 0,
                               "relevance_reason": "worker_error"}
            done += 1
            if done % 5 == 0 or done == len(rows):
                print(f"[summarize] {done}/{len(rows)} done", file=sys.stderr)

    with open(args.out_path, "w", encoding="utf-8") as f:
        for r in out_rows:
            if r is not None:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"[summarize] wrote {sum(1 for r in out_rows if r)} rows to {args.out_path}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())