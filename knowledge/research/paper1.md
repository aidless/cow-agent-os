# PAPER1 — Entity

_2026-07-11 创建。从 research-changelog-2026-07-11.md 自动抽取。_

---

## 📋 基础信息

| 字段 | 值 |
|---|---|
| **状态** | 🟢 audit-ready / final |
| **路径** | `F:\Research\PAPER1_CONSOLIDATED` |
| **字数** | 7487 words |
| **图表** | 1 figs / 7 tables / 0 algorithms |
| **main.tex 大小** | 57.9 KB |
| **协议 / 验证 / Release Notes** | ✓ / ✓ / ✗ |
| **Audit score** | 9 / 11 |
| **7/11 v0.3.0 audit** | 0 HIGH / 6 MED / 3 LOW |
| **Verify scripts** | verify_p1.py, verify_decite.py, verify_fixes.py |
| **备份** | 4 个 `.bak_*` files |

---

## 📖 内容概述(🟡 自动抽 2026-07-11,w9 草稿,待精修)

> ⚠️ **草稿说明**:从 `F:\Research\PAPER1_CONSOLIDATED\main.tex` 自动抽取,精度 ~70%。
> 全文 LaTeX 命令(`\DeltaCAF` 等)已清洗为可读形式,关键数值保留。

### Abstract(草稿)

> **论文标题**:What Communication Does to Multi-Agent LLM Systems: Strategy Consensus and Calibration Contagion

我们假设多 Agent LLM 系统中的通信会诱发两种可测量的效应:**策略共识(strategic consensus)** 与 **校准传染(calibration contagion)**。我们在 13 个实验条件、跨 4 个 LLM 系列、合计 36,000 次 GPT-4o API 调用和 55,000 项 Chatbot Arena 人类偏好判断上验证了这一假设。核心发现三点:

