# Agent OS V8 详细实施计划

_2026-07-13 21:25 · 作者:泰 · 依据:[sources/agent-os-architecture-full-2026-07-11.md §11-15](./../sources/agent-os-architecture-full-2026-07-11.md) + [agent-os-v8-review-2026-07-11.md](./agent-os-v8-review-2026-07-11.md)_

> **本文档定位**:面向 V8 实施 session 的接力 plan,纯文档,无代码改动。
> **风格**:每任务有 ID + DoD + 依赖 + 输出物路径 + 估算工时,可被其他 ML session 直接接力。
> **不要把它当论文** — 它是 RFC 落地清单,V8 论文(若要写)拆 4 个独立 paper,见 §5。

---

## 🎯 总览:V8 = 4 个新层 × 2 阶段(10 周)

| 层 | 主题 | 总估时 | 论文关联 |
|---|---|---|---|
| **§11 RC 契约** | 单体可靠性契约 + Spec→Acceptance Oracle | 2 周 | #6 / #9 |
| **§12 UTB 边界** | 信任-隐私效用边界 + 可验证声誉协议 | 2 周 | #2 / #3 / #10 |
| **§13 GaaS 自举** | 治理自融资 + Consortium 激励 + 切换判定 | 1.5 周 | #11 / #12 / #18 |
| **§14 红队 Harness** | Adversarial Eval Harness + ELR 量化 + 25 漏洞实测 | 4 周 | #6 / #13 / #17 |
| **横向基础** | §15 5 个 KPI 仪表盘 + V8 硬规则 3 条落地 | 0.5 周 | — |

**关键依赖**:14 红队 Harness **必须最后做**(因为它依赖 §11-13 提供的契约/边界/治理作为 probe 对象)。

**正确顺序**:§11 → §12 → §13 → §15 KPI 串起来 → §14 实测验证。

---

## 📦 第 1 阶段:§11 RC 契约(2 周)

### T11.1 RC 契约 schema 定义

- **DoD**:`specs/rc-contract.schema.json` 落地,v2026-07-11.rc1
- **DoD**:12 个 guarantee 字段 + failure_taxonomy + oracle + evidence_required 全是 enum(可校验)
- **DoD**:单元测试覆盖每个 enum 至少 1 边界(0 valid + 1 invalid 边界)
- **依赖**:无
- **输出物**:`specs/rc-contract.schema.json` + `specs/test_rc_schema.py`
- **工时**:3 天
- **可被接力给**:paper-review-toolkit(可借 schema validator)

### T11.2 RC 公共注册中心

- **DoD**:`GET /api/v1/agent/:id/rc` 端点,可查询任一 Agent 当前 RC + 历史版本
- **DoD**:`POST /api/v1/agent/:id/rc` 仅 admin 可写(签名 + audit log)
- **DoD**:RC 版本演进 v0.1 → v0.2 必须保留 v0.1 兼容(向后兼容)
- **依赖**:T11.1
- **输出物**:`specs/rc-registry-api.md` + mock 实现
- **工时**:2 天
- **可被接力给**:泰玄 Flask app(借 blueprint 模式)

### T11.3 Spec→Acceptance Oracle 设计

- **DoD**:`criterion_compiler.py` 接受 JSON `criterion` → 输出 `compiled_test`
- **DoD**:支持 4 种 test type:`http_head` / `regex_match` / `json_schema_match` / `custom_js` 起步
- **DoD**:不可编译的 criterion 在任务创建时拒绝,错误信息含"建议如何改写"
- **依赖**:T11.1
- **输出物**:`tools/criterion_compiler.py` + `tools/test_criterion_compiler.py`(≥20 边界用例)
- **工时**:5 天
- **论文对应**:**#6 Benchmark-to-Real Gap**(核心,因为 criterion 自动化覆盖率是 paper 关键数字)

### T11.4 RC 接入烟测

- **DoD**:把 1 个 demo agent(`haolo.main` 测试用例)的 RC 接到 A2A 模拟器
- **DoD**:无 RC 接入被 reject(硬规则实现)
- **DoD**:有 RC 接入被 allow,且能跑通 3 个 acceptance test
- **依赖**:T11.1-T11.3 全部
- **输出物**:`tests/integration/rc_smoke_test.py`
- **工时**:1 天

---

## 📦 第 2 阶段:§12 UTB 边界(2 周)

