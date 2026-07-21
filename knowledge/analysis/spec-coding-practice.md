# Spec Coding 实践总结 — 泰玄小站 v2.0

> Source: 2026-07-10 深夜,泰玄小站 `wx-miniprogram/specs/` 框架搭建 + 3 个 scanner 数据驱动改造
> 适用场景:任何"AI + 合规"导向的 B 端/C 端产品

## 一句话总结

**Spec coding 在 AI 合规项目的真正价值不是"约束 AI",而是"把团队的隐性约束显性化、版本化、可测试化"。**

## 何时该用 spec coding

| 场景 | 是否适合 |
|---|---|
| AI 输出结果要被多个子系统消费(前端渲染 / 后端审计 / 数据统计) | ✅ 强适合 |
| 有明确的合规约束(广告法 / 平台规则 / 行业规范) | ✅ 强适合 |
| 业务规则多版本(8 派命理 × 4 场景 × 2 套餐) | ✅ 强适合 |
| 一次性 demo / 个人玩具 / 内部脚本 | ❌ 杀鸡用牛刀 |
| 业务规则 1-2 条且不变 | ❌ 过度设计 |

## 三层架构(经过验证)

```
specs/                       ← 单一事实源(JSON/YAML,机器可读)
  ↓ 读
scanner scripts              ← 把 spec 变成可执行断言
  ↓ 输出
tests/*-report.md            ← 人类可读报告
```

**关键约束**:
- specs/ 是**一等公民**:契约变更先改 spec,再改代码,后改叙述文档
- scanner 不重复 spec 内容,只读 + 断言
- 报告是**派生物**,可删除重建

## 5 类 spec 模板(按价值排序)

| # | 类型 | 例子 | 价值 |
|---|---|---|---|
| 1 | **合规禁词表** | `mingli_banned_words.json` | 最高 — 直接挡审核 |
| 2 | **API 契约** | `v1.endpoints.json` / `v2.endpoints.json` | 极高 — 前后端唯一对齐 |
| 3 | **结果 schema** | `schools/*.result.schema.json` | 极高 — AI 输出契约 |
| 4 | **LLM Prompt 模板** | `prompts/*.yaml`(8 派) | 极高 — 后端工程师可直接 yaml.load() 渲染 |
| 5 | **场景模板** | `scenes/relationship.yaml` | 中 — 后端 prompt 注入 |
| 6 | **语气/风格规则** | `tone_rules.json` | 中 — 报告但不阻塞 |

## 3 类 scanner 模式

| 模式 | 行为 | exit code | 例子 |
|---|---|---|---|
| **block** | 命中即失败 | 1(block 命中)/ 0(全过) | `check-objective-language.js`(广告法风险) |
| **warn** | 报告不阻塞 | 永远 0 | `audit-wxml-tone.js`(语气软化) |
| **acceptance** | 元测试(spec 自洽性) | 1(任何 spec 异常)/ 0(全过) | `liupai-reader-test.js` Layer 2 |

**为啥要分 3 类**:
- block 解决"必须做"的事(合规底线)
- warn 解决"建议做"的事(质量提升)
- acceptance 解决"不能忘"的事(spec 漂移)

混在一起 = 团队要么被噪音淹没,要么忽略信号。

## Schema 设计的 5 个反模式

写 `schools/bazi.result.schema.json` 时踩过的坑:

1. **❌ 字段名过早特化** — `bazi_specific_five_elements` 而非 `fiveElements` —— 8 派应有统一键名,后端映射层做特化
2. **❌ 必填字段太多** — 把 `disclaimer` 设必填会导致 demo 阶段就被 reject —— 必填只放真正契约级别的
3. **❌ 用 `enum` 锁死未来** — 8 派如果将来要加新流派,枚举锁死会成阻碍 —— 用 `pattern` + 后端校验更灵活
4. **❌ 字段顺序当语义** — JSON 不保证 key 顺序,前端若依赖 `sections[0]` 是 "总论",`sections[1]` 是 "建议" 会翻车 —— 用 `head`/`title` 字段语义化
5. **❌ 字符串长度不约束** — `summary` 字段不设 `maxLength`,后端 LLM 可能吐出 5000 字 —— 必须 `minLength + maxLength`

## $ref 引用 — 减少漂移的关键技巧

v2.endpoints.json 直接引用 v1.endpoints.json 的 `$defs/FourPillars`:

```json
"fourPillars": {"$ref": "v1.endpoints.json#/$defs/FourPillars"}
```