1. **策略共识仅在高噪声实像条件下涌现**(ΔCAF = −0.11),文本代理设置中不存在;
2. **校准传染仅来自时间累积效应**(E_T = +0.228,Cohen's d = 4.70),与 agent 数量无关;
3. **二者机制分离**——前者通过 TTRL 权重动力学,后者通过同伴锚定——形成"通信增强集体一致性但削弱个体自我感知"的悖论。

这些发现映射到 LLM 评估的不可能性三角,揭示根本性张力:降低行为多样性的力量同时损害校准保真度。系统设计者必须显式平衡"集体稳定性"(sync/nosync 条件下 CAF 置信区间不重叠)与"个体校准损失"(ΔECE = +0.228, p < 0.0001)。

### 主论点(三句话)

1. **统一框架**:把"策略共识"与"校准传染"解释为多 Agent 通信的两种相互独立的可测量效应;
2. **机制分离**:TTRL 动力学(共识)≠ 同伴锚定(传染),二者涌现时间尺度、可操控维度均不同;
3. **设计规则**:通信的两面性是不可消除的——只能在集体稳定 vs. 个体校准之间做权衡,不能同时优化两者。

### 关键词

- Multi-Agent LLM Systems(多 Agent LLM 系统)
- Strategy Consensus(策略共识)
- Calibration Contagion(校准传染)
- Test-Time Reinforcement Learning / TTRL(测试时强化学习)
- Evaluator Preference Coupling / EPC(评估器偏好耦合)
- Expected Calibration Error / ECE(期望校准误差)
- Consensus-Against-Field Coefficient / ΔCAF(共识-反场系数)
- Impossibility Triangle(不可能性三角)
- Constraining Force Hypothesis(约束力假说)
- Peer Confidence Anchoring(同伴信心锚定)

### 实验原料

`F:\Research\PAPER1_CONSOLIDATED\` 下:
- 数据:`data/`、`arxiv/`、`arxiv_1m/`、`arxiv_p13/`、`arxiv_p14/`、`arxiv_submission_paper1/`(共 36,000 GPT-4o 调用)
- 图表:`figures/`(1 fig + 7 tables)
- 协议/验证:`protocol.md`、`verify_p1.py`、`verify_decite.py`、`verify_fixes.py`
- 历史备份:`main.tex.bak_pre_decite`、`main.tex.bak_pre_polish`、`main.tex.bak_pre_unicode_fix`、`main.tex.bak_real`

### 章节大纲(主结构)

```
§1 Introduction
§2 Face 1: Strategy Consensus
   §2.1 EPC Framework / §2.2 Impossibility Triangle / §2.3 Communication Effect (Conditional)
§3 Face 2: Calibration Contagion
   §3.1 Self-Calibration Phenomenon / §3.2 Experimental Evidence / §3.3 Peer Confidence Anchoring
§4 External Validation(Chatbot Arena, 55,000 judgments)
§5 Complete Picture — 两面 + 约束力假说 + 与三角的连接
§6 Implications(系统设计 / 评估 / 仿真)
§7 Related Work / §8 Discussion / §9 Limitations / §10 Conclusion / §11 Appendix
```

### 🎯 核心位置(在主研究主线中)

- **理论基础**:继承 PAPER2 的不可能性三角(Impossibility Triangle)
- **实验支撑**:为 PAPER3 的"校准疲劳"重分解提供初始现象(ECE gap = +0.228)
- **元层意义**:为 PAPER4 的 N-敏感性框架提供第一个 case study 的素材

---

## 📈 演化轨迹

- **7/9**: 改进报告完成,12 句 Abstract + Limitations 章节已加
- **7/10**: 工具链 `paper-writing-agent` v24.0 已在此论文上跑通

---

## 📋 下一步

| 任务 | 状态 |
|---|---|
| 12 句 Abstract | ✅ 已加 |
| Limitations 章节 | ✅ 已加 |
| BibTeX 编译 | 🟡 待 |
| 投递 TMLR | 🟡 待 |

---

## 🔗 相关资源

| 工具 | 用途 |
|---|---|
| `paper-writing-agent` v24.0 | 改进报告生成 |
| `verify_p1.py` | 验证脚本 |
| `verify_decite.py` | 离散度验证 |
| `verify_fixes.py` | 修复回归验证 |

---

## 🎯 与 Agent OS 方案对接

**可能的研究主线对应**:(待补充 abstract 后确认)
- 如果是 multi-agent 通信 → 对接 [Multi-Agent 协作概念](../concepts/multi-agent-collaboration.md)
- 如果是 calibration → 对接 [Calibration 概念](../concepts/calibration.md)

可挖掘 idea:
- IDEA-A4(Verifier Capture Resistance)
- IDEA-B3(Dynamic Worker Pool)
- IDEA-B1(PDP 校准)

---

## 📋 2026-07-11 10:40 — paper-review-toolkit v0.3.0 audit

**触发**:用 `review_paper.py all main.tex` 跑全套审计(quick + standard + full + audit)

| 维度 | 结果 |
|---|---|
| Quality 评分 | B 级 80.75%(启发式) |
| Verify findings | **0 HIGH + 6 MED + 3 LOW** = 9 个 |
| 主要问题 | C7 ceremonial cites × 5 + C9 fig:triangle 未引用 + C10 reproducibility 缺 |
| LLM review | 5 个 prompt 跑通,$0.0153 |

**修复前/后差异**:无(本次 PAPER1 没 HIGH 揭示,因为没有 C9 missing caption 类)

**action 清单**:
1. 5 处 C7 cite 加 engage verb(line 328, 334, 336)
2. fig:triangle 加 `\ref{}`(在 body 里)
3. 补 reproducibility 段落(learning rate / seed / library version)

**完整结果**:[paper-review-audit-2026-07-11.md](../analysis/paper-review-audit-2026-07-11.md)

---

_最后更新:2026-07-11 12:50 → 10:40 audit 追加 11:00_
