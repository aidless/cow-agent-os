#!/usr/bin/env python3.11
"""
experiment-tracker / aggregate_to_notes.py

Given JSONL from parse_log.py, build a CHANGELOG-style section grouped by
commit type. Optionally filters by version / version_hint / scope.

Output: Markdown (default) or JSON of the section structure.

CLI:
  python aggregate_to_notes.py --in PATH.jsonl --out PATH.md
                               [--version v0.X.Y]
                               [--format md|json]
                               [--group-by type|scope|date]
                               [--no-stats]

Structure of the Markdown (matches Keep-a-Changelog):
  ## [{version or "Unreleased"}] - {date}
  ### Added      (feat)
  ### Changed    (refactor / perf)
  ### Fixed      (fix)
  ### Tests      (test)
  ### Docs       (docs)
  ### Build / CI (build, ci)
  ### Other      (chore, style, audit, ...)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from typing import Any

# Type → CHANGELOG section name
SECTION_FOR_TYPE = {
    "feat":     "Added",
    "fix":      "Fixed",
    "test":     "Tests",
    "docs":     "Docs",
    "refactor": "Changed",
    "perf":     "Changed",
    "build":    "Build / CI",
    "ci":       "Build / CI",
    "chore":    "Other",
    "style":    "Other",
    "revert":   "Other",
    "deps":     "Other",
    "audit":    "Other",
    "meta":     "Other",
    "release":  "Other",
}

# Within a section, ordering of subsections (so docs appear last)
SECTION_ORDER = ["Added", "Changed", "Fixed", "Tests",
                 "Build / CI", "Docs", "Other"]


def section_for(t: str) -> str:
    return SECTION_FOR_TYPE.get(t, "Other")


def format_commit_line(c: dict[str, Any]) -> str:
    """One-line CHANGELOG bullet from a commit record."""
    scope = c.get("scope")
    subj = c.get("subject", "").rstrip(".")
    prefix = f"**{scope}**: " if scope else ""
    line = f"- {prefix}{subj}"

    # Append cross-refs if we got interesting metadata
    extras = []
    if c.get("bug_targets"):
        extras.append("/".join(c["bug_targets"]))
    if c.get("category_refs"):
        extras.append("/".join(c["category_refs"]))
    if c.get("doc_anchors"):
        extras.append(" ".join(c["doc_anchors"]))
    if c.get("test_count"):
        # De-dup; show max
        extras.append(f"{max(c['test_count'])} tests")
    if extras:
        line += f"  _(refs: {', '.join(extras)})_"
    return line


def aggregate(records: list[dict[str, Any]],
              version: str | None = None) -> dict[str, Any]:
    """Return a structured dict: {version, sections: {sec: [lines]}, stats}."""
    # Filter by version if requested.
    if version:
        norm = version.lstrip("v")
        records = [r for r in records
                   if any(v.startswith(norm) for v in r.get("version_hint", []))]
        if not records:
            # fallback: nothing filtered, but allow caller to know
            pass

    # Bucket by section
    by_section: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        by_section[section_for(r["type"])].append(r)

    # Stats
    stats: dict[str, Any] = {
        "total_commits": len(records),
        "by_type": dict(Counter(r["type"] for r in records)),
        "by_section": {k: len(v) for k, v in by_section.items()},
        "first_date": min((r["date"] for r in records), default=None),
        "last_date":  max((r["date"] for r in records), default=None),
        "unique_authors": sorted(set(r["author"] for r in records)),
        "category_refs": sorted({c for r in records for c in r.get("category_refs", [])}),
        "bug_targets":  sorted({b for r in records for b in r.get("bug_targets", [])}),
        "version_hints": sorted({v for r in records for v in r.get("version_hint", [])}),
    }

    # Stable per-section ordering: newest commits first
    for sec in by_section:
        by_section[sec].sort(key=lambda r: r["date"], reverse=True)

    # Decide section version label
    version_label = version or (
        f"v{stats['version_hints'][-1]}" if stats["version_hints"] else "Unreleased"
    )

    return {
        "version": version_label,
        "sections": dict(by_section),
        "stats": stats,
    }


def render_md(agg: dict[str, Any], no_stats: bool = False) -> str:
    lines: list[str] = []
    lines.append(f"## [{agg['version']}] — {agg['stats']['first_date']} → {agg['stats']['last_date']}")
    lines.append("")

    if not no_stats:
        s = agg["stats"]
        lines.append(f"_Commits: {s['total_commits']} · "
                     f"Authors: {', '.join(s['unique_authors'])}_")
        if s["category_refs"]:
            lines.append(f"_Audit categories touched: {', '.join(s['category_refs'])}_")
        if s["bug_targets"]:
            lines.append(f"_Bugs closed: {', '.join(s['bug_targets'])}_")
        lines.append("")

    for sec in SECTION_ORDER:
        records = agg["sections"].get(sec, [])
        if not records:
            continue
        lines.append(f"### {sec}")
        lines.append("")
        for r in records:
            lines.append(format_commit_line(r))
        lines.append("")
    return "\n".join(lines)


def render_json(agg: dict[str, Any]) -> str:
    return json.dumps(agg, ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Aggregate commit records into a CHANGELOG section.")
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", dest="out_path", required=True)
    p.add_argument("--version", default=None,
                   help="Filter commits to those whose version_hint matches.")
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--no-stats", action="store_true")
    args = p.parse_args(argv)

    records = [json.loads(l) for l in open(args.in_path, encoding="utf-8") if l.strip()]
    agg = aggregate(records, version=args.version)
    out = render_md(agg, no_stats=args.no_stats) if args.format == "md" else render_json(agg)

    os.makedirs(os.path.dirname(args.out_path) or ".", exist_ok=True)
    with open(args.out_path, "w", encoding="utf-8") as f:
        f.write(out)

    print(f"[aggregate] version={agg['version']}, "
          f"sections={list(agg['sections'].keys())}, "
          f"commits={agg['stats']['total_commits']} → {args.out_path}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())