### T12.1 D1-D5 分级数据采集协议

- **DoD**:5 个 collector:D1 调用日志 / D2 工具统计 / D3 用户内容(本地) / D4 源码(本地) / D5 跨平台
- **DoD**:D3/D4 默认 **不出本地** —— collector 只有"hash 导出"选项
- **DoD**:D1/D2 可聚合 + `dp(ε=1.0, δ=1e-6)` 管线
- **依赖**:V7 §5.1-5.3 已沉淀,**本次只是落实 D0-D5 分级**
- **输出物**:`specs/data-classification.md` v2.0 + `tools/dp_aggregator.py`
- **工时**:3 天
- **可被接力给**:paper-review-toolkit(它已经有 policy.yaml)

### T12.2 可验证声誉协议(VRP)

- **DoD**:`reputation.json` schema 落地,字段:trust_level / reputation_score / computed_from / privacy_proof / not_computed_from
- **DoD**:`computed_from` 用白名单(仅 D1/D2 聚合 + 行为哈希)
- **DoD**:任何 computed_from 含 D3/D4 → 自动 reject 并告警
- **依赖**:T12.1
- **输出物**:`specs/reputation.schema.json` + `tools/reputation_validator.py`
- **工时**:3 天

### T12.3 信任-隐私 Pareto 前沿实测

- **DoD**:用 6 个真实 agent × 5 个 ε 档(0.1/0.5/1.0/2.0/5.0)画曲线
- **DoD**:验证"ε < 1.0 饱和"假设 × 6 agent 是否成立
- **DoD**:输出 1 张图(PDF)+ 1 个 CSV + 1 段 ≤300 字解读
- **依赖**:T12.1 + T12.2
- **输出物**:`experiments/utb-pareto-2026-XX-XX.{pdf,csv,md}`
- **工时**:4 天
- **🪡 注意**:这实验是 **paper #2 Trust 弹性曲线** 的核心数据,直接出 paper 图

### T12.4 违反检测器

- **DoD**:cron job 每小时扫所有 reputation.json,命中"含 D3/D4"立即降级
- **DoD**:降级动作可观察(写 audit log + 发 webhook + 不静默)
- **依赖**:T12.2 + T12.3
- **输出物**:`tools/violation_detector.py` + cron 配置(参考泰玄 ECS Layer 1 healthcheck.sh 写法)
- **工时**:3 天

---

## 📦 第 3 阶段:§13 GaaS 自举(1.5 周)

### T13.1 Treasury 独立账户设计

- **DoD**:treasury 与 platform 账户物理隔离(双 key,交叉签名才能转账)
- **DoD**:`balance_audit.py` 公开展示 — 任何人可查 treasury 当前余额 + 历史流入流出
- **依赖**:无
- **输出物**:`specs/treasury-design.md` + mock 合约
- **工时**:2 天

### T13.2 GaaS 收费曲线实施

- **DoD**:`treasury_collector.py` 从每笔 escrow 提 0.5% 进 treasury
- **DoD**:`governance_funding_mode(total_tx, treasury, runway_months=12)` 函数实现且有单测
- **DoD**:切换前必须"双达标"(交易量 + treasury 月数)否则维持微税补贴
- **依赖**:T13.1
- **输出物**:`tools/treasury_collector.py` + 单测
- **工时**:3 天

### T13.3 Consortium 激励机制

- **DoD**:会员费 = f(认证等级 L0-L5,审计池资格)定价公式
- **DoD**:贡献红队发现 = f(发现 severity × ELR)积分
- **DoD**:积分 → 提升 T3 声誉 → 模拟跑 30 天看是否 individual rational = system rational
- **依赖**:T13.2 + (§14 实测数据作输入)
- **输出物**:`experiments/consortium-sim/{model.py,results.json}`
- **工时**:4 天
- **论文对应**:**#11 Benchmark governance 博弈论**(直接出 paper)

---

## 📦 第 4 阶段:§15 V8 KPI + 硬规则(0.5 周 = 3.5 天)

### T15.1 5 个 KPI 仪表盘

| KPI | 目标 | 数据源 | 仪表盘组件 |
|---|---|---|---|
| RC 契约覆盖率 | 100% | T11.2 + 所有 agent 列表 | stat card |
| S→A Oracle 自动覆盖率 | ≥85% | T11.3 compile log | stat card |
| 信任信号判别 AUC | ≥0.75 | T12.3 实验输出 | line chart |
| 治理资金独立托管率 | 100% | T13.1 audit log | stat card |
| 25 漏洞 ELR 均值 | ≥0.7 | T14 harness 输出 | bar chart |

