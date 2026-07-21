# Agent OS Reference Architecture V1→V7 — 实施计划表

_2026-07-11 沉淀。基于 `sources/agent-os-architecture-full-2026-07-11.md`(53 KB,10 层架构 + 6 补丁 + 25 漏洞)整理的可执行计划。_

> **核心**:把方案文档变成可执行的时间表 + KPI + 责任人 + 优先级。

---

## 🎯 总体目标

**从"Agent OS 战略蓝图" → "V1.0 Agent Marketplace 商业网络"**

**总时间线**:6-12 个月(基于工作量估计)

---

## 📋 8 阶段计划表

### 第一阶段:战略蓝图 V1 ✅ DONE

| 项 | 状态 | 产出 |
|---|---|---|
| 12 层线性架构 → 5 平面架构 | ✅ | 战略框架确定 |
| 6 阶段推进路线 | ✅ | 单体 → 工具 → 多 Agent → A2A → 商业 |
| 根命题确认 | ✅ | "A2A 的价值不是能连别人,而是你自己足够可靠" |
| **完成时间** | 7/11 | 0.5 天 |

---

### 第二阶段:运营平台 V2 ✅ DONE

| 项 | 状态 | 产出 |
|---|---|---|
| 5 平面 + 横切 Control Plane | ✅ | `agent-os-architecture` §2 |
| 6 版本路线图(V0.1-V1.0)| ✅ | §8 完整 KPI 表 |
| 5 类演化机制 | ✅ | §7(任务级/用户级/项目级/生态级/模型策略级) |
| **完成时间** | 7/11 | 1 天 |

---

### 第三阶段:工程实现 V3 🟡 60% 完成

| 模块 | 当前状态 | 待做 | 工作量 | 优先级 |
|---|---|---|---|---|
| **PDP 决策接口** `/control/evaluate` | ✅ 定义 | 实现 PDP 服务(参考 OPA/Cedar) | 1 周 | 🔴 P0 |
| **PEP 8 个 hook** | ✅ 定义 | 在泰玄小站实施 V0.2 | 2-3 周 | 🔴 P0 |
| **Cedar Policy DSL** | ✅ 示例 | 写成可执行 schema + 5 测试 | 1 周 | 🔴 P0 |
| **Audit log 7 字段** | ✅ 定义 | 落 DB(分等级存储) | 1 周 | 🔴 P0 |
| **Cedar + Rego hybrid** | 🟡 提案 | 选型(建议 Cedar) + 集成 | 1 周 | 🟡 P1 |
| **Policy explain 全 trace** | 🟡 提案 | 实现 explain() + 三视图 | 2 周 | 🟡 P1 |
| **PDP 分层(Central+Local+Sidecar)** | 🟡 提案 | 实施双层 | 2 周 | 🟡 P1 |
| **Streaming DP 7 层管道** | 🟡 提案 | 实施 V1(hygiene) | 2 周 | 🟡 P1 |
| **小计** | | | **~10-12 周** | |

---

### 第四阶段:生产可靠 V4 🟡 50% 完成

| 主题 | 当前状态 | 待做 | 工作量 | 优先级 |
|---|---|---|---|---|
| **8 PEP hook** | ✅ 定义 | 实施(同 V3)| — | 🔴 P0 |
| **Privacy hygiene + DP V1 标准** | ✅ 定义 | 实施 + 监控 | 2 周 | 🔴 P0 |
| **PDP 分层** | 🟡 提案 | Central + Local 双层 | 2 周 | 🟡 P1 |
| **Policy Explain 全 trace** | 🟡 提案 | explain() + simulator | 2 周 | 🟡 P1 |
| **Streaming DP aggregation** | 🟡 提案 | windowed + contribution bounding | 2 周 | 🟡 P1 |
| **Sandbox Task Library** | 🟡 提案 | 建公共 sandbox 任务池 | 3 周 | 🟡 P1 |
| **Benchmark Governance Plane** | 🟡 提案 | 治理任务池生命周期 | 2 周 | 🟡 P1 |
| **Dynamic 反作弊** | 🟡 提案 | 8 类异常检测 | 2 周 | 🟡 P1 |
| **Audit trail 5 字段** | ✅ 定义 | 实施分级存储 | 1 周 | 🟢 P2 |
| **Kill Switch 多签** | 🟡 提案 | L1/L2/L3 分级 | 1 周 | 🟢 P2 |
| **小计** | | | **~15-17 周** | |

