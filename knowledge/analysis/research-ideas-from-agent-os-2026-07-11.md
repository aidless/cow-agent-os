# Agent OS 方案迭代研究 idea 挖掘

_2026-07-11 基于 V1→V7 完整方案 + 25 个漏洞分析,挖掘 15 个 paper idea 候选。_

> **方法**:A(漏洞 → 算法)+ B(主线 → 反向验证)+ C(meta-迭代)+ D(综合排序)

---

## 🎯 核心方法论

每个 idea 都回答 4 个问题:
1. **研究问题**:具体要解决什么?
2. **理论框架**:用什么方法?
3. **可验证性**:怎么证明工作?
4. **可行性**:实现成本 + 风险

并按 **4 维评分**:
- **N**ovelty(新颖性):Low / Medium / High
- **F**easibility(可行性):Low / Medium / High
- **I**mpact(影响力):Low / Medium / High
- **P**ublication fit(期刊适配):TMLR / NeurIPS / ICML / AAMAS / IEEE S&P

---

# Part A:从漏洞 → 算法问题(7 个 idea)

## IDEA-A1 — Distributed Policy Consensus with Staleness Bounds

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #1 PDP Boring Middle,#15 Control Plane SPOF |
| Novelty | **High**(policy consensus 鲜有人研究) |
| Feasibility | **Medium**(需要分布式系统实现) |
| Impact | **High**(任何 A2A 平台都需要) |
| Publication fit | NeurIPS / IEEE S&P |

### 研究问题

Local PDP 缓存 policy bundle 后,如何量化"中间期 staleness"对决策一致性的影响,并设计**最优 staleness bound + 风险分级策略**?

### 理论框架

- 把 PDP 决策建模为 **distributed consensus with bounded staleness**
- 用 **CAP 理论扩展** —— 在 policy consistency / availability / partition tolerance 中选最优
- 借鉴 **PBFT / Raft** 的 leader-based 决策 + 异步 fallback

### 方法

```text
1. 形式化定义:
   staleness(s) = max_delay(s, central_decision)
   consistency(s) = Pr[local_decision(s) == central_decision]
   
2. 优化目标:
   minimize total_loss = Σ over_actions P(critical | action) × E[cost_mismatch]
   subject to: staleness <= TTL(risk_level)
   
3. 算法:
   - Multi-armed bandit:不同 risk level 的最优 TTL
   - Meta-learning:跨任务的 staleness 预测模型
   - Theoretical bound:最坏情况下的 staleness-cost 关系
```

### 验证

- **仿真**:在 1000 个 Local PDP 节点上模拟 partition 场景
- **真实数据**:用 Wechat-MP validation 流水线的真实 policy 调用数据
- **指标**:decision consistency rate, false allow rate, false deny rate

### 你的优势

- 你已经在做 validate.bat 流水线(可拿到真实 policy 数据)
- paper-review-toolkit 是天然的 benchmark(可作为测试场景)
- 你的研究主线"多 Agent 协作"完美对接

---

## IDEA-A2 — Trust System Resilience under Compound Attacks

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #2 Kill Switch,#5 Trust 跳水,#11 Verified 投票作弊 |
| Novelty | **High**(trust system 弹性是空白) |
| Feasibility | **High**(可纯理论 + 仿真) |
| Impact | **High**(市场信任是 A2A 命脉) |
| Publication fit | TMLR / AAMAS |

### 研究问题

A2A trust 等级在遭遇单次严重故障时,应该**降几级、降多快、是否允许"断裂"**(永久降级)?最优降级 + 恢复曲线是什么?

### 理论框架

- 把 trust 视为**有限状态机** + 风险价值函数
- 用 **optimal stopping theory** 决定降级时机
- 借鉴 **保险精算** 的思想 —— 信任崩塌的预期损失 = 概率 × 严重度

### 方法

```text
1. 状态空间:
   T ∈ {T0, T1, T2, T3, T4}
   transition(t, t+1) 由 incident + recovery action 决定
   
2. 优化目标:
   maximize: Σ discounted(util(Trust)) - Σ cost(incident)
   subject to: P(downgrade_to_T0) <= α
   
3. 算法:
   - Q-learning on trust state space
   - Pareto frontier:严格降级 vs 宽容降级
   - Adversarial robustness:对恶意举报的弹性
```

