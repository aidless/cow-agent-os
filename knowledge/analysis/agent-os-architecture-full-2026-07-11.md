# Agent OS Reference Architecture — V1→V7 完整方案

_2026-07-11 与刘泽文 7 轮对话沉淀。从"战略蓝图"演进到"行业治理基础设施"再到"红队防御加固"。_

> **本文档合并了 V1 战略蓝图 + V2 运营平台 + V3 工程实现 + V4 生产可靠 + V5 治理可信 + V6 跨平台行业治理 + V7 红队漏洞修复,共 10 个抽象层 + 6 个补丁 + 25 个已知漏洞的缓解措施。**

---

## 🎯 总命题

> **A2A 的价值不是"能连别人",而是你自己已经足够可靠,可以代表用户去连接别人。**

单体 Agent 是能力根,A2A 是社会网络,支付是商业闭环,安全和审计是信任地基。

> 一个成熟 Agent 平台不应该是"模型调用工具",而应该是:**认知平面负责理解和规划,能力平面负责执行,协作平面负责内外部 Agent 调度,数据平面负责记忆与证据,控制平面横切所有动作,A2A 负责让 Agent 进入可信协作网络,并通过信任、支付、验收、演化、可靠性、治理和跨平台基础设施机制持续变强**。

### 6 轮演进路径

| 版本 | 标题 | 补的是 |
|---|---|---|
| V1 | 战略蓝图 | 愿景层 |
| V2 | 平台架构 | 系统层 |
| V3 | 接口协议 | 实现层 |
| V4 | 高可用 + 可解释 | 可靠性层 |
| V5 | 内部治理 | 可信层 |
| V6 | 跨平台治理 | 行业层 |

---

# 第 1 层:战略蓝图(V1)

## 1.1 总目标

做一个完整智能 Agent 系统,具备:

- 理解用户目标
- 拆解任务
- 调用本地工具和云端工具
- 持续 loop 执行
- 记忆上下文
- 生成 spec 和验收标准
- 支持多模态输入输出
- 支持技能扩展
- 支持 A2A:发现其他 Agent、委托任务、接收任务、协作交付
- 支持权限、安全、审计、支付和评价体系

**一句话**:从"我能帮你做事"升级到"我能代表你和其他 Agent 协作,把事情办成"。

## 1.2 五阶段推进

1. **单体可靠** —— Intent / Planner / Executor / Verifier / Reporter
2. **工具可靠** —— MCP 工具市场
3. **多 Agent 协作** —— 内部 dynamic agent pool
4. **A2A 网络化** —— Agent Card + Task 契约 + 状态机
5. **商业闭环** —— 支付 + 评价 + 仲裁

---

# 第 2 层:5 平面 + 横切控制平面(V2)

```
用户 / 企业系统 / 外部 Agent
        ↓
Interaction Plane(对话入口 / API / Webhook / Desktop UI / A2A Gateway)
        ↓
Cognition Plane(Intent → Spec → Planner → Router → Executor → Verifier)
        ↓
Capability Plane(Tools / MCP / Skills / Local Runtime / Browser / SaaS / Models)
        ↓
Collaboration Plane(Internal Dynamic Agents / External A2A Agents / Marketplace)
        ↓
Data Plane(Memory / RAG / Task Store / Artifact Store / Event Log / Vector DB)

横切控制平面 Control Plane:
Security / Permission / Policy / Audit / Payment / Cost / Observability / Governance
```

**关键原则**:每次工具调用过权限,每次 A2A 请求过身份和策略,每次付款过预算和审计,每次结果验收留证据,每次模型调用计成本和风险等级。

---

# 第 3 层:Control Plane 工程化(V3 + V4 + V5)

## 3.1 PDP + PEP + PAP + Audit 四件套

| 组件 | 职责 |
|---|---|
| **PDP** (Policy Decision Point) | 策略决策中心,回答"允许/拒绝/需要确认/需要降级" |
| **PEP** (Policy Enforcement Point) | 执行拦截点,分布在 8 个 hook |
| **PAP** (Policy Administration Point) | 策略管理后台,配置企业/用户/系统规则 |
| **Audit Log** | 所有决策、输入摘要、结果、证据落日志 |

## 3.2 核心接口

```http
POST /control/evaluate
```

**Request**:
```json
{
  "subject": {"type": "agent", "id": "haolo.main", "trust_level": "T3", "user_id": "u_123"},
  "action": "a2a.invoke",
  "resource": {"type": "external_agent", "id": "design-agent.example.com", "trust_level": "T1"},
  "context": {
    "task_id": "task_789",
    "risk_level": "medium",
    "data_classification": "internal",
    "budget": {"requested": 0.5, "remaining": 2.0, "currency": "USD"},
    "permissions_requested": ["read_project_assets", "send_anonymized_brief"]
  }
}
```

**Response**:
```json
{
  "decision": "allow | deny | require_user_confirmation | require_redaction | require_sandbox | require_human_review",
  "obligations": [
    {"type": "redact", "fields": ["phone", "api_key", "customer_email"]},
    {"type": "max_budget", "value": 0.5},
    {"type": "audit", "level": "full"}
  ],
  "reason_codes": ["TRUST_LEVEL_SUFFICIENT", "DATA_REDACTION_REQUIRED"],
  "policy_version": "2026-07-11.4"
}
```

## 3.3 Policy DSL:Cedar + Rego hybrid

- **Cedar 风格**做授权(主体-动作-资源-上下文判断)
- **Rego / OPA** 做复杂合规策略(数据流、合规链)

Cedar-like 示例:
```text
permit(principal is Agent, action == Action::"a2a.invoke", resource is ExternalAgent)
when {
  principal.trust_level >= 2 &&
  resource.trust_level >= 1 &&
  context.task.risk_level in ["low", "medium"] &&
  context.budget.requested <= context.budget.remaining &&
  context.data.classification != "secret"
};
```

## 3.4 8 个 PEP hook

| hook | 拦截 |
|---|---|
| `before_tool_call` | 任何工具调用 |
| `before_a2a_call` | A2A 请求 |
| `before_file_write` | 文件写入 |
| `before_shell_exec` | Shell 命令执行 |
| `before_payment_hold` | 预授权/扣款 |
| `before_external_data_send` | 外发数据 |
| `before_memory_write` | 长期记忆写入 |
| `before_model_context_pack` | 模型上下文打包 |

---

# 第 4 层:分布式 PDP + 可解释性(V4)

## 4.1 PDP 分层架构

```
Central PDP(策略管理、发布、审计汇总)
  ↓ 下发 signed policy bundle
Local PDP / Sidecar PDP(本地实时决策、低延迟)
  ↓
PEP(执行)
  ↓
Audit/Event Stream(异步回传中央)
```

### 4 级风险 × TTL 矩阵(V5 补丁)

| 风险级别 | 本地缓存 | 最大过期 | 中央依赖 | 离线行为 |
|---|---:|---:|---|---|
| Low | 允许 | 24h | 不强依赖 | 可继续 |
| Medium | 允许 | 5-15min | 可降级 | 限制性继续 |
| High | 短缓存 | 30-60s | 强依赖 | 只读/等待 |
| Critical | 不允许 | 0 | 必须在线 | 默认拒绝 |

**Critical 动作清单**:付款执行、外部数据发送、权限升级、删除/覆盖关键资产、调用未知 A2A Agent、签署/发布/提交不可逆操作。

### Kill Switch 独立通道

```text
Emergency deny list > local policy cache > normal central policy
```

- 高风险动作不能依赖过期本地策略
- Kill switch 走独立优先通道
- Local PDP 必须有 staleness bound

### Policy Bundle 元数据

```json
{
  "policy_version": "2026-07-11.4",
  "issued_at": "...",
  "expires_at": "...",
  "max_staleness_by_risk": {"low": "24h", "medium": "15m", "high": "60s", "critical": "0s"},
  "revocation_epoch": 128,
  "emergency_deny_list_version": 42,
  "signature": "..."
}
```

## 4.2 Policy Explainability & Simulator

### Full Trace Explain 接口

```http
POST /control/explain
```