---

### 第五阶段:治理可信 V5 🟡 50% 完成

| 主题 | 当前状态 | 待做 | 工作量 | 优先级 |
|---|---|---|---|---|
| **T0-T4 信任等级** | ✅ 定义 | 实施 sandbox 试运行 | 2 周 | 🔴 P0 |
| **Cold start 5 步** | ✅ 定义 | 实施 consortium 任务池 | 3 周 | 🔴 P0 |
| **Trust bootstrap 5 级** | ✅ 定义 | 身份验证 + 限额 | 2 周 | 🟡 P1 |
| **Trust 渐进降级 + 修复证明** | 🟡 提案 | 降级规则 + 申诉通道 | 2 周 | 🟡 P1 |
| **Verified 多源 + 权重** | ✅ 定义 | 实施 weighted verified_by | 2 周 | 🟡 P1 |
| **DP 4 阶段诚实标注** | ✅ V1/V2/V3/V4 定义 | V1(hygiene)→ V3(TEE) | 4 周 | 🟡 P1 |
| **Audit Committee 4 件套** | ✅ 定义 | PDP + PEP + PAP + Audit | 2 周 | 🟡 P1 |
| **Audit Committee 4 级分级** | ✅ 定义 | L1 auto / L2 quick / L3 deep / L4 ext | 1 周 | 🟡 P1 |
| **Policy explain 三视图** | 🟡 提案 | dev/admin/user | 1 周 | 🟡 P1 |
| **5 类演化机制** | ✅ 定义 | 实施(优先任务级 + 用户级) | 3 周 | 🟢 P2 |
| **Transparency 三阶段** | ✅ 定义 | Phase 1 制度透明 | 2 周 | 🟢 P2 |
| **小计** | | | **~20-24 周** | |

---

### 第六阶段:跨平台治理 V6 ✅ 80%(理论)

| 主题 | 当前状态 | 待做 | 工作量 | 优先级 |
|---|---|---|---|---|
| **5 边 policy 交集公式** | ✅ 公式 | 实施 algorithm | 2 周 | 🟡 P1 |
| **Policy Negotiation Protocol** | ✅ 定义 | requester/provider JSON | 1 周 | 🟡 P1 |
| **Jurisdiction Policy Engine** | ✅ 定义 | 预检 + 降级 | 3 周 | 🟡 P1 |
| **Meta-audit 多方制衡** | ✅ 定义 | 6 层治理结构 | 2 周 | 🟢 P2 |
| **透明度报告三阶段** | ✅ 定义 | Phase 1 实施 | 2 周 | 🟢 P2 |
| **5 层分级认证** | ✅ 定义 | L0-L5 认证体系 | 3 周 | 🟢 P2 |
| **Audit trail 5 件套** | ✅ 定义 | audit 记录实施 | 1 周 | 🟢 P2 |
| **AI 审计 AI 6 约束** | ✅ 定义 | LLM 辅助审计 | 2 周 | 🟢 P2 |
| **小计** | | | **~16 周** | |

---

### 第七阶段:红队加固 V7 🟡 70% 完成

| 主题 | 当前状态 | 待做 | 工作量 | 优先级 |
|---|---|---|---|---|
| **4 轮红队 54 漏洞** | ✅ 文档 | (待 patch) | — | 🔴 P0 |
| **Critical 11 漏洞 triage** | ✅ 文档 | **必做 1h**:决定 patch/paper/defer | 1 h | 🔴 P0 |
| **V8 补丁(R3 must-fix 5)** | 🟡 提案 | 实施 patch | 3 周 | 🔴 P0 |
| **V9 补丁(R4 must-fix 5)** | 🟡 提案 | 实施 patch | 3 周 | 🔴 P0 |
| **3 个暗模式应对原则** | ✅ 文档 | 实践到代码 | 持续 | 🟡 P1 |
| **P0/P1/P2/P3 修复优先级** | ✅ 矩阵 | 跟踪执行 | 持续 | 🟡 P1 |
| **小计** | | | **~6-7 周** | |

