#!/usr/bin/env python3
"""
render_bak_changelog.py — 把 parse_bak.py 输出的 JSONL 渲染成 Markdown changelog.

7/11 新增(实验-tracker 重定位):从 git log → .bak_* 文件级 backup.
"""
import argparse
import json
from datetime import datetime
from pathlib import Path


def render_paper_changelog(records: list[dict], paper_dir: str, today: str) -> str:
    """Render one paper's .bak_* records as a changelog."""
    if not records:
        return f"# 📝 {paper_dir} — 无 .bak_* 文件\n\n> 该论文目录没有 `main.tex.bak_*` 文件,experiment-tracker 无演化痕迹可追踪。\n\n"

    lines = []
    lines.append(f"# 📝 {paper_dir} — .bak_* 演化痕迹({today})")
    lines.append("")
    lines.append(f"> 自动生成 from `experiment-tracker` skill(7/11 重定位:git log → `.bak_*` 文件级 backup)。")
    lines.append(f"> 共 **{len(records)}** 个 backup,覆盖 **{records[0]['mtime']}** → **{records[-1]['mtime']}**")
    lines.append("")

    # 总览表
    total_word_delta = sum(r["delta_words"] for r in records if r["delta_words"])
    total_size_delta = sum(r["delta_size_bytes"] for r in records if r["delta_size_bytes"])
    main_tex_size = records[-1].get("main_tex_word_count", 0)
    lines.append("## 🎯 总览")
    lines.append("")
    lines.append(f"- **当前 main.tex**: {main_tex_size} words")
    lines.append(f"- **首个 .bak_***: {records[0]['word_count']} words ({records[0]['stage']})")
    lines.append(f"- **末个 .bak_***: {records[-1]['word_count']} words ({records[-1]['stage']})")
    lines.append(f"- **总增长**: +{total_word_delta} words / +{total_size_delta} bytes(across {len(records)} backups)")
    lines.append("")

    # 演化轨迹
    lines.append("## 📅 演化轨迹(按时序)")
    lines.append("")
    for r in records:
        delta_w = r["delta_words"]
        delta_b = r["delta_size_bytes"]
        delta_w_str = f"{delta_w:+d}w" if delta_w is not None else "(start)"
        delta_b_str = f"{delta_b:+d}B" if delta_b is not None else ""
        is_current = " 📍 **CURRENT**" if r.get("is_current") else ""
        lines.append(f"### {r['mtime']} — `{r['stage']}`{is_current}")
        lines.append("")
        lines.append(f"- **Words**: {r['word_count']:,} ({delta_w_str}) | **Size**: {r['size_bytes']:,} bytes ({delta_b_str})")
        lines.append(f"- **File**: `{r['bak_name']}`")
        lines.append(f"- **Title (first 200 chars)**: {r['first_chars'][:150]}...")
        lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="input", required=True, help="Input JSONL from parse_bak.py")
    p.add_argument("--out", default=None, help="Output markdown path")
    p.add_argument("--today", default=None)
    args = p.parse_args()

    records = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    today = args.today or datetime.now().strftime("%Y-%m-%d")
    paper_dir = records[0]["paper_dir"] if records else "unknown"
    markdown = render_paper_changelog(records, paper_dir, today)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown, encoding="utf-8")
        print(f"[render_bak_changelog] wrote {out}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()