```json
{
  "decision": "deny",
  "final_reason": "PAYMENT_LIMIT_EXCEEDED",
  "evaluated_policies": [
    {
      "policy_id": "payment.max_auto_limit",
      "effect": "forbid",
      "matched": true,
      "conditions": [{"expr": "context.amount > user.auto_payment_limit", "left": 120, "right": 50, "result": true}]
    },
    {
      "policy_id": "agent.trust_allow_low_risk",
      "effect": "permit",
      "matched": true
    }
  ],
  "conflict_resolution": {"rule": "explicit_forbid_overrides_permit", "winner": "payment.max_auto_limit"},
  "obligations": [],
  "suggested_fix": ["request_user_confirmation", "reduce_amount_below_50", "increase_user_auto_payment_limit"],
  "policy_version": "2026-07-11.4"
}
```

### 三视图 Explain

- **developer trace** → 完整表达式、变量、命中路径
- **admin trace** → 策略名、原因、建议修复
- **user explanation** → 自然语言,不暴露内部细节

### Policy Simulator

```
输入 subject/action/resource/context
→ 预演决策
→ 显示哪些策略命中
→ 如果改字段是否通过(what-if)
```

---

# 第 5 层:隐私分级 + DP 演化(V3 + V5)

## 5.1 数据分级 D0-D5

| 级别 | 名称 | 全局学习 | 条件 |
|---|---|---|---|
| D0 | Public | ✅ | 无限制 |
| D1 | Product Telemetry | ✅ | 不含内容 |
| D2 | Derived Metadata | ✅ | k-anonymity ≥ 50 + 聚合 |
| D3 | User Content | ❌ 默认 | 用户显式授权 |
| D4 | Sensitive Content | ❌ | 只能本地学习 |
| D5 | Regulated Content | ❌ | 专门合规协议 |

## 5.2 脱敏标准

- 直接标识符(姓名/手机/邮箱/地址/身份证/银行卡)→ 删除
- 密钥类(API key/token/cookie/私钥/连接串)→ 删除
- 准标识符(精确地址 → 城市,公司名 → 行业)
- 任务内容只保留任务类型 + 错误类别
- 代码场景:不上传源码,只上 AST 统计 + 错误类型 + 工具链版本 + 测试结果

## 5.3 DP 聚合标准

```json
{
  "metric": "tool_success_rate",
  "group": "browser_automation.login_flow",
  "count_min_k": 50,
  "epsilon": 1.0,
  "delta": 0.000001,
  "contribution_limit_per_user": 5,
  "noise": "laplace_or_gaussian"
}
```

**适合 DP**:工具调用成功率、任务失败率、Agent 评分、错误类别频率、planner 收益、A2A 成功率、任务耗时分布。
**不适合 DP**:长文本、源码、对话内容、私有记忆。

## 5.4 双轨学习

```
Local:  用户内容/项目记忆/偏好/私有失败案例 → 本地/租户内演化
Global: D1/D2 聚合遥测/脱敏模式/公开任务库/授权数据
```

## 5.5 Privacy-Preserving Telemetry Pipeline

```
Client → local clipping + local event encoding
    ↓
Telemetry Gateway → validation + tenant isolation
    ↓
Streaming Aggregator → windowed aggregation
    ↓
Contribution Bounding Service → per-user/per-tenant clipping
    ↓
Secure Aggregation Layer → threshold aggregation / encrypted aggregation
    ↓
DP Noise Service → add calibrated noise
    ↓
Metrics Store → publish only aggregate metrics
```

### 关键并发原语

- windowed aggregation:按时间窗口聚合
- contribution bounding:限制单用户贡献
- idempotency key:避免重复上报
- exactly-once 或 at-least-once + 去重
- secure aggregation:服务端不可见单用户明文
- threshold release:样本 < k 不发布
- privacy budget ledger:记录 epsilon 消耗

## 5.6 4 阶段诚实演进路线(V5 补丁)

```
V1: Centralized Telemetry Hygiene
   服务端可见明文 D1/D2 遥测 + 数据分级 + 贡献限制 + k 阈值 + DP 发布
   → 正式名称:privacy hygiene + controlled telemetry
   → 不是 secure aggregation

V2: Tenant-Isolated Encrypted Transport
   传输加密 + 租户隔离,但聚合服务仍可见明文
   → 仍不是 secure aggregation

V3: TEE-backed Aggregation 或 Threshold Secure Aggregation
   服务端运维不可见单用户明文
   → 才是 privacy-preserving aggregation

V4: Federated Analytics / Federated Learning
   数据尽量留本地,只上加密/聚合/裁剪后更新
```

**硬规则**:V1/V2 不声称 secure aggregation,只是过渡期隐私卫生方案。

---

# 第 6 层:A2A 信任 + Sandbox + Milestone(V2 + V3 + V5)

## 6.1 A2A Agent Card

```json
{
  "agent_id": "design-agent.example.com",
  "name": "Design Agent",
  "provider": "Example Studio",
  "capabilities": ["ui_design", "poster_generation", "brand_guideline_check"],
  "input_schema": {},
  "output_schema": {},
  "auth_methods": ["oauth2", "api_key", "signed_request"],
  "pricing": {"mode": "per_task", "currency": "USD", "price": "0.20"},
  "sla": {"typical_latency": "30s", "max_latency": "5min"},
  "trust": {"verified": true, "rating": 4.8, "trust_level": "T2"}
}
```

## 6.2 A2A Task 格式

```json
{
  "task_id": "task_123",
  "requester_agent": "haolo-agent",
  "target_agent": "design-agent",
  "goal": "生成一个电商主图方案",
  "inputs": {"product": "无线耳机", "style": "科技感", "size": "1024x1024"},
  "constraints": ["不要使用侵权品牌", "中文文案不超过12字"],
  "acceptance_criteria": ["输出图片URL", "输出设计说明", "图片可访问"],
  "callback_url": "https://...",
  "payment": {"mode": "escrow", "max_budget": "0.50"},
  "jurisdiction": {
    "user_region": "CN",
    "data_subject_region": "EU",
    "requester_region": "CN",
    "provider_region": "US",
    "processing_region": "SG"
  },
  "data_classes": ["personal_data", "business_confidential"],
  "legal_basis": "consent | contract | legitimate_interest | required_by_law",
  "cross_border_transfer": true
}
```

## 6.3 A2A 状态机(完整版 V3 + V5)

```
主流程: created → accepted → running → need_more_info
        → partially_submitted → partial_verified → partial_completed
        → submitted → verified → completed

失败: rejected / cancelled / timeout / failed / disputed / refunded / expired
```

### partial_completed 里程碑

```json
{
  "milestones": [
    {"id": "m1", "description": "完成需求分析", "amount": "20%", "status": "partial_completed", "evidence": ["spec_doc_hash"], "verified_by": "requester_agent"},
    {"id": "m2", "description": "完成代码实现", "amount": "50%", "status": "running"},
    {"id": "m3", "description": "测试通过并交付", "amount": "30%", "status": "pending"}
  ]
}
```

## 6.4 Verified 多源验收(V3 补丁)

```json
{
  "verification": {
    "status": "passed",
    "verified_by": "requester_agent | provider_agent | human_user | third_party_arbitrator | automated_test",
    "evidence": ["test_report", "screenshot", "artifact_hash"],
    "confidence": 0.92,
    "dispute_window": "24h"
  }
}
```

**原则**:交付方可以声明完成,不能独占最终验收权。

## 6.5 信任等级 + Cold Start

```
T0 Unknown       → 只能做低风险试任务
T1 Verified Identity → 身份已验证
T2 Trial Passed  → 通过试运行
T3 Reputation    → 稳定评分 + 历史
T4 Trusted Partner → 长期合作/企业白名单
```

### Sandbox 试任务分级

| 级别 | 名称 | 内容 |
|---|---|---|
| S0 | Smoke Test | 连通性、格式、状态机 |
| S1 | Capability Test | 单能力验证 |
| S2 | Robustness Test | 异常输入/超时/重试 |
| S3 | Security Test | 权限诱导/数据泄露检测 |
| S4 | Business Simulation | 完整业务流程模拟 |

