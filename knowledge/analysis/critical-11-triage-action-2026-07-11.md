# Critical 11 漏洞 Triage — 行动包

_2026-07-11 16:05 沉淀。基于 `agent-os-critical-11-triage-2026-07-11.md`(9.5 KB)转化出的**可立即执行**行动清单。_

> **核心问题**:triage 文档存在,但缺少"**今天/这周/这个月**具体做什么"的转化。

---

## 🎯 一句话核心结论

**11 个 Critical 漏洞 100% 都能发 paper**(学术空白 + 增量大)。**这是研究的金矿,不是工程的负担**。

---

## 📋 P0/P1/P2 实施时间表(未来 12 月)

### 🔴 P0 — 立即启动(1 周内)

| 任务 | 工作量 | 理由 |
|---|---|---|
| **#35 Frontier 对齐退化** 启动 paper | 1 周(paper outline) | USENIX Security 顶会命中率高 |
| **#28 PQC 迁移** 启动 patch | 1 周(assessment) | 平台 V1.0 必备,NIST 标准已发布 |
| **w5 4 组 ablation** | 4 h | 给 B3 paper 提供 ground truth |
| **Critical 11 paper tracking** | 2 h | 建一个 paper-tracker,11 漏洞 → 11 候选 |

**总投入**:~1 周

### 🟡 P1 — 1-3 月内

| 任务 | 工作量 | 备注 |
|---|---|---|
| **#35 paper 完整写完**(Anthropic Sleeper Agents 后,顶会高度关注) | 2 月 | 行为测试集已建 1 月 |
| **#27 Certificate Transparency for A2A** | 2-3 月 | 经典问题+新场景 |
| **#32 Sigstore for AI** 学术 + 工程并行 | 2 月 | 双绿 |
| **#44 GDPR Data Passport Protocol** | 3 月 | 2025 起欧盟高度重视 |

### 🟢 P2 — 3-12 月内

| 任务 | 工作量 | 备注 |
|---|---|---|
| **#49 Jurisdiction-aware Kill Switch** | 3 月 | FOCI (USENIX) |
| **#51 Model Provenance / Export Control** | 4 月 | TMLS (ML Safety) |
| **#48 责任归属黑洞** | 4 月 | ICAIL (AI Law) |
| **#53 LAWS 武器化/Ethical Dual-Use** | 3 月 | AAAI Ethics |
| **#26 Cedar/Rego 0day 传导** | 3 月 | USENIX Security |
| **#33 LLM Model Switching / Behavior Contract** | 4 月 | NeurIPS 安全 workshop |
| **#34 LLM 绕过 PDP**(从 R3 High 提升) | 4 月 | NeurIPS/ACL workshop |

---

## 🎯 11 漏洞总览(决策 + 优先级)

| # | 漏洞 | 决策 | 优先级 | 顶会 |
|---|---|---|---|---|
| #26 | Cedar/Rego 0day 传导 | 🟢 Paper | 🟢 P2 | USENIX Security |
| #27 | Registry 中间人 | 🟢 Paper | 🟡 P1 | S&P / NDSS |
| #28 | Policy CA 量子破解 | 🔧 Patch | 🔴 P0 | (辅) EuroS&P workshop |
| #32 | Sandbox 镜像投毒 | 🟡 Paper+Patch | 🟡 P1 | NDSS / EuroS&P |
| #33 | LLM 模型切换 | 🟢 Paper | 🟢 P2 | NeurIPS 安全 workshop |
| #35 | Frontier 对齐退化 | 🟡 Paper+Patch | 🔴 P0 | **USENIX Security 顶会** |
| #44 | GDPR A2A 跨境 | 🟢 Paper | 🟡 P1 | PETS |
| #48 | 责任归属黑洞 | 🟢 Paper | 🟢 P2 | ICAIL (AI Law) |
| #49 | 国家级 Kill Switch | 🟡 Paper+Patch | 🟢 P2 | FOCI (USENIX) |
| #51 | 模型出口管制 | 🟢 Paper | 🟢 P2 | TMLS (ML Safety) |
| #53 | LAWS 武器化 | 🟢 Paper | 🟢 P2 | AAAI Ethics |

---

## 🎯 决策表(给你今天用)

### 决策 A:5 月 deadline 写什么?

