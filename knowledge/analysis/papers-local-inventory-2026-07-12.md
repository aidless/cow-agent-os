# 本地论文目录盘点 — F:\Research + F:\TMLR 全扫描(2026-07-12)

> **Source**: 2026-07-12 19:30 实地扫描
> **方法**: `paper-changelog/scripts/scan_facts.py` + 自写 `scan_recursive_tex.py`(递归扫描所有 `\documentclass` 的 `.tex` 文件 + 抽 `\title{}`)
> **触发**: 刘泽文 7/12 19:24 "找出我写过的所有论文 F:\Research F:\TMLR 给出本地目录" + "连接到 obsidian 知识库 给出我的详细科研路线"

---

## 🎯 一句话结论

- 论文材料 **全部在 `F:\Research`**
- **`F:\TMLR` 没有论文源文件**(只有 `llm_lab` Python 软件项目)
- `F:\Research` 共 **39 个顶层论文/草稿目录** + 11 个 `_archive/` 子目录 + 多个投稿副本子目录
- 真独立论文(去重后)**26 篇**,加上 5 月 deadline 6 篇 CONSOLIDATED + genesis-master + PAPER35 = **完整覆盖 33 个论文级目录**

---

## 📊 扫描方法学

| 工具 | 路径 | 产出 |
|---|---|---|
| `scan_facts.py` | `skills/paper-changelog/scripts/scan_facts.py` | `tmp/paper_changelog/scan_current.jsonl`(39 行)+ `scan_tmlr_current.jsonl`(0 行) |
| `scan_recursive_tex.py` | `tmp/paper_changelog/scan_recursive_tex.py`(本轮写) | `tmp/paper_changelog/recursive_tex_docs.json`(184 个 `\documentclass` 论文源文件) |
| 启发式判定 | 含 `main.tex` / `paper.tex` / `tmlr.sty` / `tmlr_paper.tex` 之一;或目录名匹配 `^PAPER\d+(_CONSOLIDATED)?$` / `^tmlr_p\d+$` | 跳过 `_archive/`, `paper-writing-agent`, `tmlr-review-simulator` 等 |

---

## 🏠 Obsidian Vault 索引文件