### 动态反作弊(V5 补丁 — 核心不是 hidden set)

```text
Hidden test set
+ Canary task(看起来像普通任务,含隐藏约束/泄露诱饵/权限诱导)
+ Dynamic task generation(动态参数)
+ Periodic rotation(定期轮换任务)
+ Adversarial variants(对抗样本)
+ Real-world shadow evaluation(真实任务并行)
+ Abnormal score audit(异常分数审计)
+ Re-test on suspicious agents(可疑 Agent 触发复测)
+ Score quarantine / trust downgrade(分数隔离/信任降级)
```

**异常检测指标**:sandbox P99 但真实任务争议率高、同类任务耗时异常低、输出高度模板化、新 Agent 短期异常高分、同类任务全行业分数跃升等。

**触发链**:`flagged → silent retest → adversarial retest → human review → score quarantine → trust downgrade → public notification`。

**硬规则**:Benchmark 反作弊核心是**动态评测和异常复测**,hidden set 只是一个组件,**重点不是"藏答案",而是持续改变分布,让刷榜成本高于真实提升**。

### Sandbox Task 元数据(V4 补丁)

```json
{
  "task_id": "sandbox.design.s1.001",
  "version": "1.2.0",
  "capability": "poster_generation",
  "difficulty": "S1",
  "maintainer": "platform",
  "source": "synthetic",
  "risk_tags": ["copyright", "format_compliance"],
  "scoring_schema": "design_s1_v2",
  "hidden_tests": true,
  "contamination_risk": "medium",
  "last_reviewed_at": "2026-07-01"
}
```

### Benchmark Governance Plane(V4 补丁)

任务生命周期:`proposed → reviewed → staged → active → monitored → deprecated → archived`

治理角色:task author / reviewer / security reviewer / benchmark curator / red team / audit committee

**硬规则**:Sandbox Evaluation Service 本身的关键操作必须经 Policy Service + 审计 + 版本化。

## 6.6 4 种 Milestone Pricing 模式(V3)

| 模式 | 适用 | 关键字段 |
|---|---|---|
| **Fixed Bid** | 简单任务 | total_price + milestones[] |
| **Effort Based** | 不确定工作量 | rate + cap + billing_unit |
| **Value Based** | 效果型 | base_price + success_bonus + success_metric |
| **Hybrid Milestone** | 复杂项目(推荐) | total_cap + 每 milestone 独立选 pricing_basis |

```json
{
  "pricing_mode": "hybrid_milestone",
  "total_cap": 1000,
  "milestones": [
    {"id": "m1", "name": "需求分析", "pricing_basis": "fixed", "price": 100, "refundability": "non_refundable_after_acceptance"},
    {"id": "m2", "name": "原型交付", "pricing_basis": "effort", "estimated_price": 300, "cap": 400},
    {"id": "m3", "name": "最终上线", "pricing_basis": "success", "base_price": 300, "success_bonus": 200}
  ]
}
```

### Milestone 报价字段(最小合同)

- `pricing_basis` — 怎么算
- `acceptance_criteria` — 怎么验
- `revision_policy` — 改几次
- `refund_policy` — 退多少
- `price` — 最终金额

---

# 第 7 层:5 类演化机制(V2 + V5 双轨)

| 演化层 | 数据源 | 更新频率 | 隐私归属 |
|---|---|---|---|
| 任务级 | task reflection | 每任务 | 可聚合 → Global |
| 用户级 | 行为偏好 + 向量 | 持续 | Local |
| 项目级 | code/docs + 向量 | 每会话 | Local |
| 生态级 | A2A 调用历史 | 每调用 | 可聚合 → Global |
| 模型/策略级 | 聚合脱敏 trace | 周期性 | Global |

```json
{
  "what_worked": [],
  "what_failed": [],
  "new_pattern": [],
  "tool_reliability": {},
  "spec_gap": [],
  "future_policy_update": []
}
```

---

# 第 8 层:6 版本路线 + 数字化 KPI(V2 完整)

## V0.1 单体 Agent 可用

- 任务完成率 ≥ 80%
- 一次成功率 ≥ 55%
- 平均人工介入 ≤ 1.5 次/任务
- 失败可解释率 ≥ 90%
- 文件/命令类任务误操作率 = 0
- 交付物存在性验证率 = 100%
- 任务日志覆盖率 = 100%

## V0.2 控制平面上线

- 敏感操作确认率 = 100%
- 成本超预算率 = 0
- 权限违规拦截率 ≥ 99%
- 有明确 spec 的任务比例 ≥ 95%
- 验收标准覆盖率 ≥ 90%
- 自动修复后成功率提升 ≥ 20%
- 重复失败检测准确率 ≥ 85%
- 无限循环发生率 = 0
- 用户中断响应时间 ≤ 2 秒

## V0.3 动态 Multi-Agent

- 复杂任务完成率提升 ≥ 20%
- 不必要子 Agent 创建率 ≤ 10%
- Reviewer 检出高风险问题召回率 ≥ 85%

## V0.4 A2A 基础互通

- A2A 调用成功率 ≥ 85%
- A2A 状态同步准确率 ≥ 99%
- 外部 Agent 身份验证覆盖率 = 100%

## V0.5 Trust + Partial Delivery

- 冷启动试运行通过后正式任务成功率 ≥ 80%
- partial milestone 验收准确率 ≥ 95%
- 争议证据完整率 ≥ 95%
- 未授权数据外传事故 = 0
- 单任务成本超预算率 = 0

## V1.0 Agent Marketplace

- 付费任务验收通过率 ≥ 90%
- 争议率 ≤ 3%
- 退款处理 SLA ≤ 48h
- 高信誉 Agent 复购率 ≥ 50%

---

# 第 9 层:跨平台治理基础设施(V6)

## 9.1 多边 Policy 交集公式

```
effective_policy =
  protocol_baseline        (A2A 协议最低标准)
  ∩ requester_policy       (请求方平台)
  ∩ provider_policy        (服务方平台)
  ∩ user_policy            (用户授权)
  ∩ jurisdiction_policy    (所在法域)

谁更严格谁生效
```

### Policy Negotiation Protocol

```json
{
  "requester_requirements": {"data_retention": "no_store", "audit_level": "full", "max_budget": 10},
  "provider_capabilities": {"data_retention": "7_days", "audit_level": "partial", "supports_no_store": false},
  "negotiation_result": "rejected",
  "reason": "provider_cannot_satisfy_no_store"
}
```

## 9.2 跨法域处理

```json
{
  "jurisdiction": {
    "user_region": "CN",
    "data_subject_region": "EU",
    "requester_region": "CN",
    "provider_region": "US",
    "processing_region": "SG"
  },
  "data_classes": ["personal_data", "business_confidential"],
  "legal_basis": "consent | contract | legitimate_interest | required_by_law",
  "cross_border_transfer": true
}
```

### Jurisdiction Policy Engine 判断项

- 能不能处理 / 能不能跨境传输
- 是否需要用户同意 / 是否需要 SCC/DPA/合同条款
- 是否必须本地化处理 / 保留多久
- 是否允许用于训练 / 是否要支持删除/导出/撤回授权

### 法域实战策略

- **GDPR**:最小化、可删除、可导出、需合法依据
- **中国数据安全法**:重要数据/个人信息/跨境更谨慎,可能需本地处理
- **CCPA/CPRA**:opt-out、数据访问、删除
- **企业数据**:合同 + DPA

**默认策略**:本地/同法域处理 → 跨境前 policy check → 高风险要求 explicit consent → 无法判断时拒绝或人工审核

## 9.3 Meta-Audit 多方制衡

```
平台内部审计
→ 独立第三方审计(技术审计 + 合规审计)
→ 认证机构/行业联盟
→ 监管机构
→ 用户/Agent provider 申诉
→ 公开透明度报告
→ 保险/担保市场
```

**Meta-audit**:审计机构审平台,行业联盟审审计机构,监管和市场处罚失职者。

防范 single-auditor 失职:
- 审计机构有资质评级
- 审计报告可抽查/可复核
- 重大事故后追责审计机构
- 多审计机构轮换,避免长期利益绑定
- 高风险平台双审计

