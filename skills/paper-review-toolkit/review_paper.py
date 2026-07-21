#!/usr/bin/env python3
"""
review_paper.py - Unified CLI for the Liu Zewen paper review toolkit.

Wraps the three core tools into one entry point:

  1. paper-writing-agent   (F:\\Research\\paper-writing-agent\\)
     - identify / evaluate / citations / plagiarism / ethics

  2. tmlr-review-simulator (F:\\Research\\tmlr-review-simulator\\)
     - simulate_review / multi_review / self_review / rebuttal_gen
     - paper_profile / pdf_ingest / tex_ingest

  3. tmlr_pipeline         (F:\\Research\\tmlr_pipeline\\)
     - 6-stage scaffold (s1..s6)

Plus per-paper audit scripts (verify_p<N>.py) when present in the
project directory.

USAGE
-----

  # Quick triage (no LLM, ~5 seconds, ~$0):
  python review_paper.py quick PAPER.tex

  # Standard review (one LLM call, ~$0.05):
  python review_paper.py standard PAPER.tex

  # Full multi-reviewer pipeline (3 LLM calls + self-review, ~$0.15):
  python review_paper.py full PAPER.tex

  # Generate rebuttal from an existing review:
  python review_paper.py rebuttal REVIEW.md --paper PAPER.tex

  # Per-paper audit (calls verify_p<N>.py if found in cwd):
  python review_paper.py audit

  # Whole bundle (everything we can do offline):
  python review_paper.py all PAPER.tex

  # One specific tool:
  python review_paper.py tool identify --file PAPER.tex
  python review_paper.py tool evaluate --file PAPER.tex

By default the wrapper writes outputs into ./reviews/ relative to the
current working directory. Override with --out-dir.

PATH OVERRIDES
--------------

If your tools live elsewhere, set these env vars (or edit TOOL_PATHS
below):

  REVIEW_TOOL_PWA       - paper-writing-agent root
  REVIEW_TOOL_SIM       - tmlr-review-simulator root
  REVIEW_TOOL_PIPE      - tmlr_pipeline root

DEPS
----

  pip install pdfplumber     # for PDF ingestion
  # LLM is OpenAI-compatible; set OPENAI_API_KEY (and optionally OPENAI_API_BASE).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, Optional

# ---------------------------------------------------------------------------
# Tool locations
# ---------------------------------------------------------------------------

DEFAULT_TOOL_PATHS = {
    "pwa":  r"F:\Research\paper-writing-agent",
    "sim":  r"F:\Research\tmlr-review-simulator",
    "pipe": r"F:\Research\tmlr_pipeline",
}

# Cost estimates (USD) for one LLM call, by mode. These are coarse upper
# bounds based on PAPER5's v24.0/v26.0 runs.
COST_ESTIMATES = {
    "quick":     0.00,
    "profile":   0.02,
    "standard":  0.05,
    "full":      0.15,
    "rebuttal":  0.05,
    "audit":     0.00,
    "all":       0.22,
}

BANNER = """
+---------------------------------------------------------------+
|  review_paper.py - Liu Zewen paper review toolkit wrapper     |
+---------------------------------------------------------------+
"""


def tool_paths() -> dict[str, Path]:
    """Resolve tool paths, honoring env overrides."""
    return {
        "pwa":  Path(os.environ.get("REVIEW_TOOL_PWA",  DEFAULT_TOOL_PATHS["pwa"])),
        "sim":  Path(os.environ.get("REVIEW_TOOL_SIM",  DEFAULT_TOOL_PATHS["sim"])),
        "pipe": Path(os.environ.get("REVIEW_TOOL_PIPE", DEFAULT_TOOL_PATHS["pipe"])),
    }


def which_tool(p: Path) -> Optional[Path]:
    """Return the tool root if it exists, else None."""
    return p if p.exists() else None


def print_status(label: str, ok: bool, detail: str = "") -> None:
    """Pretty-print a status line."""
    mark = "OK " if ok else "X  "
    print(f"  [{mark}] {label:<22} {detail}")


# ---------------------------------------------------------------------------
# Individual subcommands
# ---------------------------------------------------------------------------

def cmd_doctor(_args: argparse.Namespace) -> int:
    """Check that the three tools are reachable."""
    print(BANNER)
    print("Tool discovery:")
    paths = tool_paths()
    for name, p in paths.items():
        ok = which_tool(p) is not None
        print_status(name, ok, str(p))
    print()
    print("Python:", sys.executable, sys.version.split()[0])
    print("CWD   :", os.getcwd())
    return 0


def cmd_tool(args: argparse.Namespace) -> int:
    """Pass-through to paper-writing-agent's subcommands.

    NOTE: We do NOT shell out to paper_writing_agent/cli.py because of
    Bug A (eager relative imports in __init__.py break the CLI both
    as a script and as `python -m`). Instead, we re-use the same
    direct-import path as the `quick` command.
    """
    paths = tool_paths()
    pwa = which_tool(paths["pwa"])
    if pwa is None:
        print(f"ERROR: paper-writing-agent not found at {paths['pwa']}", file=sys.stderr)
        return 1

    # Find --file from toolargs
    file_arg = None
    rest = []
    it = iter(args.toolargs)
    for tok in it:
        if tok in ("--file", "-f"):
            file_arg = next(it, None)
        else:
            rest.append(tok)
    if file_arg is None:
        print("ERROR: `tool` requires --file PATH", file=sys.stderr)
        print("       e.g. python review_paper.py tool identify --file main.tex",
              file=sys.stderr)
        return 1

    sink_dir = Path("./reviews").resolve()
    sink_dir.mkdir(parents=True, exist_ok=True)
    sink = sink_dir / f"{Path(file_arg).stem}.{args.toolcmd}.md"

    rc = _run_pwa_subcommand(args.toolcmd, Path(file_arg).resolve(), sink)
    if rc == 0:
        print(f"\n  -> wrote {sink}")
        print(f"  hint: try `python review_paper.py quick {file_arg}` for the full bundle.")
    return rc


def cmd_quick(args: argparse.Namespace) -> int:
    """Heuristic-only triage, no LLM. Runs identify + evaluate + audit."""
    print(BANNER)
    paper = Path(args.paper).resolve()
    if not paper.exists():
        print(f"ERROR: paper not found: {paper}", file=sys.stderr)
        return 1

    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    print(f"Paper: {paper}")
    print(f"Out  : {out}")
    print()

    # 1. paper-writing-agent: identify + evaluate
    rc = _run_pwa_subcommand("identify", paper, out / "profile.md")
    rc2 = _run_pwa_subcommand("evaluate", paper, out / "quality.md")
    if rc != 0 and rc2 != 0:
        print("WARNING: paper-writing-agent offline; skipping profile/quality.")

    # 2. tmlr-review-simulator: paper_profile (extension-aware to bypass PDF-only bug)
    profile_rc = _run_paper_profile(paper, out / "paper_profile.md")
    if profile_rc != 0:
        print("  [--] paper_profile       (sim offline or unsupported)")

    # 3. per-paper verify_p<N>.py if present in cwd
    audit_rc = _maybe_run_verify(audit_only=True, out=out)
    if audit_rc is None:
        print("  [..] per-paper audit      (no verify_p<N>.py in cwd, skipped)")

    _print_cost("quick")
    return 0


def cmd_standard(args: argparse.Namespace) -> int:
    """One LLM-call review via simulate_review.py."""
    print(BANNER)
    paper = Path(args.paper).resolve()
    if not paper.exists():
        print(f"ERROR: paper not found: {paper}", file=sys.stderr)
        return 1

    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    print(f"Paper: {paper}")
    print(f"Out  : {out}")
    print()

    rc = _run_sim_subcommand(
        "simulate_review.py",
        [str(paper), "--out", str(out / f"{paper.stem}.review.md")],
        cwd=out,
    )
    _print_cost("standard")
    return rc


def cmd_full(args: argparse.Namespace) -> int:
    """Multi-reviewer pipeline + self-review."""
    print(BANNER)
    paper = Path(args.paper).resolve()
    if not paper.exists():
        print(f"ERROR: paper not found: {paper}", file=sys.stderr)
        return 1

    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    print(f"Paper: {paper}")
    print(f"Out  : {out}")
    print()

    # 1. multi-reviewer (3 personas + meta)
    rc1 = _run_sim_subcommand(
        "multi_review.py",
        [str(paper), "--out", str(out / f"{paper.stem}.multi")],
        cwd=out,
    )
    # 2. self-review on the meta-review (if produced)
    meta = out / f"{paper.stem}.multi" / "meta-review.md"
    if meta.exists():
        rc2 = _run_sim_subcommand(
            "self_review.py",
            [str(meta), "--out", str(out / f"{paper.stem}.multi" / "meta-review.meta.md")],
            cwd=out,
        )
    else:
        print("  [..] self-review skipped (meta-review.md not produced yet)")
        rc2 = 0

    _print_cost("full")
    return rc1 or rc2


def cmd_rebuttal(args: argparse.Namespace) -> int:
    """Generate a TMLR point-by-point rebuttal prompt + fill it."""
    print(BANNER)
    review = Path(args.review).resolve()
    paper  = Path(args.paper).resolve() if args.paper else None
    if not review.exists():
        print(f"ERROR: review not found: {review}", file=sys.stderr)
        return 1
    if paper and not paper.exists():
        print(f"ERROR: paper not found: {paper}", file=sys.stderr)
        return 1

    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    print(f"Review: {review}")
    print(f"Paper : {paper or '(none)'}")
    print(f"Out   : {out}")
    print()

    cmd_args = [str(review), "--out", str(out / f"{review.stem}.rebuttal-prompt.md")]
    if paper:
        cmd_args += ["--paper", str(paper)]
    rc = _run_sim_subcommand("rebuttal_gen.py", cmd_args, cwd=out)
    _print_cost("rebuttal")
    return rc


def cmd_audit(args: argparse.Namespace) -> int:
    """Run verify_p<N>.py if present, else print guidance."""
    print(BANNER)
    rc = _maybe_run_verify(audit_only=True, out=Path(args.out_dir).resolve())
    if rc is None:
        print("No verify_p<N>.py found in current directory.")
        print("To create one:")
        print("  copy F:\\Research\\PAPER5_CONSOLIDATED\\verify_p5.py verify_p<N>.py")
        print("  # then edit ROOT and CHECKS_CONFIG")
        return 1
    _print_cost("audit")
    return rc


def cmd_all(args: argparse.Namespace) -> int:
    """Bundle: quick + standard + full + audit (skip stages with --skip)."""
    print(BANNER)
    skip = set(args.skip or [])
    paper = Path(args.paper).resolve()
    if not paper.exists():
        print(f"ERROR: paper not found: {paper}", file=sys.stderr)
        return 1
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    rc_total = 0
    t0 = time.time()

    if "quick" not in skip:
        print(">>> Stage 1: quick profile (no LLM)")
        rc_total |= cmd_quick(argparse.Namespace(paper=str(paper), out_dir=str(out)))
    if "standard" not in skip:
        print("\n>>> Stage 2: standard single-reviewer (1 LLM call)")
        rc_total |= cmd_standard(argparse.Namespace(paper=str(paper), out_dir=str(out)))
    if "full" not in skip:
        print("\n>>> Stage 3: multi-reviewer + self-review (3+ LLM calls)")
        rc_total |= cmd_full(argparse.Namespace(paper=str(paper), out_dir=str(out)))
    if "audit" not in skip:
        print("\n>>> Stage 4: per-paper audit")
        rc = _maybe_run_verify(audit_only=True, out=out)
        if rc is None:
            print("  [..] no verify_p<N>.py; skipping")
        else:
            rc_total |= rc

    dt = time.time() - t0
    print(f"\n>>> Done in {dt:.1f}s, total estimated cost: ${COST_ESTIMATES['all']:.2f}")
    return rc_total


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_pwa_subcommand(sub: str, paper: Path, sink: Path) -> int:
    """Run a paper-writing-agent analysis and capture output to sink.

    Bypasses the buggy paper_writing_agent/__init__.py (which eagerly
    imports .core and breaks both `python cli.py` and
    `python -m paper_writing_agent.cli`). Instead, we:
      1. chdir to the pwa root,
      2. add pwa root to sys.path,
      3. import the .core modules directly,
      4. call the matching function on the paper text.

    Mapping of sub -> (module, function, paper-text-kwarg):
      identify  -> PaperTypeIdentifier.identify(text)
      evaluate  -> QualityEvaluator.evaluate(text)
      citations -> CitationChecker.check(text)
      plagiarism -> PlagiarismDetector.detect(text)
      ethics    -> EthicsReviewer.review(text)
    """
    paths = tool_paths()
    pwa = which_tool(paths["pwa"])
    if pwa is None:
        print(f"  [--] {sub:<14} (paper-writing-agent offline)")
        return 1

    # Map subcommand -> (import target, function name)
    targets = {
        "identify":   ("core.paper_type_identifier", "PaperTypeIdentifier", "identify"),
        "evaluate":   ("core.quality_evaluator",    "QualityEvaluator",    "evaluate"),
        "citations":  ("core.citation_checker",     "CitationChecker",     "check"),
        "plagiarism": ("core.plagiarism_detector",  "PlagiarismDetector",  "detect"),
        "ethics":     ("core.ethics_reviewer",      "EthicsReviewer",      "review"),
    }
    if sub not in targets:
        print(f"  [X ] unknown pwa subcommand: {sub}")
        return 2
    mod_name, cls_name, fn_name = targets[sub]

    # Read paper text
    try:
        paper_text = paper.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  [X ] {sub} cannot read paper: {e}")
        return 1

    # Set up isolated import context
    pwa_str = str(pwa)
    added = pwa_str not in sys.path
    if added:
        sys.path.insert(0, pwa_str)
    old_cwd = os.getcwd()
    try:
        os.chdir(pwa_str)
        try:
            module = __import__(mod_name)
        except Exception as e:
            print(f"  [X ] {sub} import failed: {type(e).__name__}: {e}")
            print(f"        (paper-writing-agent core may have missing deps)")
            return 1
        cls = getattr(module, cls_name)
        instance = cls()
        fn = getattr(instance, fn_name)
        result = fn(paper_text)

        # Render result to sink
        sink.parent.mkdir(parents=True, exist_ok=True)
        body = _render_pwa_result(sub, result)
        sink.write_text(body, encoding="utf-8")
        print_status(sub, True, f"-> {sink}")
        return 0
    except Exception as e:
        print(f"  [X ] {sub} crashed: {type(e).__name__}: {e}")
        return 1
    finally:
        os.chdir(old_cwd)
        if added:
            try:
                sys.path.remove(pwa_str)
            except ValueError:
                pass


def _render_pwa_result(sub: str, result) -> str:
    """Format a paper-writing-agent result dict/object into a readable md block."""
    lines: list[str] = [f"# paper-writing-agent / {sub}\n"]

    if sub == "identify":
        # identify() returns (paper_type, confidence, scores_dict)
        try:
            ptype, conf, scores = result
        except Exception:
            lines.append(f"```\n{result}\n```")
            return "\n".join(lines)
        lines.append(f"**Paper type**: {ptype}")
        lines.append(f"**Confidence**: {conf:.2%}\n")
        lines.append("**All scores:**")
        for k, v in sorted((scores or {}).items(), key=lambda x: x[1], reverse=True):
            if v:
                lines.append(f"  - {k}: {v:.2%}")

    elif sub == "evaluate":
        # QualityEvaluator returns a dict
        rd = result if isinstance(result, dict) else {"raw": str(result)}
        lines.append(f"**Overall score**: {rd.get('total_score', 0):.2%}")
        lines.append(f"**Grade**: {rd.get('grade', '?')}\n")
        lines.append("**Dimension scores:**")
        for dim, data in (rd.get("dimension_scores") or {}).items():
            if isinstance(data, dict):
                lines.append(f"  - {dim}: {data.get('score', 0):.2%} (weight {data.get('weight', 0)})")
        if rd.get("strengths"):
            lines.append("\n**Strengths:**")
            for s in rd["strengths"]:
                lines.append(f"  - {s}")
        if rd.get("weaknesses"):
            lines.append("\n**Weaknesses:**")
            for w in rd["weaknesses"]:
                lines.append(f"  - {w}")

    elif sub == "citations":
        lines.append(f"**Total issues**: {getattr(result, 'total_issues', '?')}")
        if hasattr(result, "errors"):
            lines.append(f"**Errors**: {len(result.errors)}, **Warnings**: {len(result.warnings)}")
        if hasattr(result, "issues"):
            for issue in result.issues:
                lines.append(f"  - [{getattr(issue, 'severity', '?').upper()}] {getattr(issue, 'description', str(issue))}")

    elif sub == "plagiarism":
        lines.append(f"**Overall risk**: {result.get('overall_risk', '?') if isinstance(result, dict) else getattr(result, 'overall_risk', '?')}")
        for sev in ("high", "medium", "low"):
            key = f"{sev}_severity"
            n = (result.get(key, []) if isinstance(result, dict) else getattr(result, key, []))
            lines.append(f"**{sev.title()} severity**: {len(n) if hasattr(n, '__len__') else n}")

    elif sub == "ethics":
        if isinstance(result, dict):
            lines.append(f"**Ethics score**: {result.get('overall_ethics_score', 0):.2%}")
        else:
            lines.append(f"**Ethics score**: {getattr(result, 'overall_ethics_score', 0):.2%}")
        for sev in ("high", "medium", "low"):
            key = f"{sev}_severity"
            n = (result.get(key, []) if isinstance(result, dict) else getattr(result, key, []))
            lines.append(f"**{sev.title()} severity**: {len(n) if hasattr(n, '__len__') else n}")

    else:
        lines.append(f"```\n{result}\n```")

    return "\n".join(lines) + "\n"


def _run_sim_subcommand(script: str, args: list[str], cwd: Path, prefix: str = "") -> int:
    """Run a script in tmlr-review-simulator/, capture exit code."""
    paths = tool_paths()
    sim = which_tool(paths["sim"])
    if sim is None:
        print(f"{prefix}[--] {script} (tmlr-review-simulator offline)")
        return 1
    script_path = sim / script
    if not script_path.exists():
        print(f"{prefix}[--] {script} (not found in {sim})")
        return 1
    cmd = [sys.executable, str(script_path)] + args
    print(f"{prefix}$ {' '.join(cmd)}")
    try:
        rc = subprocess.call(cmd, cwd=str(cwd))
    except KeyboardInterrupt:
        print(f"{prefix}[X ] {script} interrupted")
        return 130
    print_status(script, rc == 0, "")
    return rc


def _run_paper_profile(paper: Path, sink: Path) -> int:
    """Build a paper profile card, dispatching on file extension.

    Bypasses paper_profile.py's hardcoded pdf_ingest call (Bug B):
      .pdf -> run pdf_ingest.py (CLI)
      .tex -> run tex_ingest.py (CLI)
    The ingest scripts print a structured card to stdout, which we
    capture to sink.
    """
    paths = tool_paths()
    sim = which_tool(paths["sim"])
    if sim is None:
        return 1

    suffix = paper.suffix.lower()
    if suffix == ".pdf":
        ingest_script = sim / "pdf_ingest.py"
    elif suffix in (".tex", ".latex"):
        ingest_script = sim / "tex_ingest.py"
    else:
        # try tex first as a fallback (works for plain text too)
        ingest_script = sim / "tex_ingest.py"

    if not ingest_script.exists():
        print(f"  [--] ingest script missing: {ingest_script}")
        return 1

    cmd = [sys.executable, str(ingest_script), str(paper)]
    print(f"  $ {' '.join(cmd)}")
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print("  [X ] paper_profile ingest timed out")
        return 1
    if out.returncode != 0:
        print(f"  [X ] {ingest_script.name} failed:")
        stderr = (out.stderr or out.stdout or "").strip()
        print("       " + stderr.replace("\n", "\n       "))
        return out.returncode

    sink.parent.mkdir(parents=True, exist_ok=True)
    body = (out.stdout or "").strip()
    if not body:
        print(f"  [X ] {ingest_script.name} returned empty output")
        return 1
    sink.write_text(body + "\n", encoding="utf-8")
    print_status(f"paper_profile ({suffix})", True, f"-> {sink}")
    return 0


def _maybe_run_verify(audit_only: bool, out: Path) -> Optional[int]:
    """Find verify_p<N>.py in cwd and run it. Returns exit code, or None if absent.

    verify_p<N>.py scripts intentionally exit non-zero when findings
    exist (they're auditors, not tests). We treat any rc != 2 (which
    usually means the script crashed) as "ran successfully with findings"
    and only flag rc == 2 or no-output as failures.
    """
    cwd = Path.cwd()
    candidates = sorted(cwd.glob("verify_p*.py"))
    if not candidates:
        return None
    rc_total = 0
    for script in candidates:
        print(f"  $ {sys.executable} {script.name}")
        rc = subprocess.call([sys.executable, str(script)])
        if rc == 0:
            print_status(script.name, True, "0 findings")
        elif rc == 2:
            print_status(script.name, False, f"crashed (rc={rc})")
        else:
            # 1 = "found issues" — that's the script's job, not a wrapper failure
            print_status(script.name, True, f"audit ran (findings present, rc={rc})")
        rc_total |= rc
    return rc_total


def _print_cost(mode: str) -> None:
    c = COST_ESTIMATES.get(mode, 0.0)
    if c > 0:
        print(f"\nEstimated LLM cost: ${c:.2f}")
    else:
        print("\nEstimated LLM cost: $0.00 (heuristic only)")


# ---------------------------------------------------------------------------
# Argparse wiring
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="review_paper",
        description="Unified CLI for the Liu Zewen paper review toolkit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python review_paper.py quick main.tex\n"
            "  python review_paper.py standard main.tex --out-dir reviews/\n"
            "  python review_paper.py full main.tex\n"
            "  python review_paper.py rebuttal reviews/main.review.md --paper main.tex\n"
            "  python review_paper.py audit\n"
            "  python review_paper.py all main.tex --skip full\n"
            "  python review_paper.py tool identify --file main.tex\n"
            "  python review_paper.py doctor\n"
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    # doctor
    sub.add_parser("doctor", help="check that the three tools are reachable")

    # quick
    q = sub.add_parser("quick", help="heuristic-only triage (no LLM, ~$0)")
    q.add_argument("paper", help="path to main.tex or paper.pdf")
    q.add_argument("--out-dir", default="./reviews", help="where to write outputs (default: ./reviews)")

    # standard
    s = sub.add_parser("standard", help="single-reviewer pipeline (~1 LLM call, ~$0.05)")
    s.add_argument("paper", help="path to main.tex or paper.pdf")
    s.add_argument("--out-dir", default="./reviews")

    # full
    f = sub.add_parser("full", help="multi-reviewer + self-review (~4 LLM calls, ~$0.15)")
    f.add_argument("paper", help="path to main.tex or paper.pdf")
    f.add_argument("--out-dir", default="./reviews")

    # rebuttal
    r = sub.add_parser("rebuttal", help="generate TMLR point-by-point rebuttal")
    r.add_argument("review", help="path to existing review.md")
    r.add_argument("--paper", help="optional path to main.tex for context")
    r.add_argument("--out-dir", default="./reviews")

    # audit
    a = sub.add_parser("audit", help="run verify_p<N>.py if present in cwd")
    a.add_argument("--out-dir", default="./reviews")

    # all
    al = sub.add_parser("all", help="run quick + standard + full + audit in sequence")
    al.add_argument("paper", help="path to main.tex or paper.pdf")
    al.add_argument("--out-dir", default="./reviews")
    al.add_argument("--skip", nargs="*", choices=["quick", "standard", "full", "audit"],
                    help="stages to skip")

    # tool (direct call)
    t = sub.add_parser("tool", help="run one paper-writing-agent subcommand directly")
    t.add_argument("toolcmd", help="subcommand: identify | evaluate | citations | plagiarism | ethics")
    t.add_argument("toolargs", nargs=argparse.REMAINDER, help="extra args (e.g. --file main.tex)")

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "doctor":   cmd_doctor,
        "quick":    cmd_quick,
        "standard": cmd_standard,
        "full":     cmd_full,
        "rebuttal": cmd_rebuttal,
        "audit":    cmd_audit,
        "all":      cmd_all,
        "tool":     cmd_tool,
    }
    return dispatch[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())