### 验证

- **仿真**:在 10000 个 Agent 上模拟 1 年的 trust 演化
- **真实数据**:用 paper-graveyard 的 9 类 paper 死因作为"事故"输入
- **指标**:Gini coefficient of trust distribution, time to recovery

### 你的优势

- Trust 系统和你的"偏好耦合"研究主线天然契合(用户对信任的偏好)
- paper-graveyard 可以提供"事故"案例数据
- 9 类 paper 死因 ≈ 9 类事故,可作为 benchmark

---

## IDEA-A3 — Multi-Party Policy Intersection as Combinatorial Optimization

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #4 Jurisdiction 无解,#9 无声拒绝,#20 跨法域冲突 |
| Novelty | **High**(policy intersection 没有形式化研究) |
| Feasibility | **Medium**(需要法律专家 + 实现) |
| Impact | **High**(跨平台 A2A 关键) |
| Publication fit | TMLR / AAMAS / ACM EC |

### 研究问题

`effective_policy = protocol_baseline ∩ requester ∩ provider ∩ user ∩ jurisdiction` 何时为空?给定 N 个 policy 集合,如何**最大化交集**或**最优降级**?

### 理论框架

- 把 policy 集合建模为 **CSP (Constraint Satisfaction Problem)**
- 借鉴 **Pareto optimality** 思想 —— 找到"最不严格"的可行解
- **降级策略** 类似 **constraint relaxation**

### 方法

```text
1. 形式化:
   P = {p1, p2, ..., pn} 每个 pi 是 attribute 的约束集
   intersection(P) = {x | ∀i: x ⊨ pi}
   fallback(P) = argmin_x L(x) s.t. x is partial feasible
   
2. 算法:
   - SMT solver (Z3) 找可行解
   - LP relaxation 找降级
   - Heuristic:删除最不关键的约束
   - Learning:从历史任务学习常见降级模式
   
3. 关键挑战:
   - Jurisdiction 是法条 → 需要 NLP → structural mapping
   - User policy 是用户授权 → 需要从 policy DSL 解析
```

### 验证

- **基准**:构造 1000 个跨法域 A2A 任务,测试可行率
- **真实数据**:用你的 spec coding 任务作为 ground truth
- **指标**:feasibility rate, fallback minimality, user satisfaction

### 你的优势

- 你的"多 Agent 协作"主线完美对接
- 泰玄小站已有 spec coding 体系(可作为 policy DSL 实验场)
- 多边交集是 AI/OR 经典问题,你可发挥算法优势

---

## IDEA-A4 — Verifier Capture Resistance in Multi-Source Verification

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #7 LLM 幻觉传染,#11 Verified 投票作弊,#13 审计员疲劳 |
| Novelty | **High**(AI 审计的"verifier capture"是 2024+ 新问题) |
| Feasibility | **High**(可实验) |
| Impact | **High**(LLM 审计普及) |
| Publication fit | TMLR / NeurIPS / AIES |

### 研究问题

LLM-assisted 审计中,如何抵抗 **automation bias** 和 **verifier capture**?如何设计 audit protocol 让 LLM 偏差无法系统性传染?

### 理论框架

- 把 audit decision 视为 **adversarial setting**:
  - LLM 可能被对抗性训练数据污染
  - 审计员可能 rubber-stamp
  - 串通方可能让 verified 失真
- 借鉴 **Byzantine fault tolerance** —— N 个 verifier 中 f 个被攻陷时仍能保证正确

### 方法

```text
1. Adversarial Model:
   - LLM 有 ε-bias:Pr[LLM_correct] = 1 - ε
   - 审计员有 δ-fatigue:Pr[auditor_independent] = 1 - δ
   - 串通概率:Pr[collusion] = γ
   
2. Optimal Aggregation:
   - 设计 audit protocol 抵抗 bias
   - Blind audit + adversarial LLM + multiple human reviewers
   - Theoretical:1 - ε^N > 1 - ε (N 个 LLM 的多数投票)
   
3. 算法:
   - Multi-LLM ensemble:每个 LLM 不同训练数据
   - Human-in-the-loop:关键决策必须人
   - Self-consistency:同一 case 多次跑
```

### 验证

- **基准**:用 paper-review-toolkit 的现有 review 数据
- **人为注入偏差**:训练一个"恶意 LLM" 故意找某类 Agent 的茬
- **指标**:detection rate of adversarial LLM, false positive rate

