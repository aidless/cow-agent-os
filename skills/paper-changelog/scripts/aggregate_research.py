#!/usr/bin/env python3
"""
aggregate_research.py — 把 scan.jsonl + entities/liu-zewen-research.md + MEMORY.md
合并成 research_changelog.json,带 narrative 字段.

实现:
  - facts: 自动(从 scan.jsonl)
  - narrative("trajectory", "next_step", "reflection"): 从 entities/liu-zewen-research.md
    和 MEMORY.md 用关键词抽取(简单 keyword match,不做 LLM)
  - 留 TODO 字段:人没写过的状态留 <!-- TODO: user -->

输出:tmp/paper_changelog/aggregated.json
"""
import argparse
import json
import re
from pathlib import Path
from typing import Optional


ENTITY_FILE = Path("knowledge/entities/liu-zewen-research.md")
MEMORY_FILE = Path("MEMORY.md")
KNOWLEDGE_ROOT = Path("knowledge")


def load_facts(scan_jsonl: Path) -> list[dict]:
    records = []
    with scan_jsonl.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_narrative_corpus() -> str:
    """从整个 knowledge/ 树扫所有 .md 文件,作为 narrative 抽取源.

    覆盖:
      - knowledge/entities/*.md        (人写的项目档案)
      - knowledge/analysis/*.md        (深度分析)
      - knowledge/concepts/**/*.md     (概念性条目)
      - knowledge/index.md + log.md    (顶层)
      - MEMORY.md                      (顶层长期记忆)

    Fix 1(7/11 打磨):扩展抽取源从 2 个文件到全 knowledge 树,让 11 个 stub-only 论文
    也能抽到 narrative(虽然大多是被间接提到的).
    """
    parts = []
    seen_paths = set()

    # 1. 顶层 MEMORY.md
    if MEMORY_FILE.exists():
        parts.append(f"=== {MEMORY_FILE} ===\n" + MEMORY_FILE.read_text(encoding="utf-8"))
        seen_paths.add(str(MEMORY_FILE))

    # 2. knowledge/ 全树扫描
    if KNOWLEDGE_ROOT.exists():
        for md_file in sorted(KNOWLEDGE_ROOT.rglob("*.md")):
            # 跳过 .ingested-* 缓存目录(arxiv-watch 的 L2 cache)
            if ".ingested" in str(md_file):
                continue
            if str(md_file) in seen_paths:
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                # 过滤太长的文件(>50KB)避免塞爆 corpus,只保留头 50KB
                if len(content) > 50000:
                    content = content[:50000] + "\n\n... [truncated at 50KB]"
                parts.append(f"=== {md_file} ===\n{content}")
                seen_paths.add(str(md_file))
            except Exception:
                pass

    return "\n\n".join(parts)


def extract_paper_narrative(paper_name: str, corpus: str) -> dict:
    """从 corpus 里抽取包含 paper_name 的所有行,作为 narrative.

    策略:不分类,直接把该论文相关的所有行打包进 trajectory 字段.
    简化:不再启发式区分 trajectory/next_step/reflection,因为用户 entity 文件
    里的句子本来就是「一行一状态」格式,粗暴打包更忠实.

    Fix 3(7/11 打磨):删掉 reflection 字段(从来没实现抽取,只是留 TODO,
    会让人看 dashboard 麻木).dashboard 现在只显示 trajectory 和 next_step.
    """
    paper_keys = [paper_name]
    m = re.match(r"^(PAPER|tmlr_p|arxiv_p)(\d+)", paper_name, re.I)
    if m:
        paper_keys.append(f"{m.group(1).upper()}{m.group(2)}")
        paper_keys.append(f"{m.group(1).lower()}_{m.group(2)}")
        paper_keys.append(f"{m.group(1).capitalize()}{m.group(2)}")

    hits = []
    seen = set()
    for line in corpus.split("\n"):
        if any(k.lower() in line.lower() for k in paper_keys):
            stripped = line.strip()
            if stripped and stripped not in seen:
                hits.append(stripped)
                seen.add(stripped)

    if not hits:
        return {
            "trajectory": "<!-- TODO: trajectory -->",
            "next_step": "<!-- TODO: next_step -->",
        }

    # 把所有 hits 打包成 trajectory(用换行连成块)
    trajectory = "\n".join(hits)
    # 启发式:从 hits 里找带"待"/"需"/"stub"等关键词的行,作为 next_step
    next_step_hits = [h for h in hits if any(k in h for k in ["待", "需", "stub", "未", "TODO", "缺"])]
    next_step = "\n".join(next_step_hits) if next_step_hits else "<!-- TODO: next_step -->"

    return {
        "trajectory": trajectory,
        "next_step": next_step,
    }


