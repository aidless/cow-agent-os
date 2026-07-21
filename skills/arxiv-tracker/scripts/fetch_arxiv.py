#!/usr/bin/env python3.11
"""
arxiv-tracker / fetch_arxiv.py

Fetch arxiv papers from the last N days matching a research-keyword set.

Design contract:
- Zero LLM dependency (this stage only does HTTP).
- Returns deterministic JSON to stdout (paper list with normalized fields).
- Failed / partial results MUST emit non-zero exit + stderr line.

Output schema (one JSON object per line, line-delimited):
{
  "arxiv_id": "2407.12345",
  "title": "...",
  "authors": ["...", "..."],
  "abstract": "...",
  "categories": ["cs.CL", "cs.AI"],
  "published": "2026-07-01T12:00:00Z",
  "updated": "2026-07-02T08:30:00Z",
  "pdf_url": "https://arxiv.org/pdf/2407.12345",
  "html_url": "https://arxiv.org/abs/2407.12345",
  "matched_keywords": ["multi-agent"],
  "source": "arxiv"
}

CLI:
  python fetch_arxiv.py [--days 30] [--max-results 200] [--cats cs.CL,cs.AI,cs.LG]
                        [--keywords "multi-agent,calibration,preference,..."]
                        [--out PATH]
  - default --days 30
  - default --max-results 200 (arxiv API hard cap per call is 2000 but we cap for sanity)
  - default cats: cs.CL, cs.AI, cs.LG
  - default keywords: see DEFAULT_KEYWORDS below
  - if --out given, write JSONL to that path; else to stdout
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

# --- defaults -----------------------------------------------------------------

DEFAULT_CATS = ["cs.CL", "cs.AI", "cs.LG"]
DEFAULT_KEYWORDS = [
    "multi-agent", "multi agent", "agent collaboration",
    "agent communication", "agent calibration",
    "preference", "self-evolving agent", "agent debate",
    "llm agent", "agent framework",
    "consensus", "calibration",
]

# arxiv API uses ATOM; namespace map for safe tag access
NS = {"atom": "http://www.w3.org/2005/Atom",
      "arxiv": "http://arxiv.org/schemas/atom"}

# arxiv user-agent: per arxiv.org guidance, identify yourself
USER_AGENT = "arxiv-tracker-skill/0.1 (research; mailto:liu_zewen@research.local)"

# --- helpers ------------------------------------------------------------------

def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def parse_iso(ts: str | None) -> str | None:
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        return ts


def build_query(cats: list[str], keywords: list[str]) -> str:
    """Compose arxiv API search query.
    - Category filter via cat:cs.CL OR ...
    - Keyword filter via all:term1 OR all:term2 ...
    Both branches are intersected with AND parens.
    """
    cat_branch = " OR ".join(f"cat:{c}" for c in cats)
    # `all:` searches title+abstract; safe for short keywords
    kw_branch = " OR ".join(f'all:"{k}"' for k in keywords)
    return f"({cat_branch}) AND ({kw_branch})"


def http_get(url: str, retries: int = 3, backoff: float = 2.0) -> bytes:
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:
            last_err = e
            if attempt < retries:
                wait = backoff ** attempt
                time.sleep(wait)
            else:
                break
    raise RuntimeError(f"arxiv GET failed after {retries} retries: {last_err}")


def extract_text(elem: ET.Element | None) -> str:
    if elem is None or elem.text is None:
        return ""
    return elem.text.strip()


def keyword_match(text: str, keywords: Iterable[str]) -> list[str]:
    """Substring match (case-insensitive, word-boundary aware for multi-word)."""
    t = text.lower()
    hits = []
    for kw in keywords:
        kw_l = kw.lower()
        # word-boundary for single tokens, substring for multi-word phrases
        if " " in kw_l or "-" in kw_l:
            if kw_l in t:
                hits.append(kw)
        else:
            if re.search(rf"\b{re.escape(kw_l)}\b", t):
                hits.append(kw)
    return hits


def parse_entry(entry: ET.Element, keywords: list[str]) -> dict[str, Any] | None:
    arxiv_id_raw = extract_text(entry.find("atom:id", NS))
    # arxiv id url is like http://arxiv.org/abs/2407.12345v2
    m = re.search(r"arxiv\.org/abs/([\w./\-]+)", arxiv_id_raw)
    if not m:
        return None
    arxiv_id = m.group(1)
    # strip version suffix for dedup key (keep display version separate if needed)
    arxiv_id_base = re.sub(r"v\d+$", "", arxiv_id)

    title = extract_text(entry.find("atom:title", NS)).replace("\n", " ").strip()
    abstract = extract_text(entry.find("atom:summary", NS)).replace("\n", " ").strip()

    # match against title+abstract
    matched = keyword_match(f"{title} {abstract}", keywords)
    if not matched:
        # skip noise
        return None

    authors = [extract_text(a.find("atom:name", NS))
               for a in entry.findall("atom:author", NS)]
    authors = [a for a in authors if a]

    # arxiv's <category term="..."> uses DEFAULT namespace (no arxiv: prefix);
    # only <arxiv:primary_category> uses the arxiv: prefix. So walk both.
    cats: list[str] = []
    for c in entry.findall("atom:category", NS):
        term = c.attrib.get("term")
        if term:
            cats.append(term)
    for c in entry.findall("arxiv:primary_category", NS):
        term = c.attrib.get("term")
        if term and term not in cats:
            cats.append(term)

    published = parse_iso(extract_text(entry.find("atom:published", NS)))
    updated = parse_iso(extract_text(entry.find("atom:updated", NS)))

    return {
        "arxiv_id": arxiv_id_base,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "categories": cats,
        "published": published,
        "updated": updated,
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id_base}",
        "html_url": f"https://arxiv.org/abs/{arxiv_id_base}",
        "matched_keywords": sorted(set(matched)),
        "source": "arxiv",
    }


def fetch_window(days: int, max_results: int,
                 cats: list[str], keywords: list[str]) -> list[dict[str, Any]]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    # arxiv submittedDate range is YYYYMMDDHHMM in UTC; we use coarse day precision
    date_filter = f"submittedDate:[{start.strftime('%Y%m%d')}0000 TO {end.strftime('%Y%m%d')}2359]"
    query = build_query(cats, keywords)
    full_q = f"{query} AND {date_filter}"

    base = "http://export.arxiv.org/api/query"
    results: list[dict[str, Any]] = []
    start_idx = 0
    page_size = min(100, max_results)

    while len(results) < max_results:
        params = {
            "search_query": full_q,
            "start": start_idx,
            "max_results": page_size,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{base}?{urllib.parse.urlencode(params)}"
        raw = http_get(url)

        root = ET.fromstring(raw)
        total_el = root.find("atom:totalResults", NS)
        total = int(extract_text(total_el) or "0")

        page_hits = []
        for entry in root.findall("atom:entry", NS):
            parsed = parse_entry(entry, keywords)
            if parsed is not None:
                page_hits.append(parsed)

        results.extend(page_hits)
        start_idx += page_size

        if start_idx >= total or not page_hits:
            break

        # polite pause between paginated calls
        time.sleep(3.0)

    # dedupe by arxiv_id (keep first occurrence)
    seen = set()
    deduped = []
    for r in results:
        if r["arxiv_id"] in seen:
            continue
        seen.add(r["arxiv_id"])
        deduped.append(r)

    return deduped[:max_results]


# --- CLI ----------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fetch arxiv papers in window matching keywords.")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--max-results", type=int, default=200)
    p.add_argument("--cats", type=str, default=",".join(DEFAULT_CATS))
    p.add_argument("--keywords", type=str, default=",".join(DEFAULT_KEYWORDS))
    p.add_argument("--out", type=str, default=None,
                   help="Write JSONL to this path; default stdout")
    args = p.parse_args(argv)

    cats = [c.strip() for c in args.cats.split(",") if c.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    try:
        rows = fetch_window(args.days, args.max_results, cats, keywords)
    except Exception as e:
        print(f"[fetch_arxiv] FATAL: {e}", file=sys.stderr)
        return 2

    payload = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload + ("\n" if payload else ""))
    else:
        sys.stdout.write(payload)
        if payload:
            sys.stdout.write("\n")

    print(f"[fetch_arxiv] fetched {len(rows)} unique papers (days={args.days}, cats={cats})",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())