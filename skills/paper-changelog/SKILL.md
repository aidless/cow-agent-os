---
name: paper-changelog
description: |
  把 F:\Research\ 下所有论文目录扫描成一份研究级 CHANGELOG。
  触发场景:用户说"我的研究状态如何"、"论文整体盘点"、"5 月 deadline 进度"、
  "PAPER1 现在状态"、"research dashboard"、"paper audit 进度看板"时启动。
  
  与 experiment-tracker 的区别:experiment-tracker 是 git commit 级(代码)、
  paper-changelog 是论文目录级(LaTeX),正交不重叠。
---

# 📚 paper-changelog — 研究生命周期 CHANGELOG 自动生成

_把 `F:\Research\` 38 个论文目录的 facts + 从 `entities/liu-zewen-research.md` / `MEMORY.md` 抽取的 narrative,合成一份研究级 CHANGELOG。_

---

## 🎯 触发关键词

- "**研究状态盘点**" / "**论文整体盘点**" / "**5 月 deadline 进度**"
- "**PAPER1 现在状态**" / "**论文 audit 进度**" / "**research dashboard**"
- "**哪些论文没写完**" / "**哪些论文 audit-ready**"
- "**研究生命周期 CHANGELOG**" / "**paper-changelog**"

**不适用场景**:
- 单一论文的修改记录 → 用 git log / `experiment-tracker`(git-based)
- 实验笔记 / protocol.md 的细节 → 直接读 paper_dir
- 论文提交后的版本回溯 → 用 paper-review-toolkit 的 `verify_*.py`

---

## 📐 工作流

```
F:\Research\
    │
    ↓ scan_facts.py
scan.jsonl  ────────────────── 38 个 paper_dir 的 facts
    │                              (字数 / 图表数 / 文件存在性 / 兄弟目录)
    ↓ aggregate_research.py
aggregated.json  ─────────────── facts + narrative 合并
    │                              (narrative 从 entity / MEMORY 关键词抽取)
    ↓ render_changelog.py
research-changelog-YYYY-MM-DD.md ── 最终 CHANGELOG
```

---

## 🚀 快速开始

### 一键运行(默认参数)

```bash
python skills/paper-changelog/scripts/orchestrate.py --today 2026-07-10
```

输出:
- `tmp/paper_changelog/scan.jsonl`
- `tmp/paper_changelog/aggregated.json`
- `knowledge/analysis/research-changelog-2026-07-10.md`

### 单独跑某一步

```bash
# Step 1: 扫 facts
python skills/paper-changelog/scripts/scan_facts.py \
  --research-root F:\\Research \
  --output tmp/paper_changelog/scan.jsonl

# Step 2: 合并 narrative
python skills/paper-changelog/scripts/aggregate_research.py \
  --scan tmp/paper_changelog/scan.jsonl \
  --output tmp/paper_changelog/aggregated.json

# Step 3: render
python skills/paper-changelog/scripts/render_changelog.py \
  --aggregated tmp/paper_changelog/aggregated.json \
  --today 2026-07-10