> **答案**:**PAPER5**(已 verify 6/6 PASS,无需新工作)
> **风险**:再写新 paper 来不及 5 月。

### 决策 B:哪个 1 篇做下一轮(2026/11 NeurIPS 或 2027/5)?

> **强烈推荐**:**#35 Frontier 对齐退化**
> - 1 月 patch(行为测试集)+ 2 月 paper = 3 月可投递 NeurIPS
> - USENIX Security 顶会命中率高
> - 与刘泽文 EPC 框架完美对齐

### 决策 C:启动 patch 必须的 1 项?

> **强烈推荐**:先做 **#28 PQC 迁移**
> - 即使不写 paper,平台 V1.0 必备
> - 3 月工作量,可分阶段
> - 与 #32 Sigstore 一起做可复用基础设施

---

## 📋 实施顺序(未来 12 月)

```
Month 1:   P0 启动(#35 paper outline + #28 PQC assessment + w5 ablation)
Month 2:   #35 paper 主体写作(行为测试集) + #28 PQC 工程启动
Month 3:   #35 投 NeurIPS / #28 PQC 50% 完成
Month 4:   #27 CT-for-A2A 启动 + #32 Sigstore 启动
Month 5:   #44 GDPR 启动
Month 6:   #35 R&R / #27 paper 完稿
Month 7-9: #49, #51, #48 启动(法律/政治方向)
Month 9-12: #53, #26, #33, #34 启动(伦理/安全方向)
```

---

## 🎯 3 个立即可启动的 RFC(给泰写 paper outline)

### RFC-A: #35 Frontier 对齐退化 paper outline

```
Title: "Agent Behavior Regression: Detecting Frontier Model Misalignment in Multi-Agent Systems"
Venue: USENIX Security 2026
Sections:
  1. Introduction: Sleeper Agents 之后的下一步
  2. Threat Model: 攻击者植入 misalignment + Agent chain 扩散
  3. Behavior Regression Test Suite: 500+ scenarios
  4. Empirical Study: GPT-4 / Claude / Gemini 的对齐退化测量
  5. Mitigation: Pinned SHA + Behavior Contract
  6. Related Work: AI Safety + Adversarial ML
  7. Conclusion

工作量:1 月 patch + 2 月 paper = 3 月
负责人: 泰(写 paper 草稿)+ 刘泽文(提供 EPC 框架方法论)
```

### RFC-B: #27 CT-for-A2A paper outline

```
Title: "Certificate Transparency for Agent Registries"
Venue: S&P 2026
Sections:
  1. Introduction: A2A Registry 信任危机
  2. Background: Web PKI CT / Sigsum / Trillian
  3. Threat Model: Registry MITM
  4. Protocol Design: CT log for A2A
  5. Implementation: 基于 Trillian
  6. Evaluation: Overhead vs Security
  7. Deployment Considerations
  8. Conclusion

工作量:2-3 月
负责人: 泰(写 paper)+ 工程(Trillian 集成)
```

### RFC-C: #44 GDPR Data Passport Protocol

```
Title: "Data Passport: GDPR-Compliant Cross-Border A2A"
Venue: PETS 2026
Sections:
  1. Introduction: A2A 跨境合规
  2. GDPR Art. 44-49 + EU AI Act 映射
  3. Data Passport 设计
  4. Implementation: 嵌入 Agent Card
  5. Evaluation: 5 跨境场景
  6. Related Work: Privacy-Enhancing Tech
  7. Conclusion

工作量:3 月
负责人: 泰 + 法律顾问(待找)
```

---

## 🔗 跨文档链接

- [Critical 11 漏洞 Triage 完整报告](./agent-os-critical-11-triage-2026-07-11.md)(9.5 KB)
- [Agent OS V1→V7 实施计划表](./agent-os-implementation-plan-2026-07-11.md)
- [R3 红队 17 漏洞 #26-#42](./agent-os-red-team-r3-2026-07-11.md)
- [R4 红队 12 漏洞 #43-#54](./agent-os-red-team-r4-2026-07-11.md)
- [研究 idea 挖掘 35 候选池](./research-ideas-from-agent-os-2026-07-11.md)
- [11 窗口全量进度](./windows-progress-2026-07-11.md)

---

_最后更新:2026-07-11 16:05 · 泰 triage 行动包_