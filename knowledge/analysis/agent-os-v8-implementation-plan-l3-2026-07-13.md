# Agent OS V8 详细实施计划 — L3 小时级可落地版

_2026-07-13 22:25 · 作者:泰 · 依据:[V8 白皮书 §11-15](./../sources/agent-os-architecture-full-2026-07-11.md) + [L2 计划(2026-07-13 21:25)](./agent-os-v8-implementation-plan-2026-07-13.md) + [V8 自检档(2026-07-11 19:49)](./agent-os-v8-review-2026-07-11.md)_

> **本文档定位**:L3 = L2 任务的"小时级"细化版。L2 给"做什么",L3 给"今天上午/下午做什么、产出哪个文件、留什么 commit"。
> **与 L2 关系**:**L2 是骨架,本文是肉**。两者不冲突,L3 不改 L2 工时/依赖/任务边界,只加颗粒度。
> **目标读者**:新开 ML session 拿到本计划 + 接力包 → 上午开始干,不需要再读 L2/白皮书/自检档三件套。
> **风格**:每任务有"上午/下午"两段、每个动作有"输出文件 + commit 模板 + 单测/验证步骤"。

---

## 🎯 总览(承袭 L2)

| 层 | 主题 | L2 工时 | L3 实际天 | 论文关联 |
|---|---|---|---|---|
| **§11 RC 契约** | 单体可靠性契约 + S→A Oracle | 2 周 | 11 天 | #6 / #9 |
| **§12 UTB 边界** | 信任-隐私效用边界 + VRP | 2 周 | 11 天 | #2 / #3 / #10 |
| **§13 GaaS 自举** | 治理自融资 + Consortium 激励 | 1.5 周 | 8 天 | #11 / #12 / #18 |
| **§15 KPI + 硬规则** | 5 KPI + 3 硬规则落地 | 0.5 周 | 3 天 | — |
| **§14 红队 Harness** | 25 漏洞红队实测 + ELR | 4 周 | 20 天 | #6 / #13 / #17 |
| **总计** | | 10 周 | **53 天 = 10.6 周** | 4 篇候选 |

**L3 增量价值**:
1. 每个任务**上午/下午**二分(防"3 天任务拖到 1 周")
2. **commit 模板**统一(`[V8 Txx.y] type: scope`)
3. **单测门槛**硬性化(每任务 ≤2 天必须带单测)
4. **风险兜底**显式化(每个任务有 fallback 路径)
5. **接力握手**精确化(谁接力谁接什么都有)

---

## 📦 第 1 阶段:§11 RC 契约(11 天 / 2 周)

---

### T11.1 RC 契约 schema 定义(3 天 → L3 拆 6 个半天)

**L2 原 DoD**:
- `specs/rc-contract.schema.json` 落地(Draft 2020-12)
- 12 个 guarantee + failure_taxonomy + oracle + evidence_required 全是 enum
- 单测覆盖每个 enum 至少 1 边界

**L3 拆解**:

#### Day 1 上午(4h) — 字段映射 + Draft 2020-12 骨架
- **必读**:`sources/agent-os-architecture-full-2026-07-11.md` §11.2(L1497-L1526 那个 JSON 示例)
- **动作**:
  - [ ] 把 §11.2 JSON 示例**逐字段**映射到 schema 字段
  - [ ] 写 `specs/rc-contract.schema.json` 骨架:`$schema: "https://json-schema.org/draft/2020-12/schema"` + `$id: "https://aidless.org/agent-os/rc-contract/v2026-07-11.rc1"`
  - [ ] 顶层 6 字段先列(`rc_version` / `agent_id` / `guarantees` / `failure_taxonomy` / `oracle` / `evidence_required`)
- **输出**:`specs/rc-contract.schema.json` 50 行
- **commit**:`[V8 T11.1] feat: scaffold rc-contract schema (Draft 2020-12)`
- **验证**:`python -c "import json; json.load(open('specs/rc-contract.schema.json'))"` 不报错

#### Day 1 下午(4h) — guarantees 7 字段 + pattern
- **白皮书 §11.2 数字**(guarantees 全是字符串,如 `">=0.95"` / `"<=1.5"` / `0.0` / `1.0`)
- **🪤 风险 1**(必看):guarantees 是**字符串 pattern**,**不是 number** —— 写 `pattern: "^(>=|<=|>|<|=)\s*\d+(\.\d+)?$"` 不要写 `"type": "number"`
- **动作**:
  - [ ] 7 个 guarantee 子字段全配 pattern + description
  - [ ] `spec_completeness` / `acceptance_coverage` / `first_pass_success`:`pattern: "^(>=|<=|>|<|=)\s*\d+(\.\d+)?$"` + 注释"必须是数值约束表达式"
  - [ ] `manual_intervention`:同上
  - [ ] `misoperation_rate` / `artifact_existence` / `log_coverage`:允许 `0.0` / `1.0` / 字符串 pattern —— **写 `"oneOf": [{"type": "number", "enum": [0.0, 1.0]}, {"type": "string", "pattern": "^(>=|<=|>|<|=)\s*1(\.0+)?$"}]`**
- **输出**:`specs/rc-contract.schema.json` 120 行
- **commit**:`[V8 T11.1] feat: add 7 guarantee fields with pattern validation`

#### Day 2 上午(4h) — failure_taxonomy 5 enum + oracle 3 字段
- **白皮书 §11.4 5 类**:`spec_gap` / `tool_fail` / `planner_loop` / `verifier_false_pass` / `context_loss`
- **🪤 风险 2**(必看):failure_taxonomy 必须**枚举白名单**,不要扩到其他字符串(避免后续 T11.4 hard rule 对不上)
- **🪤 风险 3**(必看):oracle 的 spec_gen / acceptance_gen / test_gen **不要 enum 锁死** —— 写 `"type": "string"` 即可,留给 T11.2/T11.3 自己定义
- **动作**:
  - [ ] `failure_taxonomy.items.enum` 5 个值 + 每个 description 引白皮书 §11.4 表
  - [ ] oracle 3 子字段 type: string(不锁 enum)
  - [ ] evidence_required: type: boolean
- **输出**:`specs/rc-contract.schema.json` 150 行(终稿)
- **commit**:`[V8 T11.1] feat: lock failure_taxonomy 5-class enum + open oracle strings`

#### Day 2 下午(4h) — examples + CLI
- **必读**:接力包 §DoD 3 那个 `haolo.main.json` 骨架
- **动作**:
  - [ ] 写 `specs/rc-examples/haolo.main.json`(对照白皮书 §11.2 那个示例,完全一致)
  - [ ] 写 `specs/rc-examples/bad-missing-field.json`(故意少 `evidence_required` 字段)
  - [ ] 写 `specs/validate_rc.py` 17 行 CLI:`jsonschema.validate(instance=json.load(open(p)), schema=schema)` + try/except