### 你的优势

- paper-review-toolkit 已经是 review audit 工具
- 9 类 paper 死因 ≈ 9 类 "audit 维度"
- 你的"校准"主线天然对接(校准 LLM 偏差是核心)

---

## IDEA-A5 — Cold-Start Sandbox Task Library Design

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #8 冷启动死循环,#3 反作弊反作弊 |
| Novelty | **Medium**(已有 benchmark 设计工作) |
| Feasibility | **High**(纯工程) |
| Impact | **Medium**(应用价值高于理论) |
| Publication fit | AAMAS demo / TMLR application track |

### 研究问题

Sandbox Task Library 应该包含哪些任务类型、难度分布、更新频率,才能既支持冷启动又防止 overfit?最优任务池设计是什么?

### 理论框架

- 把任务池视为 **coverage + discrimination 的权衡**
- 借鉴 **educational testing** 的 IRT (Item Response Theory) 思想
- 用 **anti-cheating** 形式化

### 方法

```text
1. 任务池设计:
   - 任务类型分布:覆盖所有 capability
   - 难度分布:正态分布,P50 中等难度最多
   - 动态化:每 N 个月 20% 任务轮换
   - Hidden task 比例:30% 隐藏 + 70% 公开
   
2. Anti-cheating:
   - 任务参数动态生成
   - 评分规则部分隐藏
   - Adversarial task 注入
   
3. 验证:
   - Sandbox 分数 vs 真实表现 的相关系数
   - 作弊检测率(注入已知作弊 Agent)
   - 冷启动平台首次成功率
```

### 验证

- 用 paper-graveyard 9 类 detector 作为任务池的"能力维度"
- 真实 benchmark:用 paper-review-toolkit 跑全套测试作为 ground truth
- 指标:Pearson correlation between sandbox and real

### 你的优势

- paper-graveyard 9 类 detector 已经是 S2 Robustness Test 实例
- paper-review-toolkit 可作为 benchmark runner
- 你的"校准"主线直接对接(sandbox 校准真实表现)

---

## IDEA-A6 — Privacy Budget Composition in Streaming DP Aggregation

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #10 双轨泄漏,#18 DP 组合失效 |
| Novelty | **High**(streaming DP composition 是前沿) |
| Feasibility | **Medium**(需要理论 + 实现) |
| Impact | **High**(DP 实践关键) |
| Publication fit | NeurIPS Privacy in ML / TMLR |

### 研究问题

在 streaming DP aggregation 中,多次查询的 privacy budget 如何最优分配?如何检测 "correlated query attack"?

### 理论框架

- 借鉴 **DP composition theorem** (advanced composition / zCDP)
- 借鉴 **adaptive composition** 思想
- 用 **optimal stopping** 决定何时停止查询

### 方法

```text
1. 形式化:
   - 每个查询消耗 ε_i
   - total budget B
   - 目标:maximize information gain subject to Σ ε_i ≤ B
   
2. 算法:
   - Greedy allocation:每个查询边际信息增益最大优先
   - Bayesian DP:把 budget 视为 random variable
   - Adaptive stopping:query 收益 < cost 时停止
   
3. Correlated query detection:
   - 用 mutual information 检测查询间相关性
   - 高相关查询合并 → 共享 budget
```

### 验证

- **仿真**:模拟 1000 个用户、10000 次查询
- **基线**:vs uniform allocation, vs greedy without correlation
- **指标**:utility (information gain), privacy loss, correlation detection rate

### 你的优势

- 你的"校准 + 隐私 ML" 双主线天然对接
- DP 隐私预算是 ML 社区热门话题
- 算法工作容易发(NeurIPS Privacy in ML workshop)

---

## IDEA-A7 — Orhon Task Auto-Recovery in A2A State Machine

| 维度 | 评分 |
|---|---|
| 来源漏洞 | #16 A2A 中间态挂起,#1 PDP 中间态 |
| Novelty | **Medium**(状态机可靠性是经典) |
| Feasibility | **High**(纯工程) |
| Impact | **Medium**(生产价值) |
| Publication fit | IEEE S&P / TMLR engineering track |

### 研究问题

A2A 任务在中间态(need_more_info / partial_submitted)挂起时,如何自动检测 + 恢复 + 转交,保证不丢任务?

