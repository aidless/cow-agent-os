# 5 月 Deadline 研究论文总览

_2026-07-11 沉淀。来源:F:\Research + research-changelog-2026-07-11.md。_

---

## 🎯 关键信息

**目标**:5 月 deadline 至少投递 1 篇 CONSOLIDATED 论文到 TMLR / AAMAS / NeurIPS。

**当前状态**(2026-07-11 自动扫描):

| 状态 | 数量 | 论文 |
|---|---|---|
| 🟢 **可投递** | 0 | (audit 后修正,5 篇都需修复)|
| 🟡 **needs-fix-HIGH** | 4 | PAPER2, PAPER3, PAPER4, PAPER5 |
| 🟡 **needs-fix-MED** | 1 | PAPER1 |
| 🔴 **stub** | 1 | PAPER6 |

**关键洞察**(7/11 10:40 audit 后修正):
- 5 篇 CONSOLIDATED 论文**距投稿都"中等"**,没有"最近"
- PAPER5 不再"唯一可投递"(3 张 figure 缺 caption 是 HIGH)
- PAPER2 HIGH=1 已 patch(7/11 12:12),**未 verify**
- 总修复工时:11 小时 + $1 LLM 成本
- 完整 audit 结果见 [`paper-review-audit-2026-07-11.md`](../analysis/paper-review-audit-2026-07-11.md)

---

## 📚 6 篇 CONSOLIDATED 论文清单

| 论文 | 主题 | 状态 | 路径 | entity |
|---|---|---|---|---|
| PAPER1 | **What Communication Does to Multi-Agent LLM Systems**: Strategy Consensus & Calibration Contagion(统一框架) | 🟡 audit-ready, 0H/2M/3L | F:\Research\PAPER1_CONSOLIDATED | [PAPER1.md](./paper1.md) |
| PAPER2 | **The Impossibility Triangle of LLM Evaluation**: Bias-Reliability-Coupling Tradeoff(三定理 + 紧下界) | 🟡 1H(power)/4M/2L | F:\Research\PAPER2_CONSOLIDATED | [PAPER2.md](./paper2.md) |
| PAPER3 | **Calibration Fatigue, Self-Evaluation Fragility & Coupling-Noise Tradeoff**(纯 T 90.8% 因子分解) | 🟡 1H/10M/3L | F:\Research\PAPER3_CONSOLIDATED | [PAPER3.md](./paper3.md) |
| PAPER4 | **N-Sensitivity**: When Measurement Instability Reverses Qualitative Conclusions(元方法论) | 🟡 2H/7M/4L | F:\Research\PAPER4_CONSOLIDATED | [PAPER4.md](./paper4.md) |
| PAPER5 | **Empirical Comparison of Memory Architectures for Bias-Resistant Multi-Agent LLM Systems**(纯工程) | 🟢 0H/3M/3L(verify 实测)| F:\Research\PAPER5_CONSOLIDATED | [PAPER5.md](./paper5.md) |
| **Genesis-Master** | **A Self-Creating, Self-Iterating Multi-Agent System with Four Levels of Feedback**(4 层反馈循环,18 AgentSpec) | ✅ **v1.0 已投 TMLR 7/9** | F:\Research\genesis-master | [genesis-master.md](../entities/genesis-master.md) |
| PAPER6 | **Empirical Study of Aggregation Methods Under Verifier Capture**(7 methods × 4 scenarios,Negative Result,verify 11/12 PASS) | 🟢 **W3 完工(17:42)** | F:\Research\PAPER6_CONSOLIDATED | [PAPER6.md](./paper6.md) |
| PAPER35 | **Agent Behavior Regression Test Suite**: Frontier Model Drift in Multi-Agent Pipelines(BDS metric,6 模型 × 9 月窗口,AUC=0.81 60 天预测) | 🟡 **skeleton ready + scripts smoke-tested** | F:\Research\PAPER35_FRONT_DRIFT | [PAPER35.md](./paper35.md) |