---

### 第八阶段:生态落地 🟡 40% 完成

| 主题 | 当前状态 | 待做 | 工作量 | 优先级 |
|---|---|---|---|---|
| **18 个对研究主线接口** | ✅ 文档 | 选 1 个写 paper | 6-8 周 | 🟡 P1 |
| **35 个 paper idea 候选**(原 15 + R3 8 + R4 12)| ✅ 文档 | 排序 + 写 1 篇 | 6-8 周 | 🟡 P1 |
| **泰玄小站 V0.2 控制平面**(对接 B1)| 🟡 部分 | 实施(1-2 周) | 1-2 周 | 🟡 P1 |
| **paper-review-toolkit 动态化**(对接 B3)| 🟢 85% | 跑 4 组 ablation | 4 h | 🟡 P1 |
| **w7 OS paper 投递 arxiv** | 🟢 包齐 | 投递 | 30 min | 🟡 P1 |
| **小计** | | | **~10-14 周** | |

---

## 🎯 4 条 Critical 路径(并行可推进)

### 路径 1:安全基础设施(可立即启动)

```
[1] PDP + PEP 8 个 hook 实现          2-3 周
[2] Audit log 分级存储                1 周
[3] Privacy hygiene + DP V1 标准      1-2 周
[4] Sandbox 任务池 consortium 治理   2-3 周
```
**总工时**:6-9 周

---

### 路径 2:红队 11 Critical 漏洞修复(必做)

```
[1] Critical 11 triage(决策)          1 h       ← 必做
[2] R3 5 must-fix patch              2-3 周
[3] R4 5 must-fix patch              2-3 周
[4] Kill Switch 多签实施             1 周
[5] GDPR 跨境冲突 fix                1 周
[6] Jurisdiction kill switch         1 周
```
**总工时**:8-10 周

---

### 路径 3:学术产出(可立即启动)

```
[1] 选 1 个 idea(B3 Dynamic Worker 推荐)   1 周
[2] paper-review 4 组 ablation               4 h
[3] 写 paper(8-12 页)                     2-3 周
[4] 投稿 TMLR                             1 周
```
**总工时**:6-8 周

---

### 路径 4:泰玄小站工程实现(已部分推进)

```
[1] policy.yaml Cedar-like               2 h
[2] cost scanner 接入 validate.bat        2 h
[3] permission scanner 接入               2 h
[4] spec 加 permissions_required 字段    1 h
[5] 421+ 断言不退步                      2 h
```
**总工时**:1-2 周

---

## 📊 数字总览

| 阶段 | 完成度 | 待做(周) |
|---|---|---|
| 第一阶段 V1 战略 | 100% | 0 |
| 第二阶段 V2 运营 | 100% | 0 |
| 第三阶段 V3 工程 | 60% | 10-12 |
| 第四阶段 V4 可靠 | 50% | 15-17 |
| 第五阶段 V5 治理 | 50% | 20-24 |
| 第六阶段 V6 跨平台 | 80% | 16 |
| 第七阶段 V7 红队 | 70% | 6-7 |
| 第八阶段 生态 | 40% | 10-14 |
| **总计** | **~64%** | **~78-90 周** |

**总时间估算(单人全时)**:18-22 个月(单人全时);**实际可并行 4 路径,3-6 个月到 V0.5**

---

## 🎯 我的建议执行顺序(基于 ROI)

### 第 1 阶段(立即,1 周内)

| 优先级 | 任务 | 工作量 |
|---|---|---|
| 🥇 | Critical 11 triage | 1 h |
| 🥈 | w7 投递 arxiv(包齐)| 30 min |
| 🥉 | w5 4 组 ablation(接 B3) | 4 h |
| 4 | w1 TMLR 投递 | 30 min |
| 5 | w10 健康检查 + DB VACUUM | 1 h |

