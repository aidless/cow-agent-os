# PAPER3 — Entity

_2026-07-11 创建。从 research-changelog-2026-07-11.md 自动抽取。_

---

## 📋 基础信息

| 字段 | 值 |
|---|---|
| **状态** | 🟡 needs-fix-HIGH(audit 后修正)|
| **路径** | `F:\Research\PAPER3_CONSOLIDATED` |
| **特殊情况** | 标准结构 + arxiv_submit 子目录 |
| **7/11 v0.3.0 audit** | 1 HIGH + 10 MED + 3 LOW |

---

## ⚠️ 状态说明

🟡 **needs-fix-HIGH** — 7/11 10:40 audit 已完成,现需修复 1 HIGH(power section)+ 10 MED。

---

## 📖 内容概述(🟡 自动抽 2026-07-11,w9 草稿,待精修)

> ⚠️ **草稿说明**:从 `F:\Research\PAPER3_CONSOLIDATED\main.tex` 自动抽取,精度 ~70%。
> 全文 LaTeX 命令已清洗为可读形式。

### Abstract(草稿)

> **论文标题**:Calibration Fatigue, Self-Evaluation Fragility, and the Coupling-Noise Tradeoff in Multi-Agent LLM Systems

校准在多 Agent LLM 系统中可以从两个视角研究:**目标**(交互是否损害自评?)和**工具**(校准评估器是否能改善动力学?)。本文通过 136,500+ 真实 API 调用和 60 个仿真条件统一了两者。三个核心发现:

1. **时间性校准疲劳占主导**:通过 6 个隔离基线解混淆,初始"校准传染"发现(ΔECE = +0.228, 95% CI [+0.205, +0.253], d=4.70)中有 **90.8% 归因于时间维度本身**(ΔECE = +0.207, 95% CI [+0.181, +0.234], d=4.85, p<0.0001, Bonferroni k=5, α'=0.010),剩余 9.2% 的通信成分(p=0.041, 95% CI [+0.003, +0.041], d=0.38)在多重比较校正后**不显著**(Bonferroni-adjusted p=0.205)。上下文累积在 ±0.05 等价边界内被排除(no-history ECE=0.208 vs. with-history ECE=0.219,95% CIs overlap)。

2. **自评免疫具有模型依赖性**:DeepSeek-V4-Pro 自评产生 γ ≈ 1.06,**直接反驳**了 DeepSeek-chat 的近零结果(γ ≈ 0.03);校准将耦合降低 42%。

3. **校准增加噪声但降低耦合**:60 个仿真条件下,五种校准方法都增加 CV(+7% 到 +18%),但 confidence-gated TTRL 同时降低偏好耦合 γ ↓ 35-37%(N=15,bootstrap CIs 不重叠)。

### 主论点(三句话)

1. **校准疲劳 vs. 校准传染的解混**:先前看似"通信引起"的 ECE gap 实际 90.8% 是时间维度的产物——重新定义"传染"为单 Agent 现象;
2. **自评免疫的非普遍性**:DeepSeek-V4-Pro 自评 γ≈1.06 反驳了"自评无偏好"的普适假设,模型依赖必须显式建模;
3. **耦合-噪声权衡的工程化**:confidence-gated TTRL 在 60 条件下同时实现降耦与可控噪声,给出实操方案。

### 关键词

- Calibration Fatigue(校准疲劳)
- Calibration Contagion(校准传染)— **本论文论证此现象主要为时间效应**
- Self-Evaluation Fragility(自评脆弱性)
- Coupling-Noise Tradeoff(耦合-噪声权衡)
- Expected Calibration Error / ECE(期望校准误差)
- BOUNDARY_SYNC Protocol(BOUNDARY_SYNC 协议)
- Pure Factor Decomposition(纯因子分解)
- Confidence-Gated TTRL(信心门控 TTRL)
- DeepSeek-V4-Pro Self-Evaluation
- Multi-Agent Calibration Landscape(多 Agent 校准景观)
- Empty Favorable Regime(空有利区间)
- Model-Dependent Effect(模型依赖效应)

### 章节大纲(主结构)

```
§1 Introduction
   §1.1 Two Perspectives on Calibration
   §1.2 The Calibration Landscape
   §1.3 Three Findings and Contributions
§2 Method
   §2.1 BOUNDARY_SYNC Protocol for Calibration
   §2.2 Experimental Design: Eight Conditions
   §2.3 Pure Factor Decomposition
   §2.4 Confidence-Gated TTRL
   §2.5 Theoretical Results
§3 Results
   §3.1 Finding 1: Temporal Calibration Fatigue Dominates
   §3.2 Finding 2: Self-Evaluation Immunity Is Model-Dependent
   §3.3 Finding 3: Calibration Increases Noise but Reduces Coupling
§4 The Calibration Landscape
   §4.1 Unified Framework / §4.2 Formal Hypothesis
§5 Discussion
   §5.1 Practical Guidelines
   §5.2 Calibration Monitor: A Practical Tool
   §5.3 Cross-Domain Generalizability
   §5.4 Alternative Explanations
   §5.5 Limitations
   §5.6 Memory Architecture Design in Light of Recent Work(→ 引 PAPER5)
§6 Conclusion / Appendix
```

### ⚠️ 关键统计警示

- **Bonferroni α' = 0.010(k=5)** 已显式写入 abstract,合规。
- **ΔECE 三个分量**(总 +0.228,纯 T +0.207,纯 sync +0.021)置信区间已给。
- **DeepSeek-V4-Pro γ_T→V = 1.064, 95% CI [0.76, 1.41]** 已声明。
- audit 报告:**HIGH=1 (power analysis 缺) / MED=10 / LOW=3**——待修。

### 🎯 核心位置(在主研究主线中)

- **承接 PAPER1**:把"校准传染"从二元假设拆为"时间 + 同步"两个分量,90.8% 时间效应;
- **支撑 PAPER4**:Case 1 的解混过程是 N-敏感性的具体实例;
- **反向引 PAPER5**:§5.6 "Memory Architecture Design in Light of Recent Work" 直接引用 PAPER5 的架构选型结果。

---

## 📋 下一步

| 任务 | 状态 |
|---|---|
| 论文结构 | ✅ 标准 |
| 复制 verify_p3.py | 🟡 待(从 PAPER5 复制,改 ROOT + CHECKS_CONFIG)|
| Audit(用 paper-review-toolkit) | 🟡 待 |
| 投递 TMLR | 🟡 待 |

---

## 🔗 相关资源

| 资源 | 用途 |
|---|---|
| `arxiv_submit/` | arxiv 子目录 |
| `verify_p3.py`(待补) | 验证脚本 |

---

## 🎯 审计起点建议

```bash
# 用 paper-review-toolkit 的 full 模式
review_paper.py full F:\Research\PAPER3_CONSOLIDATED
```

---

## 📋 2026-07-11 10:40 — paper-review-toolkit v0.3.0 audit

**触发**:用 `review_paper.py all main.tex` 跑全套审计(verify_p3.py 本来就跑通)

| 维度 | 结果 |
|---|---|
| Quality 评分 | B 级 87.0%(启发式) |
| Verify findings | **1 HIGH + 10 MED + 3 LOW** = 14 个 |
| 主要问题 | C2 无 power section (HIGH) + C7 ceremonial cites × 8 + C5 × 4 |
| LLM review | 5 个 prompt 跑通,$0.0152 |

**修复前/后差异**:2 个 MED 升 HIGH(C9 missing caption 类)

**action 清单**:
1. 加 power analysis section (HIGH)
2. 8 处 C7 cite 改写(line 78/98/125/138/402/463/477)
3. abstract line 62 的 4 处 p-value 加 test name

**完整结果**:[paper-review-audit-2026-07-11.md](../analysis/paper-review-audit-2026-07-11.md)

---

_最后更新:2026-07-11 12:50 → 10:40 audit 追加 11:00_