def detect_narrative_facts_conflict(facts: dict, narrative: dict) -> str | None:
    """Fix 2(7/11 打磨):检测 narrative 跟 facts 是否矛盾.

    启发式:
    - word_count < 500 但 trajectory 含「完成 / 已写 / final / submitted」 → 矛盾 ⚠️
    - word_count > 5000 但 trajectory 含「stub / 未写 / 仅废稿」 → 矛盾 ⚠️
    - status = stub-only 但 trajectory 含「audit-ready / final / 提交」 → 矛盾 ⚠️

    返回:None(没矛盾)或 str(矛盾描述,带 ⚠️ 标记)
    """
    traj = narrative.get("trajectory", "")
    if traj.startswith("<!--"):
        return None  # 没有 narrative,无法判断矛盾

    word_count = facts.get("word_count", 0)
    status = facts.get("status", "")

    # 矛盾规则 1:内容很少但 narrative 说「完成」
    complete_keywords = ["完成", "已写", "final", "submitted", "可提交", "audit-ready", "verify_p.* PASS"]
    if word_count < 500 and any(re.search(k, traj, re.I) for k in complete_keywords):
        return f"⚠️ narrative 提「完成/final」但 word_count={word_count}(<500,内容过少)"

    # 矛盾规则 2:内容很多但 narrative 说「stub」
    stub_keywords = ["stub", "未写", "仅废稿", "FABRICATED", "待起"]
    if word_count > 5000 and any(re.search(k, traj, re.I) for k in stub_keywords):
        return f"⚠️ narrative 提「stub/废稿」但 word_count={word_count}(>5000,内容充足)"

    # 矛盾规则 3:状态 stub-only 但 narrative 说「可提交」
    if "stub-only" in status and any(re.search(k, traj, re.I) for k in ["audit-ready", "可提交", "已 submit", "verify_p.* PASS"]):
        return f"⚠️ 状态为 stub-only 但 narrative 提「可提交/audit-ready」"

    return None


def aggregate(scan_jsonl: Path) -> dict:
    facts = load_facts(scan_jsonl)
    corpus = load_narrative_corpus()

    # 总览
    total = len(facts)
    with_main = sum(1 for f in facts if f["has_main_tex"])
    with_protocol = sum(1 for f in facts if f["has_protocol"])
    with_verify = sum(1 for f in facts if f["has_verify_script"])
    with_release = sum(1 for f in facts if f["has_release_notes"])
    consolidated = sum(1 for f in facts if "CONSOLIDATED" in f["name"].upper())

    # 派生字段:audit 状态评分
    enriched = []
    for f in facts:
        score = 0
        if f["has_main_tex"]: score += 1
        if f["has_protocol"]: score += 2
        if f["has_verify_script"]: score += 3
        if f["word_count"] >= 3000: score += 2
        if f["word_count"] >= 6000: score += 1
        if f["has_release_notes"]: score += 2

        if score >= 9:
            status = "🟢 audit-ready / final"
        elif score >= 6:
            status = "🟡 needs-audit"
        elif score >= 3:
            status = "🟠 stub-with-tex"
        else:
            status = "🔴 stub-only"

        narrative = extract_paper_narrative(f["name"], corpus)
        # Fix 2: 检测 narrative 跟 facts 的矛盾
        conflict = detect_narrative_facts_conflict({**f, "status": status}, narrative)

        enriched.append({
            **f,
            "audit_score": score,
            "status": status,
            "narrative_conflict": conflict,
            **narrative,
        })

    # 按 status 分组
    by_status = {}
    for e in enriched:
        by_status.setdefault(e["status"], []).append(e["name"])

    summary = {
        "total_papers": total,
        "with_main_tex": with_main,
        "with_protocol": with_protocol,
        "with_verify_script": with_verify,
        "with_release_notes": with_release,
        "consolidated_count": consolidated,
        "by_status": by_status,
    }

    return {"summary": summary, "papers": enriched}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan", default="tmp/paper_changelog/scan.jsonl")
    parser.add_argument("--output", default="tmp/paper_changelog/aggregated.json")
    args = parser.parse_args()

    result = aggregate(Path(args.scan))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    s = result["summary"]
    print(f"[aggregate] Total: {s['total_papers']} / consolidated: {s['consolidated_count']}")
    print(f"[aggregate] Status breakdown:")
    for status, papers in s["by_status"].items():
        print(f"  {status}: {len(papers)} papers")
        for p in papers[:5]:
            print(f"    - {p}")
        if len(papers) > 5:
            print(f"    ... and {len(papers) - 5} more")

    # Fix 2: 输出 narrative-facts 矛盾
    conflicts = [p for p in result["papers"] if p.get("narrative_conflict")]
    if conflicts:
        print(f"\n[aggregate] ⚠️  Narrative-Facts 矛盾 ({len(conflicts)} 篇):")
        for p in conflicts:
            print(f"  - {p['name']}: {p['narrative_conflict']}")

    print(f"\n[aggregate] Wrote {output_path}")


if __name__ == "__main__":
    main()