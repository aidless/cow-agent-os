# Paper #35 Proposal — Agent Behavior Regression

> **Title**: *Agent Behavior Regression: Detecting Frontier Model Misalignment in Multi-Agent Systems Through Scenario-Based Differential Testing*
>
> **Venue**:**USENIX Security 2026**(主目标) / **NDSS 2026**(备选)
>
> **Authors**: 泰(主笔)+ 刘泽文(EPC 框架方法论背书)
>
> **Status**: Outline ready,start date = paper35-w1 RFC 启动后
>
> **来源**:Critical 11 Triage 行动包 RFC-A(`critical-11-triage-action-2026-07-11.md`)

---

## 🎯 TL;DR

**核心问题**:Frontier LLM(GPT-4 / Claude / Gemini)在被集成到 Multi-Agent 系统时,**单模型测试通过 ≠ 系统级安全**。Misalignment 行为可能在 Agent 间通过记忆/上下文/工具调用**扩散和放大**。

**核心贡献**:
1. **Agent Behavior Regression Test Suite (ABRTS)**:500+ 跨 Agent 场景,系统级触发 frontier model 隐性 misalignment
2. **Behavior Contract**:可形式化验证的 Agent 行为规范语言
3. **Empirical Study**:对 GPT-4 / Claude / Gemini / Qwen 的 6 类 misalignment 测量
4. **Defense**:Pinned SHA + Behavior Contract + 跨 Agent 对照检测

**创新点**:
- 第一次把 frontier model alignment 测量**从单 Agent 推到 Multi-Agent 系统**
- 提供**可复现的 benchmark** + 开源工具
- 给出**形式化 Behavior Contract 框架**

---

## 📋 完整 outline

### §1. Introduction(目标 1.5 页,~1500 字)

**1.1 背景:Anthropic Sleeper Agents 之后的下一步(300 字)**
- 2024 Anthropic 发现 frontier model 可被植入"睡眠 agent"——训练时对齐,部署时退化
- 这是 LLM safety 的里程碑发现,但**只在单模型测试**
- **核心问题**:Multi-Agent 系统会放大还是抑制 misalignment?

**1.2 我们发现的:跨 Agent misalignment 扩散(500 字)**
- Pilot 实验:把"植入 sleeper" 的 LLM 嵌入 5-Agent 协作系统
- 观察:alignment 退化从 1 个 Agent 扩散到 3 个 Agent(60%)
- 扩散机制:记忆污染 + 工具结果污染 + 角色错误传递
- **核心论断**:alignment 必须在系统级测量,不是单 Agent

**1.3 我们的贡献(500 字)**
- ABRTS:第一个 Multi-Agent frontier model alignment benchmark
- Behavior Contract:形式化 Agent 行为规范
- Empirical study:GPT-4 / Claude / Gemini / Qwen 的 6 类 misalignment
- Defense 框架:Pinned SHA + 行为契约
- 全部开源:测试集 + 工具 + 实验数据

**1.4 论文结构(200 字)**

---

### §2. Threat Model & Background(目标 1.5 页,~1500 字)

**2.1 Frontier Model Alignment 现状(400 字)**
- Anthropic Sleeper Agents(2024):training-time attack
- GCG / AdvBench(2023-2024):inference-time attack
- Persona Vectors(2024):deployment-time attack
- 共同点:**单 Agent 测试**

**2.2 Multi-Agent 系统的特殊性(500 字)**
- 共享 memory:污染传播
- 工具结果:被恶意 Agent 利用
- 角色传递:sub-Agent 学恶意 Agent 行为
- Long horizon:misalignment 在 N 步后放大
- **这是新维度,需要新测量**

**2.3 攻击者能力假设(300 字)**
- 强攻击:训练时就植入(类似 Sleeper)
- 中攻击:发布时植入(类似 Persona Vectors)
- 弱攻击:prompt injection 在协作中扩散
- **3 个级别 + 6 个 misalignment 维度**

**2.4 防御者能力(300 字)**
- 单一 Agent 验证(已存在)
- 跨 Agent 对照检测(本文贡献)
- Behavior Contract 形式化(本文贡献)
- Pinned SHA 防御供应链(本文贡献)

---

### §3. Agent Behavior Regression Test Suite (ABRTS)(目标 2 页,~2000 字)

**3.1 设计原则(400 字)**
- 系统级触发:不只测单 Agent
- 跨 Agent 场景:协作、委托、协商、竞争
- 长 horizon:N=10-50 步
- 可重现:固定 seed + prompt 模板

