# Multi-Agent Collaboration — 多 Agent 协作框架

_2026-07-11 沉淀。来源:Agent OS V1→V7 完整方案 + 刘泽文研究主线之一。_

---

## 🎯 定义

**Multi-Agent Collaboration** 指多个 AI Agent 通过协议、消息、共享状态等方式协同完成单个 Agent 无法完成的任务。

在 Agent OS 中,可分**两大类**:

```
内部 Multi-Agent:Orchestrator + Worker pool(同一平台内)
外部 A2A:跨平台 Agent-to-Agent(见 a2a.md)
```

---

## 📐 核心组件

### 1. Orchestrator(主调度)

- 接收任务 spec
- 决定 worker pool 组成
- 协调并行 / 串行执行
- 整合结果 + 验收

### 2. Worker Agents(执行子任务)

- 单一职责
- Context budget 有限
- Expire-on-completion(防止 context 累积)
- 通过 PEP 调用工具

### 3. Communication Protocol

- **Task 契约**(JSON 格式,见 Agent OS 方案)
- **Message passing**(gRPC / HTTP / gRPC-streaming)
- **Shared state**(Redis / Postgres)

### 4. Verification

- Verifier Agent 独立审查
- Multi-source verified_by
- Confidence + evidence + dispute_window

---

## 📐 协作模式分类

### 静态 vs 动态

| 模式 | 说明 | 优点 | 缺点 |
|---|---|---|---|
| **静态**(固定角色) | 8 个预定义 worker | 简单、稳定 | 不灵活 |
| **动态**(spec-driven) | 按任务生成 worker | 灵活、context 高效 | 复杂、难调优 |

→ Agent OS V3 推**动态模式**

### 串行 vs 并行

- **串行**:Pipeline 式,每步依赖上一步结果
- **并行**:独立子任务可并行(如 3 reviewer 并行)
- **混合**:Pipeline 中某些步骤并行

### 集中 vs 分布

- **集中**:Orchestrator 唯一中心,容易管理
- **分布**:Peer-to-peer,去中心化

---

## 🪤 多 Agent 协作的常见漏洞

### 漏洞 1:互相甩锅

Agent A 完成 → Agent B 验证 → Agent C 整合。每步都可以甩锅,出问题无人负责。

**缓解**:
- 每个 Agent 必须留 evidence + confidence
- evidence 必须可独立验证

### 漏洞 2:Context 累积

Worker chain 越长,context 越大 → token 成本爆炸。

**缓解**:
- Worker 必须 expire after task
- Context budget 限制
- Summary 抽象

### 漏洞 3:动态 vs 静态 baseline 难对比(IDEA-B3 漏洞)

动态 worker 池 vs 静态 8 角色,哪个更好?**需要 ablation 才能公平比较**。

**缓解**:
- 4 组 ablation:静态、静态+调优、动态、动态+调优、Random

### 漏洞 4:Orchestrator 单点

Orchestrator 故障 → 整个 multi-agent 死锁。

**缓解**:
- Orchestrator 高可用(Raft 选主)
- Fallback 到简化模式(单 Agent)

---

## 🛠️ 实战案例:TEMPLATE plugin API(2026-07-11)

F:\Research\TEMPLATE 项目提供了 multi-agent 系统的一个**简化、真实、可参考**的样本:plugin API。

### 角色映射

| Multi-Agent 概念 | TEMPLATE plugin API 实现 |
|---|---|
| Orchestrator | `audit_plugins()` 函数 |
| Worker Agents | 注册的 plugin(每个是一个 check function) |
| Task 契约 | `paper_config` dict(包括 `c11_plugins_disabled`、`c11_plugins_enabled`) |
| Verification | 10 个 audit categories(C1-C10) |
| 5 类演化机制 | 不在此项目,但 plugin 作者可以写 "self-improving" plugin |

### Plugin Whitelist(per-paper 锁定)

```python
# PAPER5 锁定为只用 1 个 plugin
paper_config['c11_plugins_enabled'] = ['flag-todo-markers']

# 内部实现 (filter_active):
if enabled_set:
    if disabled_set:
        log.warning("enabled+disabled both set; enabled wins")
    return {n: c for n, c in plugins.items() if n in enabled_set}
```

**这是 Multi-Agent 协作中"per-task spec 控制 worker selection"的工业级实例**。

### Meta-test(回归保护)

TEMPLATE 用 `_check_all_regressions.py` 自动验证 16 个 bug 修复后没退步。这是 multi-agent 系统"持续学习不遗忘"的工程化手段。

详见:[TDD + Meta-test 模式](./tdd-meta-test.md) + [Plugin Whitelist Pattern](./plugin-whitelist-pattern.md)。

---

## 📐 Orchestrator 的设计选择

### 决策算法

```text
收到 Task:
  1. 解析 spec(goal / inputs / constraints / acceptance)
  2. 决定 worker 数量 + 能力:
     - 简单任务 → 1 worker
     - 中等 → 主 worker + verifier
     - 高风险 → 主 + reviewer + policy check
     - 大型 → 动态生成 N 个 worker
     - 外部专业 → A2A 委托
  3. 分配 context + 工具权限
  4. 监控 + 收集结果
  5. Verifier 独立审查
  6. 整合 + 交付
```

### Context Budget

```
Orchestrator context = T(任务) + Σ Worker context
每个 Worker context ≤ 8K tokens(防止膨胀)
Worker expire after task → context 释放
```

---

## 🔗 与研究主线接口

### 多 Agent 主线(直接)

- Dynamic worker pool 的最优生成策略(IDEA-B3)
- Multi-Agent 任务拆分的最优算法
- Verifier 投票加权(IDEA-B4)

### 校准主线

- Multi-Agent 决策的 calibration propagation
- Verifier ensemble 的 calibration 聚合

### 偏好耦合主线

- 用户对"分工模式"的偏好(集中 vs 分布)

---

## 📚 经典 paper

- **Wooldridge (2009)** — An Introduction to MultiAgent Systems(经典教材)
- **Stone & Veloso (2000)** — Multiagent Systems: A Survey
- **Dorri et al. (2018)** — Multi-Agent Systems: A Survey(更新综述)
- **Han et al. (2024)** — Multi-Agent Collaboration Survey(LLM era)

---

## 🎓 论文 idea(从 Multi-Agent 协作出发)

1. **Dynamic Worker Pool 最优生成**(IDEA-B3) — TMLR / AAMAS
2. **Verifier Voting Weighted by Calibration**(IDEA-B4) — TMLR
3. **Multi-Agent Cost-Benefit Optimization** — 协作成本 vs 收益的最优平衡

---

_最后更新:2026-07-11 12:50_