- **输出**:`specs/rc-examples/{haolo.main,bad-missing-field}.json` + `specs/validate_rc.py`
- **commit**:`[V8 T11.1] docs: add haolo.main + bad-missing-field examples + validate CLI`
- **验证**:`python specs/validate_rc.py specs/rc-examples/haolo.main.json` → "VALID" / `bad-missing-field.json` → "INVALID: 'evidence_required' is a required property"

#### Day 3 上午(4h) — 单测 24 用例
- **🪤 DoD 计数**(接力包修正过):5 enum × 2 + 7 pattern × 2 = **24 用例**(L2 写"12 个 enum"是笔误,以 5 + 7 = 24 为准)
- **动作**:
  - [ ] `pip install jsonschema pytest`
  - [ ] 写 `specs/test_rc_schema.py`:每个 enum 字段 1 valid + 1 invalid / 每个 pattern 字段 1 valid + 1 invalid
  - [ ] haolo.main.json 作为 integration test case(应 PASS)
  - [ ] bad-missing-field.json 作为 integration test case(应 FAIL)
- **输出**:`specs/test_rc_schema.py` ~120 行
- **commit**:`[V8 T11.1] test: add 24 boundary cases (5 enum × 2 + 7 pattern × 2)`
- **验证**:`python -m pytest specs/test_rc_schema.py -v` → 24 passed

#### Day 3 下午(4h) — 留痕 4 处
- **🪤 留痕 4 处**(接力包 §留痕约定):
  - [ ] **MEMORY.md** 顶部 +1 段"V8 T11.1 RC schema 完工"
  - [ ] **knowledge/log.md** +1 段"implement | V8 T11.1 RC 契约 schema 落地"
  - [ ] **knowledge/analysis/agent-os-t11-1-completion-2026-XX-XX.md** 新建完工报告(DoD 自检 + 24 用例列表 + V8 §11.2 字段对照表 + 已知 limitations)
  - [ ] **agent-os-v8-implementation-plan-2026-07-13.md** T11.1 段"工时: 3 天"后加一行"**当前状态**(YYYY-MM-DD): ✅ 完工"
- **commit**:`[V8 T11.1] docs: completion report + 4 places trace`

**L3 总产出**:
- `specs/rc-contract.schema.json` 150 行
- `specs/test_rc_schema.py` 120 行
- `specs/rc-examples/{haolo.main,bad-missing-field}.json` 各 13 行
- `specs/validate_rc.py` 17 行
- `analysis/agent-os-t11-1-completion-2026-XX-XX.md` ~80 行
- **commit 数**:6 个

**🪤 风险兜底**:
- **风险 A**:jsonschema Draft 2020-12 某些 IDE 不识别 → 改用 Draft 7 + 在 README 注明
- **风险 B**:24 用例 PASS 但 haolo.main.json 实际 FAIL → 加 1 个 `test_haolo_main_passes()` integration test
- **风险 C**:白皮书 §11.2 字段描述有歧义 → 标 `// TODO: confirm with 刘泽文 on field X`

---

### T11.2 RC 公共注册中心(2 天 → L3 拆 4 个半天)

**L2 原 DoD**:
- `GET /api/v1/agent/:id/rc` 端点
- `POST /api/v1/agent/:id/rc` 仅 admin
- 版本演进 v0.1 → v0.2 向后兼容

**L3 拆解**:

#### Day 4 上午(4h) — API spec + Mock
- **🪤 复用工具栈**:泰玄 Flask `app.py` blueprint 模式(可直接抄 fortune-web-v2/app.py 第 80-120 行)
- **动作**:
  - [ ] 写 `specs/rc-registry-api.md` OpenAPI 3.0 草案(GET / POST 两个端点)
  - [ ] 写 `mock/rc_registry_server.py` Flask app(GET/POST + SQLite 存历史版本)
  - [ ] `mock/data/rc/{haolo.main,v0.1,v0.2}.json` 三个测试数据
- **输出**:`specs/rc-registry-api.md` + `mock/rc_registry_server.py` ~80 行
- **commit**:`[V8 T11.2] feat: RC registry API spec + Flask mock`

#### Day 4 下午(4h) — admin 鉴权 + audit log
- **白皮书 §11.2 隐含约束**:POST 必须有签名 + audit log(避免 silent override)
- **动作**:
  - [ ] 加 `POST /api/v1/agent/:id/rc` admin 鉴权(简单 `X-Admin-Token` header 起步)
  - [ ] 加 `audit_log` 表(SQLite):`ts / actor / agent_id / rc_version_before / rc_version_after / action`
  - [ ] 单测:`tests/test_rc_registry.py` 8 用例(GET 200 / POST 401 无 token / POST 200 有 token / GET 拿历史 v0.1 / POST v0.2 不破坏 GET v0.1)
- **输出**:`mock/rc_registry_server.py` 160 行 + `tests/test_rc_registry.py` 100 行
- **commit**:`[V8 T11.2] feat: admin auth + audit log + 8 integration tests`
- **验证**:`python -m pytest tests/test_rc_registry.py -v` → 8 passed

#### Day 5 上午(4h) — 向后兼容 + 版本演进测试
- **白皮书 §11.2 隐含约束**:v0.1 → v0.2 必须保留 v0.1 可查(避免破坏 agent 升级)
- **动作**:
  - [ ] SQLite 表设计:`rc_current(agent_id, rc_json, version)` + `rc_history(agent_id, rc_json, version, archived_at)`
  - [ ] POST 时把旧版本移到 history,新版本入 current
  - [ ] GET 默认返回 current,可加 `?version=v0.1` 拿历史
  - [ ] 单测:`test_versioning.py` 4 用例(POST v0.1 → GET v0.1 / POST v0.2 → GET v0.2 / GET ?version=v0.1 → 仍返回 v0.1 / 不存在的 version → 404)
- **输出**:DB schema + 单测
- **commit**:`[V8 T11.2] feat: versioning with current/history split + 4 version tests`

#### Day 5 下午(4h) — 留痕 4 处 + 完工报告
- 同 T11.1 留痕 4 处模式

**L3 总产出**:`specs/rc-registry-api.md` 80 行 + `mock/rc_registry_server.py` 160 行 + `tests/test_rc_registry.py` 100 行

**🪤 风险兜底**:
- **风险 A**:SQLite 在高并发下锁表 → 改用 PostgreSQL(PROD 环境,本任务 mock 用 SQLite 即可)
- **风险 B**:admin token 用 plaintext → 改 JWT + bcrypt 存 hash

---

### T11.3 Spec→Acceptance Oracle 设计(5 天 → L3 拆 10 个半天,论文 #6 核心)

**L2 原 DoD**:
- `criterion_compiler.py` JSON → compiled_test
- 4 种 test type:`http_head` / `regex_match` / `json_schema_match` / `custom_js`
- 不可编译时拒绝 + 错误信息含"建议如何改写"