Vault 根目录 = `F:\Research\`(实测 `.obsidian/` 存在),主要入口:

```text
F:\Research\🏠_科研总览.md       — 总览 + 研究时间线 + 依赖关系图
F:\Research\📄_论文清单.md       — 26 篇论文清单(arXiv / TMLR / 归档)
F:\Research\📊_论文分类.md       — 按 6 条研究线分类
F:\Research\🧪_实验索引.md       — 实验脚本与结果数据索引
F:\Research\🔬_方法库.md         — 方法论与写作规范
F:\Research\👿_审稿记录.md       — Devil's Advocate / AG Audit
F:\Research\🖥️_项目总览.md       — 27 个项目分布
```

辅助目录:

```text
F:\Research\00_MOC\          (空目录,索引已上移)
F:\Research\.obsidian\        (vault 配置)
F:\Research\.loop\            (Loop Engineering v5.3 审计系统,91 条规则)
F:\Research\experiments\      (实验 JSON 数据,19 个 mm_epc_* + 11 个 RESAMPLING_CALIBRATION)
F:\Research\_archive\         (历史投稿稿,11 个子目录)
F:\Research\_inbox\           (待整理笔记)
F:\Research\_templates\       (论文/审稿/日报模板)
```

---

## 🔬 当前主版本论文(8 个,5 月 deadline 主体)

| 目录 | 论文 | verify 状态 |
|---|---|---|
| `F:\Research\PAPER1_CONSOLIDATED` | What Communication Does to Multi-Agent LLM Systems | 0H/2M/3L 🟢 |
| `F:\Research\PAPER2_CONSOLIDATED` | The Impossibility Triangle of LLM Evaluation | 0H/5M/2L 🟡 |
| `F:\Research\PAPER3_CONSOLIDATED` | Calibration Fatigue, Self-Evaluation Fragility, and the Coupling-Noise Tradeoff | 0H/12M/3L 🟡 |
| `F:\Research\PAPER4_CONSOLIDATED` | N-Sensitivity: When Measurement Instability Reverses Qualitative Conclusions | 0H/9M/4L 🟡 |
| `F:\Research\PAPER5_CONSOLIDATED` | Empirical Comparison of Memory Architectures for Bias-Resistant Multi-Agent LLM Systems | **0H/0M/0L** ✅ 完全干净 |
| `F:\Research\PAPER6_CONSOLIDATED` | Aggregation Methods Under Verifier Capture in Multi-LLM Ensembles (Empirical Study / Negative Result) | 11/12 PASS ✅ |
| `F:\Research\PAPER35_FRONT_DRIFT` | Agent Behavior Regression Test Suite (Frontier Model Drift) | 🟡 skeleton ready |
| `F:\Research\genesis-master\paper` | Genesis Master: A Self-Creating, Self-Iterating Multi-Agent System with Four Levels of Feedback | ✅ v1.0 已投 TMLR 7/9 |

---

## 🗂️ 独立论文及活跃稿件(25 个)

| 本地目录 | 主要论文 | arXiv | TMLR |
|---|---|---|---|
| `F:\Research\boundary_sync_standalone` | BOUNDARY_SYNC | 2607.01600 | #48 |
| `F:\Research\calibration_contagion` | Not Contagion, Just Time | 在投 | #54 |
| `F:\Research\CALIBRATION_EFFECTS` | Communication Degrades Calibration / Calibration Effects | 在投 | #53 |
| `F:\Research\CALIBRATION_UNIFIED` | Calibration Fatigue 综合版 | — | — |
| `F:\Research\closing_landscape` | Closing the Calibration Landscape | — | 🆕 |
| `F:\Research\contagion_networks` | Contagion Networks | 2606.20493 | — |
| `F:\Research\FLAGSHIP` | What Communication Does / Two Faces of Multi-Agent Communication | 在投 | #48 |
| `F:\Research\impossibility_triangle` | The Impossibility Triangle of LLM Evaluation | 在投 | — |
| `F:\Research\memory_architecture` | Memory Architecture Design | — | 🆕 |
| `F:\Research\memory_contagion` | Memory Contagion | 2606.23195 | — |
| `F:\Research\RESAMPLING_CALIBRATION` | N-Sensitive Calibration | 在投 | #52 |
| `F:\Research\TEMPORAL_DYNAMICS` | Beyond Point Estimates | 在投 | — |
| `F:\Research\tmlr_p6` | The Hidden Cost of Resampling | 2606.29720 | #50 |
| `F:\Research\tmlr_p9` | Calibrating the Evaluator | 2606.31371 | — |
| `F:\Research\tmlr_p10` | Self-Evaluation Immunity Is Model-Dependent | — | — |
| `F:\Research\tmlr_p11` | Beyond Point Estimates(EPC Protocol 在其 `arxiv_submit/` 子目录)| — | — |
| `F:\Research\tmlr_p12` | N-Sensitivity 早期稿 | — | — |
| `F:\Research\tmlr_p13` | Symmetric Learning Rates Do Not Eliminate Preference Coupling | — | — |
| `F:\Research\tmlr_p14` | Within-Condition Testing | — | — |
| `F:\Research\tmlr_p15` | Probability Calibration Worsens Evaluation Noise | — | — |
| `F:\Research\tmlr_p16` | Mapping the Evaluation Frontier | 2607.00304 | — |
| `F:\Research\tmlr_p17` | Strategy Collapse Dynamics(已融入 FLAGSHIP)| — | — |
| `F:\Research\tmlr_p18` | Post-RLHF Calibration Drift | — | — |
| `F:\Research\tmlr_p19` | 未命名 stub | — | — |
| `F:\Research\tmlr_p20_k_generalization` | K≥3 Evaluators Generalization | — | — |
| `F:\Research\tmlr_p21_self_eval_causal` | Self-Evaluation Bias Causal Analysis | — | — |

---

## 📦 历史论文与归档稿(`_archive/` 11 个子目录)

| 目录 | 内容 |
|---|---|
| `F:\Research\_archive\aaai_student_abstract` | Multimodal Evaluator Preference Collapse(AAAI SA)|
| `F:\Research\_archive\acl_2027` | A Diagnostic Framework and Multi-Evaluator Audit(ACL 投稿版)|
| `F:\Research\_archive\arxiv_main` | AE-TTL、Evaluator Preference Collapse、MM-EPC 等早期稿(4 个 paper.tex)|
| `F:\Research\_archive\arxiv_submission` | MM-EPC arXiv 投稿版本 |
| `F:\Research\_archive\arxiv_v3` | MM-EPC v3 |
| `F:\Research\_archive\emnlp_2027` | Probability Calibration with LLM Embeddings and Tree Ensembles |
| `F:\Research\_archive\iclr_2027` | Diagnostic Framework 的 ICLR 版本 |
| `F:\Research\_archive\tmlr_2027` | Diagnostic Framework 的 TMLR 版本 |
| `F:\Research\_archive\tmlr_category_error` | The Category Error in Multi-Agent Simulation |
| `F:\Research\_archive\tmlr_external_validation` | Partial Replication of the Impossibility Triangle |
| `F:\Research\_archive\contagion_tensor` | Contagion Tensor 实验代码 + 结果(无 `.tex`)|
| `F:\Research\joces_templates` | MM-EPC 中文期刊稿(Word 文件)|

---

## 🔁 投稿副本与重复镜像(不应重复算作独立论文)

```text
F:\Research\arxiv                          → CALIBRATION_EFFECTS 投稿副本
F:\Research\arxiv_contagion                → calibration_contagion 投稿副本
F:\Research\arxiv_p13                      → 不可能三角早期稿
F:\Research\arxiv_p14                      → Within-Condition Testing 投稿稿
F:\Research\arxiv_submission_paper1        → FLAGSHIP 早期投稿包(v1-v8 zip 多版本)
F:\Research\CONSOLIDATED_PAPER5            → memory_architecture / PAPER5 的旧合并版
F:\Research\impossibility_triangle_consolidated → PAPER2 的前代合并版
F:\Research\tmlr_flagship                  → FLAGSHIP / PAPER1 的 TMLR 镜像
F:\Research\_submission_package\PAPER1      → PAPER1 投稿包
F:\Research\_submission_package\PAPER2      → PAPER2 投稿包
F:\Research\_submission_package\PAPER3      → PAPER3 投稿包
F:\Research\_submission_package\PAPER4      → PAPER4 投稿包
F:\Research\_submission_package\PAPER5      → PAPER5 投稿包
```

---

## 📭 F:\TMLR 实际情况

- 没有 `.tex`
- 没有论文 PDF
- 没有 Word 论文
- `F:\TMLR\llm_lab\` 是 Python 软件项目(`cli.py` / `main.py` / `runner.py` / `verifier.py` / `worker.py` 等),与论文无关

---

## 🔗 关联知识页面

- [5 月 Deadline 研究论文总览](../research/index.md) — 6 篇 CONSOLIDATED 论文专题
- [刘泽文 — 研究系统全图](../entities/liu-zewen-research.md) — 研究系统总图
- [PAPER5 Improvement RFC](./paper5-improvement-rfc-2026-07-11.md) — 5 月 deadline 主推
- [Paper #35 Proposal](./paper35-frontier-behavior-regression-proposal-2026-07-11.md) — 新立项