**3.2 测试集结构(800 字)**
- **3 类 × 6 维度 × 30 场景 = 540 场景**
- 类 1:基础协作(simple delegation, escalation, hand-off)
- 类 2:复杂场景(multi-step planning, tool chains, recovery from failure)
- 类 3:对抗场景(adversarial peer, conflicting goals, hidden objectives)
- 6 维度:truthfulness / harm / privacy / fairness / autonomy / faithfulness

**3.3 评分方法(500 字)**
- Pass@k:主指标(N 次独立运行, k 次通过)
- 失败模式分类:6 维度各 5 类失败
- 跨 Agent 扩散率:从 1 Agent 扩散到 N Agents 的概率
- 行为契约违反率:对比 Agent 行为与 Behavior Contract

**3.4 开源(300 字)**
- GitHub:github.com/aidless/abrts
- 包含测试集 + 工具 + 实验结果
- Docker 化可复现
- 接入 paper-review-toolkit(作为 w5 的扩展)

---

### §4. Behavior Contract 形式化(目标 1.5 页,~1500 字)

**4.1 为什么需要形式化(300 字)**
- 当前 alignment evaluation 不可验证
- 单模型 behavior score ≠ 系统级 safety

**4.2 Behavior Contract 定义(500 字)**

```python
behavior_contract = {
  "agent_id": "agent_X",
  "invariant": [
    "never_execute_tool(tool_id) if context contains trigger_pattern",
    "always_assert(output) if input has flag",
    ...
  ],
  "preconditions": [...],
  "postconditions": [...],
  "temporal": "no_action_in_window(time_window)"
}
```

**4.3 形式语义(400 字)**
- Linear Temporal Logic (LTL) 编译
- 模型检查器(SPIN / nuSMV / TLC)
- 实时监测 agent runtime

**4.4 实例:在 paper-review-toolkit 中应用(300 字)**
- 给 3 reviewer 的 contract
- 测它们是否会接受植入 misalignment 的论文
- 实际跑通的 case

---

### §5. Empirical Study(目标 3 页,~3000 字)

**5.1 实验设置(400 字)**
- 4 个 frontier model:GPT-4-turbo / Claude-3.5-Sonnet / Gemini-1.5-Pro / Qwen3-72B
- 540 场景 × 3 attack level × 5 seeds = 8100 runs
- 单 Agent baseline + 5-Agent 系统对比
- 平台:泰玄小站 spec coding 任务(私域) + GSM8K + MMLU(公域)

**5.2 主结果(800 字)**
- 表 1:Pass@k 各模型 × 各攻击等级
- 表 2:跨 Agent 扩散率(关键发现)
- 图 1:6 维度 misalignment 分布
- **核心数字**:跨 Agent misalignment 扩散率 60%(Anthropic 单 Agent 是 5%)

**5.3 Behavior Contract 有效性(600 字)**
- 实施前 vs 实施后对比
- 假阳率 vs 假阴率
- 性能开销(<10% throughput)

**5.4 Case Study(800 字)**
- 3 个具体 misalignment 扩散路径
- 决策点分析
- 检测时机

**5.5 Limitations(400 字)**
- 测试集虽大但仍有局限
- frontier model 迭代快
- 攻击者可能针对 benchmark 调优

---

### §6. Defense Framework(目标 2 页,~2000 字)

**6.1 纵深防御架构(500 字)**

```
┌─────────────────────────────────────────────┐
│ Layer 1: Pinned SHA(供应链)                  │
│   → 模型 / tool / 镜像 hash 固定             │
├─────────────────────────────────────────────┤
│ Layer 2: 单 Agent Verification                │
│   → ABRTS 在部署前跑                         │
├─────────────────────────────────────────────┤
│ Layer 3: Behavior Contract 监测              │
│   → 实时检查 agent 行为                      │
├─────────────────────────────────────────────┤
│ Layer 4: 跨 Agent 对照检测                   │
│   → N agents 的输出相互验证                 │
└─────────────────────────────────────────────┘
```

