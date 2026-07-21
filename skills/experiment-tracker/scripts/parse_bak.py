#!/usr/bin/env python3
"""
parse_bak.py — scan paper_dir's main.tex.bak_* files as "experiments timeline".

7/11 重定位:experiment-tracker 原本设计是基于 git log,
但 F:\Research\ 下 38 个 paper_dir **都没 git**。
用户实际用 .bak_* 文件名做论文版本备份(替代 git commit history),
所以把 .bak_* 文件级 backup 当作「准 git commit」。

每个 .bak_* 文件的演化轨迹:
  - 文件名 = "提交说明"(e.g. pre_bonferroni, post_c7_fix)
  - mtime = 提交时间
  - size / word_count / diff-to-prev = 提交改动量
  - first_100_chars = commit message 头部(LaTeX 标题)

输出 JSONL,每条 record:
{
  "paper_dir": "PAPER5_CONSOLIDATED",
  "bak_name": "main.tex.bak_pre_bonferroni",
  "bak_path": "F:\\Research\\...\\main.tex.bak_pre_bonferroni",
  "mtime": "2026-07-08T10:30:00",     # ISO format
  "size_bytes": 43693,
  "word_count": 5130,
  "stage": "pre_bonferroni",         # extracted from filename suffix
  "delta_words": -1234,              # vs prev bak, None if first
  "delta_size_bytes": -12345,        # vs prev bak
  "commit_message": "pre_bonferroni", # the human-written stage name
  "first_chars": "% Empirical Comparison...",  # LaTeX title for context
  "is_current": false                # True if this is the latest .bak_* before main.tex
}

CLI:
  python parse_bak.py --paper-dir F:\\Research\\PAPER5_CONSOLIDATED
                       [--out PATH.jsonl]
                       [--main-tex PATH]
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Iterator

# Stage keywords to extract from .bak_* filename suffixes
STAGE_KEYWORDS = [
    # Order matters: more specific first
    ("post_reviewer_D_patches", "post-reviewer-D-patches"),
    ("post_reviewer_D_fixes", "post-reviewer-D-fixes"),
    ("post_c7_fix", "post-c7-fix"),
    ("pre_reviewer_D_fixes", "pre-reviewer-D-fixes"),
    ("pre_bonferroni", "pre-bonferroni"),
    ("pre_blacklist_fix", "pre-blacklist-fix"),
    ("pre_p5_audit_fix", "pre-p5-audit-fix"),
    ("pre_unicode_fix", "pre-unicode-fix"),
    ("pre_yields_fix", "pre-yields-fix"),
    ("pre_framing", "pre-framing"),
    ("pre_polish", "pre-polish"),
    ("pre_decite", "pre-decite"),
    ("during_edit", "during-edit"),
    ("draft", "draft"),
    ("thanks_try", "thanks-try"),
    ("pre_final", "pre-final"),
    ("pre_audit", "pre-audit"),
]


def extract_stage(filename: str) -> str | None:
    """Extract the human-written stage label from 'main.tex.bak_<stage>'."""
    if not filename.startswith("main.tex.bak_"):
        return None
    suffix = filename[len("main.tex.bak_"):]
    # Try exact keyword match first
    for kw, normalized in STAGE_KEYWORDS:
        if suffix == kw or suffix.startswith(kw):
            # Strip date suffix if present (e.g. "pre_framing_20260708")
            tail = suffix[len(kw):]
            if tail and re.match(r"^_\d{6,8}$", tail):
                return f"{normalized} ({tail[1:]})"
            return normalized
    # Fallback: use whole suffix, normalize underscores to hyphens
    return suffix.replace("_", "-")


def iter_baks(paper_dir: Path, main_tex: Path | None = None) -> Iterator[Path]:
    """Yield .bak_* files sorted by mtime (oldest first)."""
    baks = sorted(paper_dir.glob("main.tex.bak_*"), key=lambda p: p.stat().st_mtime)
    yield from baks


def diff_stats(prev_text: str | None, cur_text: str) -> dict:
    """Compute word/size delta between previous bak and current."""
    if prev_text is None:
        return {"delta_words": None, "delta_size_bytes": None}
    prev_words = len(prev_text.split())
    cur_words = len(cur_text.split())
    return {
        "delta_words": cur_words - prev_words,
        "delta_size_bytes": len(cur_text.encode("utf-8")) - len(prev_text.encode("utf-8")),
    }


def scan_paper(paper_dir: Path, main_tex_override: Path | None = None) -> list[dict]:
    """Scan one paper_dir, return list of records for each .bak_*."""
    records = []
    main_tex = main_tex_override or (paper_dir / "main.tex")
    main_tex_mtime = main_tex.stat().st_mtime if main_tex.exists() else None

    baks = list(iter_baks(paper_dir))
    if not baks:
        return records

    # Read all .bak_* files into memory (paper .bak_* are typically <100KB)
    prev_text = None
    for i, b in enumerate(baks):
        try:
            text = b.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[parse_bak] WARN: cannot read {b}: {e}", file=sys.stderr)
            continue
        stats = b.stat()
        stage = extract_stage(b.name)
        delta = diff_stats(prev_text, text)
        record = {
            "paper_dir": paper_dir.name,
            "bak_name": b.name,
            "bak_path": str(b),
            "mtime": dt.datetime.fromtimestamp(stats.st_mtime).isoformat(timespec="seconds"),
            "size_bytes": stats.st_size,
            "word_count": len(text.split()),
            "stage": stage,
            "commit_message": stage or "(unknown stage)",
            "delta_words": delta["delta_words"],
            "delta_size_bytes": delta["delta_size_bytes"],
            "first_chars": text[:200].replace("\n", " ").replace("\r", " "),
            "is_current": (main_tex_mtime is not None and stats.st_mtime < main_tex_mtime
                           and (i == len(baks) - 1 or baks[i + 1].stat().st_mtime > main_tex_mtime)),
            "main_tex_size_bytes": main_tex.stat().st_size if main_tex.exists() else 0,
            "main_tex_word_count": len(main_tex.read_text(encoding="utf-8", errors="replace").split())
                                   if main_tex.exists() else 0,
        }
        records.append(record)
        prev_text = text

    # Sort by mtime ascending (already done, but explicit)
    records.sort(key=lambda r: r["mtime"])
    # Update is_current: the last .bak_* before main.tex is "the immediate predecessor"
    if records:
        # Find the bak whose mtime is closest to (but before) main.tex.mtime
        last_idx = -1
        for i, r in enumerate(records):
            if main_tex_mtime is None or r["mtime"] <= dt.datetime.fromtimestamp(main_tex_mtime).isoformat(timespec="seconds"):
                last_idx = i
        if last_idx >= 0:
            records[last_idx]["is_current"] = True

    return records


def main():
    p = argparse.ArgumentParser(description="Scan .bak_* files as experiments timeline")
    p.add_argument("--paper-dir", required=True, help="F:\\Research\\PAPER5_CONSOLIDATED etc.")
    p.add_argument("--out", default=None, help="Output JSONL path. Default: stdout")
    p.add_argument("--main-tex", default=None, help="Override main.tex path")
    args = p.parse_args()

    paper_dir = Path(args.paper_dir)
    if not paper_dir.exists():
        print(f"[parse_bak] ERROR: {paper_dir} does not exist", file=sys.stderr)
        return 1

    main_tex = Path(args.main_tex) if args.main_tex else None
    records = scan_paper(paper_dir, main_tex)

    print(f"[parse_bak] {paper_dir.name}: found {len(records)} .bak_* files", file=sys.stderr)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"[parse_bak] wrote {len(records)} records to {out_path}", file=sys.stderr)
    else:
        for r in records:
            print(json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())