- **DoD**:5 个 panel,Grafana JSON 或自写 HTML
- **DoD**:每周快照(可看趋势)
- **依赖**:§11-§13 + §14 数据源
- **输出物**:`dashboards/v8-kpi.{html,json}`
- **工时**:2 天

### T15.2 V8 硬规则 3 条落地

| 规则 | 实现位点 |
|---|---|
| 能力根必须持证 | T11.4 reject 路径 |
| 声誉只可比较 | T12.4 违反检测器 |
| 缓解分两档 | §14 harness 的 `verified` / `designed` 标注 |

- **DoD**:每条规则都有 1 个 violation 测试用例(主动触发 → 必须被拦)
- **依赖**:上面 4 阶段全部
- **输出物**:`tests/hard_rules/test_v8_rules.py`
- **工时**:1.5 天

---

## 📦 第 5 阶段:§14 Adversarial Eval Harness(4 周,**最后做**)

### T14.1 harness 核心循环

- **DoD**:`harness.py` 跑以下循环:deploy → probe → measure ELR → (ELR<0.5? redesign : ship)
- **DoD**:可配置 1-N 个漏洞,每个独立触发
- **DoD**:结果写 ELR table(`elr_results.json`)
- **依赖**:§11-§13 全部 + §15 KPI 数据源
- **输出物**:`tools/red_team_harness.py` + 单测
- **工时**:5 天

### T14.2 25 漏洞红队 probe 注册

- **DoD**:`red_team_probes/{1-25}.py` 每个漏洞 1 个 probe
- **DoD**:probe 默认 deploy 然后 exploit,记录 P_pre/P_post/Impact
- **DoD**:**重用 7/11 已沉淀的漏洞清单**(`analysis/agent-os-vulnerabilities-2026-07-11.md` §)
- **依赖**:T14.1
- **输出物**:`tools/red_team_probes/{1..25}.py`
- **工时**:10 天
- **🪡 提示**:这是个**重任务**,可拆给 5-10 个 ML session 并行,1 个负责 5 个漏洞 probe

### T14.3 ELR 报告 + 透明度文档生成

- **DoD**:`elr_report.py` 跑完后输出:`elr-table.md`(25 行)+ `verified-vs-designed.json`
- **DoD**:`verified` 必须满足 `ELR ≥ 0.5` + 红队实测通过(V8 硬规则)
- **DoD**:总体 ROAI(mean ELR)≥ 0.7
- **依赖**:T14.2
- **输出物**:`reports/v8-elr-2026-XX-XX.md`
- **工时**:3 天
- **论文对应**:**#6 / #13 / #17 透明度 paper**

### T14.4 持续红队循环

- **DoD**:cron 每周跑一次 harness,ELR 下降趋势可见
- **DoD**:新出现的漏洞进 `red_team_probes/26.py` 流程化
- **依赖**:T14.3
- **输出物**:`cron/v8-red-team-weekly.sh`
- **工时**:2 天

---

## 🚀 总行动序列 + 依赖图

```
Week 1-2:  T11.1 → T11.2 → T11.3 ──┐
                                  ├─→ T11.4
Week 3-4:  T12.1 → T12.2 → T12.3 ┐
                                  ├─→ T12.4
Week 5-6:  T13.1 → T13.2 →──────┐│
                                │├─→ T13.3
Week 7:     T15.1 + T15.2(并行,等 §11-13 数据)
Week 8-11:  T14.1 → T14.2 → T14.3 → T14.4
```

**关键路径**:T11.3 + T12.3 + T13.3 → 这 3 个是论文实验,排在前面做可以为 V8 4 个 paper 提供数据。

**可并行的子任务**(可同时给多个 session 跑):
- 论文 #11(Benchmark governance):T13.3 数据
- 论文 #6(Benchmark-to-Real):T11.3 + T14.3 数据
- 论文 #2(Trust 弹性曲线):T12.3 数据
- 论文 #17(DP 透明度):T12.4 + T14.3 数据

---

## ⚠️ 风险与阻塞

