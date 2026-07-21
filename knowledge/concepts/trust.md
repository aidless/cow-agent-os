# Trust — 信任体系在 Agent OS 中的设计

_2026-07-11 沉淀。来源:Agent OS V1→V7 完整方案 + 漏洞分析。_

---

## 🎯 定义

在 A2A (Agent-to-Agent) 网络中,**Trust** 是衡量一个 Agent 可信度的多维属性,通常包括:

- **Identity Trust** — 身份是否验证
- **Capability Trust** — 声称的能力是否真实
- **Behavioral Trust** — 历史行为是否一致
- **Reputation** — 社区评价

---

## 📐 Trust 等级体系(Agent OS V5)

```
T0 Unknown        → 只能做低风险试任务
T1 Verified Identity → 身份已验证
T2 Trial Passed   → 通过试运行
T3 Reputation     → 稳定评分 + 历史
T4 Trusted Partner → 长期合作/企业白名单
```

### 关键设计原则

1. **渐进信任** —— 从 T0 起步,通过 sandbox 试运行 + 真实任务表现逐步升级
2. **可降级** —— 一次事故可能 T4→T2,不是直接 T4→T0(避免跳水)
3. **多源验证** —— Trust 不是 single source,需要 cross-validation
4. **凭证化** —— Trust Level 必须 signed,可被任何第三方验证

---

## 🪤 Trust 系统常见漏洞

### 漏洞 1:Trust 跳水(High × Easy × Medium)

一次严重事故 → T4→T0 → 误伤长期信任的 Agent → 没有"修复证明"机制

**缓解**:
- 渐进降级 + 修复证明
- 分级事故响应(L1/L2/L3)
- Trust Insurance(保费反映风险)

### 漏洞 2:Sandbox 刷榜(High × Medium × Hard)

Agent 在 sandbox 表现好,但真实任务差 → Trust 评估失真

**缓解**:
- Pareto-frontier 分析:sandbox 分数 vs 真实任务表现
- sandbox P99 + 真实 < P50 → 自动触发审计

### 漏洞 3:Trust 集合可能为空(Critical × Medium × Medium)

跨平台 Trust 等级不对齐 → 5 边交集可能不存在

**缓解**:
- 多边 policy 交集公式
- Fallback 降级策略
- Trust bridge 协议

---

## 🔗 与研究主线接口

### 校准主线

- **ECE** 衡量 Trust 评分 vs 实际表现的偏差
- Trust rating 应该被**校准**(overconfident vs underconfident)

### 偏好耦合主线

- 用户对"信任降级速度"有不同偏好
- 可以用 RLHF 训练个性化 Trust 策略

### 多 Agent 协作主线

- Trust 是 multi-agent 协作的核心机制
- distributed trust graph 类似 PGP web of trust

---

## 📚 参考来源

- [Agent OS 完整方案 — 信任等级章节](../sources/agent-os-architecture-full-2026-07-11.md)
- [漏洞 #5 Trust 跳水](../analysis/agent-os-vulnerabilities-2026-07-11.md)
- [漏洞 #2 Kill Switch](../analysis/agent-os-vulnerabilities-2026-07-11.md)
- [论文 idea — Trust System Resilience](../analysis/research-ideas-from-agent-os-2026-07-11.md)

---

_最后更新:2026-07-11 12:50_