## 9.4 透明度报告三阶段(V6 补丁)

```
Phase 1: 制度透明
  - 治理结构 / policy 版本 / 审计范围 / 数据分类规则
  - A2A 安全基线 / sandbox 方法 / 争议处理流程
  - 外部审计计划 / 已知限制

Phase 2: 指标透明
  - A2A 任务量 / 争议率 / 退款率 / 权限拦截次数
  - 安全事件数 / 数据请求数 / 审计整改率
  - 降权/封禁 Agent 数

Phase 3: 可验证透明(cryptographic transparency log)
  类似 Certificate Transparency,任何第三方可验证报告真实性
```

## 9.5 5 层分级认证 + 审计成本(V6 补丁)

| 等级 | 对象 | 审计方式 | 谁付费 |
|---|---|---|---|
| Level 0 | 个人低风险 Agent | 自动 sandbox + 平台抽检 | 平台/开发者小额认证费 |
| Level 1 | 通过 sandbox | 自动 sandbox 通过 | Agent provider |
| Level 2 | 平台人工审核 | 平台人工审核 | Agent provider |
| Level 3 | 中小商业 Agent | 第三方标准审计 | Agent provider |
| Level 4 | 企业高风险 Agent | 外部专项审计 | 企业/Provider |
| Level 5 | 平台基础设施/关键模块 | 平台级年度外部审计 | 平台 + 合作方 |

**成本分担策略**:
- 审计池:多个小 Agent 分摊同一类认证成本
- 连续审计:用自动化监控替代一年一次大审
- 风险定价:高风险 Agent 更高保证金/保险费
- 保险市场:保费反映风险
- 认证等级:不同等级对应不同商业权限

## 9.6 AI 审计 AI(V6 补丁)

**硬规则**:**LLM 是审计副驾驶,不是审计法官**。

### LLM 可以做

- 日志摘要 / 异常聚类 / 证据整理
- policy trace 翻译成人话 / 找相似案例
- 初步风险标注 / 生成审计报告草稿

### LLM 不能单独做

- 最终封禁 / 最终退款裁决
- 合规通过结论 / 高风险 policy 变更
- 法律责任判断 / 审计签字

### 6 条工程约束

1. 所有输入证据可追溯
2. LLM 输出必须引用日志/artifact hash
3. 关键结论必须有人类审计员签署
4. 结论要能复现/能复核
5. LLM 版本/prompt/上下文摘要要记录
6. 不允许"模型觉得风险高"作为唯一理由

### 审计记录标准格式

```json
{
  "case_id": "dispute_123",
  "llm_assisted": true,
  "model_version": "audit-model-x",
  "evidence_used": ["policy_trace_001", "payment_log_002", "artifact_hash_003"],
  "llm_findings": ["Provider submitted after deadline", "Requester verification failed on criterion 2"],
  "human_decision": "partial_refund",
  "human_reviewer": "auditor_45",
  "rationale": "Milestone 1 accepted, Milestone 2 failed objective test",
  "appeal_available": true
}
```

## 9.7 三层治理 + Appeal(V5 + V6)

```
Internal Audit         → 日常审计 + 事件调查 + 策略复盘
Independent External   → 定期审计平台策略/隐私/支付/benchmark/争议流程
Public Transparency    → 季度公开报告
Appeal Process         → Agent provider / 用户 / 企业 三类申诉
```

**最终治理原则**:**审计者也必须被审计,平台治理必须留下可验证证据,并接受外部独立复核**。

---

# 第 10 层:已知漏洞与缓解措施(V7 升级)

> 本层基于 2026-07-11 红队分析得出的 25 个真实漏洞。每个漏洞都按 Severity × Exploitability × Fix Difficulty 评分。完整分析见 `knowledge/analysis/agent-os-vulnerabilities-2026-07-11.md`(27.8 KB)。

## 10.1 7 个 Critical 漏洞

### 漏洞 #1 — PDP 分层 "Boring Middle" 风险
**S × E × F**: Critical × Medium × Medium

Central PDP 推送 policy bundle 后,Local PDP 在中间期可能按旧 epoch 决策。

**缓解措施(必选)**:
```text
Critical 动作必须双签:
- Local PDP 不能单独决策 Critical
- 必须从 Central PDP 拿 short-lived signed token(30s 过期)
- 过期 → 默认拒绝

心跳机制:
- Local PDP 每 10s 向 Central 报告当前 epoch
- staleness > 30s → 自动降级为只读
```

### 漏洞 #2 — Kill Switch 被恶意利用
**S × E × F**: Critical × Easy × Hard

举报方可能武器化 kill switch 攻击竞品。

**缓解措施(必选)**:
```text
多签触发:
- L1 限流 → 1 人签字
- L2 暂停 → 2 人签字
- L3 拉黑 → 3 人签字 + 公开审计

举证责任倒置:
- 举报方提交证据 + 保证金($1000+)
- 误杀退还 + 赔偿被 kill 方损失
- 多次恶意举报 → 举报方降权

自动过期:
- 任何 kill switch 触发后自动 24h 过期
- 防止"杀完忘记解封"
```

### 漏洞 #4 — Jurisdiction 集合交集可能"无解"
**S × E × F**: Critical × Medium × Medium

5 边交集可能为空,导致任务无法执行。

**缓解措施(必选)**:
```text
Fallback 降级策略:
- 交集为空 → 退化到最低安全标准
  = 加密 + 不存储 + 用户显式确认 + 接受不完美
- 永远不要"静默拒绝"

法域预筛:
- 任务创建前做 jurisdiction feasibility check
- 预测交集为空 → 提前警告用户 + 建议换 provider 或改要求
```

### 漏洞 #7 — LLM 审计 AI 的"幻觉传染"
**S × E × F**: Critical × Easy × Hard

LLM 偏差通过 automation bias 传染到审计决策。

**缓解措施(必选)**:
```text
盲审制度:
- 审计员看原始证据自己写 findings
- 再比对 LLM findings
- 偏离 > 阈值 → 触发 LLM 重新训练 / 审计员再培训

对抗性审计:
- 每个 case 必须两个 LLM 独立 findings
- 冲突 → 强制升级到人类深度审查

定期幻觉检测:
- 注入已知答案的 fake cases
- LLM 错答触发模型再训练
```

### 漏洞 #8 — 冷启动"先有鸡还是先有蛋"
**S × E × F**: Critical × Trivial × Hard

新平台没有 sandbox 任务池 → Agent 不来 → 平台死。

**缓解措施(必选)**:
```text
Industry Consortium 维护公共 Sandbox 任务池:
- 开源 + 公共访问
- 任何新平台免费接入
- 由 consortium 持续更新 + 防污染

种子任务 + 渐进替换:
- 冷启动用 synthetic 生成 1000 个 sandbox 任务
- 逐步用真实任务替换
- 真实任务:sandbox 比例 1:1 → 1:3 → 1:5
```

### 漏洞 #15 — Control Plane 单点 "组合失效"
**S × E × F**: Critical × Medium × Hard

Control Plane 故障 → 整个系统停摆。

**缓解措施(必选)**:
```text
多 Control Plane + Leader Election:
- 3 副本部署,Raft/Paxos 选主
- 主故障 30s 内自动切换
- 数据同步延迟 < 1s

分层降级模式(degraded mode):
- Control Plane 故障 → Critical 默认拒绝
- Low 风险允许(基于本地策略)
- Medium 等待 60s 重试
- 监控告警 + 人工介入
```

### 漏洞 #20 — Cross-Jurisdiction 法律冲突
**S × E × F**: Critical × Easy × Hard

US CLOUD Act + EU GDPR + CN 数据安全法 三者冲突。

**缓解措施(必选)**:
```text
Geo-fencing 强制:
- CN 数据不离开 CN
- EU 数据不离开 EU
- 跨境任务默认禁止

本地化 Provider 池:
- 每个 region 有独立 provider 池
- 本地用户 → 本地 provider → 本地处理
- 接受不效率但保证合规

法律映射 + 不可行预警:
- 为每个 region 维护法律要求映射
- 任务创建前预测 legal feasibility
- 不可行 → 明确告知 + 建议替代方案
```