### 理论框架

- 把状态机视为 **Markov Decision Process**
- **Watchdog + heartbeat** 机制
- 借鉴 **distributed transactions** 的 saga pattern

### 方法

```text
1. State Machine Augmentation:
   - 每个状态有 timeout
   - heartbeat 监控 provider liveness
   - 自动 transfer 到 fallback provider
   
2. Recovery Strategies:
   - Resume from checkpoint
   - Reassign to other provider
   - Cancel + refund
   
3. 优化:
   - minimize lost work
   - minimize false cancellation
```

### 验证

- **仿真**:模拟 10000 个 task 经历各种 failure
- **真实**:用 paper-review-toolkit 的历史 review 状态作为测试
- **指标**:task recovery rate, time to recovery, false cancellation rate

### 你的优势

- paper-review-toolkit 已经有状态机(8 子命令)
- 工程化工作,可作为 TMLR application track

---

# Part B:从研究主线 → 反向验证方案(5 个 idea)

> 这些 idea 从你的 3 个研究主线出发,看方案中哪些地方可以用你的方法改进。

## IDEA-B1 — 校准主线:PDP 决策的 Calibration Error 量化

| 维度 | 评分 |
|---|---|
| 研究主线 | 校准(已有 5+ 论文) |
| 切入点 | PDP 的决策 allow/deny 概率可校准 |
| Novelty | **High**(决策校准 = 新方向) |
| Feasibility | **High**(你有 calibration 工具) |
| Impact | **High** |
| Publication fit | TMLR / NeurIPS |

### 研究问题

PDP 决策 `allow/deny/confirmation` 的概率估计如何校准?如何量化"PDP 说自己 90% 确定 allow,实际 allow 率多少"?

### 方法

```text
1. Calibration Error:
   - ECE:Expected Calibration Error
   - 用你的 calibration 方法评估 PDP 概率
   
2. Improved PDP:
   - Temperature scaling on PDP confidence
   - Platt scaling on decision boundary
   - Conformal prediction for risk-set
   
3. 验证:
   - 用 validate.bat 的真实 policy 决策数据
   - 校准前 vs 校准后 ECE 对比
```

### 你的优势

- 校准是你的**最强主线**(已有 5 篇论文)
- validate.bat 给你提供真实 policy 数据
- 这是"你的方法 → 改进方案"的范例

---

## IDEA-B2 — 偏好耦合主线:Trust 等级降级的用户偏好

| 维度 | 评分 |
|---|---|
| 研究主线 | 偏好耦合 |
| 切入点 | 用户对 trust 降级速度的偏好不同 |
| Novelty | **High**(trust + 偏好是空白) |
| Feasibility | **Medium**(需要用户研究) |
| Impact | **High** |
| Publication fit | TMLR / AAMAS / HCI |

### 研究问题

用户对"信任降级速度"是否有偏好?应该用 RLHF 训练个性化 trust 策略吗?

### 方法

```text
1. User Study:
   - 1000 用户,对不同 trust 场景做选择
   - 收集 preference:立即降 vs 渐进降 vs 信任修复
   
2. Personalized Trust Policy:
   - RLHF:训练模型从用户历史学习 trust 偏好
   - DPO:直接优化 preference
   
3. A/B Test:
   - 个性化 trust 策略 vs 统一策略
   - 指标:用户满意度、长期 trust
```

### 你的优势

- 偏好耦合是你的核心主线
- 用户研究 → 训练 → 部署 完整 pipeline
- 这是"你的方法 + 方案 = 新 paper" 的范例

---

## IDEA-B3 — 多 Agent 协作主线:Dynamic Worker Pool 的最优生成策略

| 维度 | 评分 |
|---|---|
| 研究主线 | 多 Agent 协作 |
| 切入点 | V3 提到 dynamic worker generation,如何最优? |
| Novelty | **High**(dynamic agent spawning 是新问题) |
| Feasibility | **Medium** |
| Impact | **High** |
| Publication fit | AAMAS / TMLR |

### 研究问题

给定 task spec,Orchestrator 应该如何动态决定:需要几个 worker、每个什么能力、是否并行?最优生成策略是什么?

### 方法

