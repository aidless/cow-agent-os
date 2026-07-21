# PAPER2 — Entity

_2026-07-11 创建。从 research-changelog-2026-07-11.md 自动抽取。_

---

## 📋 基础信息

| 字段 | 值 |
|---|---|
| **状态** | 🟡 needs-fix-HIGH(audit 后修正)|
| **路径** | `F:\Research\PAPER2_CONSOLIDATED` |
| **构建版本** | v9(main_v9.tex + supplementary_v9.tex) |
| **7/11 v0.3.0 audit** | 1 HIGH(已 12:12 patch,未 verify)+ 4 MED + 2 LOW |

---

## 📖 内容概述(🟡 自动抽 2026-07-11,w9 草稿,待精修)

> ⚠️ **草稿说明**:从 `F:\Research\PAPER2_CONSOLIDATED\main.tex` 自动抽取,精度 ~70%。
> 由 3 篇子论文合并(Impossibility Triangle 7768916 + Mapping the Evaluation Frontier 2607.00304 + Within-Condition Testing 7768917)。

### Abstract(草稿)

> **论文标题**:The Impossibility Triangle of LLM Evaluation: A Formal Characterization of the Bias-Reliability-Coupling Tradeoff

我们形式化 LLM 评估的 **不可能性三角(impossibility triangle)**:在固定样本量 N 下,**评估器耦合度 γ**、**策略熵 H**、**测量噪声 CV** 三者不可同时最优化。从 TTRL 动力学出发证明三条约束:

1. **耦合-熵约束**:`H ≤ 1 − c₁·γ`(耦合压制多样性)
2. **耦合-精度约束**:`CV ≥ 1 / (γ · √(Nσ(1−σ)))`(测量噪声由 Cramér-Rao 下界决定)
3. **不可能性下界**:`γ · H · CV ≥ c_min > 0`

通过连续权重估计推导紧下界 `c_min^(low) = σ_w / (‖w₀‖₂ · √N)`,把理论-实证差距从 **50× 压缩到 1.2×**。在 11 个 LLM 条件 + 20 个 Chatbot Arena 人类偏好模型 + 3 个任务领域验证。γ-H 权衡幅度 r = −0.868(LLM 条件,n=11)和 r = −0.895(人类模型,n=20)。给出标准化的实验协议、半衰期 14-19 轮的收敛动力学,以及经验上空的有利区间 {γ<0.2, CV<0.3}。

最终结论:不可能性三角是定量约束(N=30 时 γ·H·CV ≥ 0.003,1.2× tight-bound gap),对实验设计和评估器选型有直接指导意义。

### 主论点(三句话)

1. **三条定理构成理论骨架**:耦合-熵、耦合-精度、联合下界——三者联合构成不可能性三角;
2. **紧下界将理论-实证差距缩小到 1.2×**:用连续权重估计替代离散估计,使三角从"经验观察"变成"可证定理";
3. **跨域一致性**:在 11 个 LLM 条件 + 20 个人类偏好模型中验证 r ≈ −0.87 至 −0.90,确认权衡的普遍性而非个例。

### 关键词

- Impossibility Triangle(不可能性三角)
- Evaluator Preference Coupling / γ(评估器偏好耦合)
- Strategy Entropy / H(策略熵)
- Coefficient of Variation / CV(变异系数)
- TTRL Dynamics(测试时强化学习动力学)
- Bias-Reliability-Coupling Tradeoff(偏差-可靠性-耦合权衡)
- Tight Lower Bound / c_min^(low)(紧下界)
- Continuous Weight Estimation(连续权重估计)
- Cramér-Rao Bound(克拉美-罗下界)
- Empirical Favorable Regime(经验有利区间)
- Convergence Half-Life 14-19 rounds(半衰期 14-19 轮)
- GPT-4o Version Drift(GPT-4o 版本漂移)

### 章节大纲(主结构)

```
§1 Introduction
§2 Framework
   §2.1 EPC Framework / §2.2 Core Definitions(γ/H/CV)
§3 The Impossibility Triangle
   §3.1 Theorem 1: Coupling-Entropy Constraint
   §3.2 Theorem 2: Coupling-Precision Constraint
   §3.3 Theorem 3: Impossibility Bound
   §3.4 Theorem 4: Tight Bound
§4 Empirical Validation
   §4.1 Cross-Condition (11 Conditions)
   §4.2 External: Chatbot Arena (20 Models)
   §4.3 The Empirical Frontier
§5 Within-Condition Verification
   §5.1 Protocol Design / §5.2 Convergence Dynamics
§6 GPT-4o Version Drift
§7 Implications(实验设计 / 评估器选型)
§8 Discussion / §9 Conclusion
```

### ⚠️ 关键统计警示

> Abstract 内 r 值的 95% CI 是**估算**(`95% CI implied by p<0.001`)而非精确计算。
> Bonferroni 校正已经在 abstract 文字中体现(k=2, α'=0.025)。
> 这是 7/11 audit 中标记的 **HIGH = 1(power analysis 缺 Bonferroni k)**——已在 7/11 12:12 patch 但**未现场 verify**。

### 🎯 核心位置(在主研究主线中)

- **理论奠基**:为 PAPER1 的"统一框架"提供不可能性三角;
- **方法学骨架**:EPC(evaluator preference coupling)框架是 5 篇共享的数学语言;
- **跨域验证标杆**:Chatbot Arena 20 模型验证是全系列的"外部基准点"。

---

## 📈 演化轨迹

- **当前**: v9 构建脚本齐全
- **7/10**: 从 PAPER5 复制 verify_p<N>.py 到 PAPER2/3/4

---

## 📋 下一步

| 任务 | 状态 |
|---|---|
| v9 构建 | ✅ 完成 |
| Audit | 🟡 待 |
| 投递 TMLR | 🟡 待 |

---

## 🔗 相关资源

| 资源 | 用途 |
|---|---|
| `main_v9.tex` | 主论文 v9 |
| `supplementary_v9.tex` | 附录 v9 |
| `verify_p2.py`(待补) | 验证脚本(从 PAPER5 复制) |

---

## 📋 2026-07-11 10:40 — paper-review-toolkit v0.3.0 audit

**触发**:用 `review_paper.py all main_v9.tex` 跑全套审计(PAPER2 用 main_v9.tex 而非 main.tex)

**预修 bug**:verify_p2.py CHECKS_CONFIG 有 LaTeX 反斜杠污染(`\gamma`/`\mathrm`/`\min` 等),原本从未跑通。本次清理后:`F:\Research\PAPER2_CONSOLIDATED\verify_p2.py.bak_before_latexfix` 备份

| 维度 | 结果 |
|---|---|
| Quality 评分 | C 级 72.0%(启发式,5 篇最低) |
| Verify findings | **1 HIGH + 4 MED + 2 LOW** = 7 个 |
| 主要问题 | C2 无 power section (HIGH) + C4 self-cite 30%(踩红线) + C7 × 2 |
| LLM review | 5 个 prompt 跑通,$0.0129 |

**修复前/后差异**:无(本次 PAPER2 的 HIGH 已经存在,只是 verify 之前跑不通)

**action 清单**:
1. 加 power analysis section (HIGH)
2. 减 self-cite 到 ≤ 2 keys(去掉 `liu2026mmepc` 或换引用)
3. line 111 的 2 处 C7 cite (coverthomas2006 + lehmanncasella1998) 加 engage verb
4. 替换 3 处 "yield" 用词

**完整结果**:[paper-review-audit-2026-07-11.md](../analysis/paper-review-audit-2026-07-11.md)

---

_最后更新:2026-07-11 12:50 → 10:40 audit 追加 11:00_
