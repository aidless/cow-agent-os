# PAPER4 — Entity

_2026-07-11 创建。从 research-changelog-2026-07-11.md 自动抽取。_

---

## 📋 基础信息

| 字段 | 值 |
|---|---|
| **状态** | 🟡 needs-fix-HIGH(audit 后修正)|
| **路径** | `F:\Research\PAPER4_CONSOLIDATED` |
| **特殊情况** | 标准结构 + prebonferroni 备份 |
| **7/11 v0.3.0 audit** | 2 HIGH + 7 MED + 4 LOW |

---

## 📖 内容概述(🟡 自动抽 2026-07-11,w9 草稿,待精修)

> ⚠️ **草稿说明**:从 `F:\Research\PAPER4_CONSOLIDATED\main.tex` 自动抽取,精度 ~70%。
> 注意:这是 5 篇中**唯一元方法论论文**——讲"测量的不稳定性如何反转定性结论"本身。
> 全文 LaTeX 命令已清洗。

### Abstract(草稿)

> **论文标题**:N-Sensitivity: When Measurement Instability Reverses Qualitative Conclusions in LLM Evaluation

我们报告一个跨三项独立 LLM 评估研究中反复出现的模式:**定性结论(排名、效应方向、体制分类)系统性地依赖于样本量或实验设计**——小样本/混淆测量下的结论会在大样本/解混淆测量下反转。我们命名这一现象为 **N-sensitivity**(N 敏感性)。本文呈现两个详细案例研究:

1. **多 Agent 校准实验**(100,500 API 调用):初始混淆设计将 +0.228 ECE 差距归因于通信;迭代解混淆后揭示 **90.8% 归因于时间维度本身**,推翻"校准传染"解释。
2. **控制评估器耦合基准**(N=5 seeds,两评估器 × 两 LR 模式):同一评估器(Qwen)在非对称 LR 下测得最低耦合 γ̄=0.77 [0.60, 0.99],在对称 LR 下跻身最高 γ̄=1.38 [1.18, 1.59]——**单一设计参数驱动的定性反转**,95% CIs 完全不重叠。

我们通过最小仿真模型形式化 N-sensitivity:非平凡测量方差 + 分布偏度足以产生排名反转,并提供诊断工具和实践建议。三项独立调查中定性反转均以 p<0.05 + 效应量 ≥ 0.21 出现(Case 1 ΔECE 反转;Case 2 γ̄ 从 0.77 跳到 1.38;分类器校准排名在 N=200 vs. 5000 时翻转)。

### 主论点(三句话)

1. **N-sensitivity 是一个跨域模式**:不是单次实验失误,而是评估测量系统的结构性属性——同一现象在不同分辨率下会呈现相反结论;
2. **两个案例研究路径相反但同源**:Case 1 是混淆 → 解混淆的反转,Case 2 是同一评估器在不同 LR 模式下的反转——前者展示**实验设计的重要性**,后者展示**单一参数敏感性**;
3. **诊断工具落地**:N-sensitivity check + 最小样本量指南,从"识别问题"到"工程对策"。

### 关键词

- N-Sensitivity(N 敏感性)
- Qualitative Conclusion Reversal(定性结论反转)
- Confounded Experimental Design(混淆实验设计)
- Iterative Deconfounding(迭代解混淆)
- Calibration Contagion → Temporal Fatigue(校准传染 → 时间疲劳)
- Evaluator Preference Coupling γ̄(评估器偏好耦合均值)
- Learning-Rate Mode Asymmetry(学习率模式不对称)
- Distribution Skew(分布偏度)
- Measurement Variance Floor(测量方差下限)
- Ranking Reversal(排名反转)
- Sample Size Threshold(样本量阈值)
- Replication Crisis Methodology(复制危机方法论)

### 章节大纲(主结构)

```
§1 Introduction — 三个独立调查中反复出现的"反向结论"现象
§2 Case 1: From Calibration Contagion to Temporal Fatigue
   §2.1 Initial Design and the Confound
   §2.2 Expanded Design and Factor Decomposition
   §2.3 Pure Factor Decomposition
   §2.4 Cross-Model Evidence and Ablations
   §2.5 Summary of Case 1
§3 Case 2: Evaluator Coupling Benchmark
   §3.1 Background: Evaluator Preference Coupling
   §3.2 Benchmark Design
   §3.3 Results
   §3.4 Summary of Case 2
§4 The N-Sensitivity Framework
   §4.1 Definition
   §4.2 Why N-Sensitivity Occurs
   §4.3 Relationship to Statistical Power
§5 Synthesis: N-Sensitivity as a Structural Property
§6 Practical Recommendations
§7 Related Work
§8 Limitations
§9 Conclusion
```

### ⚠️ 关键统计警示

- **核心反转**:ΔECE +0.228 → 0.207 / 0.021 因子分解,90.8% 时间效应;
- **γ̄ 反转**:Qwen 0.77 [0.60, 0.99] → 1.38 [1.18, 1.59],CIs 完全不重叠;
- **三域 cross-domain 验证**:校准传染 + 评估器耦合 + 分类器校准均符合 N-sensitivity;
- audit 报告:**HIGH=2 / MED=7 / LOW=4**——待修(包含 power section 缺 + figure caption)。

### 🎯 核心位置(在主研究主线中)

- **元层抽象**:把 PAPER1-3 的"具体现象"上升为"评估系统的结构性属性";
- **方法学贡献**:N-sensitivity check + 最小样本量指南是其他 4 篇可直接使用的工具;
- **诚实研究样本**:把"我们自己的实验犯的错"系统化——这是少见的**研究透明性示范**,对 TMLR reviewer 有强说服力。

---

## 📋 下一步

| 任务 | 状态 |
|---|---|
| 论文结构 | ✅ 标准 |
| 备份完整 | ✅ prebonferroni 保留 |
| Audit | 🟡 待 |
| 投递 TMLR | 🟡 待 |

---

## 🎯 与 Agent OS 方案对接

如果涉及统计校正方法,可对接:
- 校准主线(Ece / Bonferroni / 多重比较)
- Calibration 概念[→](../concepts/calibration.md)

---

## 📋 2026-07-11 10:40 — paper-review-toolkit v0.3.0 audit

**触发**:用 `review_paper.py all main.tex` 跑全套审计

**预修 bug**:verify_p4.py 跟 verify_p2.py 同样病(LaTeX 反斜杠污染),原本跑不通。`F:\Research\PAPER4_CONSOLIDATED\verify_p4.py.bak_before_latexfix` 备份

| 维度 | 结果 |
|---|---|
| Quality 评分 | C 级 75.75%(启发式) |
| Verify findings | **2 HIGH + 7 MED + 4 LOW** = 13 个 |
| 主要问题 | C2 无 power section (HIGH) + C9 figure 216 缺 caption (HIGH) + C7 × 6 + "reveal" × 3 |
| LLM review | 5 个 prompt 跑通,$0.0163 |

**修复前/后差异**:1 个 MED 升 HIGH(C9 line 216 missing caption)

**action 清单**:
1. 加 power analysis section (HIGH)
2. figure 216 加 `\caption{}` (HIGH)
3. 6 处 C7 cite 改写(line 68/110/208/328)
4. 替换 3 处 "reveal" 用词

**完整结果**:[paper-review-audit-2026-07-11.md](../analysis/paper-review-audit-2026-07-11.md)

---

_最后更新:2026-07-11 12:50 → 10:40 audit 追加 11:00_
