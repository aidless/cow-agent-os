#!/usr/bin/env python3
"""
scan_facts.py — 扫描 F:\\Research\\ 下所有论文目录,提取 facts(确定性数据)

输出:JSON,每个 paper_dir 一条记录,字段:
  - path: 绝对路径
  - name: 目录名
  - has_main_tex: bool
  - has_protocol: bool
  - has_verify_script: bool(verify_p*.py / verify_*.py)
  - has_release_notes: bool
  - word_count: int(main.tex 字数,若无则为 0)
  - figure_count: int(\\begin{figure} 出现次数)
  - table_count: int(\\begin{table} 出现次数)
  - algorithm_count: int(\\begin{algorithm} 出现次数)
  - bak_count: int(main.tex.bak_* 数量)
  - sibling_dirs: list[str](兄弟目录)
  - file_size_kb: int(main.tex 大小,KB)

用法:
  python scan_facts.py --research-root F:\\Research --output tmp/paper_changelog/scan.jsonl
"""
import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterator


def iter_paper_dirs(research_root: Path) -> Iterator[Path]:
    """F:\\Research\\ 下,识别「可能是论文目录」的子目录.

    判定:含 main.tex 或 protocol.md 或 tmlr.sty 或 verify_p*.py.
    """
    if not research_root.exists():
        return
    for child in sorted(research_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        # 启发:含 main.tex 或 protocol.md 或 tmlr.sty
        markers = ["main.tex", "protocol.md", "tmlr.sty", "tmlr.bst"]
        if any((child / m).exists() for m in markers):
            yield child
        # 也包含 arxiv-style 目录(consolidated 系列)
        elif re.match(r"^PAPER\d+(_CONSOLIDATED)?$", child.name, re.I) or \
             re.match(r"^tmlr_p\d+$", child.name, re.I) or \
             re.match(r"^arxiv_\d{4}\.\d{5}$", child.name):
            yield child


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, re.IGNORECASE))


def scan_paper(paper_dir: Path) -> dict:
    """扫描单个 paper_dir,返回 facts 字典."""
    main_tex = paper_dir / "main.tex"
    protocol = paper_dir / "protocol.md"

    has_main = main_tex.exists()
    has_proto = protocol.exists()

    # 找 verify_p*.py
    verify_scripts = list(paper_dir.glob("verify_p*.py")) + list(paper_dir.glob("verify_*.py"))
    has_verify = len(verify_scripts) > 0

    has_release = (paper_dir / "RELEASE_NOTES.md").exists() or (paper_dir / "CHANGELOG.md").exists()

    # 读 main.tex,统计
    word_count = 0
    fig_count = 0
    tab_count = 0
    alg_count = 0
    file_size_kb = 0
    if has_main:
        text = main_tex.read_text(encoding="utf-8", errors="replace")
        word_count = len(text.split())
        file_size_kb = round(len(text.encode("utf-8")) / 1024, 1)
        fig_count = count_pattern(text, r"\\begin\{figure")
        tab_count = count_pattern(text, r"\\begin\{table")
        alg_count = count_pattern(text, r"\\begin\{algorithm")

    # .bak_* 计数
    bak_count = len(list(paper_dir.glob("main.tex.bak_*")))

    # 兄弟目录
    siblings = [s.name for s in paper_dir.parent.iterdir() if s.is_dir() and s.name != paper_dir.name]

    return {
        "path": str(paper_dir),
        "name": paper_dir.name,
        "has_main_tex": has_main,
        "has_protocol": has_proto,
        "has_verify_script": has_verify,
        "verify_script_names": [v.name for v in verify_scripts],
        "has_release_notes": has_release,
        "word_count": word_count,
        "figure_count": fig_count,
        "table_count": tab_count,
        "algorithm_count": alg_count,
        "bak_count": bak_count,
        "sibling_dirs": siblings[:20],  # 截断
        "file_size_kb": file_size_kb,
    }


def main():
    parser = argparse.ArgumentParser(description="Scan paper directories for facts")
    parser.add_argument("--research-root", default=r"F:\Research", help="F:\\Research 根目录")
    parser.add_argument("--output", default="tmp/paper_changelog/scan.jsonl", help="输出 JSONL 路径")
    args = parser.parse_args()

    research_root = Path(args.research_root)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    papers = list(iter_paper_dirs(research_root))
    print(f"[scan_facts] Found {len(papers)} paper dirs in {research_root}")

    with output_path.open("w", encoding="utf-8") as f:
        for p in papers:
            try:
                record = scan_paper(p)
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                print(f"  ✓ {record['name']}: {record['word_count']}w / "
                      f"{record['figure_count']}f / {record['bak_count']} bak")
            except Exception as e:
                print(f"  ✗ {p.name}: ERROR {e}")

    print(f"[scan_facts] Wrote {output_path}")


if __name__ == "__main__":
    main()