| 风险 | 影响 | 应对 |
|---|---|---|
| **§11 强行引入 RC 阻断 现有 agent** | 老 agent 全 fail | v0 阶段 RC 允许 `manual_override`,v1 必须发布 |
| **§12 ε<1.0 饱和假设 不成立** | T12.3 出负结果 | 预设对照组 6 agent 已涵盖 3 个 model family,假设失败也是 paper 数据 |
| **§13 consortium 模拟 跑不通**(个体理性 ≠ 系统理性) | T13.3 paper 失败 | 已留 fallback:换 Stackelberg 博弈 |
| **§14 25 漏洞 probe 有些 exploit 不可构造** | probe 个数 < 25 | 允许 probe 标 `non_exploitable_evidence`,仍算 verified |
| **整体 10 周紧** | 投产延期 | §11 + §12 最关键(论文支撑数据),可先投 §11/12,§13/14 后续 |

---

## 🔗 与 18 个论文方向的映射

| V8 章节 | 任务 ID | 论文方向 | 论文 ID |
|---|---|---|---|
| §11 RC 契约 | T11.1-T11.4 | Benchmark-to-Real Gap | **#6** |
| §11 RC | T11.3 | Policy 可解释性量化 | **#9** |
| §12 UTB | T12.3 | Trust 弹性曲线 | **#2** |
| §12 UTB | T12.1 | 跨 Agent FL | **#3** |
| §12 UTB | T12.1 | DP 预算分配 | **#10** |
| §13 GaaS | T13.3 | Benchmark governance 博弈 | **#11** |
| §13 GaaS | T13.2 | Auditor 独立性 | **#12** |
| §13 GaaS | T13.3 | 认证市场均衡 | **#18** |
| §14 Harness | T14.3 | DP 透明度 | **#13** |
| §14 Harness | T14.3 | Cryptographic + DP 透明度 | **#17** |
| §14 Harness | T14.2 | Benchmark-to-Real | **#6**(同 T11.3,共用数据) |

**潜在产出**:**4 篇 paper 候选**(选 #2 / #6 / #11 / #17)—— 全部 9/15 TMLR 节点的话工作量极大,**建议先做 #6 + #11(已有数据路线)**。

---

## 🎯 给未来的接力指引

### 立即可推(单 session,1-2 天)

- **T11.1 RC schema** — 单文件落地,无依赖,可起点
- **T15.2 硬规则 1 / 2** — 等 §11/12 落地后接

### 中等接力(session 长 3-5 天)

- **T11.3 criterion_compiler** — 论文 #6 核心数据来源
- **T12.3 Pareto 前沿** — 论文 #2 核心数据来源
- **T13.3 consortium sim** — 论文 #11 核心数据来源

### 重型(session 长 5-10 天 或 多人并行)

- **T14.2 25 漏洞 probe** — 可拆给 5-10 个 ML session 并行
- **T14.3 ELR 报告** — 论文 #6 / #13 / #17 数据来源

### 不要立刻碰

- **T14.1 harness 主循环** — 必须等 §11-13 全做完才有意义
- **T14.4 持续 cron** — 必须等 T14.3 报告干净后才上

---

## 📊 资源估算

| 资源 | 用量 |
|---|---|
| 总人天 | ~75 人天(单人 10-12 周) |
| 并行假设 3 session | **5-6 周**实际工时 |
| 并行假设 5 session | **3-4 周**实际工时 |
| 论文产出 | 4 篇候选(挑 2 投 9/15 TMLR) |
| 代码产出 | ~6 KB schema + 4-5 个 Python 工具 + 25 个 probe |
| 文档产出 | 1 份 ELR 报告 + 1 份 transparency report |

---

## 📝 与其他 session 的交接清单

任何接力这个计划的 session 应验证:

- [ ] 读过 `sources/agent-os-architecture-full-2026-07-11.md` §11-15 全文
- [ ] 读过 `analysis/agent-os-v8-review-2026-07-11.md`(V8 自检报告,257 行)
- [ ] 读过 `analysis/agent-os-vulnerabilities-2026-07-11.md`(25 漏洞详解)
- [ ] 看了 7/11 Agent OS 系列 index 段(`analysis/agent-os-critical-11-triage-2026-07-11.md`)
- [ ] 没有跨"职责外"——本计划**与泰玄小站无关**(职责外,泰不介入)

---

**计划完。等刘泽文指派 / 任一执行 session 来接力。**