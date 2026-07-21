# A2A — Agent-to-Agent Protocol

_2026-07-11 沉淀。来源:Agent OS V1→V7 完整方案核心议题。_

---

## 🎯 定义

**A2A(Agent-to-Agent Protocol)** 是不同 AI Agent 之间互相发现、委托任务、接收任务、协作交付的通信协议。

A2A 不同于 API 调用,关键差别:
- **Agent 是 autonomous**(自主决策)而非 deterministic(确定性)
- **Task 是不确定长度和结果** 而非固定 endpoint
- **Trust 必须是 dynamic** 而非 static API key

---

## 📐 A2A 核心组件(Agent OS V1-V6)

### 1. Agent Card(Agent 名片)

类比 OpenAPI Spec,每个 Agent 必须有公开的"名片":

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

### 2. Task 协议

任务创建、流转、交付的标准化格式:

```json
{
  "task_id": "task_123",
  "requester_agent": "haolo-agent",
  "target_agent": "design-agent",
  "goal": "生成电商主图方案",
  "inputs": {"product": "无线耳机", "style": "科技感", "size": "1024x1024"},
  "constraints": ["不要使用侵权品牌", "中文文案不超过12字"],
  "acceptance_criteria": ["输出图片URL", "输出设计说明", "图片可访问"],
  "callback_url": "https://...",
  "payment": {"mode": "escrow", "max_budget": "0.50"}
}
```

### 3. 状态机

```
created → accepted → running → need_more_info
       → partially_submitted → partial_verified → partial_completed
       → submitted → verified → completed

失败: rejected / cancelled / timeout / failed / disputed / refunded / expired
```

### 4. Verified 多源

```json
{
  "verified_by": "requester_agent | provider_agent | human_user | third_party_arbitrator | automated_test",
  "evidence": ["test_report", "screenshot", "artifact_hash"],
  "confidence": 0.92,
  "dispute_window": "24h"
}
```

---

## 📐 A2A vs MCP 边界

| | A2A | MCP |
|---|---|---|
| **通信双方** | Agent ↔ Agent | Agent ↔ Tool |
| **自主性** | 双方都是 autonomous | Agent 自主,Tool 确定性 |
| **典型延迟** | 秒-分钟(不确定) | 毫秒-秒(确定) |
| **支付** | Yes(escrow / pricing) | No |
| **Trust 模型** | Trust level + reputation | API key + scope |

> **MCP 管工具,A2A 管 Agent**(核心原则)

---

## 🪤 A2A 常见漏洞

### 漏洞 1:跨平台 Policy 无交集(Critical)

不同平台 policy 交集可能为空 → 任务无法执行。

**缓解**:
- Fallback 降级
- Jurisdiction 预检

### 漏洞 2:Verified 串通(High)

Requester + Provider 互相 verified → verified 失去意义。

**缓解**:
- 多源加权(automated_test 0.2 / human_user 0.4)
- 轮换 + 盲审

### 漏洞 3:Orphan Task 挂起(High × Easy × Easy)

Provider 进程崩溃 → 任务永远 need_more_info。

**缓解**:
- 24h 超时自动 cancel
- 心跳机制

---

## 📐 与 MCP / A2P 的关系

```
MCP (Model Context Protocol)
  Agent → Tool(本地或云工具)
  
A2A (Agent-to-Agent)
  Agent → Agent(同/跨平台)
  
A2P (Agent-to-Platform)  ← 当前协议空白
  Agent → SaaS Platform(Salesforce / 飞书 / 钉钉)
```

A2P 是 V6 未解决的协议空白(见漏洞 C2)。

---

## 📐 A2A 状态机的中间态可靠性

中间态(need_more_info / partial_submitted)是**比宕机更危险**的状态。

详见 [漏洞分析](../analysis/agent-os-vulnerabilities-2026-07-11.md) 漏洞 #16。

---

## 🔗 与研究主线接口

- **多 Agent 主线**: A2A 是多 Agent 主线的极端形式
- **校准主线**: A2A verified_by 可用 calibration 加权
- **偏好耦合**: 用户对 verified_by 来源的偏好

---

## 📚 A2A 协议参考

- **OpenAI Function Calling**(2023) —— 早期 A2A 雏形
- **LangChain Agent Protocol**(2024) —— 多 Agent 协调
- **CrewAI / AutoGen**(2024) —— 编程式 multi-agent
- **Google A2A Protocol**(2025 草案) —— 标准化尝试
- **Anthropic MCP**(2024) —— MCP 协议已成熟

---

## 🎓 论文 idea(从 A2A 出发)

1. **A2A 状态机中间态恢复**(IDEA-A7) — TMLR engineering
2. **跨平台 policy 交集最优性**(IDEA-A3) — TMLR
3. **Trust 跨平台 bridge 协议** — 整合 T0-T4 + 跨平台 calibration

---

_最后更新:2026-07-11 12:50_
