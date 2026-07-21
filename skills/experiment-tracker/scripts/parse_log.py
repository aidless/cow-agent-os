#!/usr/bin/env python3.11
"""
experiment-tracker / parse_log.py

Parse `git log` output into structured records.

Supports Conventional Commits (type[scope]: subject). Recognized types:
  feat, fix, docs, test, refactor, perf, build, ci, chore, style, revert
  (plus arbitrary `meta` for "tmaudit meta-test" / "audit" lines).

What we extract per commit:
  - hash (short)
  - date (ISO)
  - author
  - type            (feat|fix|docs|...)
  - scope           (optional, e.g. c7, plugins, meta-test)
  - subject         (post-type line)
  - body            (rest of commit message, if any)
  - refs            (PR / issue numbers like #18, plus free text refs)
  - bug_targets     (e.g. "Bug 12", "bug 6" → ["Bug 12", "Bug 6"])
  - category_refs   (e.g. "C9", "C12" → ["C9", "C12"])
  - version_hint    (v0.X.Y in subject / body, or from `git tag --points-at`)
  - test_count      (e.g. "12 tests", "176 unit tests" → 12/176)
  - doc_anchors     (§14, §3.2, etc.)
  - raw             (raw `subject` for debugging)

Output: JSONL, one record per commit.

CLI:
  python parse_log.py --repo PATH [--since ISO] [--until ISO] [--tag TAG]
                      [--out PATH.jsonl] [--max N]

If --repo is omitted, runs in current dir. If --tag is given, also collects
all commits reachable from the tag (i.e., the commits belonging to that
version). If --since is given, restricts by date.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any

RECOGNIZED_TYPES = {
    "feat", "fix", "docs", "test", "refactor", "perf",
    "build", "ci", "chore", "style", "revert",
    "audit", "meta", "release", "deps",
}

# Conventional Commits regex (with optional scope)
CC_RE = re.compile(
    r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?\s*:\s*(?P<subject>.+)$"
)

REF_RE = re.compile(r"#\d+")
BUG_RE = re.compile(r"\b[Bb]ug\s*(\d+)\b")
CAT_RE = re.compile(r"\bC(\d{1,2})\b")  # C1..C12 audit categories
VER_RE = re.compile(r"\bv?(\d+\.\d+\.\d+)\b")
DOC_ANCHOR_RE = re.compile(r"§\s*\d+(?:\.\d+)*")
TEST_COUNT_RE = re.compile(r"(\d+)\s*(?:unit\s+)?tests?", re.IGNORECASE)


def _git(cmd: list[str], cwd: str) -> str:
    """Run a git command, return stdout (stripped). Raises on error."""
    full = ["git", *cmd]
    result = subprocess.run(full, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(cmd)} failed: {result.stderr.strip()}")
    return result.stdout


def parse_subject(subject: str) -> dict[str, Any]:
    """Parse first line of commit message into type / scope / subject."""
    m = CC_RE.match(subject.strip())
    if not m:
        return {"type": "other", "scope": None, "subject": subject.strip(),
                "cc_breaking": False}
    type_ = m.group("type").lower()
    scope = m.group("scope") or None
    sub = m.group("subject").strip()
    breaking = bool(m.group("bang"))
    # If type is not recognized, downgrade to "other"
    if type_ not in RECOGNIZED_TYPES:
        return {"type": "other", "scope": scope, "subject": sub,
                "cc_breaking": breaking}
    return {"type": type_, "scope": scope, "subject": sub,
            "cc_breaking": breaking}


def extract_metadata(text: str) -> dict[str, Any]:
    """Pull auxiliary info out of the subject+body."""
    return {
        "refs": sorted(set(REF_RE.findall(text))),
        "bug_targets": sorted(set(f"Bug {n}" for n in BUG_RE.findall(text))),
        "category_refs": sorted(set(f"C{n}" for n in CAT_RE.findall(text))),
        "version_hint": sorted(set(VER_RE.findall(text))),
        "doc_anchors": sorted(set(DOC_ANCHOR_RE.findall(text))),
        "test_count": [int(m.group(1)) for m in TEST_COUNT_RE.finditer(text)],
    }


def parse_repo(repo: str, since: str | None = None,
               until: str | None = None,
               tag: str | None = None,
               max_count: int | None = None) -> list[dict[str, Any]]:
    """Run git log and produce structured records."""
    # Use a printable separator since NUL survives cmd.exe poorly.
    SEP = "\x1f"   # ASCII Unit Separator, unlikely to appear in commit msgs
    END = "\x1e"   # ASCII Record Separator
    fmt = SEP.join(["%H", "%h", "%ad", "%an", "%s", "%b"]) + END
    args = ["log", f"--pretty=format:{fmt}", "--date=short"]
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")
    if max_count is not None:
        args.append(f"-n{max_count}")

    if tag:
        # Commits between tag and its parent (one release's worth)
        prev = _git(["tag", "--sort=-version:refname"], repo).strip().split("\n")
        try:
            idx = prev.index(tag)
        except ValueError:
            raise RuntimeError(f"tag {tag!r} not found")
        if idx + 1 < len(prev):
            args.append(f"{prev[idx + 1]}..{tag}")
        else:
            args.append(tag)

    raw = _git(args, repo)
    if not raw.strip():
        return []

    records: list[dict[str, Any]] = []
    for block in raw.split(END):
        block = block.strip("\n")
        if not block.strip():
            continue
        parts = block.split(SEP)
        if len(parts) < 5:
            continue
        long_hash, short_hash, date, author, subject = parts[:5]
        body = parts[5] if len(parts) > 5 else ""
        # Trim trailing SEP if present
        body = body.rstrip(SEP).strip("\n")
        text = subject + "\n" + body

        head = parse_subject(subject)
        meta = extract_metadata(text)
        rec = {
            "hash": short_hash.strip(),
            "long_hash": long_hash.strip(),
            "date": date.strip(),
            "author": author.strip(),
            **head,
            **meta,
            "raw_subject": subject.strip(),
            "body": body,
        }
        records.append(rec)
    return records


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Parse git log into structured JSONL.")
    p.add_argument("--repo", default=".",
                   help="Path to a git repository. Default: cwd.")
    p.add_argument("--since", default=None, help="ISO date, e.g. 2026-06-01.")
    p.add_argument("--until", default=None)
    p.add_argument("--tag", default=None,
                   help="Limit to commits in this version (between tag and prior tag).")
    p.add_argument("--max", type=int, default=None)
    p.add_argument("--out", required=True)
    args = p.parse_args(argv)

    records = parse_repo(
        repo=args.repo,
        since=args.since, until=args.until,
        tag=args.tag, max_count=args.max,
    )

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Quick summary on stderr
    by_type: dict[str, int] = {}
    by_scope: dict[str, int] = {}
    for r in records:
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
        sc = r["scope"] or "(none)"
        by_scope[sc] = by_scope.get(sc, 0) + 1
    print(f"[parse_log] {len(records)} commits → {args.out}", file=sys.stderr)
    if records:
        print(f"[parse_log] by_type: {by_type}", file=sys.stderr)
        top_scopes = sorted(by_scope.items(), key=lambda kv: -kv[1])[:8]
        print(f"[parse_log] top scopes: {top_scopes}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())