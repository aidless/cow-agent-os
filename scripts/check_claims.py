#!/usr/bin/env python3
"""Recompute the root README from the tree and from pytest.

`make check` runs this file. It fails if README.md, the gated block in
PREREG.md, or tools/licenses/README.md differ from a fresh render.
Nothing here calls a model or reads git history.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
PREREG_PATH = ROOT / "PREREG.md"
FAILURES_PATH = ROOT / "FAILURE_MODES.md"
LICENSES_README = ROOT / "tools" / "licenses" / "README.md"
TOOLS_README = ROOT / "tools" / "README.md"
APP_PY = ROOT / "fortune-web-v2" / "app.py"
CHANGELOG = ROOT / "fortune-web-v2" / "CHANGELOG.md"
BENCH_DIR = ROOT / "benchmarks"

# Recorded once from `git show 9a7c090e:tools/.../LICENSE`.
# make check hashes the copies in tools/licenses/. It does not resolve the commit.
LICENSE_COMMIT = "9a7c090ed90c692dc3f15b837c42f718715906b0"
LICENSE_REMOVAL = "98ef4fabbf9a993e08badc9ad6e31493fc579a93"

LICENSE_FILES = (
    ("AionUi.LICENSE", "tools/AionUi/AionUi-main/LICENSE"),
    (
        "AutoResearchClaw.LICENSE",
        "tools/AutoResearchClaw-main/AutoResearchClaw-main/LICENSE",
    ),
    (
        "Awesome-Hacking.LICENSE",
        "tools/Awesome-Hacking/Awesome-Hacking-master/LICENSE",
    ),
    ("ECC.LICENSE", "tools/ECC/ECC-main/LICENSE"),
    (
        "TrendRadar.LICENSE",
        "tools/TrendRadar-master/TrendRadar-master/LICENSE",
    ),
)

UPSTREAM_URLS = (
    "https://github.com/iOfficeAI/AionUi",
    "https://github.com/aiming-lab/AutoResearchClaw",
    "https://github.com/Hack-with-Github/Awesome-Hacking",
    "https://github.com/affaan-m/ECC",
    "https://github.com/sansan0/TrendRadar",
)

REMOVED_PREFIXES = (
    "tools/AionUi/",
    "tools/AutoResearchClaw-main/",
    "tools/Awesome-Hacking/",
    "tools/ECC/",
    "tools/TrendRadar-master/",
)

COMBINED = (
    "tests/test_phase5_lockout.py",
    "tests/test_phase6_reset_flow.py",
)

SK_MIN = 20

LABELS = {
    "fortune-web-v2": "Flask application under test",
    "benchmarks": "Committed benchmark artifacts. The check reads the JSON files only.",
    "knowledge": "Workspace notes, not a third-party code tree",
    "skills": "Workspace skills",
    "memory": "Dated memory notes",
    "installed": "Install records",
    "tools": "Pointer README plus historical license copies. Project trees are not in HEAD.",
    "scheduler": "Workspace scheduler data",
    ".github": "Workflows and templates",
    "scripts": "Offline check that renders the root README",
    "entries": "A single file, not a directory",
    "Makefile": "Runs make check",
    "FAILURE_MODES.md": "What the check does not prove",
    "README.md": "Gated results, rendered by scripts/check_claims.py",
    "PREREG.md": "Questions. Measured numbers sit only in the gated block.",
    "AGENT.md": "Workspace identity document. Not machine-checked.",
    "RULE.md": "Workspace rules document. Not machine-checked.",
    "MEMORY.md": "Workspace memory document. Not machine-checked.",
    "WORKFLOW.md": "Workspace flow document. Not machine-checked.",
    "USER.md": "User-level notes",
    "AGENT_HISTORY.md": "Identity history",
    "CHANGELOG.md": "Repository changelog",
    "CONTRIBUTING.md": "Contributor guide",
    "CODE_OF_CONDUCT.md": "Code of conduct",
    "SECURITY.md": "Security contact",
    "SUPPORT.md": "Support notes",
    "LICENSE": "MIT license for this workspace",
    "requirements.txt": "Points at fortune-web-v2/requirements.txt",
    ".gitignore": "Ignore rules",
    ".gitattributes": "Git attributes",
    ".editorconfig": "Editor defaults",
    ".gitleaks.toml": "Secret-scan rules used by the separate gitleaks workflow",
    ".gitleaksignore": "Secret-scan ignore list",
    ".pre-commit-config.yaml": "Optional pre-commit config",
}

PROBES = (
    ("application context", "Working outside of application context"),
    ("missing OllamaQwen3Backend", "cannot import name 'OllamaQwen3Backend'"),
    ("missing login_attempts", "no such table: login_attempts"),
    ("access_token", "KeyError: 'access_token'"),
    ("password policy", "at least 3 of"),
    ("IndexError", "IndexError"),
    ("HTTP 429", "429"),
    ("status 400 vs 200", "400 == 200"),
    ("status 200 vs 400", "200 == 400"),
)

GATED_START = "<!-- GATED-FACTS:START -->"
GATED_END = "<!-- GATED-FACTS:END -->"


def die(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def git_ls_files() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        die(proc.stderr.strip() or "git ls-files failed")
    return [line for line in proc.stdout.splitlines() if line]


def parse_summary(text: str) -> dict[str, int]:
    """Parse the last pytest summary line. Warning counts are ignored."""
    chosen = None
    for line in text.splitlines():
        if " in " not in line:
            continue
        if re.search(r"\d+\s+(?:failed|passed|errors?|skipped)\b", line):
            chosen = line
    if chosen is None:
        die("pytest produced no summary line:\n" + text[-1500:])
    counts = {"failed": 0, "passed": 0, "error": 0, "skipped": 0}
    for kind, key in (
        ("failed", "failed"),
        ("passed", "passed"),
        ("skipped", "skipped"),
    ):
        match = re.search(rf"(\d+)\s+{kind}\b", chosen)
        if match:
            counts[key] = int(match.group(1))
    err = re.search(r"(\d+)\s+errors?\b", chosen)
    if err:
        counts["error"] = int(err.group(1))
    return counts


def _self_test_parser() -> None:
    samples = {
        "6 passed, 16 warnings in 0.20s": (0, 6, 0),
        "8 passed, 31 warnings in 0.18s": (0, 8, 0),
        "16 failed, 3 passed in 0.12s": (16, 3, 0),
        "3 failed, 5 passed, 17 warnings in 0.16s": (3, 5, 0),
        "1 error in 0.07s": (0, 0, 1),
        "3 failed, 11 passed, 43 warnings in 0.20s": (3, 11, 0),
    }
    for line, (failed, passed, error) in samples.items():
        got = parse_summary(line + "\n")
        if (got["failed"], got["passed"], got["error"]) != (failed, passed, error):
            die(f"parser self-test failed on {line!r}: {got}")


def run_pytest(args: list[str]) -> tuple[dict[str, int], str, int]:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=line",
            "--color=no",
            "-p",
            "no:cacheprovider",
            *args,
        ],
        cwd=ROOT / "fortune-web-v2",
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    text = proc.stdout + "\n" + proc.stderr
    counts = parse_summary(text)
    clean = counts["failed"] == 0 and counts["error"] == 0 and counts["skipped"] == 0
    if clean and proc.returncode != 0:
        die(f"pytest exit {proc.returncode} but summary was clean for {args}")
    if (not clean) and proc.returncode == 0:
        die(f"pytest exit 0 but summary was not clean for {args}")
    return counts, text, proc.returncode


def signals_in(text: str) -> list[str]:
    found = []
    lowered = text.lower()
    for label, needle in PROBES:
        hay = lowered if needle == "at least 3 of" else text
        probe = needle.lower() if needle == "at least 3 of" else needle
        if probe in hay:
            found.append(label)
    return found


def load_benchmarks() -> list[dict]:
    paths = sorted(BENCH_DIR.glob("benchmark_*.json"))
    rows = []
    for path in paths:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw, parse_float=str)
        overall = data.get("overall") or {}
        qwen = overall.get("qwen3_4b") or {}
        deepseek = overall.get("deepseek") or {}
        qwen_runs = 0
        qwen_len0 = 0
        qwen_errors = 0
        ds_errors = []
        ds_ok = 0
        for prompt in data["prompts"]:
            backends = prompt["backends"]
            for run in backends.get("qwen3_4b", {}).get("runs", []):
                qwen_runs += 1
                if "error" in run:
                    qwen_errors += 1
                else:
                    if int(run["score"]["len"]) == 0:
                        qwen_len0 += 1
            for run in backends.get("deepseek", {}).get("runs", []):
                if "error" in run:
                    ds_errors.append(run["error"])
                else:
                    ds_ok += 1
        rows.append(
            {
                "name": path.name,
                "date": str(data["started_at"])[:10],
                "runs_per_prompt": int(data["runs_per_prompt"]),
                "prompts": len(data["prompts"]),
                "qwen": qwen.get("weighted_composite"),
                "qwen_latency": qwen.get("avg_latency_sec"),
                "deepseek": deepseek.get("weighted_composite"),
                "qwen_runs": qwen_runs,
                "qwen_len0": qwen_len0,
                "qwen_errors": qwen_errors,
                "ds_errors": ds_errors,
                "ds_ok": ds_ok,
            }
        )
    if not rows:
        die("no benchmark JSON files")
    return rows


def fmt_cell(value) -> str:
    if value is None:
        return "—"
    return str(value)


def inventory(paths: list[str]) -> list[tuple[str, int, str]]:
    counts: dict[str, int] = {}
    for path in paths:
        top = path.split("/", 1)[0]
        counts[top] = counts.get(top, 0) + 1
    unknown = sorted(set(counts) - set(LABELS))
    if unknown:
        die("unlabeled tracked path: " + ", ".join(unknown))
    rows = []
    for name in sorted(counts):
        rows.append((name, counts[name], LABELS[name]))
    return rows


def detect_license(text: str) -> str:
    head = text[:800]
    if "Apache License" in head and "Version 2.0" in head:
        return "Apache License 2.0"
    if text.startswith("MIT License"):
        return "MIT License"
    if text.startswith("CC0 1.0"):
        return "CC0 1.0 Universal"
    if "GNU GENERAL PUBLIC LICENSE" in head and "Version 3" in head:
        return "GNU GPL v3"
    die("unrecognized license heading")
    return ""


def copyright_line(text: str) -> str:
    for line in text.splitlines()[:40]:
        stripped = " ".join(line.split())
        if re.match(r"Copyright\s+\(c\)", stripped, re.I):
            return stripped
    return "—"


def license_rows() -> list[dict[str, str]]:
    rows = []
    for filename, historical in LICENSE_FILES:
        path = ROOT / "tools" / "licenses" / filename
        if not path.is_file():
            die(f"missing license copy {path}")
        blob = path.read_bytes()
        text = blob.decode("utf-8")
        rows.append(
            {
                "file": filename,
                "historical": historical,
                "kind": detect_license(text),
                "copyright": copyright_line(text),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    return rows


def app_version() -> str:
    changelog = CHANGELOG.read_text(encoding="utf-8")
    match = re.search(r"^##\s+v(\d+\.\d+\.\d+)\b", changelog, re.M)
    if not match:
        die("fortune-web-v2/CHANGELOG.md has no leading version heading")
    version = match.group(1)
    app = APP_PY.read_text(encoding="utf-8")
    literals = set(re.findall(r'"version":\s*"([^"]+)"', app))
    if literals != {version}:
        die(
            "app.py version literals "
            + ", ".join(sorted(literals))
            + f" do not match CHANGELOG {version}"
        )
    head = "\n".join(app.splitlines()[:8])
    if version not in head:
        die(f"app.py module docstring does not contain {version}")
    return version


def source_ok() -> None:
    backends = (ROOT / "fortune-web-v2" / "llm_backends.py").read_text(encoding="utf-8")
    if "class OllamaQwenBackend" not in backends:
        die("llm_backends.py does not define OllamaQwenBackend")
    if "class OllamaQwen3Backend" in backends:
        die("llm_backends.py defines OllamaQwen3Backend; the README sentence would be false")
    for rel in ("benchmark_llm.py", "tests/test_llm_backends.py"):
        text = (ROOT / "fortune-web-v2" / rel).read_text(encoding="utf-8")
        if "OllamaQwen3Backend" not in text:
            die(f"{rel} no longer imports OllamaQwen3Backend")
    app = APP_PY.read_text(encoding="utf-8")
    fn = re.search(r"def _validate_question\(.*?\n(?=def |\Z)", app, re.S)
    if not fn or "jsonify(" not in fn.group(0):
        die("_validate_question does not call jsonify")
    if 'DB_PATH = LOG_DIR / "readings.db"' not in app:
        die("app.py no longer sets DB_PATH from readings.db")


def secret_scan(paths: list[str]) -> None:
    pattern = re.compile(rf"sk-[A-Za-z0-9]{{{SK_MIN},}}")
    for rel in paths:
        path = ROOT / rel
        if not path.is_file():
            continue
        data = path.read_bytes()
        if b"\0" in data[:1024]:
            continue
        text = data.decode("utf-8", "replace")
        match = pattern.search(text)
        if match:
            die(f"secret-shaped token in {rel} (length {len(match.group(0))})")


def workflow_ok() -> None:
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    if not workflows:
        die("no workflows")
    for path in workflows:
        text = path.read_text(encoding="utf-8")
        versions = re.findall(r'python-version:\s*"([^"]+)"', text)
        for version in versions:
            if version != "3.12":
                die(f"{path.name} uses Python {version}, not 3.12")
    for name in ("ci.yml", "pr-checks.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        if "make check" not in text:
            die(f"{name} does not run make check")
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    if re.search(r"\d+\s+failed", ci):
        die("ci.yml still hard-codes a failed-test count")


def knowledge_ok(paths: list[str]) -> list[str]:
    extra = []
    for rel in paths:
        if not rel.startswith("knowledge/"):
            continue
        if rel.endswith("/LICENSE") or rel.endswith("/LICENSE.md"):
            die(f"unexpected LICENSE inside knowledge: {rel}")
        if not rel.endswith(".md"):
            extra.append(rel)
    return sorted(extra)


def forbidden_absent(paths: list[str]) -> None:
    for rel in paths:
        for prefix in REMOVED_PREFIXES:
            if rel.startswith(prefix):
                die(f"removed tree is back in HEAD: {rel}")


def tools_readme_ok() -> None:
    text = TOOLS_README.read_text(encoding="utf-8")
    for url in UPSTREAM_URLS:
        if url not in text:
            die(f"tools/README.md is missing {url}")
    needle = "tools/licenses/"
    if needle not in text:
        die("tools/README.md does not point at tools/licenses/")


def failure_modes_ok() -> None:
    text = FAILURES_PATH.read_text(encoding="utf-8")
    if re.search(r"\d", text):
        die("FAILURE_MODES.md contains a digit; counted results belong in README.md")
    if "make check" not in text:
        die("FAILURE_MODES.md does not name make check")


def compile_app() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "compileall", "-q", "app.py", "auth_routes.py"],
        cwd=ROOT / "fortune-web-v2",
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        die(proc.stderr.strip() or "compileall failed")


def collect() -> dict:
    _self_test_parser()
    source_ok()
    compile_app()
    paths = git_ls_files()
    forbidden_absent(paths)
    secret_scan(paths)
    workflow_ok()
    tools_readme_ok()
    failure_modes_ok()
    version = app_version()
    extras = knowledge_ok(paths)
    test_files = sorted(
        str(p.relative_to(ROOT / "fortune-web-v2")).replace("\\", "/")
        for p in (ROOT / "fortune-web-v2" / "tests").glob("test_*.py")
    )
    for rel in COMBINED:
        if rel not in test_files:
            die(f"missing expected test file {rel}")
    per_file = []
    for rel in test_files:
        counts, output, _code = run_pytest([rel])
        per_file.append(
            {
                "rel": rel,
                "counts": counts,
                "signals": signals_in(output) if (counts["failed"] or counts["error"]) else [],
            }
        )
    combined_counts, combined_out, _code = run_pytest(list(COMBINED))
    benches = load_benchmarks()
    return {
        "paths": paths,
        "inventory": inventory(paths),
        "version": version,
        "knowledge_extra": extras,
        "licenses": license_rows(),
        "tests": per_file,
        "combined": {
            "counts": combined_counts,
            "signals": signals_in(combined_out),
        },
        "benchmarks": benches,
    }


def _join(items: list[str]) -> str:
    if not items:
        return "—"
    return "; ".join(items)


def _clean_rows(facts: dict) -> list[dict]:
    rows = [
        row
        for row in facts["tests"]
        if row["counts"]["failed"] == 0
        and row["counts"]["error"] == 0
        and row["counts"]["skipped"] == 0
    ]
    if {row["rel"] for row in rows} != set(COMBINED):
        got = ", ".join(row["rel"] for row in rows) or "(none)"
        die(
            "clean test files are "
            + got
            + "; scripts/check_claims.py assumes the combined pair is exactly that set"
        )
    return rows


def result_paragraph(facts: dict) -> str:
    tests = facts["tests"]
    clean = _clean_rows(facts)
    clean_bits = [
        f"`{row['rel']}` ({row['counts']['passed']} passed, 0 failed)"
        for row in clean
    ]
    benches = facts["benchmarks"]
    dates = sorted({row["date"] for row in benches})
    qwen_vals = [row["qwen"] for row in benches if row["qwen"] is not None]
    qmin = min(qwen_vals, key=float)
    qmax = max(qwen_vals, key=float)
    date_bit = (
        f"every `started_at` date is {dates[0]}"
        if len(dates) == 1
        else "started_at dates are " + ", ".join(dates)
    )
    tracked = len(facts["paths"])
    return (
        f"Result. In separate processes, {len(clean)} of {len(tests)} test files "
        f"under `fortune-web-v2/tests/` are clean: {', '.join(clean_bits)}. "
        f"`make check` re-reads {len(benches)} files `benchmarks/benchmark_*.json`; "
        f"{date_bit}. qwen3:4b `overall.weighted_composite` in those files spans "
        f"{qmin} to {qmax}. HEAD tracks {tracked} files. "
        f"The Flask healthz version is {facts['version']}, the same token as the "
        f"first heading in `fortune-web-v2/CHANGELOG.md`."
    )


def limits_paragraph(facts: dict) -> str:
    tests = facts["tests"]
    dirty = [
        row
        for row in tests
        if not (
            row["counts"]["failed"] == 0
            and row["counts"]["error"] == 0
            and row["counts"]["skipped"] == 0
        )
    ]
    combined = facts["combined"]["counts"]
    benches = facts["benchmarks"]
    qwen_vals = [row["qwen"] for row in benches if row["qwen"] is not None]
    qmin = min(qwen_vals, key=float)
    zero_all_empty = [
        row
        for row in benches
        if row["qwen"] == qmin and row["qwen_runs"] == row["qwen_len0"] and row["qwen_errors"] == 0
    ]
    zero_other = [
        row
        for row in benches
        if row["qwen"] == qmin and row not in zero_all_empty
    ]
    qwen_error_runs = sum(row["qwen_errors"] for row in benches)
    ds_error_strings = sorted({err for row in benches for err in row["ds_errors"]})
    both = [row for row in benches if row["deepseek"] is not None and row["qwen"] is not None]
    ds_higher = sum(1 for row in both if float(row["deepseek"]) > float(row["qwen"]))
    qw_higher = sum(1 for row in both if float(row["qwen"]) > float(row["deepseek"]))
    ties = len(both) - ds_higher - qw_higher
    runs = sorted({row["runs_per_prompt"] for row in benches})
    prompts = sorted({row["prompts"] for row in benches})
    parts = [
        "Limits.",
        (
            f"{len(dirty)} test files are not clean. "
            "Their passed, failed, and error counts are in the table below and are "
            "not a repair."
        ),
        (
            "Those clean files, run together in one process, "
            f"record {combined['passed']} passed and {combined['failed']} failed"
            + (
                f" (signals: {_join(facts['combined']['signals'])})."
                if facts["combined"]["signals"]
                else "."
            )
        ),
        "Separate processes are the run this result calls clean.",
        (
            f"{len(zero_all_empty)} files have qwen weighted composite {qmin} "
            "because every qwen run in that file has `score.len` 0 and no qwen error field. "
            "That zero is empty text, not an authentication failure."
        ),
    ]
    if zero_other:
        parts.append(
            f"{len(zero_other)} other files also have qwen weighted composite {qmin} "
            "for a different reason. See the table."
        )
    if qwen_error_runs == 0:
        parts.append("No qwen run in these JSON files has an error field.")
    else:
        parts.append(f"Qwen runs with an error field: {qwen_error_runs}.")
    if len(ds_error_strings) == 1:
        error_files = [row for row in benches if row["ds_errors"]]
        n_files = len(error_files)
        omit = sum(1 for row in error_files if row["deepseek"] is None)
        parts.append(
            f"The only DeepSeek error string in these files is `{ds_error_strings[0]}`. "
            f"It appears in {n_files} files. "
            f"{omit} of those files omit DeepSeek from `overall`."
        )
    elif ds_error_strings:
        parts.append(
            "DeepSeek error strings: " + "; ".join(f"`{item}`" for item in ds_error_strings) + "."
        )
    else:
        parts.append("These files contain no DeepSeek error string.")
    ds_present = [row["deepseek"] for row in benches if row["deepseek"] is not None]
    if ds_present:
        parts.append(
            f"DeepSeek `weighted_composite` is present in {len(ds_present)} files "
            f"and spans {min(ds_present, key=float)} to {max(ds_present, key=float)}."
        )
    parts.append(
        f"Of the {len(both)} files that record both weighted composites, "
        f"DeepSeek is higher in {ds_higher}, qwen3:4b is higher in {qw_higher}, "
        + (
            "and none are ties."
            if ties == 0
            else f"and {ties} are ties."
        )
        + " That is not a ranking."
    )
    parts.append(
        "`runs_per_prompt` values in the files: "
        + ", ".join(str(item) for item in runs)
        + ". Prompt counts: "
        + ", ".join(str(item) for item in prompts)
        + "."
    )
    parts.append(
        "The workspace rules are documents and are not executed. "
        "This check does not call a model, does not run `benchmark_llm.py`, "
        "and does not walk git history."
    )
    return " ".join(parts)


def render_readme(facts: dict) -> str:
    inv = facts["inventory"]
    largest = max(inv, key=lambda row: row[1])
    lines = [
        "An agent workspace still needs an identity, rules, shared memory, and a flow, plus one application that can be tested without a live model.",
        "cow-agent-os keeps that identity and those rules in Markdown (`AGENT.md`, `RULE.md`, `MEMORY.md`, `WORKFLOW.md`) and anchors them with the Flask app in `fortune-web-v2/`.",
        "Those rules are documents. This repository does not machine-check them.",
        "",
        "# cow-agent-os",
        "",
        result_paragraph(facts),
        "",
        limits_paragraph(facts),
        "",
        "## Withdrawn",
        "",
        "Withdrawn: the qwen composite at the bottom of the range is an HTTP 401. The 401 string above is a DeepSeek error. qwen rows with that bottom score are empty text.",
        "Withdrawn: the current checkout is mostly vendored third-party code under `tools/` and `knowledge/`. `knowledge/` is workspace notes. `tools/` does not contain the old project trees. Those trees remain in git history; this check does not measure pack size and does not rewrite history.",
        "Withdrawn: one `runs_per_prompt` for every benchmark file. The values are listed above.",
        "Withdrawn: a stable DeepSeek win. The per-file comparison counts are above.",
        "Withdrawn: the two clean test files stay clean when they share a process. The one-process row is in the test table.",
        "",
        "## Tests",
        "",
        "Each file runs in its own process. The last row runs the two clean files in one process. Signals are substrings of that pytest output, not a full causal taxonomy.",
        "",
        "| File | Passed | Failed | Errors | Signals in this run |",
        "|---|---:|---:|---:|---|",
    ]
    for row in facts["tests"]:
        counts = row["counts"]
        lines.append(
            f"| `{row['rel']}` | {counts['passed']} | {counts['failed']} | {counts['error']} | {_join(row['signals'])} |"
        )
    cc = facts["combined"]["counts"]
    lines.append(
        f"| `{COMBINED[0]}` + `{COMBINED[1]}` in one process | {cc['passed']} | {cc['failed']} | {cc['error']} | {_join(facts['combined']['signals'])} |"
    )
    lines += [
        "",
        "Source facts this check also requires, independent of the counts:",
        "",
        "- `llm_backends.py` defines `OllamaQwenBackend` and does not define `OllamaQwen3Backend`.",
        "- `benchmark_llm.py` and `tests/test_llm_backends.py` name `OllamaQwen3Backend`.",
        "- `_validate_question` in `app.py` calls `jsonify`.",
        "- `app.py` sets `DB_PATH` from `readings.db`. The one-process failures above are reported from their pytest signals, not attributed to that path by this check.",
        "",
        "## Benchmark JSON files",
        "",
        "Values are the strings stored in each file's `overall` object. `—` means that backend has no `overall` entry. `make check` does not re-score the model output.",
        "",
        "| File | Date | runs/prompt | Prompts | DeepSeek weighted | qwen3:4b weighted | qwen latency (s) | qwen runs | qwen runs with len 0 | DeepSeek error runs |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in facts["benchmarks"]:
        lines.append(
            "| `{name}` | {date} | {runs} | {prompts} | {ds} | {qw} | {lat} | {qr} | {zl} | {de} |".format(
                name=row["name"],
                date=row["date"],
                runs=row["runs_per_prompt"],
                prompts=row["prompts"],
                ds=fmt_cell(row["deepseek"]),
                qw=fmt_cell(row["qwen"]),
                lat=fmt_cell(row["qwen_latency"]),
                qr=row["qwen_runs"],
                zl=row["qwen_len0"],
                de=len(row["ds_errors"]),
            )
        )
    lines += [
        "",
        "## Tracked files",
        "",
        f"Counted with `git ls-files` at HEAD. Largest top-level path: `{largest[0]}` ({largest[1]} files). The check fails if a new top-level path has no label in `scripts/check_claims.py`.",
        "",
        "| Path | Files | What it is |",
        "|---|---:|---|",
    ]
    for name, count, label in inv:
        extra = ""
        if name == "knowledge" and facts["knowledge_extra"]:
            listed = ", ".join(f"`{item}`" for item in facts["knowledge_extra"])
            extra = f" Non-markdown tracked paths: {listed}."
        label_cell = label if label.endswith(".") else label + "."
        lines.append(f"| `{name}` | {count} | {label_cell}{extra} |")
    lines += [
        "",
        "## Licenses",
        "",
        f"Workspace license: `LICENSE` and `fortune-web-v2/LICENSE` both start with `MIT License`. Copies of the removed trees' own `LICENSE` files are under `tools/licenses/`, taken from commit `{LICENSE_COMMIT}` (parent of `{LICENSE_REMOVAL}`, which dropped the trees). This check hashes those copies and reads their headings. It does not resolve the commit and it does not fetch upstream. Upstream URLs stay in `tools/README.md`; this check only requires those URL strings to remain there.",
        "",
        "| Copy | Historical path | Heading read from the copy | Copyright line in the copy | sha256 |",
        "|---|---|---|---|---|",
    ]
    for row in facts["licenses"]:
        lines.append(
            f"| `tools/licenses/{row['file']}` | `{row['historical']}` | {row['kind']} | {row['copyright']} | `{row['sha256']}` |"
        )
    lines += [
        "",
        "## How to recompute",
        "",
        "```bash",
        "pip install -r requirements.txt",
        "make check",
        "```",
        "",
        "No API key and no live model host. CI runs the same command on Python 3.12 (`.github/workflows/ci.yml` and `.github/workflows/pr-checks.yml`). The check byte-compiles `fortune-web-v2/app.py` and `fortune-web-v2/auth_routes.py`, scans tracked files for an `sk-` token of "
        + str(SK_MIN)
        + " or more alphanumeric characters, and compares this README to a fresh render. A shallow clone is enough. Git history is not an input.",
        "",
        "## Proposed GitHub About",
        "",
        proposed_about(facts),
        "",
        "GitHub About is not stored in git. The line above is the text this repository asks for. `make check` regenerates it with the counts.",
        "",
        "This file is the output of `scripts/check_claims.py`. Change the script, then run `make check`.",
        "",
    ]
    return "\n".join(lines)


def proposed_about(facts: dict) -> str:
    tests = facts["tests"]
    clean = sum(
        1
        for row in tests
        if row["counts"]["failed"] == 0
        and row["counts"]["error"] == 0
        and row["counts"]["skipped"] == 0
    )
    benches = facts["benchmarks"]
    dates = sorted({row["date"] for row in benches})
    date = dates[0] if len(dates) == 1 else ",".join(dates)
    return (
        f"Agent workspace (泰): identity, rules, shared memory, and the Flask app fortune-web-v2/. "
        f"HEAD is {len(facts['paths'])} tracked files and is not a vendored code dump; "
        f"former tools/ trees are absent (license copies only). "
        f"Offline check: {clean} of {len(tests)} test files clean in their own process; "
        f"{len(benches)} benchmark JSON files dated {date}."
    )


def render_prereg_block(facts: dict) -> str:
    return result_paragraph(facts) + "\n\n" + limits_paragraph(facts) + "\n"


def render_licenses_readme(facts: dict) -> str:
    lines = [
        "# License copies",
        "",
        "Byte copies of `LICENSE` files from the third-party trees that used to live under `tools/`.",
        f"Source commit recorded here: `{LICENSE_COMMIT}`, the parent of `{LICENSE_REMOVAL}` (`chore: drop vendored third-party trees under tools/`).",
        "These copies are not a restoration of those projects and not a fetch of current upstream.",
        "`make check` hashes the bytes and reads the heading. It does not resolve the commit.",
        "",
        "| File | Historical path | Heading | Copyright line | sha256 |",
        "|---|---|---|---|---|",
    ]
    for row in facts["licenses"]:
        lines.append(
            f"| `{row['file']}` | `{row['historical']}` | {row['kind']} | {row['copyright']} | `{row['sha256']}` |"
        )
    lines.append("")
    return "\n".join(lines)


def replace_block(text: str, new_body: str) -> str:
    if GATED_START not in text or GATED_END not in text:
        die("PREREG.md is missing gated-fact markers")
    pre, rest = text.split(GATED_START, 1)
    _old, post = rest.split(GATED_END, 1)
    return pre + GATED_START + "\n" + new_body + GATED_END + post


def outside_block(text: str) -> str:
    pre, rest = text.split(GATED_START, 1)
    _old, post = rest.split(GATED_END, 1)
    return pre + post


def mit_headers_ok() -> None:
    for rel in ("LICENSE", "fortune-web-v2/LICENSE"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if not text.startswith("MIT License"):
            die(f"{rel} does not start with MIT License")


def main() -> None:
    write = "--write" in sys.argv
    mit_headers_ok()
    facts = collect()
    readme = render_readme(facts)
    prereg = replace_block(
        PREREG_PATH.read_text(encoding="utf-8"),
        render_prereg_block(facts),
    )
    if re.search(r"\d", outside_block(prereg)):
        die("PREREG.md has a digit outside the gated block")
    licenses_doc = render_licenses_readme(facts)
    if write:
        README_PATH.write_text(readme, encoding="utf-8")
        PREREG_PATH.write_text(prereg, encoding="utf-8")
        LICENSES_README.write_text(licenses_doc, encoding="utf-8")
        print("wrote README.md, PREREG.md gated block, tools/licenses/README.md")
        return
    if README_PATH.read_text(encoding="utf-8") != readme:
        die("README.md drifted from a fresh render. Run: python3 scripts/check_claims.py --write")
    if PREREG_PATH.read_text(encoding="utf-8") != prereg:
        die("PREREG.md gated block drifted.")
    if LICENSES_README.read_text(encoding="utf-8") != licenses_doc:
        die("tools/licenses/README.md drifted.")
    print("check ok")


if __name__ == "__main__":
    main()