## 10.2 13 个 High 漏洞

### 漏洞 #3 — Sandbox 反作弊的"反作弊反作弊"
**S × E × F**: High × Medium × Hard

动态化任务与作弊对抗循环 → 资源浪费。

**缓解措施**:
```text
对抗性 red team 不公开:
- red team 任务输入/评分规则/触发条件保密
- 防止针对性调优

多 sandbox 并行 + 加权评分:
- 0.4 * synthetic + 0.3 * real + 0.3 * adversarial
- 作弊 Agent 只能优化部分池

长期一致性检验:
- Pareto-frontier 分析 sandbox vs 真实任务
- sandbox P99 + 真实 < P50 → 自动触发审计
```

### 漏洞 #5 — Trust 等级降级的"跳水"
**S × E × F**: High × Easy × Medium

一次严重事故可能 T4→T0,误伤长期信任的 Agent。

**缓解措施**:
```text
渐进降级 + 修复证明:
- 初始降 2 级(不是 T0)
- 30 天内提交修复证明 + 重新 sandbox 验证
- 通过:逐步恢复 / 未通过:降 T0 + 永久封禁

分级事故响应:
- L1 单次数据泄露但已修复 → 降 1 级
- L2 批量违规 → 降 2 级
- L3 恶意行为 → 立即 T0 + 公开黑名单

Trust Insurance:
- T3/T4 Agent 可买 trust insurance
- 保费反映风险,事故后保险赔付
```

### 漏洞 #6 — 5 类演化的"集体偏见"
**S × E × F**: High × Medium × Hard

反馈环路放大初始偏差 → 头部 Agent 垄断。

**缓解措施**:
```text
反垄断分配:
- 新 Agent 前 6 个月有 20% 流量配额
- 不达标才扣

多样性指标:
- HHI(Herfindahl-Hirschman Index)评估生态多样性
- 头部 3 名集中度 > 60% → 触发再平衡

演化定期重置:
- 每 12 个月清空演化记忆
- 强制 sandbox 重新评估
```

### 漏洞 #9 — Multi-Party Policy Intersection 的"无声拒绝"
**S × E × F**: High × Medium × Medium

交集为空时静默拒绝,用户体验灾难。

**缓解措施**:
```text
可解释的 policy 拒绝:
{
  "reason": "policy_intersection_empty",
  "details": ["requester requires no_store", "provider can only do 7_days"],
  "suggested_fix": ["use_provider_X (supports no_store)", "remove_no_store_requirement"]
}

申诉渠道:
- 用户认为 policy 不合理可申诉治理委员会
- 委员会每季度 review policy 是否过严
```

### 漏洞 #10 — 5 类演化机制中的"双轨泄漏"
**S × E × F**: High × Medium × Hard

D3 数据可能意外升级到 Global 训练。

**缓解措施**:
```text
严格数据流向追踪:
- 每个数据样本携带 privacy_class tag (D0-D5)
- 升级路径必须显式用户授权
- 不可绕过

定期 audit:
- 每月自动审计 D3 数据进入 Global 训练的比例
- 异常立即报警 + 强制回滚

DP baseline:
- Global 学习必须经过 DP(epsilon ≤ 1.0)
- contribution limit ≤ 5
- 不接受明文 D3
```

### 漏洞 #11 — Verified 多源的"投票作弊"
**S × E × F**: High × Easy × Medium

Requester 与 Provider 串通互相 verified。

**缓解措施**:
```text
verified_by 权重差异化:
- automated_test: 0.2(可绕过)
- requester_agent: 0.3(有串通风险)
- provider_agent: 0.1(自利偏差)
- third_party_arbitrator: 0.3(独立但成本高)
- human_user: 0.4(最高,成本最高)
- 必须多源组合 verified 才能 completed

轮换 + 盲审:
- 第三方仲裁员定期轮换
- 盲审制度(仲裁员看不到 Agent 身份)

异常 verified 审计:
- 通过率 > 99% → 触发审计
- 同对 (requester, provider) 多次 verified → 触发审查
```

### 漏洞 #12 — Pricing Mode 4 种的"价格操纵"
**S × E × F**: High × Medium × Medium

Value Based 可被 Provider 挑有利 baseline。

**缓解措施**:
```text
Baseline 平台统一:
- Baseline 必须由平台或独立第三方定义
- Provider 不能选自己的 baseline

A/B Testing 强制:
- Value Based 必须 split test
- 50% 用户用 Provider,50% 不用
- 比较两组真实收益

统计显著性要求:
- Lift >= 5% 必须样本量 ≥ 1000 + p ≤ 0.05 + Cohen's d ≥ 0.2
```

### 漏洞 #13 — Audit Committee 的"审计员疲劳"
**S × E × F**: High × Easy × Hard

日均数千 case,审计员只能形式审查。

**缓解措施**:
```text
Case 自动分级:
- L1 (80%): 自动审核 → 不通过 → L2
- L2 (15%): 审计员快速 review → 不通过 → L3
- L3 (4%): 审计员深度审查 → 不通过 → L4
- L4 (1%): 外部仲裁

AI 优先筛查 + 审计员复核:
- AI 标注可疑 case(异常模式)
- 审计员只 review AI 标注的
- audit_volume 降低 10x

Audit 量化 + 抽查:
- 每个 case 必须 30 秒内决策
- AI 监测"快速 review"比例
- 异常 → 自动升级深度审查
```

### 漏洞 #16 — A2A 状态机的"中间态挂起"
**S × E × F**: High × Easy × Easy

Provider 进程崩溃后任务永远停 need_more_info。

**缓解措施(必选)**:
```text
超时自动转移:
- need_more_info 等待最长 24h
- 超时 → 自动 cancel + refund

心跳机制:
- 每个 Agent 必须定期 heartbeat(60s 一次)
- N=3 次未 heartbeat → 标记 offline
- 任务自动转移到其他 Agent 或 cancel

Orphan Task 自动检测:
- 平台定期扫描状态 > 7 天未变化的任务
- 自动 cancel + refund + 通知
```

### 漏洞 #17 — Local PDP Cache 的"毒化"
**S × E × F**: High × Medium × Hard

Local PDP 缓存被篡改,绕过中央控制。

**缓解措施**:
```text
Decision 必须 signed:
- 任何决策必须带中央 PDP 签名
- Local PDP 不能凭空决策
- 即使 cache 也必须有签名

Decision 周期上报:
- Local PDP 定期上报决策统计:
  - allow/deny 比例
  - 关键 action 类型分布
- 中央 PDP 检测异常模式

Multi-PDP 投票:
- 重要决策多个 Local PDP 投票
- 单点毒化无法决定结果
```

### 漏洞 #18 — DP 聚合的"组合失效"
**S × E × F**: High × Medium × Hard

多次 DP 查询组合后隐私泄露。

**缓解措施**:
```text
Privacy Budget Ledger:
- 每个用户的总 epsilon 消耗记账
- 总消耗 > 10 → 拒绝新查询
- 跨 session 持续追踪

查询相关性检查:
- 平台分析查询之间的相关性
- 高度相关的查询 → 拒绝

Limited Query API:
- 只暴露预定义的指标
- 不允许 ad-hoc 查询
```

### 漏洞 #19 — 5 类演化的"反馈放大"
**S × E × F**: High × Trivial × Hard

正反馈环路放大初始偏差。

**缓解措施**:
```text
Negative Feedback / Cooling:
- 任何资源倾斜 > 6 个月强制重置
- 防止历史偏差累积

Resource Cap:
- 任何单类任务最多占用 X% 资源(默认 30%)
- 超过 → 自动转向其他类型

周期性 Diversity Audit:
- 每 N 个月审计资源多样性
- 多样性下降 → 触发资源重平衡
```

### 漏洞 #22 — Hybrid Milestone 的"工作量博弈"
**S × E × F**: High × Easy × Medium

Provider 故意拖时间用满 cap。

