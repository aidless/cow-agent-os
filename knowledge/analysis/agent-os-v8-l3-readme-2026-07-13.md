# V8 L3 实施计划 — README(1 页开箱指南)

_2026-07-13 22:30 · 作者:泰 · 配套:[L3 详细计划](./agent-os-v8-implementation-plan-l3-2026-07-13.md)_
_目标读者:新开 ML session 接力 V8 任一任务_

> **30 秒电梯演讲**
> 你要接力 V8 实施。L3 = 15 个任务 / 75 个半天 / ~220 单测 / 4 论文候选。
> 你**不需要**读白皮书全文,**不需要**读 L2,只要读本 README + L3 对应任务那段。
> 上午干半天,跑通,下午干半天,跑通,留痕 4 处。**任务交接一次完成**。

---

## 📚 4 件必读 + 阅读顺序

| # | 文件 | 读多久 | 不读会怎样 |
|---|---|---|---|
| 1 | **本 README** | 5 min | 迷路 |
| 2 | [L3 详细计划 §你的任务段](./agent-os-v8-implementation-plan-l3-2026-07-13.md#你的任务段) | 15-30 min | 不知道上午干什么 |
| 3 | [V8 白皮书 §11-15 相应小节](../sources/agent-os-architecture-full-2026-07-11.md) | 30 min | 不知道字段语义 |
| 4 | [V8 自检档](./agent-os-v8-review-2026-07-11.md) | 10 min | 不知道哪些坑已踩 |

**🚫 不要读**:
- L2 全文(已被 L3 覆盖)
- 红队 25 漏洞详解(除非你接 T14.x)
- 泰玄小站文档(与 V8 无关)
- AGENT.md / RULE.md(会话人格配置,与你无关)

---

## 🚀 3 行命令开箱

```bash
# 1. 装环境
pip install jsonschema pytest requests flask pyodide diffprivlib mesa

# 2. 读你的任务(假设 T11.1)
# 用 read 工具读 analysis/agent-os-v8-implementation-plan-l3-2026-07-13.md 找 "T11.1" 段

# 3. 开工
mkdir -p specs/rc-examples && cd specs && touch rc-contract.schema.json
```

---

## 🔁 "上午/下午"工作循环(以 T11.1 Day 1 上午为示范)

### 上午 4 小时

```text
[0:00] 读 L3 §T11.1 Day 1 上午段(3 min)
[0:03] 读白皮书 §11.2 JSON 示例(5 min)
[0:08] 写 specs/rc-contract.schema.json 骨架(50 行,~30 min)
[0:38] python 跑通 JSON.parse 不报错(5 min)
[0:43] 加 6 顶层字段类型(40 min)
[1:23] git commit: "[V8 T11.1] feat: scaffold rc-contract schema (Draft 2020-12)"
[1:30] 上午剩余 2.5h 全部用来打磨上午段剩下的 todo 列表
```

### 下午 4 小时

```text
[0:00] 读 L3 §T11.1 Day 1 下午段(3 min)
[0:03] 读白皮书 §11.2 数字(guarantees 是字符串 pattern)(5 min)
[0:08] 写 7 个 guarantee 子字段 pattern(40 min)
[0:48] 跑 jsonschema validate 测试(10 min)
[1:00] git commit: "[V8 T11.1] feat: add 7 guarantee fields with pattern validation"
[1:05] 下午剩余 ~3h 写下午段其他 todo
```

**核心节奏**:读 L3 → 干 30-60 min → 跑测试 → commit → 继续

---

## 📝 commit 模板(强制统一)

```text
[V8 T{任务ID}] {type}: {scope}

{可选 body,50 字内}

{可选 footer,如 "Closes T11.1"}
```

**type 取值**:feat / fix / docs / test / refactor / chore(angular conventional 风格)

**scope 取值**:schema / compiler / probe / registry / validator / audit / dashboard / docs / cron

**示例**:
- `[V8 T11.1] feat: scaffold rc-contract schema (Draft 2020-12)`
- `[V8 T11.3] test: add 32 boundary cases for criterion compiler`
- `[V8 T14.2] probe: vuln #16 - A2A middle-state suspension`

---

## ✅ 单测门槛(硬性)

| 任务时长 | 最低单测数 | 最低通过率 |
|---|---|---|
| **0.5 天(半天)** | 4 用例 | 100% |
| **1 天** | 8 用例 | 100% |
| **2 天** | 14 用例 | 100% |
| **3 天** | 18 用例 | 100% |
| **5 天** | 30 用例 | 100% |

**🔴 任何任务完工前**:`python -m pytest path/to/test_xxx.py -v` 必须全绿才能 commit "feat: complete ..."

---

## 📋 留痕 4 处(每任务完工必做)

```text
1. MEMORY.md 顶部 +1 段("V8 T{xx.y} {任务名} 完工")
2. knowledge/log.md +1 段("implement | V8 T{xx.y} {任务名}")
3. knowledge/analysis/agent-os-t{xx-y}-completion-{YYYY-MM-DD}.md 新建完工报告
4. analysis/agent-os-v8-implementation-plan-l3-2026-07-13.md 任务段加"当前状态 ✅ 完工"
```

**留痕前自查**:
- [ ] 单测全绿
- [ ] commit 都已 push(如有 git 仓库)
- [ ] 完工报告含 DoD 自检 + 单测列表 + 风险与 limitations

---

## 🪤 5 个常见卡点 FAQ

### Q1:读 L3 时段找不到

**A**:用 `findstr /n "T11\|T12\|T13\|T14\|T15" analysis/agent-os-v8-implementation-plan-l3-2026-07-13.md` 定位

### Q2:白皮书 §11.2 行号漂移

**A**:**别信行号**,用 `findstr /n "^### " sources/agent-os-architecture-full-2026-07-11.md` 找 §11.2 的小节标题

### Q3:jsonschema Draft 2020-12 API 不熟

**A**:Python 官方文档 `python -c "import jsonschema; help(jsonschema.validate)"`,**不要**抄老博客(Draft 7 写法)

### Q4:某个 v8 §14 漏洞确实没法构造 exploit

**A**:标 `non_exploitable_evidence` + 提交理由 → 仍算 verified(白皮书 §14.3 允许)

### Q5:工时超出 L3 估算

**A**:
- 超 ≤ 30%:正常,继续
- 超 30-50%:写一段"超期原因"加完工报告里
- 超 > 50%:停下来 → 在完工报告里写"瓶颈分析" + 建议 L4 重排

---

## 🎯 5 阶段任务地图(L3 总览)

```
§11 RC 契约(11 天)──┐
                    ├─→ T11.4 RC 接入烟测
§11 5 个任务        │
                    └─→ T12.1(可并行启动)

§12 UTB 边界(11 天)─┐
                    ├─→ T12.4 违反检测器(cron)
§12 4 个任务        │
                    └─→ T15.1 KPI 数据源

§13 GaaS 自举(8 天)──┐
                    ├─→ T13.3 consortium 模拟(论文 #11)
§13 3 个任务        │
                    └─→ T15.1 KPI 数据源

§15 KPI + 硬规则(3 天)─┐
                      ├─→ 全部依赖收口
§15 2 个任务          │
                      └─→ T14.1 启动

§14 红队 Harness(20 天,最后)──┐
                            ├─→ T14.3 ELR 报告(论文 #6/#13/#17)
§14 4 个任务                │
                            └─→ T14.4 持续循环
```

---

## 🔧 复用工具栈速查

| skill | 复用点 | 路径参考 |
|---|---|---|
| **`paper-review-toolkit`** | schema validator / policy.yaml 模式 | `skills/paper-review-toolkit/SKILL.md` |
| **`wechat-mp-validation`** | cron + webhook 模式(T12.4/T14.4 抄 Layer 1 监控) | `skills/wechat-mp-validation/SKILL.md` |
| **`knowledge-wiki`** | 知识库索引 / log.md 留痕 4 处 | `skills/knowledge-wiki/SKILL.md` |
| **`experiment-tracker`** | git log → 完工报告(留痕第 3 处) | `skills/experiment-tracker/SKILL.md` |

---

## 🚦 接力节点精确握手

```
T11.1 → T11.2:  schema 终稿 (Draft 2020-12 + 24 用例 PASS)
T11.1 → T11.3:  schema 终稿(同上,T11.3 不依赖 T11.2 registry)
T11.1+T11.2+T11.3 → T11.4:  全部完工(mock A2A 才能跑)
T12.1 → T12.2:  D0-D5 分类 v2.0 + 5 collector + DP 工具(13 用例 PASS)
T12.1+T12.2 → T12.3:  reputation schema + validator(20 用例 PASS)
T12.x → T12.4:  所有前序完工(violation_detector 才能扫)
T13.1 → T13.2:  treasury 设计文档
T13.2 → T13.3:  governance_funding_mode 函数
T11-T13 → T15.1:  KPI 数据源全部就位
T14.x → T15.2:  hard rule violation 测试
T14.1 → T14.2:  harness 骨架
T14.2 → T14.3:  25 probe 全注册
T14.3 → T14.4:  ELR 报告生成
```

---

## ⚡ 一句话总结

```text
新 ML session:
  读本 README(5 min)
  + 读 L3 对应任务段(30 min)
  + 白皮书相应小节(30 min)
  → 上午干 4h + commit
  → 下午干 4h + commit
  → 留痕 4 处
  → 完工报告 + handoff 下一任务
```

**总用时**:**1 任务/天(半天任务)→ 1 任务/3 天(3 天任务)→ 1 任务/5 天(5 天任务)**

**整个 V8 实施**:15 任务,5 session 并行 10 周(承袭 L3 估算)

---

## ❓ 找不到答案时

```text
1. 读 L3 该任务段(承袭手册)
2. 读白皮书相应小节(原文依据)
3. 跑 findstr 在白皮书/L2 找具体内容
4. 如果还卡 → 在完工报告里写"问题 + 临时方案",不是卡死
5. 真正阻塞 → 找"泰"(另一个 session),泰能帮写交接包 / 索引同步 / 体检报告,不帮写代码
```

---

**README 完。下一个:写 T11.1 正式接力包(对应 L3 拆解的 6 个半天)。**