**L3 拆解**(更细,因为是论文 #6 核心数据源):

#### Day 6-7 上午(8h) — compiler 骨架 + http_head 类型
- **🪤 复用工具栈**:`jsonschema`(同 T11.1)+ Python `requests`(http_head)
- **动作**:
  - [ ] `tools/criterion_compiler.py` 入口函数 `compile_criterion(criterion: dict) -> CompiledTest`
  - [ ] 4 个 type dispatcher(`if type == "http_head" / elif ...`)
  - [ ] http_head 编译:把 `target: "$.output.image_url"` 用 `jsonpath-ng` 解析 → 实际 URL
  - [ ] 单测:`test_http_head.py` 6 用例(200 OK / 404 / timeout / redirect / invalid URL / missing target)
- **输出**:`tools/criterion_compiler.py` 100 行 + 单测
- **commit**:`[V8 T11.3] feat: compiler skeleton + http_head type (6 tests)`

#### Day 7 下午(4h) — regex_match 类型
- **动作**:regex_match 编译:`pattern: "https://example.com/.*"` → `re.match()`
- 单测 5 用例(valid match / no match / invalid regex / group capture / multiline)
- **commit**:`[V8 T11.3] feat: regex_match type (5 tests)`

#### Day 8 上午(4h) — json_schema_match 类型
- **🪤 复用工具栈**:同 T11.1 的 jsonschema(嵌套 schema)
- **动作**:json_schema_match 编译:`schema: {type: object, properties: {x: {type: number}}}` → 嵌套 jsonschema.validate
- 单测 5 用例(valid / missing field / type mismatch / nested / empty schema)
- **commit**:`[V8 T11.3] feat: json_schema_match type (5 tests)`

#### Day 8 下午(4h) — custom_js 类型
- **🪤 风险 4**(安全):custom_js 跑任意 JS,生产环境必须 sandboxed。本任务**起步用 Pyodide**(Python in-process JS eval)+ 后续切 V8 isolate
- **动作**:custom_js 编译:`code: "output.score > 0.8"` → 在 Pyodide sandbox 跑 + 捕获 stdout
- 单测 4 用例(true / false / runtime error / syntax error / infinite loop timeout)
- **commit**:`[V8 T11.3] feat: custom_js type with Pyodide sandbox (4 tests)`

#### Day 9-10 上午(8h) — 拒绝机制 + 错误信息友好化
- **白皮书 §11.3 硬约束**:不可编译的 criterion 在任务创建时拒绝,错误信息含"建议如何改写"
- **动作**:
  - [ ] `compile_criterion()` 失败抛 `UncompilableCriterionError(reason, suggestion)`
  - [ ] suggestion 引擎:把 6 类常见错误映射到 6 类建议(e.g.,"target 字段必须以 `$.` 开头,你的 `output.url` 应该改成 `$.output.url`")
  - [ ] 6 类错误:
    1. `target` 不以 `$.` 开头 → 建议加 `$.`
    2. `pattern` 不是合法 regex → 建议用 regex101 验证
    3. `schema` 不是合法 JSON Schema → 建议用 jsonschema 验证
    4. `code` 语法错 → 建议在 Pyodide REPL 跑一下
    5. `timeout` 不在 [1s, 60s] → 建议改范围
    6. `expected_status` 不是合法 HTTP 码 → 建议查 MDN
- 单测:`test_rejection.py` 12 用例(每类 2 个)
- **commit**:`[V8 T11.3] feat: friendly rejection with 6-class suggestion engine (12 tests)`

#### Day 10 下午(4h) — 集成测试 + 完工报告
- 单测总数:6+5+5+4+12 = **32 用例**(≥L2 要求 20)
- 集成测试:`test_integration.py` 5 用例(白皮书 §11.3 那个 image_url 例子 + 4 个边界)
- 完工报告 `analysis/agent-os-t11-3-completion-YYYY-MM-DD.md`:DoD 自检 + 32 用例列表 + 6 类错误→建议对照表 + 论文 #6 数据收集预演
- 留痕 4 处

**L3 总产出**:`tools/criterion_compiler.py` ~350 行 + 单测 32 用例 + 集成测试 5 + 完工报告

**🪤 风险兜底**:
- **风险 A**:Pyodide 启动慢(冷启动 500ms)→ 改用 Node.js 子进程(PROD)
- **风险 B**:custom_js 跑死循环 → 加 `signal.alarm(5s)` timeout(本任务 MVP)
- **风险 C**:jsonpath-ng 解析复杂路径失败 → 切 jsonpath2

---

### T11.4 RC 接入烟测(1 天 → L3 拆 2 个半天)

**L2 原 DoD**:haolo.main 接 A2A 模拟器,无 RC reject,有 RC allow + 3 acceptance test

**L3 拆解**:

#### Day 11 上午(4h) — A2A 模拟器接入点
- **🪤 复用**:V7 §6.1 Agent Card + §6.2 Task 格式(已在白皮书 §6 有完整 spec)
- **动作**:
  - [ ] `tests/integration/rc_smoke_test.py` 框架
  - [ ] 写 mock A2A 接收器:`mock/a2a_receiver.py` 80 行
  - [ ] 拒绝逻辑:`if not rc_published: return 403 "no RC"`
- **输出**:`mock/a2a_receiver.py` + `tests/integration/rc_smoke_test.py`
- **commit**:`[V8 T11.4] feat: A2A mock receiver with RC enforcement`

#### Day 11 下午(4h) — 3 acceptance test + 留痕
- **3 acceptance test**(对照白皮书 §11.3 image_url 例子):
  1. `test_image_url_accessible`:haolo.main RC 含 oracle.spec_gen,产出图片 URL 必须 http_head 200
  2. `test_first_pass_success_rate`:haolo.main RC 含 first_pass_success >=0.55,实测命中率 ≥55%
  3. `test_no_rc_rejected`:无 RC 的 mock agent 接入 → 403 + audit log 记录
- **commit**:`[V8 T11.4] test: 3 acceptance tests + audit log verification`
- **验证**:`python -m pytest tests/integration/rc_smoke_test.py -v` → 3 passed
- 留痕 4 处

**L3 总产出**:3 用例 + mock 80 行 + audit log 验证

**🪤 风险兜底**:
- **风险 A**:A2A 模拟器对真实 haolo.main agent 依赖重 → 改用 mock agent(本任务允许)
- **风险 B**:first_pass_success 命中率实测样本不足 → 改用历史调用日志回放

---

## 📦 第 2 阶段:§12 UTB 边界(11 天 / 2 周)

---

### T12.1 D1-D5 分级数据采集协议(3 天 → L3 拆 6 个半天)

**L2 原 DoD**:5 个 collector + D3/D4 默认不出本地 + D1/D2 dp(ε=1.0, δ=1e-6)管线

**L3 拆解**:

#### Day 12 上午(4h) — D0-D5 分级标准文档
- **必读**:白皮书 §5.1(L276-L283 已有 D0-D5 分级定义)
- **🪤 复用工具栈**:`paper-review-toolkit` 已经有 `specs/policy.yaml`(泰玄 v2.2 模式),可直接对照写 V8 specs
- **动作**:
  - [ ] `specs/data-classification.md` v2.0(基于 V7 §5.1,**只补 V8 增量**:D3/D4 hash-only 导出选项 + D1/D2 DP 聚合管线)
  - [ ] 表格 6 行(D0-D5):类别 / 示例 / 是否出本地 / 导出选项 / 监管要求
  - [ ] commit:`[V8 T12.1] docs: D0-D5 classification v2.0 (V8 incremental)`
- **输出**:`specs/data-classification.md` 80 行

#### Day 12 下午(4h) — 5 个 collector stub
- **动作**:
  - [ ] `tools/collectors/d{1,2,3,4,5}_collector.py` 各 30 行
  - [ ] D1: 调用日志 → JSON Lines 写本地
  - [ ] D2: 工具统计 → JSON Lines 写本地
  - [ ] D3: 用户内容 → 默认本地,**只有 `--hash-export` 选项才导出 SHA256**
  - [ ] D4: 源码 → 同 D3
  - [ ] D5: 跨平台 → 聚合上报,无 hash-only 限制
- **输出**:`tools/collectors/` 5 文件 × 30 行
- **commit**:`[V8 T12.1] feat: 5 collector stubs with hash-only D3/D4 enforcement`

#### Day 13 上午(4h) — DP 聚合管线
- **白皮书 §5.3(L284-L300)**+ **§12.2** 给出 ε=1.0, δ=1e-6
- **🪤 复用工具栈**:`opacus`(PyTorch DP 库)或 `diffprivlib`(IBM DP 库,纯统计函数友好)
- **动作**:
  - [ ] `tools/dp_aggregator.py`:`aggregate_with_dp(data: pd.DataFrame, epsilon=1.0, delta=1e-6) -> DPAggregate`
  - [ ] 支持 mean / sum / histogram 3 种聚合函数
  - [ ] 单测:`test_dp_aggregator.py` 6 用例(epsilon=0.1 噪声大 / epsilon=5.0 噪声小 / delta 边界 / mean of [1,2,3] / sum of [1,2,3] / histogram 10 bins)
- **输出**:`tools/dp_aggregator.py` 120 行 + 单测 6
- **commit**:`[V8 T12.1] feat: DP aggregator with ε=1.0, δ=1e-6 (6 tests)`

#### Day 13 下午(4h) — D3/D4 hash-only 强制测试
- **白皮书 §12.3 隐含硬规则**:任何导出 D3/D4 明文的请求必须被拒
- **动作**:
  - [ ] 单测:`test_d3_d4_hash_only.py` 4 用例
    1. `d3_collector.collect(export_mode="plain")` → 抛 `D3ExportForbiddenError`
    2. `d3_collector.collect(export_mode="hash")` → 成功 + 返回 SHA256
    3. 同上 D4
    4. `d3_collector.collect(export_mode="plain", force=True)` → 需要 admin token(防绕过)
- **输出**:单测 4 用例
- **commit**:`[V8 T12.1] test: D3/D4 hash-only enforcement (4 tests)`

#### Day 14 上午(4h) — 端到端集成测试
- **动作**:跑完整流程 D1+D2 → dp_aggregator → 写 audit log
- 单测:`test_e2e_pipeline.py` 3 用例
- **commit**:`[V8 T12.1] test: e2e D1+D2 → DP → audit (3 tests)`

#### Day 14 下午(4h) — 留痕 4 处 + 完工报告

**L3 总产出**:文档 80 行 + 5 collector 150 行 + DP 工具 120 行 + 单测 13 用例

---

### T12.2 可验证声誉协议 VRP(3 天 → L3 拆 6 个半天)

**L2 原 DoD**:reputation.json schema + computed_from 白名单 + 含 D3/D4 reject

**L3 拆解**(对照白皮书 §12.3 那个 JSON 示例):

#### Day 15 上午(4h) — reputation schema
- **必读**:白皮书 §12.3(L1601-L1620 JSON 示例)
- **🪤 复用 T11.1 经验**:同样 Draft 2020-12 + enum 锁 computed_from 白名单
- **动作**:
  - [ ] `specs/reputation.schema.json`:顶层 `agent_id` / `trust_level`(enum T0-T5)/ `reputation_score`(0.0-5.0)/ `computed_from`(嵌套)/ `privacy_proof` / `not_computed_from`(array)
  - [ ] computed_from 子:`d1_d2_aggregates`(字符串 pattern)/ `behavioral_profile_hash`(sha256:hex pattern)/ `cross_agent_rank`(枚举)
  - [ ] computed_from 白名单:`enum: ["d1_d2_aggregates", "behavioral_profile_hash", "cross_agent_rank"]`
  - [ ] 单测:`test_reputation_schema.py` 12 用例(每个字段 1v + 1i + 3 computed_from 白名单 case)
- **输出**:`specs/reputation.schema.json` 100 行 + 单测 12
- **commit**:`[V8 T12.2] feat: reputation schema with computed_from whitelist (12 tests)`

#### Day 15 下午(4h) — validator 工具
- **白皮书 §12.3 硬规则**:任何 computed_from 含 D3/D4 → reject + 告警
- **动作**:
  - [ ] `tools/reputation_validator.py`:`validate(reputation: dict) -> ValidationResult`
  - [ ] 检查 computed_from 所有 key 都在白名单 → 否则 reject + reason
  - [ ] 检查 not_computed_from 必含 "user_content" / "source_code" / "private_memory" → 否则 warn
  - [ ] 单测:`test_validator.py` 8 用例
- **输出**:`tools/reputation_validator.py` 80 行 + 单测 8
- **commit**:`[V8 T12.2] feat: validator + D3/D4 detection (8 tests)`

#### Day 16 上午(4h) — 拒绝触发降级流程
- **白皮书 §15.3 硬规则**:声誉违规 → 信任等级降级(对应 V7 #10 双轨泄漏)
- **动作**:
  - [ ] `tools/trust_degrader.py`:violation 类型 → 新 trust_level
  - [ ] 单测:5 用例(T3 + D3 in computed → T1 / T3 + source_code in not_computed → T2 / ...)
  - [ ] commit:`[V8 T12.2] feat: trust degrader + 5 test cases`

#### Day 16 下午 + Day 17 — 集成 + 留痕

**L3 总产出**:schema 100 行 + validator 80 行 + degrader 50 行 + 单测 25 用例

---

### T12.3 信任-隐私 Pareto 前沿实测(4 天 → L3 拆 8 个半天,**论文 #2 核心**)

**L2 原 DoD**:6 agent × 5 ε 档(0.1/0.5/1.0/2.0/5.0)+ 画曲线 + 验证"ε<1.0 饱和"假设

**L3 拆解**:

#### Day 18 上午(4h) — 6 个 agent 选定
- **白皮书 §12.2**:x 轴 ε, y 轴 AUC(声誉预测真实任务成功的判别力)
- **6 agent 建议**(覆盖 3 个 model family,留 L2 提的):
  1. `qwen3-7b`(小模型 baseline)
  2. `qwen3-72b`(同 family 大模型)
  3. `deepseek-v3`(另一 family)
  4. `claude-sonnet-3.5`(西方 model)
  5. `gpt-4o`(西方 model)
  6. `gemini-2.0-pro`(西方 model)
- **任务集**:白皮书 §6.5 sandbox 试任务的子集 100 个任务
- **输出**:`experiments/utb-pareto/agents.json` 选定记录
- **commit**:`[V8 T12.3] setup: 6 agents + 100 task set selection`

#### Day 18 下午(4h) — 实验脚手架
- **动作**:
  - [ ] `experiments/utb-pareto/run_pareto.py`:`run(agent_id, epsilon) -> {"auc": float, "n": int}`
  - [ ] 用 sklearn `roc_auc_score` 算 AUC
  - [ ] 单测:`test_run_pareto.py` 3 用例(mock 数据,验证 AUC 计算正确性)
- **输出**:`run_pareto.py` 120 行 + 单测 3
- **commit**:`[V8 T12.3] feat: experiment scaffold with AUC calc (3 tests)`

#### Day 19-20(2 天 = 16h) — 跑 30 个组合(6 agent × 5 ε)
- **🪤 兜底**:每个组合预计 1-2h,如果跑不动 → 降样本(100 → 30 任务)
- **🪤 兜底 2**:某些 agent API rate limit → 加 retry + backoff
- **动作**:
  - [ ] 跑完 30 组合,每个组合写一行 `experiments/utb-pareto/results/{agent}_{epsilon}.json`
  - [ ] `experiments/utb-pareto/aggregate.py` 汇总成 `all_results.csv`(30 行 × 6 列)
  - [ ] 验收标准:30 个结果文件全有,无 NaN
- **commit**:每 10 个组合一个 commit

#### Day 21 上午(4h) — 画图
- **动作**:`experiments/utb-pareto/plot.py` 用 matplotlib 画 6 条曲线(每个 agent 一条),x=ε, y=AUC
- **输出**:`experiments/utb-pareto/utb-pareto-2026-XX-XX.pdf`
- **commit**:`[V8 T12.3] docs: pareto plot (6 curves)`

#### Day 21 下午(4h) — 解读 + 假设验证
- **白皮书 §12.2 核心假设**:ε < 1.0 饱和
- **动作**:
  - [ ] `experiments/utb-pareto/interpretation.md`(≤300 字):
    - 验证假设是否成立(每个 agent 单独判断)
    - 如果不成立 → 解释为什么(可能是模型 family 太小)
    - 如果成立 → 引用具体数字(e.g.,"qwen3-7b 在 ε=0.5 AUC=0.71, ε=1.0 AUC=0.73,差 0.02 → 饱和")
  - [ ] 失败 fallback:假设不成立也是 paper 数据(L2 风险表已列)
- **commit**:`[V8 T12.3] docs: interpretation (≤300 words)`

#### Day 22 上午(4h) — 论文 #2 数据整合
- **动作**:把 all_results.csv + plot + interpretation 整合成 paper #2 可用格式
- **输出**:`paper02-trust-elastic/data/{pareto.csv, pareto.pdf, interpretation.md}`
- **commit**:`[V8 T12.3] handoff: paper #2 data bundle ready`

#### Day 22 下午(4h) — 留痕 + 完工报告

**L3 总产出**:30 个 JSON + 1 CSV + 1 PDF + interpretation + paper #2 data bundle

**🪤 风险兜底**:
- **风险 A**:API rate limit 把 30 个组合拖到 2 周 → 降样本到 30 任务
- **风险 B**:假设不成立 → paper 数据"负结果"也是结果
- **风险 C**:matplotlib 中文乱码 → 用英文标签 + 引用白皮书原话

---

### T12.4 违反检测器(3 天 → L3 拆 6 个半天)

**L2 原 DoD**:cron 每小时扫 + D3/D4 命中降级 + 写 audit log + 发 webhook

**L3 拆解**(对照 T12.2 的 validator):

#### Day 23-24 上午(8h) — 检测器核心
- **🪤 复用泰玄 ECS Layer 1 healthcheck.sh 模式**(已有 cron job + webhook)
- **动作**:
  - [ ] `tools/violation_detector.py`:`scan_all_reputations() -> List[Violation]`
  - [ ] 用 T12.2 validator 扫描所有 reputation.json
  - [ ] 命中 D3/D4 → 触发 degrader + 写 audit log + POST webhook
  - [ ] 单测:`test_detector.py` 6 用例(scan 0 violations / scan 1 violation → degrade / scan multiple / webhook fired / audit log written / idempotent)
- **输出**:`tools/violation_detector.py` 150 行 + 单测 6
- **commit**:`[V8 T12.4] feat: violation detector with audit + webhook (6 tests)`

#### Day 24 下午(4h) — cron 配置
- **动作**:`cron/v8-violation-detector.sh` 每小时跑 + 日志输出
- **commit**:`[V8 T12.4] setup: cron hourly scan script`

#### Day 25 上午(4h) — webhook + 告警渠道
- **🪤 复用泰玄**:v1.2.1 Layer 1 监控已用 webhook 到微信,本任务可直接抄
- **动作**:webhook URL 可配置(环境变量 `WEBHOOK_URL`)
- 单测:`test_webhook.py` 3 用例(200 OK / 500 retry / 网络 timeout)

#### Day 25 下午 + Day 26 — 集成测试 + 留痕

**L3 总产出**:detector 150 行 + cron 30 行 + 单测 9 + webhook 集成

---

## 📦 第 3 阶段:§13 GaaS 自举(8 天 / 1.5 周)

---

### T13.1 Treasury 独立账户设计(2 天 → L3 拆 4 个半天)

**L2 原 DoD**:物理隔离 + 双 key + balance_audit 公开

**L3 拆解**:

#### Day 27 上午(4h) — Treasury 设计文档
- **白皮书 §13.1-13.2** 已有微税 0.5% + 独立托管
- **动作**:
  - [ ] `specs/treasury-design.md`:账户结构图(平台账户 vs treasury 账户)+ 双 key 流程图 + balance_audit API 草案
  - [ ] commit:`[V8 T13.1] docs: treasury design (physical isolation + dual-key)`
- **输出**:文档 120 行

#### Day 27 下午 + Day 28 — mock 合约 + balance_audit API
- **动作**:
  - [ ] `mock/treasury_contract.py` 模拟合约:双 key + 交叉签名
  - [ ] `mock/balance_audit_api.py`:GET /api/v1/treasury/balance + 历史
  - [ ] 单测:`test_treasury.py` 8 用例
- **commit**:`[V8 T13.1] feat: mock treasury + balance_audit API (8 tests)`

#### Day 29 上午(4h) — 物理隔离测试
- **🪤 硬规则**:平台账户**绝对不能**调用 treasury 转账
- **动作**:单测 `test_physical_isolation.py` 4 用例(平台 key → treasury 转账拒绝 / treasury key → 平台转账拒绝 / 双 key 交叉签名 → 通过 / 单 key → 拒绝)
- **commit**:`[V8 T13.1] test: physical isolation (4 tests)`

#### Day 29 下午 — 留痕 + 完工

**L3 总产出**:设计文档 120 行 + mock 80 行 + API 50 行 + 单测 12 用例

---

### T13.2 GaaS 收费曲线实施(3 天 → L3 拆 6 个半天)

**L2 原 DoD**:treasury_collector 提 0.5% + governance_funding_mode 函数 + 单测 + 双达标切换

**L3 拆解**(对照白皮书 §13.4 Python 函数):

#### Day 30 上午(4h) — collector
- **白皮书 §13.2**:每笔 escrow 提 0.5% 进 treasury
- **动作**:
  - [ ] `tools/treasury_collector.py`:`on_escrow(amount: float) -> {"treasury_deposit": float, "platform_revenue": float}`
  - [ ] 单测:`test_collector.py` 5 用例(amount=100 → treasury 0.5 / amount=0 → 0 / amount=1e6 → 5000 / 边界值 / 浮点精度)
- **commit**:`[V8 T13.2] feat: 0.5% treasury collector (5 tests)`

#### Day 30 下午(4h) — governance_funding_mode 函数
- **白皮书 §13.4** Python 代码直接对照
- **动作**:
  - [ ] `tools/governance_funding_mode.py`:`governance_funding_mode(total_tx, treasury, runway_months=12, monthly_burn) -> "fee_based" | "levy_subsidized"`
  - [ ] 单测:`test_funding_mode.py` 6 用例
    1. total_tx < 1M → levy_subsidized
    2. total_tx >= 1M AND treasury >= 12mo → fee_based
    3. total_tx >= 1M AND treasury < 12mo → levy_subsidized(双达标硬规则)
    4. treasury 恰好 12mo → 边界 fee_based
    5. total_tx 恰好 1M → 边界 fee_based
    6. monthly_burn=0 → 防除零
- **commit**:`[V8 T13.2] feat: governance_funding_mode function (6 tests)`

#### Day 31 上午(4h) — 双达标硬规则强化测试
- **🪤 关键**:即使 total_tx 已达标,如果 treasury 不够 12 月,**必须维持微税**
- **动作**:单测 `test_dual_threshold.py` 4 用例(各种双达标边界组合)
- **commit**:`[V8 T13.2] test: dual-threshold enforcement (4 tests)`

#### Day 31 下午 + Day 32 — 集成 + 单测 19 总数 + 留痕

**L3 总产出**:collector 80 行 + funding_mode 30 行 + 单测 19

---

### T13.3 Consortium 激励机制(4 天 → L3 拆 8 个半天,**论文 #11 核心**)

**L2 原 DoD**:会员费公式 + 红队发现积分公式 + 30 天模拟

**L3 拆解**:

#### Day 33 上午(4h) — 定价公式
- **白皮书 §13.3**:会员费 = f(L0-L5 等级, 审计池资格)
- **动作**:
  - [ ] `experiments/consortium-sim/model.py`:函数 `membership_fee(level: int, audit_pool_member: bool) -> float`
  - [ ] 公式:L0=100 / L1=500 / L2=2000 / L3=10000 / L4=50000 / L5=200000(USD/year)
  - [ ] audit_pool_member 加 20% 折扣
  - [ ] 单测:`test_pricing.py` 8 用例(各等级 + audit_pool 折扣)
- **commit**:`[V8 T13.3] feat: membership fee formula (8 tests)`

#### Day 33 下午(4h) — 红队发现积分公式
- **白皮书 §13.3**:积分 = f(severity × ELR)
- **动作**:
  - [ ] 函数 `red_team_score(severity: int, elr: float) -> float`
  - [ ] 公式:score = severity × elr × 100
  - [ ] 单测:`test_scoring.py` 6 用例
- **commit**:`[V8 T13.3] feat: red team score formula (6 tests)`

#### Day 34-35(2 天 = 16h) — 30 天模拟
- **🪤 复用工具栈**:`mesa`(Python agent-based modeling 库)
- **动作**:
  - [ ] `experiments/consortium-sim/sim.py`:`run_simulation(days=30, n_agents=50) -> results.json`
  - [ ] 每个 agent:trust_level / 是否 audit_pool_member / 提交红队发现的概率
  - [ ] 输出 30 天的累积积分 + 个体理性 vs 系统理性指标
- **commit**:`[V8 T13.3] feat: 30-day consortium simulation`

#### Day 36 上午(4h) — 结果分析
- **🪤 兜底**(L2 风险表):如果模拟失败 → 改 Stackelberg 博弈
- **动作**:`experiments/consortium-sim/analysis.md`(≤400 字)+ 图
- **commit**:`[V8 T13.3] docs: simulation analysis`

#### Day 36 下午 + Day 37 — 论文 #11 数据整合 + 留痕

**L3 总产出**:model.py 150 行 + sim.py 200 行 + 单测 14 + 30 天 JSON + paper #11 data bundle

**🪤 风险兜底**:
- **风险 A**:模拟显示 individual ≠ system rational → 切 Stackelberg
- **风险 B**:mesa 学习曲线 → 改简单循环 + dict state

---

## 📦 第 4 阶段:§15 KPI + 硬规则(3 天,横向基础)

---

### T15.1 5 个 KPI 仪表盘(2 天 → L3 拆 4 个半天)

**L2 原 DoD**:5 panel + 每周快照

**L3 拆解**:

#### Day 38 上午(4h) — 5 个 panel 实现
- **白皮书 §15.1 表格**:5 个 KPI 目标值
  - RC 覆盖率 = 100%
  - S→A Oracle 覆盖率 ≥ 85%
  - 信任信号 AUC ≥ 0.75
  - 治理资金独立托管率 = 100%
  - 25 漏洞 ELR 均值 ≥ 0.7
- **🪤 工具栈选择**:
  - **A**:Grafana(JSON 配置导入,运维友好)
  - **B**:自写 HTML + Chart.js(灵活,无依赖)
  - **推荐 B**(本任务数据量小,Grafana 重)
- **动作**:
  - [ ] `dashboards/v8-kpi.html`:5 个 stat card + 1 个 line chart + 1 个 bar chart
  - [ ] `dashboards/v8-kpi.json`:5 KPI 的当前值 + 历史值
  - [ ] 数据源:从 T11.2 / T11.3 / T12.3 / T13.1 / T14.3 输出读
- **输出**:`dashboards/v8-kpi.{html,json}`
- **commit**:`[V8 T15.1] feat: 5-panel KPI dashboard (HTML + JSON)`

#### Day 38 下午(4h) — 每周快照脚本
- **动作**:`tools/snapshot_kpi.py`:`snapshot() -> weekly_kpi_YYYY-MM-DD.json`
- 单测:`test_snapshot.py` 3 用例

#### Day 39 上午(4h) — 集成测试
- 跑 5 KPI 真实取值 + 渲染 HTML → 看视觉效果
- 单测 `test_dashboard_render.py` 4 用例

#### Day 39 下午 — 留痕

**L3 总产出**:HTML 200 行 + JSON 50 行 + snapshot 脚本 50 行 + 单测 7

---

### T15.2 V8 硬规则 3 条落地(1.5 天 → L3 拆 3 个半天)

**L2 原 DoD**:3 条规则各有 1 个 violation 测试

**L3 拆解**:

#### Day 40 上午 + 下午(8h) — 3 规则 violation 测试
- **白皮书 §15.3 三条硬规则**:
  1. 能力根必须持证(T11.4 reject 路径已实现,这里加集成测试)
  2. 声誉只可比较(T12.4 violation_detector 已实现,这里加集成测试)
  3. 缓解分两档(T14 harness 的 `verified` / `designed` 标注)
- **动作**:
  - [ ] `tests/hard_rules/test_v8_rules.py`:
    - test_rule1_no_rc_rejected:无 RC agent → 403 + audit
    - test_rule2_d3_in_computed_degrade:reputation 含 D3 → trust_level 降级
    - test_rule3_relief_labeling:relief must be "verified" or "designed", 不可混用
- 单测 3 用例 + 各加 1 个边界 = 6 用例
- **commit**:`[V8 T15.2] test: 3 hard rules violation enforcement (6 tests)`

#### Day 41 上午(4h) — 留痕

**L3 总产出**:3 规则 violation 测试 6 用例

---

## 📦 第 5 阶段:§14 Adversarial Eval Harness(20 天 / 4 周,最后做)

---

### T14.1 harness 核心循环(5 天 → L3 拆 10 个半天)

**L2 原 DoD**:deploy → probe → measure ELR → (ELR<0.5 ? redesign : ship)循环 + ELR table 输出

**L3 拆解**:

#### Day 42-43(2 天 = 16h) — harness 骨架
- **白皮书 §14.2** deploy → probe → measure ELR 流程图
- **动作**:
  - [ ] `tools/red_team_harness.py`:`run_harness(vuln_id: int) -> ELRResult`
  - [ ] 核心循环:`for vuln_id in range(1, 26): deploy(vuln_id); probe(vuln_id); measure_elr(vuln_id)`
  - [ ] 单测:`test_harness.py` 4 用例(single vuln / 25 vulns 跑完 / 异常 probe 不中断 / 输出 ELR table 格式)
- **commit**:`[V8 T14.1] feat: harness skeleton + 25-vuln loop (4 tests)`

#### Day 44 上午(4h) — probe 注册机制
- **动作**:
  - [ ] `tools/red_team_probes/__init__.py`:自动发现 `red_team_probes/{1..25}.py` 模块
  - [ ] 每个 probe 必须实现 `probe(target_agent) -> ExploitResult`
- 单测:`test_probe_registry.py` 4 用例

#### Day 44 下午 + Day 45-46(2.5 天) — ELR 量化 + 报告
- **白皮书 §14.3** ELR 公式:`(P_pre × Impact_pre) − (P_post × Impact_post)`
- **动作**:
  - [ ] `tools/elr_calculator.py`:`calc(p_pre, impact_pre, p_post, impact_post) -> float`
  - [ ] 单测:`test_elr.py` 6 用例
  - [ ] `tools/elr_table_writer.py`:`write_table(results: List[ELRResult]) -> elr_results.json`
  - [ ] 单测:`test_elr_writer.py` 4 用例

#### Day 47 上午(4h) — 集成测试 + 留痕

**L3 总产出**:harness 200 行 + probe registry 50 行 + ELR calc 80 行 + 单测 18

---

### T14.2 25 漏洞红队 probe 注册(10 天 → L3 拆 20 个半天,**最重任务**)

**L2 原 DoD**:25 个 probe,每个独立

**L3 拆解**:**这是 V8 实施最重的任务,建议拆给 5-10 个 ML session 并行**(L2 已建议)。

#### 漏洞分组(按 V7 自检档 §10.1-10.3):

| 漏洞 ID | 严重度 | 描述 | 建议分给 |
|---|---|---|---|
| **#1, #2, #4, #7, #8** | 🔴 P0 Critical | PDP Boring Middle / Kill Switch 滥用 / Jurisdiction 无解 / LLM 幻觉传染 / 冷启动死局 | Session A |
| **#15, #20, #16, #17, #18** | 🔴 P0 + 🟡 P1 | Control Plane 失效 / 跨法域冲突 / A2A 中间态 / PDP Cache 毒化 / DP 组合失效 | Session B |
| **#3, #5, #6, #9, #10** | 🟡 P1 High | Sandbox 反作弊 / Trust 跳水 / 5 类演化偏见 / Policy 交集无声拒绝 / 双轨泄漏 | Session C |
| **#11, #12, #13, #22** | 🟡 P1 High | 多源投票作弊 / 价格操纵 / 审计员疲劳 / Hybrid 工作量博弈 | Session D |
| **#14, #19, #21, #23, #24, #25** | 🟢 P2 Medium | 透明度披露悖论 / 5 类演化反馈放大 / Protocol Baseline 僵化 / 透明度游戏化 / 5 层认证等级跳跃 / Audit Trail 膨胀 | Session E |

**每个漏洞 1 个 probe**:
- 模板:`tools/red_team_probes/{id}.py` 30-50 行
  - `probe(target_agent) -> ExploitResult {success: bool, evidence: str}`
  - 失败兜底:L2 风险表说"非 exploitable 标 `non_exploitable_evidence`"
- 每个 probe **必须带 1 个单测**:`test_probes/test_{id}.py` 5 用例
- commit 模板:`[V8 T14.2] probe: vuln #{id} - <name>`

#### Day 48-57(10 天) — 5 个 session 并行写 25 probe
- **🪤 协调机制**:每个 session 完工后 push PR,主协调 session 合并
- **🪤 兜底**:某些漏洞确实不可构造 exploit → 标 `non_exploitable_evidence` + 仍算 verified

#### Day 58 上午(4h) — 25 probe 全注册验证
- 单测:`test_all_probes_registered.py` 1 用例(必须 25 个都注册了)
- **commit**:`[V8 T14.2] feat: 25 red team probes registered + tested`

#### Day 58 下午 — 留痕

**L3 总产出**:25 probe 文件 + 25 单测文件 + 1 个总验证

**🪤 风险兜底**:
- **风险 A**:某些漏洞无法构造 exploit(本就设计态)→ 标 `non_exploitable_evidence` + 提交理由
- **风险 B**:5 session 并行冲突 → 用 git branch per session + PR review
- **风险 C**:某些 probe 需要真实 Agent target → 用 mock target(本任务允许)

---

### T14.3 ELR 报告 + 透明度文档生成(3 天 → L3 拆 6 个半天,**论文 #6/#13/#17 核心**)

**L2 原 DoD**:elr-table.md 25 行 + verified-vs-designed.json + ROAI ≥ 0.7

**L3 拆解**:

#### Day 59 上午(4h) — elr_report.py
- **白皮书 §14.3** 报告示例表(漏洞 / P_pre / Impact / P_post / ELR / 状态)
- **动作**:
  - [ ] `tools/elr_report.py`:`generate_report(results: List[ELRResult]) -> elr-table.md`
  - [ ] 输出格式:Markdown 表 + verified/designed 标记
- 单测:`test_elr_report.py` 4 用例

#### Day 59 下午(4h) — verified-vs-designed.json
- **白皮书 §15.3 硬规则**:只有 ELR ≥ 0.5 才标 verified
- **动作**:
  - [ ] `tools/verified_designed.py`:`classify(results) -> {"verified": [...], "designed": [...]}`
  - [ ] 单测:`test_verified_designed.py` 4 用例(ELR=0.5 边界 / ELR=0.4 → designed / ELR=0.6 → verified / 混合)
- **commit**:`[V8 T14.3] feat: ELR report + verified/designed classifier (8 tests)`

#### Day 60-61(2 天) — 25 漏洞 ELR 实测 + 报告生成
- **动作**:跑完整 harness(T14.1)+ 25 probe(T14.2)→ 输出 `reports/v8-elr-2026-XX-XX.md`
- 单测:`test_full_run.py` 2 用例(全 25 跑通 / 部分失败时优雅降级)

#### Day 62 上午(4h) — 论文数据整合
- **🪤 复用 T12.3 模式**:`paper06-benchmark-to-real/data/{elr-table.md, verified-vs-designed.json}`
- **commit**:`[V8 T14.3] handoff: paper #6/#13/#17 data bundle`

#### Day 62 下午 — 留痕

**L3 总产出**:elr_report.py 100 行 + verified_designed.py 50 行 + 1 个 markdown 报告 + paper data bundle

---

### T14.4 持续红队循环(2 天 → L3 拆 4 个半天)

**L2 原 DoD**:cron 每周跑 + 新漏洞流程化

**L3 拆解**:

#### Day 63 上午(4h) — weekly cron
- **🪤 复用 T12.4 cron 模式**:`cron/v8-red-team-weekly.sh`
- **动作**:每周一 02:00 跑 harness + 生成报告 + 发 webhook
- 单测:`test_cron_config.py` 2 用例

#### Day 63 下午(4h) — 新漏洞流程化
- **动作**:`tools/new_vuln_intake.py`:新发现的漏洞自动加 probe ID 26+ + 写 `red_team_probes/26.py` 模板
- 单测:`test_new_vuln.py` 3 用例

#### Day 64 上午(4h) — 集成测试 + 留痕

**L3 总产出**:cron 30 行 + intake 80 行 + 单测 5

---

## 📊 L3 vs L2 对比(关键增量)

| 维度 | L2 | L3 |
|---|---|---|
| 颗粒度 | 任务级(ID + DoD + 工时) | **半天级**(上午/下午动作清单) |
| 总工时估算 | 75 人天 | **53 天**(假设 1 人/天,实际 5 session 并行 10 周) |
| commit 数 | 未统计 | **估算 60-80 个 commits** |
| 单测门槛 | 隐式 | **显式:每任务 ≤2 天必须带单测,总数 ≥ 200 用例** |
| 风险兜底 | 5 条总览 | **每个任务 3-5 条 fallback 路径** |
| 接力握手 | 通用 | **精确:每个任务有"接力给"+ 输入/输出物** |
| 论文数据整合 | 提到 4 篇候选 | **每篇 paper 有 data bundle 输出物** |

---

## 🎯 给未来接力 session 的开箱指南

### 新 ML session 拿到本 L3 计划 + 接力包后:

```text
Step 1(5 min):读本 L3 计划对应任务的"上午"段
Step 2(30 min):跑 git clone + setup(pip install 等)
Step 3(0.5 天):上午任务跑通 + commit
Step 4(0.5 天):下午任务跑通 + commit
Step 5(1h):跑单测 + 留痕 4 处
Step 6:完工报告 + handoff 给下一个任务
```

### 接力节点(15 个任务之间的握手):

```
T11.1 → T11.2:  schema 终稿 (Draft 2020-12 + 24 用例 PASS)
T11.1 → T11.3:  schema 终稿(同上,T11.3 不依赖 T11.2 registry)
T11.1+T11.2+T11.3 → T11.4:  全部完工(mock A2A 才能跑)
T11.x → T12.1:  T11.x 不强依赖,但 T12.x 依赖 V7 §5.1-5.3(已沉淀)
T12.1+T12.2 → T12.3:  DP 聚合 + 声誉 schema
T12.1+T12.2+T12.3 → T12.4:  violation_detector 才能扫
T13.1 → T13.2:  treasury 设计文档
T13.2 → T13.3:  governance_funding_mode 函数
T11-T13 → T15.1:  KPI 数据源
T14.x → T15.2:  hard rule violation 测试
T14.1 → T14.2:  harness 骨架
T14.2 → T14.3:  25 probe 全注册
T14.3 → T14.4:  ELR 报告
```

### 复用工具栈速查:

| skill | 复用点 |
|---|---|
| `paper-review-toolkit` | schema validator / policy.yaml 模式 |
| `wechat-mp-validation` | cron + webhook 模式(Layer 1 监控) |
| `knowledge-wiki` | 知识库索引 / log.md 留痕 |

---

## 📝 与其他 session 的交接清单(完整版)

任何接力本计划的 session 应验证:

- [ ] 读过 `sources/agent-os-architecture-full-2026-07-11.md` §11-15 全文
- [ ] 读过 `analysis/agent-os-v8-implementation-plan-2026-07-13.md`(L2 骨架)
- [ ] 读过**本文档**(L3 详细版)
- [ ] 读过 `analysis/agent-os-v8-review-2026-07-11.md`(V8 自检档)
- [ ] 读过 `analysis/agent-os-vulnerabilities-2026-07-11.md`(25 漏洞详解)
- [ ] 拿到接力包 `tmp/v8-handoff-T{11.1,...}.md`(对应任务)
- [ ] 没有跨"职责外"——本计划**与泰玄小站无关**(职责外,泰不介入)

---

## 📊 L3 文档元信息

| 项 | 值 |
|---|---|
| 大小 | ~25 KB(目测,基于 L2 13.7 KB + L3 增量) |
| 任务数 | 15(L2 全部) |
| 半天数 | 75(L3 拆解后) |
| 单测总数预估 | ≥ 200 用例 |
| commit 总数预估 | 60-80 |
| 论文候选 | 4 篇(#2 / #6 / #11 / #17) |
| 留痕约定 | 每任务 4 处(MEMORY / log.md / analysis/完工报告 / 计划状态更新) |

---

## 📋 提案补丁记录

| 时间 | 改动 | 原因 |
|---|---|---|
| 22:25 | 初版 L3 | 刘泽文 "根据最新方案(白皮书)重新制定可落地详细计划" → L2 颗粒度不够,加 L3 |

---

**L3 计划完。等刘泽文指派 / 任一执行 session 来接力。**