```

---

## 📦 输出字段说明

### `scan.jsonl` 每条记录的字段

| 字段 | 类型 | 来源 |
|---|---|---|
| `path` | str | paper_dir 绝对路径 |
| `name` | str | 目录名 |
| `has_main_tex` | bool | `main.tex` 存在 |
| `has_protocol` | bool | `protocol.md` 存在 |
| `has_verify_script` | bool | `verify_p*.py` / `verify_*.py` 存在 |
| `has_release_notes` | bool | `RELEASE_NOTES.md` / `CHANGELOG.md` 存在 |
| `word_count` | int | `main.tex` 字数 |
| `figure_count` | int | `\begin{figure}` 出现次数 |
| `table_count` | int | `\begin{table}` 出现次数 |
| `algorithm_count` | int | `\begin{algorithm}` 出现次数 |
| `bak_count` | int | `main.tex.bak_*` 文件数 |
| `sibling_dirs` | list[str] | 兄弟目录(前 20 个) |
| `file_size_kb` | float | main.tex 大小(KB) |

### `aggregated.json` 额外字段

| 字段 | 算法 |
|---|---|
| `audit_score` | 0-11,综合分:has_main +1 / has_protocol +2 / has_verify +3 / words≥3000 +2 / words≥6000 +1 / has_release +2 |
| `status` | `🟢 audit-ready` (≥9) / `🟡 needs-audit` (≥6) / `🟠 stub-with-tex` (≥3) / `🔴 stub-only` (<3) |
| `trajectory` | 从 `entities/liu-zewen-research.md` + `MEMORY.md` 抽取的所有含论文名的行(用 `\n` 连成块) |
| `next_step` | 同上,但只保留含 "待"/"需"/"stub"/"未"/"TODO"/"缺" 关键词的行 |
| `reflection` | 暂未填,留 `<!-- TODO: reflection -->` |

### `research-changelog-*.md` 章节结构

1. **🎯 总览**: 论文数 / 含 main.tex 数 / 含 protocol 数 / 状态分布
2. **🟢 audit-ready / final** 章节(PAPER1/2/4/5)
3. **🟡 needs-audit** 章节(PAPER3)
4. **🟠 stub-with-tex** 章节(15 篇)
5. **🔴 stub-only** 章节(18 篇)

每篇论文 section 包含:facts + **演化轨迹**(从 entity 抽) + **下一步**(从 entity 抽)

---

## 🔧 核心设计

### 1. 路径启发式识别 paper_dir

```python
# 判定:含 main.tex / protocol.md / tmlr.sty 之一
# 或匹配正则: ^PAPER\d+(_CONSOLIDATED)?$ / ^tmlr_p\d+$ / ^arxiv_\d{4}\.\d{5}$
```

设计意图:**避免把非论文目录(如 `experiments/`、`arxiv-tracker/`、`paper-writing-agent/`)误识别**。

### 2. audit_score 评分规则

| 信号 | 分值 | 设计意图 |
|---|---|---|
| has_main_tex | +1 | 最低门槛:有 LaTeX 源 |
| has_protocol | +2 | 实验协议可追溯 |
| has_verify_script | +3 | 自检脚本就位 = audit-ready 信号 |
| words≥3000 | +2 | 不是 1-2 页短文 |
| words≥6000 | +1 | 长论文加分 |
| has_release_notes | +2 | release notes / CHANGELOG 已写 |

总 11 分。**≥9 = audit-ready**(可提交状态);**6-8 = needs-audit**;**3-5 = stub-with-tex**;**<3 = stub-only**。

### 3. narrative 抽取策略

- 不分类,直接把 entity / MEMORY 里含论文名的所有行打包进 `trajectory` 字段
- `next_step` 是 `trajectory` 的子集(只含 "待"/"需"/"stub" 等关键词)
- **忠实保留源数据**,不强行启发式分配到 trajectory / next_step / reflection 三类

---

## 🪤 失败兜底表

| 失败 | 原因 | workaround |
|---|---|---|
| `scan.jsonl` 找不到文件 | `cwd` 不对 / 路径错 | `cd` 到 workspace 根跑,或用绝对路径 |
| narrative 全是 `<!-- TODO -->` | entity / MEMORY 没提到这个论文 | 这是正常的——`reflection` / `next_step` 留 TODO 是设计意图 |
| aggregated.json 出现 `TODO` 但 entity 写了 | cwd 隐藏 bug(相对路径读不到文件) | 在 workspace 根跑,不要 `cd` 到 `skills/paper-changelog/scripts` |
| `wc -w` 不准(中文 / LaTeX 标记) | `len(text.split())` 不区分 word 边界 | 当前版本可接受偏差,后续可换 `texcount` |
| `figure_count` 漏 | `\begin{figure*}` / `\begin{wrapfigure}` 不匹配 | 当前正则只匹配 `\begin{figure`,后续可扩展 |

---

## 🧪 真实测试产物(2026-07-10)

跑出来的 `knowledge/analysis/research-changelog-2026-07-10.md`:
- 14277 chars / 466 行
- 38 个 paper_dir 全扫描
- 5 篇 CONSOLIDATED 论文 narrative 100% 自动抽取成功(PAPER1/2/3/4/5;PAPER6 因为 entity 写了 "stub" 所以 next_step 也自动填)
- 状态分布:🟢 4 / 🟡 1 / 🟠 15 / 🔴 18

---

## 🆕 7/11 打磨记录(3 个 Fix)

打磨过程中发现 dashboard 在 38 篇全跑场景下有 3 个真实问题,全部修复:

### Fix 1 — narrative 抽取源从 2 文件 → 全 `knowledge/` 树

**问题**:7/10 跑出来 38 篇中只有 26 篇 trajectory 有内容(68%)。原因是 `entity/liu-zewen-research.md` + `MEMORY.md` 没提到 11 篇 stub-only 论文。

**修法**:`aggregate_research.py` 的 `load_narrative_corpus()` 改成扫描 `knowledge/**/*.md`(entities/analysis/concepts/index/log),过滤长文件(>50KB)截断。

**效果**:
| 状态 | 7/10 覆盖率 | 7/11 覆盖率 |
|---|---|---|
| 🟢 audit-ready (4) | 4/4 = 100% | 4/4 = 100% |
| 🟡 needs-audit (1) | 1/1 = 100% | 1/1 = 100% |
| 🟠 stub-with-tex (15) | 14/15 = 93% | **15/15 = 100%** |
| 🔴 stub-only (18) | 7/18 = 39% | **18/18 = 100%** |
| **总计** | **26/38 = 68%** | **38/38 = 100%** |

### Fix 2 — narrative-facts 矛盾检测

**问题**:`PAPER6_CONSOLIDATED` 之类论文,entity 写"stub 状态"但 paper_dir 里可能 `word_count=0`,narrative 跟 facts 不一致时 dashboard 不报警。

**修法**:加 `detect_narrative_facts_conflict(facts, narrative)` 函数,3 条规则:
- word_count < 500 但 trajectory 含「完成/final」→ 矛盾 ⚠️
- word_count > 5000 但 trajectory 含「stub/废稿」→ 矛盾 ⚠️
- status = stub-only 但 trajectory 含「audit-ready/可提交」→ 矛盾 ⚠️

**效果**:当前 38 篇 narrative-facts **0 篇矛盾**(反向验证 5/5 test case 通过)。⚠️ 标志会在 dashboard 的 `> ⚠️` 行高亮。

### Fix 3 — 删 `reflection` 字段

**问题**:`reflection` 字段从来没实现抽取,只留 `<!-- TODO -->`。dashboard 显示「0/38 有 reflection」,语义噪声。

**修法**:`extract_paper_narrative` 不再返回 `reflection` 字段,`render_changelog.py` 也不再输出该字段。

**效果**:dashboard 字段精简 → 0/38 → 「该字段不存在」更诚实。

### 真测试产物(7/11)

- `knowledge/analysis/research-changelog-2026-07-11.md`(**36388 chars / 757 行**)
- 新增章节「Narrative 覆盖率(7/11 打磨后)」直接显示在 dashboard
- 38 篇 narrative 100% 抽取 + 0 篇矛盾 + 无 reflection 噪声
- 关键调试脚本:`tmp/paper_changelog/diagnose.py`

---

## 🔗 与其他 skill 的关系

| Skill | 关系 |
|---|---|
| **experiment-tracker** | 互补:experiment-tracker 看 git commits,paper-changelog 看论文目录,正交不重叠 |
| **arxiv-tracker** | 独立:arxiv-tracker 看 arxiv 新论文,paper-changelog 看用户自己的 F:\Research |
| **paper-review-toolkit** | 独立:review-toolkit 跑 TMLR 评审,paper-changelog 出进度看板 |
| **knowledge-wiki** | 输出直接进 `knowledge/analysis/research-changelog-*.md`,被 index.md 自动索引 |

---

## 🗺️ Roadmap

### 短期(可立即做)
- [ ] `audit_score` 阈值可配置(`--audit-threshold`)
- [ ] 真实 LLM 抽取 narrative(替换关键词匹配,更准确但慢且贵)
- [ ] 加 `--format=html` 输出可点击的 HTML 看板
- [ ] 加 `reflection` 自动生成(从 paper_dir 的 FINAL_REPORT.md 抽)

### 中期
- [ ] 论文审稿里程碑追踪(`protocol.md` 时间戳 → 节点)
- [ ] 跨论文 cross-reference 提取(shared refs / shared figures)

### 长期
- [ ] 接入 git(`--with-git-history`)补 narrative 演化轨迹
- [ ] Slack/微信周报自动推送

---

## 📂 关键文件

```
skills/paper-changelog/
├── SKILL.md                 ← 你正在读
└── scripts/
    ├── scan_facts.py        4820B
    ├── aggregate_research.py 5370B
    ├── render_changelog.py  5095B
    └── orchestrate.py       2570B

tmp/paper_changelog/
├── scan.jsonl               (38 条 facts)
└── aggregated.json          (带 narrative)

knowledge/analysis/
└── research-changelog-2026-07-10.md  (466 行)
```