#!/usr/bin/env python3
"""
render_changelog.py — aggregated.json → Markdown 研究级 CHANGELOG.

产物:knowledge/analysis/research-changelog-YYYY-MM-DD.md
"""
import argparse
import json
from datetime import datetime
from pathlib import Path


STATUS_ORDER = [
    "🟢 audit-ready / final",
    "🟡 needs-audit",
    "🟠 stub-with-tex",
    "🔴 stub-only",
]


def render_status_emoji(status: str) -> str:
    return status.split()[0]


def render_paper_section(p: dict) -> str:
    """单个论文的 Markdown section."""
    lines = []
    emoji = render_status_emoji(p["status"])
    lines.append(f"### {emoji} `{p['name']}`")
    lines.append("")
    lines.append(f"- **状态**: {p['status']}")
    lines.append(f"- **路径**: `{p['path']}`")
    if p["has_main_tex"]:
        lines.append(f"- **字数 / 图表**: {p['word_count']} words / "
                     f"{p['figure_count']} figs / {p['table_count']} tables / "
                     f"{p['algorithm_count']} algorithms")
        lines.append(f"- **main.tex 大小**: {p['file_size_kb']} KB")
    else:
        lines.append("- **字数 / 图表**: (无 main.tex)")
    lines.append(f"- **协议 / 验证 / Release Notes**: "
                 f"{'✓' if p['has_protocol'] else '✗'} / "
                 f"{'✓' if p['has_verify_script'] else '✗'} / "
                 f"{'✓' if p['has_release_notes'] else '✗'}")
    lines.append(f"- **Audit score**: {p['audit_score']} / 11")
    if p["verify_script_names"]:
        lines.append(f"- **Verify scripts**: {', '.join(p['verify_script_names'])}")
    if p["bak_count"]:
        lines.append(f"- **.bak_*** files: {p['bak_count']}")
    lines.append("")

    # Fix 2(7/11 打磨):显示 narrative-facts 矛盾
    if p.get("narrative_conflict"):
        lines.append(f"> **{p['narrative_conflict']}**")
        lines.append("")

    # narrative
    if p.get("trajectory") and not p["trajectory"].startswith("<!--"):
        lines.append(f"**演化轨迹**: {p['trajectory']}")
        lines.append("")
    if p.get("next_step") and not p["next_step"].startswith("<!--"):
        lines.append(f"**下一步**: {p['next_step']}")
        lines.append("")

    return "\n".join(lines)


def render_summary(summary: dict, papers: list[dict] | None = None) -> str:
    lines = []
    lines.append("## 🎯 总览")
    lines.append("")
    lines.append(f"- **论文目录总数**: {summary['total_papers']}")
    lines.append(f"- **含 main.tex**: {summary['with_main_tex']}")
    lines.append(f"- **含 protocol.md**: {summary['with_protocol']}")
    lines.append(f"- **含 verify_*.py**: {summary['with_verify_script']}")
    lines.append(f"- **含 RELEASE_NOTES.md / CHANGELOG.md**: {summary['with_release_notes']}")
    lines.append(f"- **CONSOLIDATED 系列**: {summary['consolidated_count']}")
    lines.append("")
    lines.append("### 状态分布")
    lines.append("")
    for status in STATUS_ORDER:
        papers = summary["by_status"].get(status, [])
        lines.append(f"- **{status}**: {len(papers)} 篇")
    lines.append("")
    return "\n".join(lines)


def render_full(data: dict, today: str) -> str:
    lines = []
    lines.append(f"# 📚 研究生命周期 CHANGELOG — {today}")
    lines.append("")
    lines.append("> 自动生成(facts 由 `scan_facts.py` 扫,narrative 从整个 `knowledge/` 树抽取)。")
    lines.append("> Narrative 留 `<!-- TODO: user -->` 的字段需要人手补充。")
    lines.append("")
    lines.append(render_summary(data["summary"], data["papers"]))

    # Fix 1(7/11 打磨):显示 narrative 覆盖率 + Fix 2 矛盾数
    papers = data["papers"]
    with_traj = sum(1 for p in papers if not p["trajectory"].startswith("<!--"))
    with_next = sum(1 for p in papers if not p["next_step"].startswith("<!--"))
    conflicts = sum(1 for p in papers if p.get("narrative_conflict"))
    lines.append("### Narrative 覆盖率(7/11 打磨后)")
    lines.append("")
    lines.append(f"- **演化轨迹有内容**: {with_traj} / {len(papers)} = {100*with_traj//len(papers)}%")
    lines.append(f"- **下一步有内容**: {with_next} / {len(papers)} = {100*with_next//len(papers)}%")
    if conflicts:
        lines.append(f"- **⚠️ Narrative-Facts 矛盾**: {conflicts} 篇(见下方 `> ⚠️` 行)")
    lines.append("")

    # 按状态分组
    by_status = {s: [] for s in STATUS_ORDER}
    for p in data["papers"]:
        by_status.setdefault(p["status"], []).append(p)

    for status in STATUS_ORDER:
        papers = by_status.get(status, [])
        if not papers:
            continue
        lines.append(f"## {render_status_emoji(status)} {status} ({len(papers)} 篇)")
        lines.append("")
        for p in sorted(papers, key=lambda x: x["name"]):
            lines.append(render_paper_section(p))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--aggregated", default="tmp/paper_changelog/aggregated.json")
    parser.add_argument("--output", default=None,
                        help="输出路径,默认 knowledge/analysis/research-changelog-YYYY-MM-DD.md")
    parser.add_argument("--today", default=None, help="日期字符串,默认今天")
    args = parser.parse_args()

    aggregated_path = Path(args.aggregated)
    data = json.loads(aggregated_path.read_text(encoding="utf-8"))

    today = args.today or datetime.now().strftime("%Y-%m-%d")
    if args.output is None:
        args.output = f"knowledge/analysis/research-changelog-{today}.md"

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    markdown = render_full(data, today)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"[render_changelog] Wrote {output_path}")
    print(f"[render_changelog] Length: {len(markdown)} chars / {markdown.count(chr(10)) + 1} lines")


if __name__ == "__main__":
    main()