> **8 篇论文 = 5 篇 CONSOLIDATED(PAPER1-5)+ 1 篇 PAPER6(7/11 转型 Empirical Study)+ 1 篇 PAPER35(7/11 立项 Agent OS 漏洞 #35)+ 1 篇 genesis-master 已投独立论文**。
> PAPER35 是 7/11 14:00 立项的新项目,**复用 PAPER5 的 40 个 L/A scenarios** + 新增 60 个场景,**9/15 TMLR 投递**。
> PAPER6 是 7/11 13:55 红队发现的"W3 转型"(X+Z+P1):撤 CRV 主方法 → 改写为诚实 benchmark。

---

## 🛠️ 论文写作工具栈

| 工具 | 用途 | 路径 |
|---|---|---|
| **paper-writing-agent** | 21 模块写作 agent v24.0 | F:\Research\paper-writing-agent |
| **tmlr-review-simulator** | TMLR 风格审稿人模拟 | (已装 skill) |
| **tmlr_pipeline** | 端到端 TMLR 流水线 | (已装 skill) |
| **paper-review-toolkit** | 统一 wrapper,12 种审阅 | `review_paper.py` 8 子命令 |

---

## 🎯 与 Agent OS 方案的对接

7 篇 CONSOLIDATED 论文 + Agent OS 方案 15 个 idea 之间有**深度对应**:

| 论文主题(推测) | 对应 Agent OS idea | 对接概念 |
|---|---|---|
| PAPER1-5 围绕"多 Agent 通信/校准/偏好" | IDEA-A4 Verifier Capture / IDEA-B3 Dynamic Worker | [Multi-Agent](./multi-agent-collaboration.md), [Calibration](./calibration.md) |
| 5 月 deadline 与 5 阶段演化 | (无直接对应,可作为 meta paper) | (见 C1-C3) |

具体每篇论文与 idea 的精确对接,见各 PAPER entity 页面。

---

## 📋 投递优先级建议

基于 5 月 deadline + 工具链状态:

| 优先级 | 论文 | 行动 |
|---|---|---|
| ✅ **已投** | **genesis-master** | v1.0 已投 TMLR 7/9,等 reviewer 反馈 |
| 🥇 1 | PAPER5 | 立即投递(verify 全过)|
| 🥈 2 | PAPER1 | 改进报告已完成,补 BibTeX 即可 |
| 🥉 3 | PAPER2/4 | 找时间审计 → 投递 |
| ⚪ | PAPER3 | 审计后再说 |
| ⚪ | PAPER6 | stub 状态,需补实验(7/11 13:55 更新:**不该被当成"第 6 篇论文"**,那是 genesis-master)|

---

## 📋 2026-07-11 11:00 — paper-review-toolkit v0.3.0 全量审计

**触发**:用 `review_paper.py all` × 5 papers 跑完整链路,5 篇全跑通。

**重大更新**:**PAPER5 不再是"唯一可投递"** —— v0.3.0 新规则 C9 揭示其 3 张 figure 缺 caption(HIGH 级)

| 优先级 | 论文 | 当前状态 | 行动 |
|---|---|---|---|
| 🥇 1 | **PAPER5** | 3 HIGH + 0 MED + 3 LOW | 修 3 张图 caption (HIGH) + 补 reproducibility |
| 🥈 2 | PAPER1 | 0 HIGH + 6 MED + 3 LOW | 5 处 C7 cite + fig:triangle `\ref` + reproducibility |
| 🥉 3 | PAPER3 | 1 HIGH + 10 MED + 3 LOW | power section + 8 处 C7 + C5 test name |
| 4 | PAPER2 | 1 HIGH + 4 MED + 2 LOW | power section + 减 self-cite + 2 处 C7 |
| 5 | PAPER4 | 2 HIGH + 7 MED + 4 LOW | power section + fig caption + 6 处 C7 + "reveal" |

**总工时预估**:~11 小时 + $0.0745(LLM 已花完)

**完整审计报告**:[paper-review-audit-2026-07-11.md](../analysis/paper-review-audit-2026-07-11.md)

---

## 🔗 跨文档链接

- [刘泽文 — 研究系统全图](../entities/liu-zewen-research.md)
- [论文审阅工具箱](../analysis/paper-review-toolkit.md)
- [5 篇全量审计报告(7/11)](../analysis/paper-review-audit-2026-07-11.md)
- [Agent OS 完整方案](../sources/agent-os-architecture-full-2026-07-11.md)
- [研究 idea 挖掘](../analysis/research-ideas-from-agent-os-2026-07-11.md)

---

## ✅ 7/11 14:30 — w9 entity TODO 补全完成

**触发**:`tmp/windows/w9-fill-todo/STATUS.md` 任务,从 6 个 entity 抽 abstract / 关键词 / 主论点 / 章节大纲。

**5 篇已填草稿**(精度 ~70%,LaTeX 已清洗):
- PAPER1:What Communication Does to Multi-Agent LLM Systems
- PAPER2:Impossibility Triangle of LLM Evaluation
- PAPER3:Calibration Fatigue, Self-Evaluation Fragility, Coupling-Noise Tradeoff
- PAPER4:N-Sensitivity(元方法论)
- PAPER5:Empirical Comparison of Memory Architectures

**PAPER6 显式 skip**:废稿 `main.tex.LLM_FABRICATED_DO_NOT_SUBMIT` 不抽,留决策占位(3 路径候选)。

**关键发现**(草稿时挖掘):
- **5 篇共享 EPC 框架**(Evaluator Preference Coupling γ / 策略熵 H / CV)是刘泽文研究主线的方法学骨架
- **PAPER1 ↔ PAPER2 ↔ PAPER3 互引**:三角(理论) → 双面统一 → 校准疲劳解混,形成 5 篇"梯子"
- **PAPER4 是元方法论**:把 PAPER1-3 的"具体反转"抽象成"N-sensitivity"框架
- **PAPER5 是工程落点**:从理论 → 架构选型,闭合整条主线
- **6 篇主题已在 index.md 表格填入**

**待精修 3 篇**(按 DoD 要求):
1. **PAPER2** — abstract 内 r 值 CI 是估算(`implied by p<0.001`),需对照正文精确化
2. **PAPER4** — 元方法论文 abstract 较长,关键词可能漏抽(如"Compression Test"等隐含词)
3. **PAPER5** — "Authority bias amplification 107%" 等具体数值需对照 §5.6 原文确认

**完整报告**:`tmp/windows/w9-fill-todo/REPORT.md`(待写)

---

_最后更新:2026-07-11 12:50 → 11:00 全量审计追加 → 13:22 w9 entity 草稿完成(真实系统时钟)_