```text
1. 形式化:
   task → (n_workers, capabilities, parallel_graph)
   cost = compute_cost + coordination_cost + context_loss
   benefit = completion_rate × quality
   
2. 算法:
   - ILP:约束满足的最小 worker 数
   - RL:从历史任务学最优拆分
   - LLM-based:用 LLM 本身做 meta-controller
   
3. 验证:
   - paper-review-toolkit 8 子命令的 4 静态 vs 动态 生成
   - 指标:task completion rate, time, cost
```

### 你的优势

- paper-review-toolkit 8 子命令是现成 benchmark
- 升级到动态 worker pool 是直接的实验
- 多 Agent 是你的核心主线

---

## IDEA-B4 — 校准 + 偏好:Verifier 投票的最优加权

| 维度 | 评分 |
|---|---|
| 研究主线 | 校准 + 偏好耦合 |
| 切入点 | IDEA-A4 的多源 verified,但用校准方法 |
| Novelty | **High** |
| Feasibility | **High** |
| Impact | **High** |
| Publication fit | TMLR / AAMAS |

### 研究问题

Verifier 投票(自动/AI/人)的最优加权如何从历史数据学习?如何让权重反映 verifier 实际校准能力?

### 方法

```text
1. Verifier Calibration:
   - 每个 verifier 有自己的 calibration curve
   - 训练数据:历史 verified vs 实际 completed
   
2. Optimal Weighting:
   - minimize expected verification error
   - subject to:weights sum to 1
   
3. 个性化:
   - 不同任务类型 → 不同 verifier 权重
   - 用户偏好影响权重(关键 verified_by 选 human)
```

### 你的优势

- 校准 + 偏好 双主线
- IDEA-A4 已经在做,这是更精炼版本

---

## IDEA-B5 — 隐私 ML:DP 噪声下的 Agent 演化质量

| 维度 | 评分 |
|---|---|
| 研究主线 | 隐私 ML + 校准 |
| 切入点 | V3 提到 DP 演化,质量 vs 隐私权衡 |
| Novelty | **High** |
| Feasibility | **Medium** |
| Impact | **High** |
| Publication fit | NeurIPS Privacy in ML / TMLR |

### 研究问题

DP 噪声注入后,Agent 的 planner 策略演化质量如何变化?如何最优选择 noise level?

### 方法

```text
1. DP-Regret Bound:
   - DP planner 收敛速度 vs non-DP
   - Theoretical bound on regret
   
2. Adaptive DP:
   - 根据任务敏感度调整 noise
   - Sensitive task → more noise
   - Public task → less noise
   
3. 验证:
   - 仿真 1000 个 planner 在 DP/non-DP 下
   - 指标:regret, privacy cost, task quality
```

### 你的优势

- 隐私 ML 是新兴方向
- 你的"演化机制"研究可直接对接

---

# Part C:Meta-Iteration Paper(3 个 idea)

> 这些 idea 关于"如何通过对抗性迭代设计复杂系统"—— V1→V7 本身就是一个 meta-iteration 案例。

## IDEA-C1 — Adversarial Iteration as a Design Methodology for Complex Systems

| 维度 | 评分 |
|---|---|
| 元视角 | V1→V7 演进 |
| Novelty | **High** |
| Feasibility | **High** |
| Impact | **Medium**(SE 社区兴趣) |
| Publication fit | ICSE / FSE / IEEE Software |

### 研究问题

"战略蓝图 → 工程实现 → 漏洞分析 → 修复加固"这种 **7 轮对抗性迭代** 是不是一个可推广的复杂系统设计方法论?和传统的 waterfall / agile 比有什么优势?

### 方法

- **案例研究**:V1→V7 自身(7 轮 + 25 漏洞)
- **比较研究**:传统软件工程的迭代模型
- **形式化**:把"对抗性迭代"建模为 game(architect vs red team)

### 你的优势

- V1→V7 是真实案例(不是事后总结)
- 7 轮对话有完整 artifact(knowledge 库)
- 这是 meta-research,新颖性强

---

## IDEA-C2 — Red Teaming Agent Systems: A Vulnerability Taxonomy

| 维度 | 评分 |
|---|---|
| 元视角 | 25 个漏洞的分类 |
| Novelty | **High**(首次系统化) |
| Feasibility | **High** |
| Impact | **High**(industry 需求) |
| Publication fit | IEEE S&P / USENIX Security |

### 研究问题

