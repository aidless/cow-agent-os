#!/usr/bin/env python3.11
"""
arxiv-tracker / ingest_to_vault.py

Read JSONL (output of summarize_with_llm.py) and write a vault-style markdown
file into the knowledge base, then update the knowledge index.

Vault path:
  {vault-root}/concepts/arxiv-watch/arxiv-YYYY-MM-DD.md

Index update:
  Append a single line under `## concepts` in {vault-root}/index.md:
    - [arxiv-watch YYYY-MM-DD](concepts/arxiv-watch/arxiv-YYYY-MM-DD.md) — N 篇高相关论文(≥3星)

Idempotency: a marker file
  {vault-root}/concepts/arxiv-watch/.ingested-YYYY-MM-DD
is written after a successful run; subsequent runs for the same date will
skip unless --force is given.

CLI:
  python ingest_to_vault.py --in PATH.jsonl --vault-root PATH
                            [--min-relevance 3] [--force]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from typing import Any

DEFAULT_VAULT = "knowledge"
DEFAULT_MIN_REL = 3


def today_str() -> str:
    return dt.date.today().isoformat()


def load_rows(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def marker_path(vault_root: str, day: str) -> str:
    return os.path.join(vault_root, "concepts", "arxiv-watch",
                        f".ingested-{day}")


def output_md_path(vault_root: str, day: str) -> str:
    return os.path.join(vault_root, "concepts", "arxiv-watch",
                        f"arxiv-{day}.md")


def render_markdown(day: str, rows: list[dict[str, Any]],
                    fetch_window: dict[str, Any]) -> str:
    high = [r for r in rows if int(r.get("relevance", 0)) >= 1]
    high.sort(key=lambda r: (-int(r.get("relevance", 0)), r.get("published", "")))

    cats_total: dict[str, int] = {}
    for r in rows:
        for c in r.get("categories", []) or []:
            cats_total[c] = cats_total.get(c, 0) + 1
    top_cats = sorted(cats_total.items(), key=lambda kv: -kv[1])[:5]

    kw_total: dict[str, int] = {}
    for r in rows:
        for k in r.get("matched_keywords", []) or []:
            kw_total[k] = kw_total.get(k, 0) + 1
    top_kw = sorted(kw_total.items(), key=lambda kv: -kv[1])[:5]

    lines: list[str] = []
    lines.append(f"# arxiv-watch — {day}")
    lines.append("")
    lines.append("> 自动生成的 arxiv 监控报告。来源:`arxiv-tracker` skill。")
    lines.append("")
    lines.append("## 📊 摘要统计")
    lines.append("")
    lines.append(f"- **抓取窗口**:过去 {fetch_window.get('days', 30)} 天")
    lines.append(f"- **抓取类目**:`{', '.join(fetch_window.get('cats', []))}`")
    lines.append(f"- **命中关键词总数**:`{len(rows)}`")
    lines.append(f"- **高相关(≥3星)**:`{sum(1 for r in rows if int(r.get('relevance', 0)) >= 3)}`")
    if top_cats:
        lines.append(f"- **Top 类目**:`{', '.join(f'{c}({n})' for c, n in top_cats)}`")
    if top_kw:
        lines.append(f"- **Top 命中关键词**:`{', '.join(f'{k}({n})' for k, n in top_kw)}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🔥 高相关论文(relevance ≥ 3)")
    lines.append("")

    high_rel = [r for r in rows if int(r.get("relevance", 0)) >= 3]
    if not high_rel:
        lines.append("_今日无 ≥3 星论文。_")
    else:
        for i, r in enumerate(high_rel, 1):
            stars = "⭐" * int(r.get("relevance", 0))
            lines.append(f"### {i}. {r.get('title', '(untitled)')} {stars}")
            lines.append("")
            lines.append(f"- **arxiv**:[{r.get('arxiv_id', '')}]({r.get('html_url', '')})")
            lines.append(f"- **作者**:`{', '.join(r.get('authors', [])[:6])}{' et al.' if len(r.get('authors', [])) > 6 else ''}`")
            lines.append(f"- **分类**:`{', '.join(r.get('categories', []) or [])}`")
            lines.append(f"- **发布日期**:{r.get('published', '')}")
            kw = r.get("matched_keywords", [])
            if kw:
                lines.append(f"- **命中关键词**:`{', '.join(kw)}`")
            lines.append("")
            lines.append(f"> **中文摘要**:{r.get('zh_summary', '(empty)')}")
            lines.append("")
            reason = r.get("relevance_reason", "")
            if reason:
                lines.append(f"> **评分理由**:{reason}")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 📚 全量论文(按相关度排序)")
    lines.append("")

    for i, r in enumerate(high, 1):
        stars = "⭐" * int(r.get("relevance", 0))
        lines.append(
            f"{i}. **{r.get('title', '(untitled)')}** {stars} "
            f"([{r.get('arxiv_id', '')}]({r.get('html_url', '')}))"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"_生成时间:`{dt.datetime.now(dt.timezone.utc).isoformat()}`_")
    lines.append("")
    return "\n".join(lines)


def update_index(vault_root: str, day: str, count_high: int,
                 marker: str = "-") -> None:
    """Append one line to knowledge/index.md under '## concepts' (creating if absent)."""
    index_path = os.path.join(vault_root, "index.md")
    new_line = (
        f"{marker} [arxiv-watch {day}](concepts/arxiv-watch/arxiv-{day}.md) "
        f"— {count_high} 篇高相关论文(≥3星)"
    )

    if not os.path.exists(index_path):
        # bootstrap minimal index
        header = "# Knowledge Index\n\n## concepts\n\n"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(header + new_line + "\n")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Idempotency for index: skip if exact line already present
    if new_line.strip() in text:
        return

    # If '## concepts' exists, insert after it; else create section.
    if "## concepts" in text:
        # find heading and append after its first blank line following
        idx = text.index("## concepts")
        # find end-of-section (next '## ' heading or eof)
        after = idx + len("## concepts")
        # find next '## '
        rest = text[after:]
        m = re.search(r"^## ", rest, flags=re.MULTILINE)
        if m:
            insert_at = after + m.start()
        else:
            insert_at = len(text)
        # Strip blank lines immediately after the heading so the first bullet
        # lines up flush like other sections.
        prefix = text[:insert_at].rstrip("\n") + "\n"
        suffix = text[insert_at:].lstrip("\n")
        new_text = prefix + new_line + "\n" + suffix
    else:
        # append a new section
        if not text.endswith("\n"):
            text += "\n"
        new_text = text + "\n## concepts\n\n" + new_line + "\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_text)


def parse_fetch_window(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Best-effort metadata for the vault header. Returns defaults if absent."""
    # We can't recover the original --days / --cats args here; use a compact
    # top-3 of categories observed across rows, plus a fixed days default.
    cat_counts: dict[str, int] = {}
    for r in rows:
        for c in (r.get("categories") or []):
            cat_counts[c] = cat_counts.get(c, 0) + 1
    top3 = [c for c, _ in sorted(cat_counts.items(), key=lambda kv: -kv[1])[:3]]
    return {
        "days": 30,
        "cats": top3 or ["cs.CL", "cs.AI", "cs.LG"],
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Ingest arxiv JSONL into knowledge vault.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--vault-root", default=DEFAULT_VAULT)
    p.add_argument("--min-relevance", type=int, default=DEFAULT_MIN_REL)
    p.add_argument("--force", action="store_true",
                   help="Re-run even if marker file exists for today.")
    args = p.parse_args(argv)

    day = today_str()
    marker = marker_path(args.vault_root, day)
    if os.path.exists(marker) and not args.force:
        print(f"[ingest] marker exists for {day}, skipping (use --force to override).",
              file=sys.stderr)
        return 0

    rows = load_rows(args.in_path)
    if not rows:
        print("[ingest] input has no rows; nothing to write.", file=sys.stderr)
        return 0

    fw = parse_fetch_window(rows)
    md = render_markdown(day, rows, fw)
    out_dir = os.path.dirname(output_md_path(args.vault_root, day))
    os.makedirs(out_dir, exist_ok=True)

    out_md = output_md_path(args.vault_root, day)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)

    high_count = sum(1 for r in rows if int(r.get("relevance", 0)) >= args.min_relevance)
    update_index(args.vault_root, day, high_count)

    with open(marker, "w", encoding="utf-8") as f:
        f.write(f"ingested_at={dt.datetime.now(dt.timezone.utc).isoformat()}\n"
                f"in_path={args.in_path}\n"
                f"row_count={len(rows)}\n"
                f"high_count={high_count}\n")

    print(f"[ingest] wrote {out_md} ({len(rows)} rows, {high_count} ≥ {args.min_relevance}星)",
          file=sys.stderr)
    print(f"[ingest] updated {os.path.join(args.vault_root, 'index.md')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())