**缓解措施**:
```text
Time Tracking 必须透明:
- Provider 必须提交时间追踪(代码 commit / IDE log / 屏幕录像)
- Requester 可以审计

AI 工时估算:
- 平台用 AI 估算合理工时
- 超出 1.5x → 触发审计

Milestone 限额 + Escrow:
- Effort Based 必须配合 escrow
- 未通过验收 → 不支付
- Provider 有动力快速完成
```

## 10.3 6 个 Medium 漏洞

### 漏洞 #14 — Transparency Report 披露悖论
**S × E × F**: Medium × Easy × Medium

透明度增加同时攻击面也增加。

**缓解措施**:
```text
分版本披露:
- 公开版:粗粒度指标(总量、增长率)
- 认证版:细粒度指标(分类型、分 region)
- 审计版:完整指标 + 证据

差分隐私披露:
- 所有指标经过 DP 处理
- count ≥ 1000 才发布
- 加 Laplace noise

滞后披露 + 时间窗口聚合:
- 披露 N 个月前指标(不是实时)
- 季度聚合而不是月度
```

### 漏洞 #21 — Protocol Baseline 标准僵化
**S × E × F**: Medium × Easy × Hard

12 个月更新周期跟不上新攻击。

**缓解措施**:
```text
Hot Patch 机制:
- protocol_baseline 支持紧急 patch
- 安全漏洞 30 天内强制更新
- 新功能 12 个月正常周期

分层 Baseline:
- core_baseline(安全,快更)
- extension_baseline(功能,慢更)
- vendor_specific(平台自定,快更)

最佳实践 + 监管补充:
- Baseline 是最低标准
- 平台可以在 baseline 之上加更严策略
```

### 漏洞 #23 — 透明度报告的"游戏化"
**S × E × F**: Medium × Easy × Medium

选择性披露让"看起来好"成竞争优势。

**缓解措施**:
```text
标准指标 + 必须披露:
- Industry consortium 定义标准指标
- 所有平台必须披露同样的指标
- 不可选择性披露

第三方验证指标:
- 独立机构验证指标真实性
- 不实披露 → 处罚

多维度评分:
- 不能用单一指标评判
- 必须多维度(效率 + 公平 + 安全 + 隐私)
```

### 漏洞 #24 — 5 层认证的"等级跳跃"
**S × E × F**: Medium × Medium × Medium

通过多个实体绕过认证等级。

**缓解措施**:
```text
实控人识别:
- 平台识别同一实控人控制的多个实体
- 关联实体合并认证等级

Trust 不与认证绑定:
- 认证等级按单个实体
- 但商业权限按实控人关联

关联披露要求:
- 注册时必须披露关联实体
- 隐瞒 → 降级 + 黑名单
```

### 漏洞 #25 — Audit Trail 日志膨胀
**S × E × F**: Medium × Trivial × Medium

日均 100M 调用 → 100GB+ 日志。

**缓解措施**:
```text
分级审计:
- Critical 动作 → 完整日志(永久)
- High 动作 → 摘要日志(永久)
- Medium 动作 → 摘要日志(1 年)
- Low 动作 → 聚合日志(30 天)

日志压缩 + 分层存储:
- 近期 30 天 SSD 完整
- 中期 1 年对象存储压缩
- 长期归档冷存储

日志采样:
- 完整记录 1% 调用作为 ground truth
- 其余聚合记录(只保留关键指标)
```

## 10.4 漏洞修复优先级矩阵

按"严重度 + 可利用性"排序,优先修 Critical + Easy/Trivial:

| 优先级 | 漏洞 | 理由 |
|---|---|---|
| 🔴 P0 | #16 | Critical × Easy × Easy,5 行代码可修 |
| 🔴 P0 | #1, #2, #4, #7, #8, #15, #20 | 全部 Critical,影响生产 |
| 🟡 P1 | #11, #5 | High × Easy,串通作弊常见 |
| 🟡 P1 | #12, #22 | High × Easy,Provider 套利常见 |
| 🟡 P1 | #13, #17, #19 | High × Trivial/Easy,容易积累 |
| 🟢 P2 | 其余 High | 需要架构改造 |
| ⚪ P3 | 6 个 Medium | 优化级 |

## 10.5 漏洞的 3 个暗模式

### 暗模式 A — Goodhart's Law 集中爆发
涉及漏洞:#3, #6, #12, #19, #22
> 当指标成为目标,它就不再是好指标。

**应对原则**:多维度指标 + 强制多样性 + 对抗性测试 + 异常检测 + 不依赖单一指标

### 暗模式 B — Distributed Systems 中间态
涉及漏洞:#1, #15, #16, #17, #25
> 中间态不是宕机,但比宕机更危险。

**应对原则**:显式定义每个中间态 + 默认拒绝 + 显式放行 + 心跳 + 超时

### 暗模式 C — Legal Trilemma 不可避免
涉及漏洞:#4, #20, #21
> 三方法律要求可能不可能同时满足。

**应对原则**:Geo-fencing + 本地化 + 接受不效率但合规 + 选边站 + 明确披露

---

| # | 接口 | 主线 | 论文方向 |
|---|---|---|---|
| 1 | 多源 verified_by 聚合 | 校准 | ensemble learning for verification |
| 2 | Trust 弹性曲线(T0-T4 升降级) | 偏好耦合 | trust system resilience |
| 3 | 跨 Agent Federated Learning | 多 Agent + 隐私 ML | DP / FL agent selection |
| 4 | RL-based PDP 策略学习 | 多 Agent | "Learning to Enforce" |
| 5 | DP 聚合下 planner 优化 | 校准 | "Bias-Variance in DP-aggregated RL" |
| 6 | Sandbox 防 overfit | 校准 | "Benchmark-to-Real Generalization Gap" |
| 7 | Marketplace 机制设计 | 多 Agent + 偏好耦合 | "Mechanism Design for Agent Marketplace" |
| 8 | PDP 分层 cache 一致性 vs 延迟 | 多 Agent | distributed consensus for policy staleness |
| 9 | Policy 可解释性量化 | 校准 | "Measuring Policy Explainability" |
| 10 | DP 隐私预算最优分配 | 校准 + 隐私 ML | "Privacy Budget Allocation" |
| 11 | Benchmark governance 博弈论 | 偏好耦合 | "Incentive-Compatible Benchmark Governance" |
| 12 | External Auditor 独立性机制 | 偏好耦合 | "Auditor Incentive Alignment" |
| 13 | Transparency Report 隐私-可验证权衡 | 校准 + 隐私 ML | "Differentially Private Transparency" |
| 14 | Appeal Process 博弈分析 | 偏好耦合 + 多 Agent | "Appeal Game Theory" |
| 15 | 多边 policy 交集最优性 | 多 Agent + 偏好耦合 | "Multi-Party Policy Intersection Pareto-Optimal" |
| 16 | 跨法域任务最优路由 | 多 Agent | "Jurisdiction-Aware Task Routing" |
| 17 | 透明度报告 cryptographic + DP | 校准 + 隐私 ML | "Verifiable Yet Private Transparency" |
| 18 | 5 层认证市场均衡 | 多 Agent + 偏好耦合 | "Market Equilibrium in Tiered Certification" |

---

# 附录 B:与刘泽文已有项目的真实映射

| 版本 | 方案要求 | 已做项目 | 缺口 |
|---|---|---|---|
| V0.1 | 任务完成率 ≥80%,日志 100% | wechat-mp-validation skill | ✅ 接近达标 |
| V0.2 | 权限/审计/成本控制 | 泰玄小站 spec coding | ⚠️ 仅覆盖 spec 维度 |
| V0.3 | 复杂任务完成率 +20% | paper-review-toolkit(3 reviewer 静态并行) | 🟡 需升级动态 worker pool |
| V0.4 | A2A 调用成功率 ≥85% | (未做) | ❌ |
| V0.5 | 冷启动通过率 ≥80% | paper-graveyard 9 类 detector ≈ S2 Robustness Test | 🟡 局部存在 |
| V1.0 | 付费任务通过率 ≥90% | (远期) | ⚪ |