Agent 系统的漏洞有没有可推广的分类法?V7 的 25 漏洞 + 3 暗模式是否构成完整 taxonomy?

### 方法

- **文献综述**:现有 agent security 论文
- **实证分析**:25 漏洞的维度(架构/激励/冷启动/演化/跨域)
- **可推广性**:在 paper-review-toolkit 上测试

### 你的优势

- 25 漏洞是真实分析
- 3 暗模式是抽象
- 可发表在 security venue(IEEE S&P)

---

## IDEA-C3 — From Architecture to Algorithm: A Study of Design Iteration Yield

| 维度 | 评分 |
|---|---|
| 元视角 | 6 轮 → 18 个研究接口的转化效率 |
| Novelty | **Medium** |
| Feasibility | **High** |
| Impact | **Medium** |
| Publication fit | ICSE NIER / FSE Ideas |

### 研究问题

复杂系统的设计迭代如何最大化"产出研究 idea"?V1→V7 的"6 轮 → 18 接口" 是偶然还是可设计?

### 方法

- **量化分析**:每轮对话产出的接口数(轮 1: 3, 轮 2: 4, 轮 3: 4, 轮 4: 4, 轮 5: 4, 轮 6: 0(没出新,补漏洞)→ 平均 3.5/轮)
- **回溯分析**:为什么某些轮产出多?
- **设计原则**:什么样的提问 → 更多 idea

### 你的优势

- 这是你的真实工作流(可作为 case study)
- 量化容易
- ICSE 风格的工作

---

# Part D:综合排序(15 个 idea 的优先级)

## 优先级矩阵

按 (Impact × Feasibility) / (Novelty inversion) 排序:

| 排序 | ID | 标题 | N | F | I | 适配 |
|---|---|---|---|---|---|---|
| 🥇 1 | **B1** | PDP 决策的 Calibration Error 量化 | H | H | H | TMLR |
| 🥈 2 | **A4** | Verifier Capture Resistance | H | H | H | TMLR/NeurIPS |
| 🥉 3 | **A1** | Distributed Policy Consensus | H | M | H | NeurIPS |
| 4 | **B4** | Verifier 投票的最优加权 | H | H | H | TMLR |
| 5 | **A3** | Multi-Party Policy Intersection | H | M | H | TMLR |
| 6 | **B2** | Trust 等级降级的用户偏好 | H | M | H | TMLR |
| 7 | **A2** | Trust System Resilience | H | H | H | TMLR |
| 8 | **B5** | DP 噪声下的 Agent 演化质量 | H | M | H | NeurIPS Priv |
| 9 | **A6** | Privacy Budget Composition | H | M | H | NeurIPS Priv |
| 10 | **B3** | Dynamic Worker Pool 最优生成 | H | M | H | AAMAS |
| 11 | **C2** | Red Teaming Agent Systems Taxonomy | H | H | H | IEEE S&P |
| 12 | **A5** | Cold-Start Sandbox Design | M | H | M | AAMAS demo |
| 13 | **C1** | Adversarial Iteration as Design Method | H | H | M | ICSE |
| 14 | **A7** | Orphan Task Auto-Recovery | M | H | M | TMLR eng |
| 15 | **C3** | Design Iteration Yield | M | H | M | ICSE NIER |

## 按研究主线分类

### 校准主线(5 个)
B1, B4, A2, A4, A6

### 偏好耦合主线(4 个)
B2, B4, A2, A3

### 多 Agent 协作主线(5 个)
A1, A3, A4, A7, B3

### 隐私 ML 主线(3 个)
A6, B5, A4

### Meta / SE 主线(3 个)
C1, C2, C3

### 应用 / 工程主线(2 个)
A5, A7

---

## 🎯 我的推荐:Top 3 启动 idea

| 优先级 | ID | 理由 |
|---|---|---|
| **第一篇** | **B1 — PDP 决策校准** | 校准是你最强主线,validate.bat 提供真实数据,可直接出 paper |
| **第二篇** | **A4 — Verifier Capture Resistance** | 跨主线(校准+多 Agent),有 paper-review-toolkit 作为 testbed |
| **第三篇** | **B3 — Dynamic Worker Pool** | 直接升级 paper-review-toolkit,工程+理论结合 |

---

_最后更新:2026-07-11 12:20 · 刘泽文 7 轮对话沉淀_