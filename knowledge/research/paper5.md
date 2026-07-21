# PAPER5 — Entity

_2026-07-11 创建。从 research-changelog-2026-07-11.md 自动抽取。_

> ⚠️ **2026-07-11 13:50 状态修正**(基于 7/11 10:40 paper-review-toolkit v0.3.0 audit):
> **PAPER5 不再是"唯一可投递"** — audit 揭示 3 张 figure 缺 caption (HIGH × 3)。
> 完整 findings 见 [`paper-review-audit-2026-07-11.md`](../analysis/paper-review-audit-2026-07-11.md)。

---

## 📋 基础信息

| 字段 | 值 |
|---|---|
| **状态** | 🟢 **唯一 verify 全过** |
| **路径** | `F:\Research\PAPER5_CONSOLIDATED` |
| **关键标志** | verify_p5.py 6/6 PASS |
| **投递目标** | TMLR(主) |

---

## ✅ 已完成审计

| 维度 | 分数 |
|---|---|
| correctness | 80% |
| novelty | 80% |
| reproducibility | 100% |
| clarity | 100% |
| statistical_rigor | 75% |
| prior_work | 100% |
| writing_quality | 100% |
| **总评分** | **B 级 88.5%** |
| **类型识别** | "analysis" 9.09% confidence(低置信度符合多方法论文) |

**审计来源**: paper-review-toolkit full 模式,2026-07-10 跑通。

---

## 📖 内容概述(🟡 自动抽 2026-07-11,w9 草稿,待精修)

> ⚠️ **草稿说明**:从 `F:\Research\PAPER5_CONSOLIDATED\main.tex` 自动抽取,精度 ~70%。
> 本篇是 5 篇中**唯一纯工程应用论文**(其他都是理论/元方法论)——讲"哪种记忆架构抗偏差最好"。
> 全文 LaTeX 命令已清洗。

### Abstract(草稿)

> **论文标题**:Empirical Comparison of Memory Architectures for Bias-Resistant Multi-Agent LLM Systems

多 Agent LLM 系统越来越依赖记忆架构,但先前关于 Memory Contagion 的工作仅测试了**单一设计**(append + summarization)。本文系统比较三种架构——**Append-Only**、**Summarization**、**RAG with relevance filter**——跨两个模型(DeepSeek V4-Chat, Qwen3.7-Plus)、两类偏差(长度膨胀 α=1.5;权威偏差:源标签如"according to Nature 2024")、三种污染率 p∈{0.2, 0.5, 0.8}(实验开始时被改写的存储输出比例)。偏差传播用 **Γ_temporal** 量化——带偏差 vs. 干净输出长度分布的 Wasserstein-1 距离(越低越好);显著性用配对 t 检验 + family-level Bonferroni(k=9)。

核心发现:
- **DeepSeek V4-Chat 上出现 crossover**:RAG 在 p=0.2 时最低(−27.9%, d=0.40, n.s.),Summarization 在 p=0.8 时最低(−27.3%, d=1.21, family-level Bonferroni 下不显著);
- **Qwen3.7-Plus 上无 crossover**:Append-Only 对两类偏差都严格最小化 Γ;Summarization **将权威偏差放大了 107%**(d=4.30, p_adj<0.001);
- Holm-Bonferroni、BH-FDR 和交叉点 bootstrap 检验(DeepSeek: 0.78 support;Qwen: 0.04)都确认**跨模型不对称性**。

**实践结论:必须经验验证——不存在通用最优架构。**

### 主论点(三句话)

1. **三种记忆架构不是单调排序**:DeepSeek 偏好 RAG(low contamination),Summarization(high contamination);Qwen 全程偏好 Append-Only——架构选择有**模型依赖性**;
2. **偏差类型与架构选择交互**:Summarization 在 Qwen 上对长度偏差温和,对权威偏差**放大 107%**——不是"所有偏差同等对待";
3. **不存在通用赢家**:3 架构 × 2 模型 × 2 偏差 × 3 污染率 = 162 实验,**全部需经验验证**,任何"某种架构最好"的宣称都是过拟合。

### 关键词

- Memory Architecture(记忆架构)
- Append-Only(纯追加)
- Summarization(摘要式压缩)
- RAG with Relevance Filtering(带相关性过滤的检索增强)
- Length Bias α=1.5(长度偏差)
- Authority Bias(权威偏差)
- Source Attribution Markers(源归属标记)
- Wasserstein-1 Distance Γ_temporal(Wasserstein-1 距离)
- Bias Propagation Quantification(偏差传播量化)
- Contamination Rate p∈{0.2,0.5,0.8}(污染率)
- Cross-Model Asymmetry(跨模型不对称)
- Crossover Effect(交叉效应)
- Holm-Bonferroni Correction(Holm-Bonferroni 校正)
- BH-FDR(Benjamini-Hochberg FDR)
- Multi-Agent Memory(多 Agent 记忆)

### 章节大纲(主结构)

```
§1 Introduction — 记忆偏差传播的研究缺口
§2 Related Work
   §2.1 Memory-Augmented LLM Agents
   §2.2 Bias Propagation in Multi-Agent Systems
   §2.3 RAG and Bias Mitigation
   §2.4 Bias in LLM Systems
   §2.5 Training Instability in TTRL-style RL
   §2.6 Sample Budget Bounds for Test-Time Scaling
   §2.7 LLM Summarization for Memory Compression
§3 Memory Architectures
   §3.1 Notation
   §3.2 Architecture 1: Append-Only
   §3.3 Architecture 2: Summarization
   §3.4 Architecture 3: RAG with Relevance Filtering
   §3.5 Statistical Protocol
§4 Experimental Setup
   §4.1 Bias Injection Protocol
   §4.2 Metrics(Γ_temporal 等)
   §4.3 Experimental Design
   §4.4 Hyperparameter Selection
   §4.5 Statistical Methods
§5 Results
   §5.1 Dose-Response (DeepSeek V4-Chat)
   §5.2 Crossover Effect
   §5.3 Statistical Significance
   §5.4 Calibration Impact
   §5.5 Cross-Model Validation (Qwen3.7-Plus)
   §5.6 Authority Bias
   §5.7 Gamma Decomposition
§6 Discussion
```

