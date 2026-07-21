# 刘泽文 — 研究系统全图

> Source: 2026-07-10 用户口述 + 实地扫描 F:\Research 根目录 + 读取 🏠_科研总览.md / 🖥️_项目总览.md / PAPER5_FINAL_REPORT.md
> 用户身份:刘泽文(从 🏠_科研总览.md 落款 "科研总览 — 刘泽文" 推断)

## 核心身份

- **职业**:研究者(论文密集型 AI 研究)
- **主战场**:`F:\Research\`(单根,约 70 个子目录)
- **运行平台**:本会话在 mavis 框架(`C:\Users\Administrator\.mavis\`)下运行
- **协作风格**:用户偏好在写文件/操作前会先做口头扫盘,让我"看这都有什么"

## 研究主线

**多 Agent LLM 系统中,通信、校准与偏好耦合的相互作用。**

三条核心问题(从 🏠_科研总览.md):
1. 通信引起什么效应? → Two Faces of Communication(策略共识 + 校准传染同时发生)
2. 校准能解决问题吗? → 否,效果条件依赖,有时反而加重噪声
3. 评估本身有多可靠? → 不可能三角(Bias-Reliability-Coupling 三者不可同时最优)

## F:\Research 目录结构(按功能 6 类)

### 1. 论文主目录 — 5 篇 CONSOLIDATED + 1 篇独立投稿
- `PAPER1_CONSOLIDATED` — 7/9 改进报告完成,12 句 Abstract + Limitations 章节已加
- `PAPER2_CONSOLIDATED` — v9 构建脚本齐全(main_v9.tex + supplementary_v9.tex)
- `PAPER3_CONSOLIDATED` — 标准结构,有 arxiv_submit 子目录
- `PAPER4_CONSOLIDATED` — 标准结构,有 prebonferroni 备份
- `PAPER5_CONSOLIDATED` — 7/10 最终报告,verify_p5.py 6/6 PASS,**5 篇 CONSOLIDATED 里相对最稳的候选**
- **`genesis-master/`** — **6 篇论文中唯一独立投稿 TMLR 的项目**(v1.0 已投稿 7/9,11 页 paper.pdf,195 测试全过)→ 详见 [genesis-master.md](./genesis-master.md)

### 2. 早期单篇工作目录(已大部分被 consolidated 吸收)
- `tmlr_flagship` + `tmlr_p6` / `p9` / `p10` / ... / `p19` — 早期分散版本
- `tmlr_p20_k_generalization`、`tmlr_p21_self_eval_causal` — 两个新方向分支(可能尚未合并)
- `PAPER6_CONSOLIDATED` — 7/9 新起,**仅 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 废稿**,**stub 状态**
  - ⚠️ 注意:**与 `genesis-master/` 是两件事** —— genesis-master 是已投稿的 v1.0 元级 AI 系统论文,这里是未起稿的新主题 stub

### 3. 主题实验 / 数据(6 个主题方向)
- **Contagion**:`calibration_contagion`、`contagion_networks`、`memory_contagion`、`arxiv_contagion`
- **Calibration**:`CALIBRATION_EFFECTS`、`CALIBRATION_UNIFIED`、`RESAMPLING_CALIBRATION`
- **Impossibility Triangle**:`impossibility_triangle` + `impossibility_triangle_consolidated`
- **Temporal/Boundary**:`TEMPORAL_DYNAMICS`、`closing_landscape`、`boundary_sync_standalone`
- **过渡目录**:`FLAGSHIP`、`CONSOLIDATED_PAPER5`
- **实验原料**:`experiments/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/p14/`、`arxiv_submission_paper1/`

### 4. 工具链(用户自研)
- `tmlr_pipeline/` — 6 阶段 pipeline 脚手架
- `paper-writing-agent/` — 21 模块论文写作 agent(v24.0,7/9 用于 PAPER1 改进)
- `tmlr-review-simulator/` — 审稿人模拟器
- **`genesis-master/`** — **TMLR 第 6 篇独立投稿项目**(11 页 paper.pdf 已投稿 v1.0,v8-v9 系列 post-submission 扩展材料)→ 详见 [genesis-master.md](./genesis-master.md)
- C 盘 `C:\Users\Administrator\.zcode\skills\paper-writing-agent\` 有一份,**F 盘更完整**

### 5. 元数据 / 进程
- `00_MOC/` — Map of Content 目录(空,vault 索引虚拟)
- `_ALARMS/` — 闹钟/提醒
- `_archive/`、`_corpus/`、`_git_init_backup/`、`_inbox/`、`_paper_reviews/`、`_research_radar/`、`_submission_package/`、`_templates/` — 中间/归档
- `00_系统配置/` — Obsidian 自动化系统 + PaperKB 配置文档
- `AGENTS.md`、`CLAUDE.md`、`README.md` — 项目级 agent 规则
- 根下 emoji 前缀文件:`🏠_科研总览.md` / `🖥️_项目总览.md` / `📄_论文清单.md` / `📊_论文分类.md` / `🧪_实验索引.md` / `🔬_方法库.md` / `👿_审稿记录.md` / `📝_简历*.md` — Obsidian 风格导航页

### 6. 研究支撑(系统骨架)
- `BAAI_Knowledge_Base/`、`memory_architecture/` — 知识库 / 记忆架构研究
- `ai_tools_integration/`、`ai_trend_research/` — AI 工具调研
- `planning/`、`research/`、`src/`、`scripts/`、`utils/`、`figures/`、`TEMPLATE/`、`joces_templates/`、`vendor/` — 通用工程目录
- 根下散落 `mm_epc_*.py`、`phoenix_v2/v3/v4.py`、`combined_experiments.py` 等独立实验脚本

## 交付物状态快照(7/11)

| 论文 | 状态 | 备注 |
|---|---|---|
| PAPER1 | 改进报告完成,待 BibTeX 编译 | 12 句 Abstract + Limitations 已加 |
| PAPER2 | v9 已构建 + audit **HIGH=1 已 patch** | C2 Power Analysis 已加;剩 MED=4 (C4/C5×2/C7×2) + LOW=2 |
| PAPER3 | 标准模板 | 需 v24.0 同样的 audit |
| PAPER4 | 标准模板 | 需 v24.0 同样的 audit |
| PAPER5 | **可提交** | verify_p5.py 6/6 PASS,25 页 PDF |
| PAPER6 | stub | LLM_FABRICATED 废稿,无实质内容 |

## 🔬 5 篇 PAPER audit 总览(7/11 10:37,apply_b.log)

| 论文 | TOTAL | HIGH | MEDIUM | LOW |
|---|---|---|---|---|
| PAPER1 | 9 | 0 | 6 | 3 |
| PAPER2 | 8 | 1 | 4 | 2 |
| PAPER3 | 16 | 1 | 10 | 3 |
| PAPER4 | 15 | 2 | 7 | 4 |
| PAPER5 | 6 | 3 | 0 | 3 |

**全 5 篇都有 HIGH/MED findings**。PAPER5 反而 HIGH 最多(3)—— 强烈需要 audit review。

## 🔧 PAPER2 audit 详细(7/11 12:14,verify_p2.py)

| # | 严重度 | 类别 | 行 | 问题 | 状态 |
|---|---|---|---|---|---|
| 1 | 🔴 HIGH | C2 | global | No Power Analysis section declaring Bonferroni k | ✅ **patched** (main.tex + main_v9.tex 已加 §Statistical Note and Power Analysis) |
| 2 | 🟡 MED | C4 | global | Self-cite 30% (liu2026epc/mapping/mmepc 3/10) | ⏳ 待修(需加 4-5 个外部引用) |
| 3 | 🟡 MED | C5 | L44 | abstract p-value 缺 test name | ⏳ 待修 |
| 4 | 🟡 MED | C5 | L44 | abstract p-value 缺 test name(重复)| ⏳ 待修 |
| 5 | 🟡 MED | C7 | L111 | ceremonial cite: coverthomas2006 | ⏳ 待修 |
| 6 | 🟡 MED | C7 | L111 | ceremonial cite: lehmanncasella1998 | ⏳ 待修 |
| 7 | 🟢 LOW | C10 | global | no library version reported | ⏳ 待修 |
| 8 | 🟢 LOW | C6 | L183 | Blacklist word "yield" 3x | ⏳ 待修 |

**Verify 工具路径 bug**: `verify_p2.py` 第 63 行 `MAIN = ROOT / 'main_v9.tex'` — **hardcoded 到旧版**。当前最新是 main.tex (35179 bytes, 7/11 12:12 patch)。7/11 12:14 用 git checkout 还原 main_v9.tex 到 git 版本 + patch。**未来 audit 应改 MAIN 路径**。

**未跑 verify 验证**: patch 后未重跑 verify_p2.py(下次会话第一件事 — 应看到 HIGH=0)。

## 相关页面

- [知识库索引](../index.md) — 总目录