**总投入**:半天 + 5 h

### 第 2 阶段(2-4 周)

| 任务 | 工作量 |
|---|---|
| 修 Critical 11 漏洞 | 2-3 周 |
| 选 1 个 idea 写 paper | 6-8 周(可与上面并行) |

### 第 3 阶段(1-3 月)

| 任务 | 工作量 |
|---|---|
| V3 工程:PDP + PEP 8 hook 实施 | 2-3 周 |
| V4 可靠:PDP 分层 + explain + DP streaming | 2-3 周 |

### 第 4 阶段(3-6 月)

| 任务 | 工作量 |
|---|---|
| V5 治理:Trust 实施 + DP 4 阶段 | 2-3 月 |
| V6 跨平台:Jurisdiction engine | 2-3 月 |

### 第 5 阶段(6-12 月)

| 任务 | 工作量 |
|---|---|
| V7 红队:18 Critical 全 patch | 3-6 月 |
| V8 商业化 | 6-12 月 |

---

## 🎯 关键节点(KPI)

| 节点 | 达成标准 | 估算时间 |
|---|---|---|
| **V0.1 单体 Agent** | 任务完成率 ≥ 80% | 1 周 |
| **V0.2 控制平面** | 敏感操作确认率 100% + 拦截率 99% | 2-3 周 |
| **V0.3 动态 Multi-Agent** | 复杂任务完成率 +20% | 1-2 月 |
| **V0.4 A2A 基础** | 调用成功率 ≥ 85% | 2-3 月 |
| **V0.5 Trust + Partial** | 冷启动通过率 ≥ 80% | 3-6 月 |
| **V1.0 Marketplace** | 付费任务验收通过率 ≥ 90% | 6-12 月 |

---

## 📂 与已有项目的对应

| 已有项目 | 对应 Agent OS 阶段 | 当前状态 |
|---|---|---|
| **泰玄小站 v1.x** | V0.1 单体 Agent | ✅ 跑通 |
| **wechat-mp-validation skill** | V0.1 验证流水线 | ✅ 跑通 |
| **paper-review-toolkit** | V0.3 内部 Multi-Agent | 🟢 85%(动态化进行) |
| **TEMPLATE v0.5.0** | V0.1 测试用例 + V0.3 工具 | ✅ release |
| **Aidless tmaudit** | V0.4 跨平台 A2A 雏形 | ✅ GitHub 仓库 |

---

## 🎯 总结

**当前在 V3-V7 阶段**,**最该做**(未来 1 周):

1. **Critical 11 triage**(1 h,必须)
2. **修 4 个真 HIGH**(2 h)
3. **w7 投递 arxiv**(30 min)
4. **w5 ablation(接 B3 paper)**(4 h)

**这 4 个做完,可以从 V3-V7 进入 V0.5(Trust + Partial)** —— 即 3-6 个月到 6-12 个月的里程碑。

---

## 🔗 跨文档链接

- [Agent OS Reference Architecture V1→V7 完整方案](../sources/agent-os-architecture-full-2026-07-11.md)
- [漏洞分析 V7 之前(25 漏洞)](./agent-os-vulnerabilities-2026-07-11.md)
- [第三轮红队(17 漏洞 #26-#42)](./agent-os-red-team-r3-2026-07-11.md)
- [第四轮红队(12 漏洞 #43-#54)](./agent-os-red-team-r4-2026-07-11.md)
- [Critical 11 漏洞 Triage](./agent-os-critical-11-triage-2026-07-11.md)
- [研究 idea 挖掘(15 个 paper 候选)](./research-ideas-from-agent-os-2026-07-11.md)
- [研究 idea 漏洞分析(15 个红队)](./research-ideas-vulnerabilities-2026-07-11.md)
- [11 窗口全量进度报告](./windows-progress-2026-07-11.md)

---

_最后更新:2026-07-11 16:00 · 泰整理_