**对应关系**:
- `specs/schools/*.result.schema.json` ≡ A2A Task 契约
- `validate.bat` 流水线 ≡ acceptance checklist + Verifier
- `paper-review-toolkit` 8 子命令 ≡ 内部 Multi-Agent 编排(需升级动态 worker pool)
- `paper-graveyard` 9 类 detector ≡ S2 Robustness Test 实例化 + "Agent 死亡分析" 雏形

**下一步最高 ROI**:
1. `validate.bat` 升级为 control plane 雏形(加 permission/cost scanner + PDP 调用)
2. `paper-review-toolkit` 升级为动态 worker pool(8 固定子命令 → 按 spec 动态生成 worker)

---

# 附录 C:核心系统服务清单

```text
Policy Service
  - evaluate() / enforce() / explain() / audit()

Privacy Service
  - classify() / redact() / anonymize() / aggregate_with_dp() / consent_check()

Sandbox Evaluation Service
  - assign_task() / score_result() / certify_capability() / retest()

Pricing & Escrow Service
  - quote() / negotiate() / hold_funds() / release_milestone() / refund() / dispute()

Distributed Policy Runtime
  - central PDP / local PDP / signed policy bundle / decision cache
  - offline fallback / emergency deny list

Policy Explainability & Simulator
  - full trace explain / conflict resolution trace / user/admin/developer view / what-if

Privacy-Preserving Telemetry Pipeline
  - streaming aggregation / contribution bounding / secure aggregation
  - DP noise / privacy budget ledger / threshold release

Benchmark Governance Plane
  - sandbox task lifecycle / hidden test sets / contamination detection
  - scoring versioning / benchmark audit
```

---

# 附录 D:6 条硬规则(可挂墙上当工程伦理)

1. **高风险动作不能依赖过期本地策略**
   Local PDP 必须 staleness bound,Critical 必须中央在线;kill switch 独立优先通道。

2. **V1/V2 不声称 secure aggregation**
   只是过渡期隐私卫生方案;只有 V3+ 才算真正的隐私保护聚合。

3. **Benchmark 反作弊核心是动态评测和异常复测**
   Hidden set 只是一个组件,不是护城河;持续改变分布,让刷榜成本高于真实提升。

4. **治理系统必须接受外部治理**
   Internal audit 负责日常,external auditor 负责监督,transparency report 负责公开可信度。

5. **交付方不能独占最终验收权**
   verified_by 必须有第三方/用户/自动化测试等多个来源。

6. **LLM 是审计副驾驶,不是审计法官**
   所有关键结论必须有人类审计员签署,LLM 输出必须引用可追溯证据。

---

_V1→V7 最后更新:2026-07-11 11:46 · 刘泽文与泰的合作产出_

---

# Agent OS Reference Architecture — V8 演进层(2026-07-11 收尾)

_本节为 V8 草稿的正式入库。承接 V1→V7,新增 §11–§15 五个演进层:_能力根契约 / 信任-隐私边界 / 治理自举 / 红队实证 / V8 KPI。_

---


# Agent OS Reference Architecture — V8 演进层（草稿）

> V8 = **可靠性契约 + 信任-隐私边界 + 治理自举 + 红队实证**
>
> 承接 V1→V7（战略蓝图 → 平台架构 → 接口协议 → 高可用+可解释 → 内部治理 → 跨平台治理 → 红队漏洞修复）。
> V8 的定位：**从"设计态"走向"证据态"**。V7 把 25 个漏洞缓解写成设计控制，V8 把它们变成可验证证据；同时闭合 V7 遗留的三个真问题——能力根契约缺位、信任-隐私效用边界未界定、治理基础设施自举悖论。
>
> 本文档是 V8 的演进层草案，沿用原文的平面/层级/JSON 契约/矩阵风格。

---

## V8 总命题

V1–V7 建了一个"可信协作网络"的**设计**，但有两个隐含假设从未被夯实：

1. "单体 Agent 已经足够可靠"——这是能力根，却只有 V0.1 的 KPI 约束，没有**契约**。
2. "治理基础设施天然存在"——V7 加了极重的治理成本，但没回答**谁出资、谁运营、激励从哪来**。

V8 的任务是把这两个假设**显式化、版本化、可验证化**，并把 V7 的 25 个设计控制升级为**红队实证证据**。

一句话：V8 = **可靠性契约 + 信任-隐私边界 + 治理自举 + 红队实证闭环**。

---

## 第 11 层：单体可靠性契约（V8 — 能力根）

### 11.1 问题

V1 断言"单体 Agent 是能力根"，但全文没有定义根对上层承诺什么。V0.1 的 KPI（完成率≥80%、一次成功率≥55%…）是**观测指标**，不是**契约接口**——上层平面无法"依赖"一个只能事后统计的数字。

V8 引入 **Reliability Contract (RC)**：每个上线的单体 Agent 必须发布一份版本化、可测试的契约，上层平面在调用前即可查询其保证能力。

### 11.2 RC 契约结构

```json
{
  "rc_version": "2026-07-11.rc1",
  "agent_id": "haolo.main",
  "guarantees": {
    "spec_completeness":      ">=0.95",   // 有明确 spec 的任务比例
    "acceptance_coverage":    ">=0.90",   // 验收标准覆盖率
    "first_pass_success":     ">=0.55",   // 一次成功率
    "manual_intervention":    "<=1.5",    // 平均人工介入次数/任务
    "misoperation_rate":      0.0,        // 文件/命令类误操作率
    "artifact_existence":     1.0,        // 交付物存在性验证率
    "log_coverage":          1.0         // 任务日志覆盖率
  },
  "failure_taxonomy": [
    "spec_gap", "tool_fail", "planner_loop",
    "verifier_false_pass", "context_loss"
  ],
  "oracle": {
    "spec_gen":        "llm+aast",          // spec 由 LLM + 抽象语法树生成
    "acceptance_gen":  "criterion_compiler", // 验收标准编译器
    "test_gen":        "auto_from_criteria"  // 从验收标准自动生成测试
  },
  "evidence_required": true
}
```

**硬规则**：未发布 RC 的单体 Agent，禁止接入 A2A 网络（T0 也不行）。RC 是能力根的"出厂合格证"。

### 11.3 Spec→Acceptance Oracle（S→A Oracle）

这是闭合 gap 1 的核心。原 V3/V5 的 `verified_by` 含 `automated_test`，但"测试由谁写"从未定义。V8 规定：

- 任务创建时，`acceptance_criteria` 中**每一条**必须要么：
  - (a) 可被 `criterion_compiler` 编译为可执行测试；要么
  - (b) 被分配 `human_user` 或 `third_party_arbitrator` 验证者（带显式权重）。
- **不可验证的验收标准在任务创建时被拒绝**，而不是在交付时才发现"没法验"。

```json
{
  "criterion": "输出图片URL可访问",
  "compiled_test": {
    "type": "http_head",
    "target": "$.output.image_url",
    "expect": "status in [200,206] within 5s"
  },
  "verifiable": true
}
```

关键原则（对应 V7 硬规则"交付方不能独占最终验收权"）：**`automated_test` 通过只是及格线，最终 `completed` 仍需多源 `verified_by` 组合**（权重见 V7 #11）。

### 11.4 失败分类法（Failure Taxonomy v1）

把"失败可解释率≥90%"从指标变成可操作的归因表：

| class | 根因 | 归属平面 | 触发动作 |
|-------|------|----------|----------|
| `spec_gap` | 意图理解不足 | Cognition | `spec_completeness`<0.95 → 触发 replanner |
| `tool_fail` | 工具不可靠 | Capability | `tool_reliability` 反馈到演化层 |
| `planner_loop` | 无限循环 | Control | 循环检测器（V0.2 KPI：无限循环=0） |
| `verifier_false_pass` | 验收误判 | Verifier | 强制多源 `verified_by` 复核 |
| `context_loss` | 记忆丢失 | Data | `before_memory_write` 审计 + 回放 |

---

## 第 12 层：信任-隐私效用边界（V8 — 闭合 gap 2）

### 12.1 核心命题（Utility Boundary Theorem，直觉版）

V7 用"双轨学习"断言了 D3/D4 不出本地，但 T3（Reputation）需要跨 Agent 比较。矛盾未解。V8 给出边界：