### ⚠️ 关键统计警示

- **family-level Bonferroni k=9** 已显式声明;
- **bootstrap 交叉点检验**:DeepSeek 0.78 support(支持交叉),Qwen 0.04(不支持交叉);
- **关键效应量**:Summarization + 权威偏差 on Qwen → Γ ↑ 107%, d=4.30, p_adj<0.001;
- audit 报告:**HIGH=0(真)/ MED=3 / LOW=3**——但**Bug D 残留**让 audit 报告显示"3 HIGH figure caption"(实测 verify 6 张 figure 全部有 caption)。

### 🎯 核心位置(在主研究主线中)

- **工程落点**:把 PAPER1-4 的"理论框架 + 元方法论"翻译成**具体架构选型指南**;
- **闭合回路**:PAPER3 §5.6 "Memory Architecture Design in Light of Recent Work" 反向引用本论文;
- **应用价值**:对任何构建多 Agent LLM 系统的工程师,**直接可用**的偏差控制建议。

---

## 🎯 投递行动清单

| 步骤 | 命令 / 工具 | 状态 |
|---|---|---|
| 1. 准备 BibTeX | pdflatex + bibtex | 🟡 待 |
| 2. 准备 supplementary | 整理附录 | 🟡 待 |
| 3. TMLR 格式检查 | tmlr_pipeline | 🟡 待 |
| 4. 模拟审稿 | tmlr-review-simulator full | 🟡 待 |
| 5. 准备 cover letter | 写 1 页 | 🟡 待 |
| 6. 提交 TMLR | openreview.net | 🟡 待 |

**5 月 deadline 时限**:还有 5+ 个月时间。

---

## 🔗 相关资源

| 资源 | 用途 |
|---|---|
| `PAPER5_FINAL_REPORT.md` | 终版报告 |
| `verify_p5.py` | 6/6 PASS 验证脚本 |
| `paper-review-toolkit` | 已用 full 模式审计 |

---

## 🎯 与 Agent OS 方案对接

PAPER5 已被 paper-review-toolkit 深度审计,可作为:
- 投递案例(展示已有的工具链)
- Agent OS V0.1 案例(泰玄小站 spec coding 已对标)
- Multi-Agent 实践样本

可挖掘 idea:
- PAPER5 的多方法论分析 → 启发 C1(Adversarial Iteration Methodology)
- PAPER5 的 audit → 启发 A2(Trust System)

---

## 📋 2026-07-11 10:40 — paper-review-toolkit v0.3.0 audit ⚠️ 状态更新

**触发**:用 `review_paper.py all main.tex` 跑全套审计(v0.3.0 新规则 C7-C10)

**v1 报告**(7/11 10:40)→ **v2 实测推翻**(7/11 14:05):

| 维度 | v1 报告 | v2 实测(W1 session) |
|---|---|---|
| C9 figure caption HIGH × 3 | "真问题,要修" | **❌ verify_p5.py Bug D 残留**,6 张全有 caption |
| C10 reproducibility LOW × 3 | 待补 | ✅ 仍待补(待用户给具体值) |
| 真 HIGH count | 3 | **0** |
| 真待办工时 | ~1 h | **~15 min** |

**v2 证据**(W1 实测):

1. 跑 `verify_p5.py`(当前版本 7/11 12:44 69317 bytes):
   - 输出:`6 findings · HIGH=0 / MEDIUM=3 / LOW=3`
   - 3 MED 消息**体内**仍写 `HIGH: figure (line 550/565/572) has no \caption{...}`(Bug D 残留)
2. 读 main.tex line 540-587:line 550/565/572 三处 figure 都**有**完整 `\caption{}`
3. PowerShell `[regex]::Matches(content, '\\begin\{figure\*?\}.*?\\end\{figure\*?\}', 'Singleline')` 命中 6 张 figure 全部 `hasCaption=True`

**Bug D 残留**:`verify_p5.py:181-182` 硬编码 `'C9': 'MEDIUM'` 与 finding 内部 `HIGH:` 字段冲突 —— 不影响 PAPER5 修决策,只是 verify 报告显示错位。

**修订后 action 清单**:
1. **补 reproducibility 段**:learning rate / seed / library version → 等用户给具体值
2. (可选)修 verify_p5.py Bug D 残留 → 与其他 4 篇统一改
3. ~~修 3 张 figure caption (HIGH)~~ → 已实测无需修

**真完成度**:PAPER5 仍是最容易修好的,**但真工时从 1h 降到 15 min**。

**与其他 4 篇对比**:仍是 5 篇里**最容易修好的** —— 但其"容易"源自 **C10 LOW × 3 单类问题**,而非从 v1 推断的"C9 HIGH × 3"。

**最新状态全文**:[tmp/windows/w1-paper5/STATUS.md](../../tmp/windows/w1-paper5/STATUS.md) v2

---

_最后更新:2026-07-11 12:50 → 10:40 audit 追加 11:00 ⚠️ 状态变更_
