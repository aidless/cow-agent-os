---
name: experiment-tracker
description: |
  把 git log(或 .bak_* 文件)转成结构化 CHANGELOG。
  触发场景:用户说"我的研究状态如何"、"论文整体盘点"、"5 月 deadline 进度"、
  "PAPER1 现在状态"、"research dashboard"、"paper audit 进度看板"时启动。

  双源支持:
  - **Git 源**: `F:\Research\TEMPLATE` 等进 git 的项目 → `parse_log.py` + `aggregate_to_notes.py`
  - **.bak_* 源**: `F:\Research\PAPER5_CONSOLIDATED` 等用文件级 backup 的 paper 目录
                     → `parse_bak.py` + `render_bak_changelog.py` + `scan_all_baks.py`
  (7/11 重定位:F:\Research\ 下 38 个 paper_dir **都没 git**,但 2 个用 .bak_* 备份)
---

# 📚 experiment-tracker — 双源实验 / 论文 CHANGELOG 生成器

_把 git log 或 `.bak_*` 文件级 backup 转成 Keep-a-Changelog 风格的 changelog,覆盖 LaTeX 代码 / 实验协议 / 论文版本。_

---

## 🎯 触发关键词

- "**我的研究状态如何**" / "**论文整体盘点**" / "**5 月 deadline 进度**"
- "**PAPER1 现在状态**" / "**论文 audit 进度**" / "**research dashboard**"
- "**git log → 实验笔记**" / "**paper changelog**" / "**实验记录**"
- "**论文演化痕迹**" / "**.bak_* backup**" / "**main.tex.bak_*** 演化"

**不适用场景**:
- 完整论文 review / R&R 生成 → 用 `paper-review-toolkit` / `rr-responder`
- 论文级进度看板(narrative) → 用 `paper-changelog`
- 单文件演化 → 直接 `git log -- file` / `dir *.bak_*`

---

## 📐 工作流 — 双源并行

```
                ┌─────────────────────────────────────────┐
                │  F:\Research\ 各项目根目录                │
                └─────────────────────────────────────────┘
                            │               │
                            ▼               ▼
        ┌──────────────────────────┐  ┌────────────────────────────┐
        │  Git 源(parse_log.py)     │  │  .bak_* 源(parse_bak.py)   │
        │  - .git/ 目录存在         │  │  - main.tex.bak_* 文件     │
        │  - Conventional Commits   │  │  - mtime + size + delta    │
        │  - 输出 JSONL             │  │  - 输出 JSONL              │
        └──────────────────────────┘  └────────────────────────────┘
                            │               │
                            ▼               ▼
        ┌──────────────────────────┐  ┌────────────────────────────┐
        │  aggregate_to_notes.py    │  │  render_bak_changelog.py   │
        │  Keep-a-Changelog 7 类   │  │  + scan_all_baks.py        │
        └──────────────────────────┘  └────────────────────────────┘
                            │               │
                            └───────┬───────┘
                                    ▼
                            研究级 CHANGELOG
                            (per-paper 或 dashboard)
```

---

## 🚀 快速开始

### Git 源(传统路径,7/10 交付)

```bash
python skills/experiment-tracker/scripts/parse_log.py \
  --repo F:\\Research\\TEMPLATE \
  --out tmp/exp_track_test/commits.jsonl

python skills/experiment-tracker/scripts/aggregate_to_notes.py \
  --in tmp/exp_track_test/commits.jsonl \
  --out tmp/exp_track_test/changelog_unreleased.md \
  --next-version v0.4.0
```

### .bak_* 源(7/11 重定位后)

```bash
# 单个 paper
python skills/experiment-tracker/scripts/parse_bak.py \
  --paper-dir F:\\Research\\PAPER5_CONSOLIDATED \
  --out tmp/exp_bak_test/PAPER5_CONSOLIDATED_baks.jsonl

python skills/experiment-tracker/scripts/render_bak_changelog.py \
  --in tmp/exp_bak_test/PAPER5_CONSOLIDATED_baks.jsonl \
  --out tmp/exp_bak_test/PAPER5_CONSOLIDATED_changelog.md \
  --today 2026-07-11

# 一键扫所有 paper(22 dirs / 2 含 .bak_* / 16 backups)
python skills/experiment-tracker/scripts/scan_all_baks.py
```

---

## 📦 .bak_* 源输出字段(7/11 新增)

每条 `.bak_*` JSONL record:
| 字段 | 类型 | 说明 |
|---|---|---|
| `paper_dir` | str | paper 目录名(PAPER5_CONSOLIDATED)|
| `bak_name` | str | `main.tex.bak_post_c7_fix` |
| `bak_path` | str | 绝对路径 |
| `mtime` | ISO | 文件修改时间(论文版本时间) |
| `size_bytes` | int | 文件大小 |
| `word_count` | int | `len(text.split())` |
| `stage` | str | 提取的阶段名(post-c7-fix / pre-bonferroni ...) |
| `commit_message` | str | 同 stage(模拟 git commit msg) |
| `delta_words` | int vs prev | +459 / -5 / None (start) |
| `delta_size_bytes` | int vs prev | +3500 / -69 / None |
| `first_chars` | str | LaTeX 标题(200 chars,识别论文身份) |
| `is_current` | bool | True if 此 .bak_* 是 main.tex 的最近前置 |
| `main_tex_size_bytes` | int | 当前 main.tex 大小 |
| `main_tex_word_count` | int | 当前 main.tex 字数 |

