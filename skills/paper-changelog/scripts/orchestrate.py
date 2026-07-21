#!/usr/bin/env python3
"""
orchestrate.py — paper-changelog 一键串联:
  scan_facts.py → aggregate_research.py → render_changelog.py

用法:
  python orchestrate.py --research-root F:\\Research --today 2026-07-10
"""
import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PYTHON = sys.executable


def run_step(name: str, args: list[str], cwd: Path) -> bool:
    print(f"\n{'=' * 60}")
    print(f"📦 {name}")
    print(f"{'=' * 60}")
    cmd = [PYTHON, *args]
    print(f"$ {' '.join(cmd)} (cwd={cwd})")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ {name} failed with exit code {result.returncode}")
        return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--research-root", default=r"F:\Research")
    parser.add_argument("--scan-output", default="tmp/paper_changelog/scan.jsonl")
    parser.add_argument("--aggregated-output", default="tmp/paper_changelog/aggregated.json")
    parser.add_argument("--render-output", default=None,
                        help="默认 knowledge/analysis/research-changelog-YYYY-MM-DD.md")
    parser.add_argument("--today", default=None)
    parser.add_argument("--keep-jsonl", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    workspace = Path.cwd()

    # Step 1: scan_facts
    if not run_step("Step 1: scan_facts.py",
                     [str(SCRIPT_DIR / "scan_facts.py"),
                      "--research-root", args.research_root,
                      "--output", args.scan_output],
                     cwd=workspace):
        sys.exit(1)

    # Step 2: aggregate_research
    if not run_step("Step 2: aggregate_research.py",
                     [str(SCRIPT_DIR / "aggregate_research.py"),
                      "--scan", args.scan_output,
                      "--output", args.aggregated_output],
                     cwd=workspace):
        sys.exit(1)

    # Step 3: render_changelog
    render_args = [str(SCRIPT_DIR / "render_changelog.py"),
                   "--aggregated", args.aggregated_output,
                   "--today", args.today or ""]
    if args.render_output:
        render_args.extend(["--output", args.render_output])

    if not run_step("Step 3: render_changelog.py", render_args, cwd=workspace):
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"✅ paper-changelog orchestrator done")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()