#!/usr/bin/env python3
"""
scan_all_baks.py — 扫 F:\\Research\\ 所有 paper_dir 的 .bak_* 文件,生成 dashboard.

7/11 重定位后第一份"实验-tracker 接入其他 ML 实验"的真测试产物。
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RESEARCH_ROOT = Path(r"F:\Research")


def is_paper_dir(name: str) -> bool:
    return bool(re.match(
        r"^(PAPER\d+(_CONSOLIDATED)?$|tmlr_p\d+$|arxiv_\d{4}\.\d{5}$|"
        r"CONSOLIDATED_PAPER\d+$|tmlr_flagship|FLAGSHIP|.*_consolidated$)",
        name, re.I
    ))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--research-root", default=r"F:\Research")
    p.add_argument("--out-dir", default="tmp/exp_bak_test")
    args = p.parse_args()

    research_root = Path(args.research_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    paper_dirs = [d for d in sorted(research_root.iterdir())
                  if d.is_dir() and is_paper_dir(d.name)]
    print(f"[scan_all_baks] Found {len(paper_dirs)} paper dirs in {research_root}")

    summary = []
    total_baks = 0
    for paper_dir in paper_dirs:
        baks = list(paper_dir.glob("main.tex.bak_*"))
        if not baks:
            continue
        total_baks += len(baks)

        # Call parse_bak.py for this paper
        jsonl_path = out_dir / f"{paper_dir.name}_baks.jsonl"
        subprocess.run([
            "python",
            "skills/experiment-tracker/scripts/parse_bak.py",
            "--paper-dir", str(paper_dir),
            "--out", str(jsonl_path),
        ], check=True)

        # Render
        md_path = out_dir / f"{paper_dir.name}_changelog.md"
        subprocess.run([
            "python",
            "skills/experiment-tracker/scripts/render_bak_changelog.py",
            "--in", str(jsonl_path),
            "--out", str(md_path),
            "--today", datetime.now().strftime("%Y-%m-%d"),
        ], check=True)

        # Read records for summary
        records = [json.loads(line) for line in jsonl_path.open(encoding="utf-8")]
        summary.append({
            "paper": paper_dir.name,
            "bak_count": len(records),
            "first_bak": records[0]["mtime"],
            "last_bak": records[-1]["mtime"],
            "current_words": records[-1].get("main_tex_word_count", 0),
            "first_words": records[0]["word_count"],
            "delta_words": sum(r["delta_words"] for r in records if r["delta_words"]),
        })

    # Write dashboard
    dashboard_path = out_dir / "DASHBOARD.md"
    lines = []
    lines.append(f"# 📊 Experiment-Tracker — `.bak_*` Dashboard ({datetime.now().strftime('%Y-%m-%d')})")
    lines.append("")
    lines.append(f"> 自动生成 from `experiment-tracker` skill(7/11 重定位)。")
    lines.append(f"> 扫描了 **{len(paper_dirs)}** 个 paper_dir,其中 **{len(summary)}** 个有 `.bak_*` 文件,共 **{total_baks}** 个 backup。")
    lines.append("")
    lines.append("| Paper | .bak_ 数 | 时间范围 | 首 bak 字数 | 当前 main.tex | 净增 |")
    lines.append("|---|---|---|---|---|---|")
    for s in sorted(summary, key=lambda x: -x["bak_count"]):
        lines.append(f"| **{s['paper']}** | {s['bak_count']} | "
                     f"{s['first_bak']} → {s['last_bak']} | "
                     f"{s['first_words']:,} | {s['current_words']:,} | "
                     f"{s['delta_words']:+,}w |")
    lines.append("")
    lines.append("## 📂 Per-paper changelogs")
    lines.append("")
    for s in sorted(summary, key=lambda x: x["paper"]):
        lines.append(f"- `{s['paper']}` → `tmp/exp_bak_test/{s['paper']}_changelog.md`")
    lines.append("")

    dashboard_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[scan_all_baks] Dashboard: {dashboard_path}")
    print(f"[scan_all_baks] Summary: {len(summary)} papers with {total_baks} total .bak_* files")


if __name__ == "__main__":
    main()