**收益**:
- 4 柱字段变更 → 改 1 处生效(否则要改 2 个文件)
- acceptance test 自动验证引用闭环 —— **v2.endpoints.json 真能解析到 v1.endpoints.json#/$defs/FourPillars**

**限制**:
- 跨文件 $ref 在 JSON.parse 时**不会**自动加载 —— 需要 acceptance test 显式加载并验证
- 简单项目(< 5 文件)不必用 $ref,YAML anchor 更轻

## 已知 schema-vs-demo 漂移管理

**案例**:bazi schema 要求 `summary / sections[].title / sections[].content / sections[].tone`,但 `utils/liupai-reader.js` 输出的是 `head + body`。

**对策**:
1. **不动业务代码**(避免破坏现有 demo)
2. **acceptance test 把漂移清单文档化**(用 warn 而不是 fail)
3. **漂移清单 = v2.0 迁移 TODO**

下次接 LLM 时,直接对照清单改造即可,不会忘。

## 测试反向验证(必须做)

写完 acceptance test 后,故意把 spec 改坏,确认能 fail:

```
故意把 tone_rules.json 的 rationale 砍到 1 字符
  → liupai-reader-test.js Layer 2.5 ❌ 捕获
  → 恢复原版 → ✅ 全过
```

否则 spec 写得再漂亮,scanner 写错了也不知道。

## 不写 spec coding 会怎样

如果这次没做 specs/:
- ❌ 8 派拼装测试 + LLM 输出契约分别在 utils/ 和 backend/,前端只能 markdown diff
- ❌ 广告法禁词改一处忘另一处,审核员找到一处就过不了
- ❌ v1.x → v2.0 升级,1094 行 markdown 契约 vs 5 个新接口,人工 diff 必漏
- ❌ 后端工程师接 v2.0 时,要重读 1094 行契约理解字段
- ❌ 8 派 prompt 模板散在 8 个 markdown,无法用 yaml.load() 自动渲染

**spec coding 的真正收益 = 让"规矩"被复用、被测试、被版本化**。

## LLM Prompt 结构化(`specs/prompts/*.yaml`)

8 派 prompt 模板原本是 `knowledge/20-v2-prompts/*.md`(人类可读叙事),结构化后变成 YAML,后端工程师能直接 `yaml.load()` 渲染。**通用结构**(11 个字段):

```yaml
liupai: <流派 id>
version: '1.0.0'
output_schema_ref: ../schools/<liupai>.result.schema.json  # 期望输出
role: |                      # LLM 人设
context: [...]               # 通用变量(性别/问题/真太阳时/出生地)
pan_input:                   # 流派特定排盘要素
  template: |                # markdown 模板
  variables: [...]           # 用到的所有变量
style:
  max_words: 800
  tone: warm
  banned_phrases_ref: ...    # 引用合规禁词
  requirements: [...]        # 详细要求
output_format: [...]         # 5 段结构
disclaimer:                  # 引用 compliance templates
tuning:                      # temperature/max_tokens/RAG
notes: |                     # 流派特殊提示
```

**关键设计**:
- `output_schema_ref` 指向已有 schema → 自动保证"prompt 期望输出什么"
- `disclaimer.template_ref` 指向 disclaimer_templates.json → 自动保证合规
- **`pan_input.variables`** 列出所有变量名 + 类型 + 示例,后端可生成类型定义
- **不取代**原 markdown,而是给它们结构化入口

**学到的 YAML 坑**:
- 数组项里嵌套双引号会让 parser 认错边界(报"bad indentation")
- 修法:**直接去掉内层引号**,或**整行用单引号**包起来
- 提交前**用 js-yaml / PyYAML 解析一次**比肉眼看靠谱得多

## 适用推广

| 项目 | 是否该做 spec coding | 理由 |
|---|---|---|
| 泰玄小站 v2.0 | ✅ 已做 | 多流派 + AI + 强合规 |
| 学术论文 review pipeline | ✅ 已做(见 paper-review-toolkit) | 多 reviewer × 多论文 × 多格式 |
| 单文件脚本 | ❌ | 杀鸡用牛刀 |
| 简单 CRUD app | ❌ | 框架自带表单验证 |
| AI agent 系统 | ⚠️ 看规模 | 5+ 个 prompt 模板 + 多 LLM provider 时再做 |

## 相关页面

- [泰玄小站项目全图](../entities/taixuan-miniprogram.md)
- [微信小程序 AI 内容合规](mp-ai-content-compliance.md)
- [论文审阅工具箱](paper-review-toolkit.md)