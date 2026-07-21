# 26 篇论文全量盘点 — Obsidian 路线入口(2026-07-12)

> **Source**: 2026-07-12 19:30 实地扫描 `F:\Research\` + `F:\TMLR\` + 读取 Obsidian vault 7 个索引文件
> **配套**: [本地目录盘点(analysis)](../analysis/papers-local-inventory-2026-07-12.md) — 本地路径全清单
> **触发**: 刘泽文 7/12 "连接到 obsidian 知识库 给出我的详细科研路线"

---

## 🎯 一句话主线

> **当 LLM Agent 互相通信时,输出会怎样?**
> 答案:通信带来双面性(策略共识 + 校准传染),校准不是银弹,评估本身存在不可能三角。

---

## 🌱 第一阶段 · 2024 下半年 — 概念萌芽期

| 事件 | 内容 | 本地位置 |
|---|---|---|
| **AE-TTL** 提出 | Adaptive Ensemble Test-Time Learning 框架雏形 | `F:\Research\_archive\arxiv_main\papermain.tex` |
| **EPC** 首次命名 | Evaluator Preference Collapse(评估者偏好坍缩)| `F:\Research\_archive\arxiv_main\epc_paper.tex` |
| 核心假设 | 自评估偏差在 test-time agent evolution 中系统存在 | — |

---

## 🎨 第二阶段 · 2025 上半年 — MM-EPC 时代(双模态验证)

| 事件 | 内容 | 本地位置 |
|---|---|---|
| **MM-EPC v1→v3** | 文本 + 图像双模态验证 evaluator preference coupling | `F:\Research\_archive\arxiv_main\mm_epc_paper.tex` |
| 投稿路径 | ACL 2027 → ICLR 2027 → TMLR 2027 | `F:\Research\_archive\acl_2027\` / `_archive\iclr_2027\` / `_archive\tmlr_2027\` |
| 多轮审稿 | R1 / R2 / R3 共 3 轮同行评议 | `F:\Research\_archive\arxiv_main\mm_epc_paper_review.md` / `mm_epc_paper_rereview.md` / `mm_epc_paper_acl_review_v3.md` |
| 中文期刊同步 | 投稿《计算机工程与科学》 | `F:\Research\joces_templates\` |
| **关键实验组** | 19 个 JSON 数据集:phase1 / phase3 / multi-seed / GPT-4o / Qwen3-7B / real image / ablation 等 | `F:\Research\experiments\mm_epc_*.json` |

**MM-EPC 留下的方法学遗产**:
- 19 组实验设计模式(max ablation / no-S0 ablation / symmetric / contagion / bootstrap)
- 4 个统计脚本:`ece_calibration.py` / `self_calibration_paradox.py` / `decay_curve.py` / `confirmatory_decay.py`

---

## 🔀 第三阶段 · 2025 下半年 — 分叉成 6 条研究线

经过 MM-EPC 多轮 R&R,意识到单一论文装不下所有发现,于是**主动分叉**为 6 条平行主线:

### 🔵 线 1:通信效应线

> **问题:通信引起同化还是分化?**

| 论文 | 状态 | 本地位置 |
|---|---|---|
| BOUNDARY_SYNC(独立版)| arXiv 2607.01600 / TMLR #48 | `F:\Research\boundary_sync_standalone\` |
| Two Faces of Communication(FLAGSHIP)| TMLR #48 | `F:\Research\FLAGSHIP\` |
| Contagion Networks | arXiv 2606.20493 | `F:\Research\contagion_networks\` |
| Memory Contagion | arXiv 2606.23195 | `F:\Research\memory_contagion\` |
| Strategy Collapse Dynamics(已合并)| 融入 FLAGSHIP | `F:\Research\tmlr_p17\` |

### 🟢 线 2:校准效应线

> **问题:校准什么时候有用,什么时候反而有害?**

| 论文 | 状态 | 本地位置 |
|---|---|---|
| Calibrating the Evaluator | arXiv 2606.31371 | `F:\Research\tmlr_p9\` |
| Self-Evaluation Immunity | stub | `F:\Research\tmlr_p10\` |
| Probability Calibration Worsens Noise | 归档 | `F:\Research\tmlr_p15\` |
| Calibration Effects(合并版)| TMLR #53 | `F:\Research\CALIBRATION_EFFECTS\` |

### 🟡 线 3:重采样校准线

> **问题:数据处理如何影响校准?**

| 论文 | 状态 | 本地位置 |
|---|---|---|
| Hidden Cost of Resampling | arXiv 2606.29720 / TMLR #50 | `F:\Research\tmlr_p6\` |
| EMNLP 2027 LLM Embeddings + Tree Ensembles | 归档 | `F:\Research\_archive\emnlp_2027\` |
| N-Sensitive Calibration | arXiv 7774801 / TMLR #52 | `F:\Research\RESAMPLING_CALIBRATION\` |

### 🔴 线 4:评估可靠性线

> **问题:评估本身有多可靠?**

| 论文 | 状态 | 本地位置 |
|---|---|---|
| Impossibility Triangle | arXiv 在投 | `F:\Research\impossibility_triangle\` + `arxiv_p13\` |
| Within-Condition Testing | arXiv 在投 | `F:\Research\tmlr_p14\` + `arxiv_p14\` |
| Mapping the Evaluation Frontier | arXiv 2607.00304 | `F:\Research\tmlr_p16\` |
| External Validation | 融入 FLAGSHIP | `F:\Research\_archive\tmlr_external_validation\` |

### 🟣 线 5(横切):方法与协议

| 论文 | 状态 | 本地位置 |
|---|---|---|
| EPC: Standardized Protocol | arXiv 2607.00297 / TMLR #51 | `F:\Research\tmlr_p11\arxiv_submit\` |
| Diagnostic Framework | arXiv 2606.29719 / TMLR #49 | `F:\Research\_archive\acl_2027\` |
| Contagion Tensor | arXiv 2606.28839 / TMLR #47 | `F:\Research\_archive\contagion_tensor\` + 根目录 zip |
| Multimodal EPC | arXiv 2606.16682 | `F:\Research\_archive\aaai_student_abstract\` |

### ⚪ 线 6(横切):理论批判

| 论文 | 状态 | 本地位置 |
|---|---|---|
| Category Error(多 Agent 模拟建模范畴错误)| 归档 | `F:\Research\_archive\tmlr_category_error\` |
| Symmetric LR Refutation | 融入 TEMPORAL_DYNAMICS | `F:\Research\tmlr_p13\` |

---

## 🔄 第四阶段 · 2026 上半年 — 收敛整合

把分散论文合并为**旗舰版**和**方法学统一版**:

| 整合产物 | 来源 | 位置 |
|---|---|---|
| **PAPER1 / FLAGSHIP** | BOUNDARY_SYNC + Contagion Networks + Within-Condition + Triangle + Category Error + External Validation 全部融入 | `F:\Research\FLAGSHIP\` |
| **CALIBRATION_UNIFIED** | tmlr_p9 + tmlr_p10 + tmlr_p15 + Calibration Effects 整合 | `F:\Research\CALIBRATION_UNIFIED\` |
| **impossibility_triangle_consolidated** | Triangle 各版本合并 | `F:\Research\impossibility_triangle_consolidated\` |

期间建设:
- **Loop Engineering v5.3** — 论文质量审计系统,91 条规则、15 个 Python 模块,位于 `F:\Research\.loop\` + `F:\Dev\loop-engineering\`
- **82 条自动审稿规则** — 4 级(Tier 1: 7 条阻断 / Tier 2: 10 条重要 / Tier 3: 8 条打磨 / Defense: 4 条对抗),跨论文 8 条模式
- **5 篇已发表 TMLR 基线对比** — 你的论文 CI 报告率 / 效应量报告率处于 **Top 5%**

---

## 🚀 第五阶段 · 2026-06 ~ 2026-07 — R2 提升 + 新方向

### 📌 5 月 deadline 主线(本轮)

为了 5 月 deadline 6 篇论文彻底重写:

| Paper | 标题 | 位置 | verify 状态 |
|---|---|---|---|
| **PAPER1_CONSOLIDATED** | What Communication Does to Multi-Agent LLM Systems | `F:\Research\PAPER1_CONSOLIDATED\` | 0H/2M/3L |
| **PAPER2_CONSOLIDATED** | The Impossibility Triangle of LLM Evaluation | `F:\Research\PAPER2_CONSOLIDATED\` | 0H/5M/2L |
| **PAPER3_CONSOLIDATED** | Calibration Fatigue, Self-Evaluation Fragility, and the Coupling-Noise Tradeoff | `F:\Research\PAPER3_CONSOLIDATED\` | 0H/12M/3L |
| **PAPER4_CONSOLIDATED** | N-Sensitivity | `F:\Research\PAPER4_CONSOLIDATED\` | 0H/9M/4L |
| **PAPER5_CONSOLIDATED** | Empirical Comparison of Memory Architectures | `F:\Research\PAPER5_CONSOLIDATED\` | **0H/0M/0L / exit 0** ✅ 完全干净 |
| **PAPER6_CONSOLIDATED** | A4 Verifier Capture / Empirical Study / Negative Result | `F:\Research\PAPER6_CONSOLIDATED\` | 11/12 PASS |
| **Genesis-Master** | 4 层反馈循环(已投 TMLR 7/9 v1.0)| `F:\Research\genesis-master\` | ✅ |
| **PAPER35** | Agent Behavior Regression Test Suite | `F:\Research\PAPER35_FRONT_DRIFT\` | 🟡 skeleton ready |

### 🎯 PAPER5 R2 完整工作流(2026-07-12 全部完工)

| 阶段 | 产出 | 位置 |
|---|---|---|
| Stage 1 | reproduce_peer + scoring + 17/17 测试 + Qwen 6 cells 真 γ | `F:\Research\PAPER5_CONSOLIDATED\reproduce_peer\` |
| Stage 2 | cover_letter + openreview checklist + arxiv checklist | `F:\Research\PAPER5_CONSOLIDATED\cover_letter.md` 等 |
| Stage 3 | SVD-64 dense sensitivity probe (300 calls, Γ=26.55) | `run_svd_dense_sensitivity.py` |
| Stage 3 | External judge on 5% sample (120 calls, ΔECE ±0.006) | `run_external_judge.py` |
| **A** | **SVD-64 + judge 真数字已填进 paper** | `main.tex` + `supplementary/paper5_supp_sample_budget.tex` |

### 🆕 新论文立项(2026-07-11 w2 决策)

| 论文 | 标题 | 候选会议 |
|---|---|---|
| **PAPER35** | Frontier Model "对齐退化" 静默偏移(Agent Behavior Regression Test Suite)| USENIX Security |

12 周计划已敲定,6 个兄弟窗口可喂资产(w1 Qwen n=10 baseline / w5 ablation_results / w7 arxiv 模板 / w9 EPC γ 工具 / w10 KB must-cite / w4 v1.0 预留字段)。

---

## 📊 产出统计(Obsidian vault 索引口径)

| 维度 | 数量 |
|---:|---|
| arXiv 已发表 | 10 篇(2606.16682 ~ 2607.01600)|
| arXiv 在投 | 8 篇(7774801, 7780195, 7782801, 7784925, 7786759, 7786771, 7790443, 7791466)|
| TMLR 审稿中 | 10 篇(#47-56)|
| 已合并到其他论文 | 4 篇(Category Error / External Validation / tmlr_p12 / tmlr_p17)|
| **独立论文(去重后)** | **23 篇** |
| 待写 arXiv | 1 篇(closing_landscape)|
| 实验总次数 | 100+(约 9900 BOUNDARY_SYNC API calls + others)|
| 使用模型 | 5+(GPT-4o, DeepSeek V4, Qwen3.7, Claude, GLM)|
| 投稿过的会议 | 5(ACL, ICLR, EMNLP, AAAI, TMLR)|

---

## 🔗 论文依赖与融合关系

```
AE-TTL → EPC → MM-EPC → Diagnostic Framework (#49)
                         │
        ┌────────────────┼────────────────┐
        │                │                │
  Contagion Tensor   EPC Protocol   Temporal Dynamics
  (#47)              (#51)          (待整合)
        │
  ┌─────┼─────┐
  │     │     │
Contagion  Memory  Calibration
Networks   Contagion  Contagion
(2606.20493)(2606.23195)(待交)
  │     │     │
  └─────┼─────┘
        │
  ┌─────┴─────┐
  │           │
BOUNDARY_SYNC CALIBRATION_EFFECTS
(#48)        (#53)
  │           │
Two Faces of RESAMPLING_CALIBRATION
Communication (#52)
(arXiv 7782801)
  │
  ├── 不可能三角(融入)
  └── 评估前沿 (2607.00304)
```

---

## 🎯 下一步行动(对应 Obsidian `🏠_科研总览.md`)

| 优先级 | 任务 | 目标 |
|:---:|---|---|
| 🔴 | **PAPER5 R2 投稿** | TMLR 接受(已 cover letter + checklist 备好,等你本人上传 30-45 min)|
| 🔴 | 完成 closing_landscape | 评估不可能三角的解决方案 |
| 🔴 | 不可能三角形式化证明 | 巩固 PAPER2 理论根基 |
| 🟡 | 完成 arXiv 提交(4 篇 incomplete)| #52, #53, #54, #55 |
| 🟡 | PAPER1-4 MED/LOW 修复(~4h)| 全面 audit-ready |
| 🟢 | PAPER35 12 周计划启动 | USENIX Security 投稿 |
| 🟢 | 清理 arXiv 重复(7768916, 7768917)| 已融合 Two Faces |

---

## 🔗 关联知识页面

- [5 月 Deadline 研究论文总览](./index.md) — 6 篇 CONSOLIDATED 专题
- [本地论文目录盘点(analysis)](../analysis/papers-local-inventory-2026-07-12.md) — 39 个顶层目录全清单
- [刘泽文 — 研究系统全图](../entities/liu-zewen-research.md) — 研究系统总图
- [PAPER1 Entity](./paper1.md) / [PAPER2](./paper2.md) / [PAPER3](./paper3.md) / [PAPER4](./paper4.md) / [PAPER5](./paper5.md) / [PAPER6](./paper6.md) / [PAPER35](./paper35.md)