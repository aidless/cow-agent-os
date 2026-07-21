#!/usr/bin/env python3.11
"""
rr-responder / orchestrate.py

Run stages 1 -> 2 -> 3 -> 4 in sequence on one review file.

Usage:
  python orchestrate.py --review PATH.md
                        [--author-notes PATH.txt]
                        [--work-dir tmp/rr_run_YYYYMMDD_HHMMSS]
                        [--out-md PATH.md] [--format md|latex]
                        [--skip-critique]
                        [--skip-render]

If --skip-critique is given, stage 2 is bypassed (use when budget is tight
or you only want a fast first pass).
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(cmd: list[str]) -> int:
    print(f"[orchestrate] $ {' '.join(cmd)}", file=sys.stderr)
    return subprocess.call(cmd)


def check_env() -> tuple[bool, str]:
    """Check OPENAI_API_KEY + OPENAI_API_BASE in current process env.

    Returns (is_ok, message). Key points:
    - env_config is hermes-agent internal storage, not OS env
    - subprocess inherits OS env only
    - Fix 4 (7/11 打磨): early warning before running pipeline
    """
    base = os.environ.get("OPENAI_API_BASE", "")
    key = os.environ.get("OPENAI_API_KEY", "")
    if not base:
        return False, "OPENAI_API_BASE is missing. Set with: set \"OPENAI_API_BASE=https://api.deepseek.com/v1\""
    if not key:
        # Try fallback to DEEPSEEK_API_KEY (Trap 3 from RULE.md)
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if deepseek_key:
            os.environ["OPENAI_API_KEY"] = deepseek_key
            return True, f"Using DEEPSEEK_API_KEY as fallback for OPENAI_API_KEY"
        return False, "OPENAI_API_KEY is missing. Set with: set \"OPENAI_API_KEY=sk-...\""
    return True, "OK"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="End-to-end rr-responder pipeline.")
    p.add_argument("--review", required=True)
    p.add_argument("--author-notes", default=None)
    p.add_argument("--work-dir", default=None)
    p.add_argument("--out-md", default=None,
                   help="Final assembled output (md or latex).")
    p.add_argument("--format", choices=["md", "latex"], default="md")
    p.add_argument("--skip-critique", action="store_true",
                   help="Stage 2 stub; saves ~50%% LLM cost.")
    p.add_argument("--skip-render", action="store_true",
                   help="Stop after stage 3.")
    p.add_argument("--model", default=None,
                   help="Override model (passed to all stages).")
    p.add_argument("--check-env-only", action="store_true",
                   help="Just check env and exit (for debugging).")
    args = p.parse_args(argv)

    is_ok, msg = check_env()
    if args.check_env_only:
        print(f"[orchestrate] env check: {msg}")
        return 0 if is_ok else 1
    if not is_ok:
        print(f"[orchestrate] ⚠️ {msg}", file=sys.stderr)
        print(f"[orchestrate] Pipeline will run but LLM calls will fallback to stub mode.",
              file=sys.stderr)

    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = args.work_dir or f"tmp/rr_run_{stamp}"
    os.makedirs(work_dir, exist_ok=True)

    s1 = os.path.join(work_dir, "stage1_queries.jsonl")
    s2 = os.path.join(work_dir, "stage2_critiques.jsonl")
    s3 = os.path.join(work_dir, "stage3_drafts.jsonl")
    out_md = args.out_md or os.path.join(work_dir,
                                         f"response.{args.format}")

    model_args = ["--model", args.model] if args.model else []

    # Stage 1
    cmd1 = ["python", str(HERE / "review2queries.py"),
            "--in", args.review, "--out", s1, *model_args]
    if run(cmd1) != 0:
        return 1

    # Stage 2 (optional)
    if args.skip_critique:
        print("[orchestrate] --skip-critique: copying stage1 to stage2.",
              file=sys.stderr)
        with open(s1, "r", encoding="utf-8") as r, open(s2, "w", encoding="utf-8") as w:
            w.write(r.read())
    else:
        cmd2 = ["python", str(HERE / "deep_critique.py"),
                "--in", s1, "--out", s2, *model_args]
        if run(cmd2) != 0:
            return 1

    # Stage 3
    cmd3 = ["python", str(HERE / "draft_response.py"),
            "--in", s2, "--out", s3, *model_args]
    if args.author_notes:
        cmd3 += ["--author-notes", args.author_notes]
    if run(cmd3) != 0:
        return 1

    if args.skip_render:
        print(f"[orchestrate] drafts at {s3}", file=sys.stderr)
        return 0

    # Stage 4
    cmd4 = ["python", str(HERE / "render_latex.py"),
            "--in", s3, "--out", out_md, "--format", args.format]
    if run(cmd4) != 0:
        return 1

    print(f"\n[orchestrate] ✅ all stages complete", file=sys.stderr)
    print(f"[orchestrate] intermediates in: {work_dir}", file=sys.stderr)
    print(f"[orchestrate] final output: {out_md}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())