---

## 🎯 Stage Keywords(7/11 定义,可扩展)

`parse_bak.py` 识别以下命名约定的 stage,可手动扩展 `STAGE_KEYWORDS` 列表:

- `post_reviewer_D_patches` / `post_reviewer_D_fixes` / `post_c7_fix`
- `pre_reviewer_D_fixes` / `pre_bonferroni` / `pre_blacklist_fix`
- `pre_p5_audit_fix` / `pre_unicode_fix` / `pre_yields_fix`
- `pre_framing` / `pre_polish` / `pre_decite`
- `during_edit` / `draft` / `thanks_try`
- `pre_final` / `pre_audit`

**命名约定**: `main.tex.bak_<descriptor>[_YYYYMMDD]`(日期后缀可选)

**未识别**:`main.tex.bak_<unknown>` 会 fallback 成 `<unknown>` 字符串(用户后期修正)

---

## 🧪 7/11 真测试产物

| 路径 | 说明 |
|---|---|
| `tmp/exp_bak_test/DASHBOARD.md` | 22 paper_dirs / 2 含 .bak_* / 16 backups 总览 |
| `tmp/exp_bak_test/PAPER5_CONSOLIDATED_baks.jsonl` | 12 records |
| `tmp/exp_bak_test/PAPER5_CONSOLIDATED_changelog.md` | 86 行,含 12 次备份的演化轨迹 |
| `tmp/exp_bak_test/PAPER1_CONSOLIDATED_baks.jsonl` | 4 records |
| `tmp/exp_bak_test/PAPER1_CONSOLIDATED_changelog.md` | 38 行,含 4 次备份的演化 |

**PAPER5 真实演化**(从 7/10 跑出来的):
```
draft (4108w)
  → pre_framing (4108w, +0)
  → pre_bonferroni (5130w, +1022) ← 大改
  → during_edit (6253w, +1123)
  → thanks_try (6248w, -5)
  → pre_p5_audit_fix (7597w, +1349) ← 又一个大改
  → pre_polish (8056w, +459)
  → pre_blacklist_fix (8059w, +3)
  → pre_yields_fix (8060w, +1)
  → post_c7_fix (8255w, +195) ← 审稿 C7 反馈
  → pre_reviewer_D_fixes (8255w, +0)
  → post_reviewer_D_patches (8712w, +457) ← 审稿 D patches 📍CURRENT
```

总计 +4604 words / +37187 bytes 增长,真实记录了 R&R 流程。

---

## 🔗 与其他 skill 的关系

| Skill | 关系 |
|---|---|
| **paper-changelog** | 互补:paper-changelog 看论文目录(38 dirs),experiment-tracker 看论文演化(.bak_*) |
| **paper-review-toolkit** | 互补:review-toolkit 出 reviewer report,experiment-tracker 出 CHANGELOG |
| **rr-responder** | 互补:rr-responder 处理 review,experiment-tracker 处理修订过程(.bak_* 是产物) |

---

## 🗺️ Roadmap

### 短期(可立即做)
- [ ] 抽取出 `.bak_*` 文件内 diff(用 difflib,看正文改了啥而非字数)
- [ ] LLM 给每个 stage 生成 1 句 narrative(从 stage 名 + delta 推断)
- [ ] 支持 `*.bak_*` pattern(不只 main.tex)

### 中期
- [ ] 跨 paper 聚合(PAPER1+5 共 16 bak → 联合 changelog)
- [ ] 自动检测 dev workflow(PAPER5 pattern 显示按 "audit → fix → review" 循环)

### 长期
- [ ] 接入 git(如果未来 paper 目录进 git,切换到 parse_log.py)

---

## 🔧 关键文件

```
skills/experiment-tracker/
├── SKILL.md                                  ← 你正在读(7/11 重写)
└── scripts/
    ├── parse_log.py                          git 源(7/10)
    ├── aggregate_to_notes.py                 git 源(7/10)
    ├── parse_bak.py                          .bak_* 源(7/11 新增)
    ├── render_bak_changelog.py               .bak_* 源(7/11 新增)
    └── scan_all_baks.py                      .bak_* 全扫(7/11 新增)

tmp/exp_bak_test/
├── DASHBOARD.md                              7/11 真测试产物
├── PAPER5_CONSOLIDATED_baks.jsonl            12 records
├── PAPER5_CONSOLIDATED_changelog.md          86 行
├── PAPER1_CONSOLIDATED_baks.jsonl            4 records
└── PAPER1_CONSOLIDATED_changelog.md          38 行
```