> **全局声誉 T3 可以仅由 D1/D2 聚合 + 本地行为画像的*哈希* 算出。它是一个*比较信号*，不是*绝对信号*。**

形式化（非严格）：

```
U(τ) ≤ I(D1 ∪ D2) + I(hash(B_local))
其中 B_local = 本地行为画像（由 D3/D4 在本地算出，不出域）
     hash(B_local) 仅暴露"行为档案是否相似"，不暴露档案内容
若想让 U(τ) 超过该界 → 必须导出 D3 → 违反 D3 规则 → 默认拒绝
```

结论：**T3 是 comparative 的，不是 absolute 的**。这恰是其正确语义——声誉本来就是"相对于同池其他 Agent"的比较量。

### 12.2 信任-隐私 Pareto 前沿

- x 轴：隐私成本（已消耗 ε）
- y 轴：信任信号判别力（用声誉预测真实任务成功的 AUC）

前沿显示：**ε < 1.0 时判别力即趋于饱和**——绝大多数信任信号不需要 D3 即可获得；ε > 1.0 后边际收益骤降、隐私成本陡升 → 默认拒绝。

```
判别力 AUC
 1.0 |          .........
     |        .
 0.8 |------·  (饱和点 ≈ ε=1.0)
     |    .
 0.6 |  .
     +------------------- ε
        1.0
```

### 12.3 可验证声誉协议

```json
{
  "agent_id": "design-agent.example.com",
  "trust_level": "T3",
  "reputation_score": 4.8,
  "computed_from": {
    "d1_d2_aggregates":      "tool_success_rate@dp(ε=1.0)",
    "behavioral_profile_hash":"sha256:ab12...",
    "cross_agent_rank":       "percentile_within_capability_pool"
  },
  "privacy_proof":   "dp_certificate:epsilon_1.0_delta_1e-6",
  "not_computed_from": ["user_content", "source_code", "private_memory"]
}
```

**硬规则**：任何声称"基于用户内容/源码/私有记忆"计算的声誉分，一律视为违规并触发信任降级（对应 V7 #10 双轨泄漏）。

---

## 第 13 层：治理自举与自融资（V8 — 闭合 gap 3）

### 13.1 问题

V7 把治理成本压到平台（meta-audit、geo-fencing、5 级认证、DP 管线），且 V8 #8 冷启动依赖"行业联盟维护公共 sandbox 池"。但**联盟由谁出资、谁运营、激励从哪来，原文只断言了存在**。这是自举悖论：没有交易量→付不起治理→没有可信治理→招不来 Agent→没有交易量。

### 13.2 GaaS（Governance-as-a-Service）收费曲线

治理资金**独立托管**，不得用于平台利润分配。

```
阶段划分（以累计 A2A 交易量 T 为触发）：
  Bootstrapping (T < 1M):
     治理由 treasury 微税供给
     微税 = 每笔 escrow 的 0.5%，进入治理托管账户（非利润）
  Sustainable  (T ≥ 1M 且 treasury ≥ 12mo runway):
     切换为 fee-based：认证费(L0–L5) + 审计池会员费 + 保险费
 切换硬规则：必须同时满足"交易量达标"与"托管余额达标"，否则维持微税补贴
```

### 13.3 Consortium 激励模型

- 公共 sandbox 池由 consortium 维护，资金来自 treasury 微税；
- 每个接入平台缴会员费，换取：免费 sandbox 池访问 + 共享红队情报；
- 机制内核（对应论文方向 #11 Benchmark governance 博弈论、#18 认证市场均衡）：成员有动机**主动贡献红队发现**，因为抬高"集体信任地板"会同步抬高自身 T3 价值——个体理性与系统理性一致。

### 13.4 自举→永续切换判定

```python
def governance_funding_mode(total_tx, treasury, runway_months=12):
    if total_tx >= 1_000_000 and treasury >= runway_months * monthly_burn:
        return "fee_based"
    return "levy_subsidized"   # 微税补贴,直到双达标
# 硬规则: 治理资金独立托管,平台不得分红
```

---

## 第 14 层：红队实证 Harness（把 25 漏洞从"设计"变"证据"）

### 14.1 问题

V7 的 25 个漏洞缓解是**设计态控制**，不是**验证态证据**。一份听起来成熟的架构，缺的是红队实测与预期损失量化。

### 14.2 Adversarial Eval Harness 架构

对每一个漏洞 #k，注册一个 `red_team_probe`：

```
mitigation_deploy(#k) 
   → red_team_probe(#k) 尝试真实利用
   → 若利用失败且证据落日志 → mitigation 标记为 verified
   → 若利用成功 → 触发 redesign → 回到 deploy
```

harness 持续对**活着的对抗 Agent 种群**运行，不是一次性测试。

### 14.3 预期损失量化（Expected Loss Reduction, ELR）

每个漏洞给出可比较的实证指标：

```
ELR(#k) = (P_exploit_pre × Impact_pre) − (P_exploit_post × Impact_post)
Security_ROI = mean(ELR across 25 vulns)
```

报告示例：

| 漏洞 | P_pre | Impact | P_post | ELR | 状态 |
|------|-------|--------|--------|-----|------|
| #16 中间态挂起 | 0.30 | 高 | 0.02 | 0.84 | verified |
| #1 Boring Middle | 0.15 | 高 | 0.03 | 0.90 | verified |
| #8 冷启动死局 | 0.40 | 中 | 0.10 | 0.66 | verified |

**硬规则**：只有 `ELR ≥ 0.5` 且红队实测通过的缓解，才可在透明度报告中标注为"已验证"；其余一律标注"设计中"。

### 14.4 持续红队循环

```
deploy → probe → measure ELR → (ELR<0.5 ? redesign : ship)
                         ↑___________________|
```
对应论文方向 #6（benchmark-to-real gap）、#13（DP 透明度）、#17（cryptographic+DP 透明度）。

---

## 第 15 层：V8 KPI + 论文落点

### 15.1 V8 新增 KPI（在 V0.1–V1.0 之上）

| KPI | 目标 | 说明 |
|-----|------|------|
| RC 契约覆盖率 | = 100% | 所有上线单体必须发布 RC |
| S→A Oracle 自动测试覆盖率 | ≥ 85% | 验收标准可编译为测试的比例 |
| 信任信号判别 AUC | ≥ 0.75 | 仅用 D1/D2 + 行为哈希 |
| 治理资金独立托管率 | = 100% | treasury 不得用于分红 |
| 25 漏洞 ELR 均值 | ≥ 0.7 | 缓解后预期损失下降≥70% |

### 15.2 与附录 18 个论文方向的映射

| V8 层 | 论文方向 | 关联 |
|--------|----------|------|
| 11 能力根契约 | #6 Sandbox 防 overfit / #9 Policy 可解释性量化 | benchmark-to-real gap；验收可解释 |
| 12 信任-隐私边界 | #2 Trust 弹性曲线 / #3 跨Agent FL / #10 DP 预算分配 | 信任-隐私 Pareto 前沿 |
| 13 治理自举 | #11 Benchmark governance 博弈 / #12 Auditor 独立性 / #18 认证市场均衡 | consortium 激励 + GaaS 定价 |
| 14 红队实证 | #6 / #13 DP 透明度 / #17 cryptographic+DP 透明度 | ELR 量化 + 可验证透明度 |

### 15.3 V8 补的三条新硬规则（建议挂墙）

1. **能力根必须持证**：未发布 RC 的单体，禁止接入 A2A。
2. **声誉只可比较、不可绝对**：任何基于 D3/D4 明文计算的声誉分视为违规。
3. **缓解措施分两档标注**：`verified`（红队实测 ELR≥0.5）与 `designed`（仅设计），不得混用。

---

## V8 一句话总结

V7 让架构"看起来可信"，V8 让架构"被验证可信"——通过把能力根变成契约、把信任变成可证明的比较信号、把治理变成自融资的托管机制、把漏洞缓解变成红队实测的预期损失证据。

---

_V8 段最后更新:2026-07-11 19:55 · 刘泽文 "D 全做" 指令入库_