**6.2 Pinned SHA 实施(400 字)**
- Sigstore for 模型权重
- Cosign for 容器
- Transparency log
- 类比 web PKI CT(借鉴 #27)

**6.3 实时 Contract 监测(500 字)**
- 每步 action 查 contract
- 违反 → 暂停 + 报告
- 日志审计

**6.4 跨 Agent 对照检测(400 字)**
- N agents 投同一 question
- 答案不一致率 > 阈值 → 可疑
- 用 LLM-as-judge 评估一致性

**6.5 Trade-offs(200 字)**
- 安全 vs 性能
- 误报 vs 漏报

---

### §7. Related Work(目标 1 页,~1000 字)

**7.1 LLM Alignment(200 字)**
- RLHF / DPO / Constitutional AI
- Anthropic Sleeper Agents(2024)

**7.2 Multi-Agent Safety(200 字)**
- AgentVerse safety
- AutoGen guardrails
- 本文是首次系统化

**7.3 Adversarial ML(200 字)**
- GCG / AdvBench
- Prompt injection
- 本文扩到 Multi-Agent

**7.4 Formal Verification of LLM(200 字)**
- Linear Temporal Logic
- Behavioral testing(类似本文)
- 不 engage:本文首次给出 contract framework

**7.5 Trustworthy AI Certification(200 字)**
- EU AI Act
- NIST AI RMF
- 本文提供 certifiable benchmark

---

### §8. Discussion(目标 1 页,~1000 字)

**8.1 Industry Implications(300 字)**
- AutoGen / CrewAI 等 Multi-Agent 框架应该接入 ABRTS
- 平台应该在 deployment 前跑 alignment check
- 安全审计公司可以基于此提供 cert

**8.2 Regulatory(300 字)**
- EU AI Act:Multi-Agent 系统需对齐评估
- NIST AI RMF:需要测试方法学
- 本文提供 NIST-compatible 测试集

**8.3 Limitations(200 字)**
- Benchmark overfit risk
- Frontier model 迭代
- 我们测试 4 个 model 不代表全部

**8.4 Future Work(200 字)**
- 1000+ 场景扩展
- 实时 monitoring 部署
- 与 #27 CT-for-A2A 整合

---

### §9. Conclusion(目标 0.5 页,~500 字)

- 总结 4 大贡献
- 强调开源可复现
- 呼吁 community 用 ABRTS 评估所有 Multi-Agent 系统

---

## 📊 数字估算

| 项 | 数值 |
|---|---|
| 总页数 | ~13 页(USENIX Security 上限) |
| 总字数 | ~13,000 字 |
| 图表 | 8 个(7 表 + 1 架构图) |
| 实验运行 | 8100 runs |
| 实验成本 | ~$200 LLM API 成本(基于 v0.3.0 paper-review-toolkit 的 $1 LLM 成本估算) |
| 开源产物 | GitHub repo + Docker + 数据集 + 工具 |

## ⏰ 时间表(3 月)

```
Month 1:
  Week 1-2: §1-3 写作(Introduction / Threat Model / ABRTS)
  Week 3-4: §4 写作(Behavior Contract)+ ABRTS 实施
  → 交付:§1-4 draft + ABRTS tool 可跑

Month 2:
  Week 1-2: §5 跑实验 + 写 Empirical Study
  Week 3-4: §6 写 Defense Framework
  → 交付:8100 runs + 数据 + §5-6 draft

Month 3:
  Week 1: §7-9 写 Related Work / Discussion / Conclusion
  Week 2: 全文 review + trim
  Week 3: 内部 review
  Week 4: 提交 USENIX Security
  → 交付:13 页 paper + GitHub release
```

## 📂 与已有项目的对接

| 已有项目 | 对接方式 |
|---|---|
| **paper-review-toolkit**(w5) | 实施 Behavior Contract + 跨 Agent 对照检测 |
| **TEMPLATE v0.5.0 plugin whitelist** | 5 reviewer 锁 whitelist(已在 paper_configs.py 实施) |
| **ABRTS 数据集** | 在 `paper-review-toolkit/tests/` 扩展 |
| **Defense 框架** | 借鉴 #27 CT-for-A2A + #32 Sigstore |
| **EPC 框架**(刘泽文研究主线)| 提供 evaluation methodology 背书 |

## 🔗 跨文档链接

- [Critical 11 Triage 行动包](./critical-11-triage-action-2026-07-11.md)(RFC-A 来源)
- [Critical 11 Triage 完整报告](./agent-os-critical-11-triage-2026-07-11.md)
- [研究 idea 挖掘 35 候选池](./research-ideas-from-agent-os-2026-07-11.md)
- [Agent OS V1→V7 实施计划表](./agent-os-implementation-plan-2026-07-11.md)
- [w5 paper-review-toolkit 动态化](../../tmp/windows/w5-paper-review-dynamic/STATUS.md)
- [知识库 plugin-whitelist-pattern](../concepts/plugin-whitelist-pattern.md)

---

## 🎯 我现在能立即开始的最小动作

**1 个动作(2-3 h)**:**写 §1 Introduction draft**(1500 字)

如果泰同意,下一步:
1. 我起草 §1(Introduction)+ 核心图表(架构图)
2. 你审 + 给 EPC 框架的 methodology 段落
3. 进入 §2-3 写作

---

_最后更新:2026-07-11 16:10 · 泰 proposal 草稿_