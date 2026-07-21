# Prompt 迭代方法论:契约式 vs 自然叙述式 的取舍

> **来源**:`tmp/web_623e2558.md`(llm-lab Copilot Prompt v3.1 综合报告,2026-07-12,232 行)
> **主题提炼** ✅ — 不复制原文,只抽核心洞察 + 取舍日志 + 双层修复方法
> **关键词**:prompt engineering · contract-style · few-shot · scorer negation-awareness · cross-project methodology

---

## 🎯 核心洞察(一句话)

> **契约式提示对"固定槽位任务"有益,对"自由叙述任务"有害 —— 分治,不二选一。**

这是 v1 → v2 → v3 → v3.1 四轮迭代得出来的反直觉结论。

---

## 📚 三轮迭代实证(v1 → v2 → v3)

| baseline | 总分(扩展 scorer) | 关键贡献 |
|---|---:|---|
| zero-shot | 47.97% | 基线 |
| few-shot v1(3 例) | 61.98% | few-shot > zero-shot 首次证明 |
| few-shot v2 full(8 例覆盖全 5 类) | **79.67%** | 样例丰富 + 真实字段 + 反例(tamper-proof 否认) |
| few-shot v3 full(契约式 Contract A–E) | **82.11%(修复后 82.93%)** | 槽位契约 → diagnosis +11.5pp / reviewer_qa +14.3pp |

### v2 → v3 逐任务 Δ(关键证据)

| task_type | v2 | v3 | Δ | 性质 |
|---|---:|---:|---:|---|
| `eval_yaml_generation` | 91.18% | 91.18% | 0 | 已是高,合同无额外收益 |
| **`report_summary`** | **68.18%** | **59.09%** | **−9.09** | ⚠️ 契约过刚 |
| `failure_diagnosis` | 73.08% | 84.62% | +11.54 | ✅ 槽位契约救命 |
| `verifier_design` | 90.00% | 85.00% | −5.00 | ⚠️ 略退化 |
| **`reviewer_qa`** | **71.43%** | **85.71%** | **+14.28** | ✅ 四段式救命 |

**两类任务,两个命运**:
- 槽位任务(failure_diagnosis / reviewer_qa):**填表任务** → 契约提升格式稳定性与必检点覆盖率
- 叙述任务(report_summary):**在约束下陈述事实** → 硬性句数把模型逼到丢事实

---

## ⚖️ v3.1 设计原则(分治策略)

1. **槽位任务**(eval_yaml / failure_diagnosis / verifier_design / reviewer_qa)**保留 v3 契约骨架**
   - v3 最大增量,不能丢
   - 但 verifier_design 微退化 5pp,需具体看哪个 Contract 例措辞偏刚

2. **report_summary 放弃 v3 "四句话硬契约"**
   - 回退到 v2 自然叙述风格
   - **改补 "必含事实清单"**(status / 精确计数 / 给定数字 / 证据文件 / 结构限制警告)
   - 既恢复 v2 事实完整度,又防退化到 v1 随意

3. **bedrock 5 规则(三版一致)原样保留**
   - 系统提示的 5 条核心规则是不可碰基座

4. **新增规则:"否认属性时不要复述危险词"**
   - 不是单点修复,是升为通用规则(防 tamper-proof / semantic superiority / factual correctness 等同型错误复犯)

---

## 📋 v3.1 取舍日志(10 条,每条=取自/放弃/为什么)

| # | 设计点 | 取自 | 放弃 | 为什么 |
|---|---|---|---|---|
| 1 | 系统提示 5 条 bedrock 规则 | v1/v2/v3 共有 | — | 三版一致且有效,基座 |
| 2 | 样例覆盖全 5 类、含真实字段 | **v2** | v1 稀疏样例 | v2 的 8 例带来字段真实感(base_url/timeout_sec/params),v1 太薄 |
| 3 | eval_yaml 契约:YAML only + 精确 model/provider 串 + 仅 structural verifier | **v3 Contract A** | v2 未显式 | v3 把"保留精确串"写成硬规则,直接修 v2 漏 model 名 |
| 4 | failure_diagnosis 槽位骨架(failure_type/evidence_file/why/fix/what_not_to_conclude) | **v3 Contract C** | v2 自由叙述 | 贡献 +11.5pp,v3 最大赢点;`evidence_file` 槽强制引用证据 |
| 5 | verifier_design 契约:YAML only + 优先 any_keywords + non_empty/min_chars/max_chars | **v3 Contract D** | v2 自由 | 稳定且符合 scorer 期望 |
| 6 | reviewer_qa 四段式(Direct answer / Evidence files / Limitation / Reproducibility action) | **v3 Contract E** | v2 自由 | 贡献 +14.3pp;改示例措辞去 tamper-proof(见 #9)|
| 7 | report_summary 放弃"exactly four sentences"硬契约 | 回退到 **v2** 自然风 | v3 Contract B 句数强制 | v3 硬契约挤掉 duration/精确计数,−9pp;v2 自然风 68% 更高 |
| 8 | report_summary 增"必含事实清单" | 新(综合 v2 事实 + v3 必检点) | — | 把"必检事实"从"句数"改成"清单",恢复事实完整度又不退化 |
| 9 | tamper-proof 表述:示例改 "traceable local evidence bundle, not an anti-tampering audit system" | 新(修复 v3 示例) | v3 示例 "not a tamper-proof audit system" | scorer `must_not_claim_tamper_proof` 非否定感知,含词即误判,去掉词根最稳 |
| 10 | 追加规则:"否认属性时不要复述危险词" | 新 | — | 把 #9 升为通用规则 |

---

## 🪤 tamper-proof 双层修复(经典方法论案例)

### 问题

`scripts/score_copilot_run.py` 的 `must_not_claim_tamper_proof` 是**纯子串匹配**:

```python
# 旧版(有 bug)
elif name == "must_not_claim_tamper_proof":
    add_check(result, name, not has_any(text, ["tamper-proof", "防篡改", "不可篡改"]))
```

模型写 "M0 is **not** a tamper-proof audit system"(正确否认)仍被判为"声称防篡改" → 误杀。

实测证据:`reviewer_008` 在 v3 旧 scorer 下误判挂 → 总分 `82.11%`;同批 outputs 重打分 → `82.93%`(修后)。

### 修复 A —— Prompt 侧(无需改 scorer)

Contract E 示例改为不含 "tamper-proof" 的措辞。

### 修复 B —— Scorer 侧(根治)

加 `denied_before()` 否定感知,window 48 英 / 20 中:

```python
elif name == "must_not_claim_tamper_proof":
    phrases = ["tamper-proof", "防篡改", "不可篡改"]
    matched = [p for p in phrases if p in text]
    if not matched:
        add_check(result, name, True)
    else:
        denied = all(_denied_before(text, text.index(p), window=12) for p in matched)
        add_check(result, name, denied)
```

### 教训(可迁移)

> **任何 "must_not_X" 自动检查,默认应假设自然语言会出现否定式 + 同义替换;只匹配子串 = 一定漏检或误杀。**
> 模式:`must_not_claim_<property>` → 必须支持 negation awareness + 同义(防篡改/不可篡改/immutable/...)|

---

## 🔁 跨项目复用启示(不止 llm-lab-copilot)

### 启示 1:任务先分类,再选 prompt 形式

问自己:**"这个任务的输出形态是 填表 还是 陈述事实?"**

| 性质 | 例子 | 适合 |
|---|---|---|
| **填表(槽位)** | failure_diagnosis / reviewer_qa / YAML 配置 / schema 输出 | Contract + 强制骨架 |
| **叙述(陈述)** | report_summary / 长文问答 / reasoning 解释 | 自然叙述 + 必含事实清单 |
| **混合** | Code review(结构框架 + 自由评论) | 软骨架 + 显式约束 |

### 启示 2:否定感知 = 自动检查必做项

凡是有 `must_not_*` / `must_include_*` / `must_answer_no` 这类 check,scorer 必须有:
- negation awareness(denial window 内识别 not/never/否认 等)
- synonym table(防篡改/不可篡改 → 同一家族)
- 失败模式下要区分"避免误杀真否认"和"不放过真声称"

### 启示 3:数字跨迭代必须标 "scorer 版本"

v2 的 "44.4% vs 63.6%" 跟 v3 的 "82.11% vs 82.93%" 不能直接比 —— 同一 scorer 不同时点也有差异。
**强制规范**:
- 任何 score 数字后附 `(scorer_version: YYYYMMDD-HHMM)`
- 任何"v(N) vs v(N+1)"对比表头加一行 `> 注:全部 baseline 都用 same scorer 重打`

### 启示 4:诚实承认"自动评分不是人类质量"

8 份文档反复出现 "structural verifier checks surface constraints only and does not prove semantic or factual quality" —— **这是给下游读者的免责声明,也是给自己的护栏**。

任何自动评估体系都需要这句话,否则读者会把 high score 误读为"模型真的好用"。

---

## 📦 8 份文档序列(LLM 工作流时间线)

来源全部位于 `tmp/web_*.md`(2026-07-12 13:44:59 批量抓取):

| # | 文件 | 角色 |
|---|---|---|
| 1 | `web_be7841d5.md` | R1 smoke baseline(zero vs few-shot 首轮信号) |
| 2 | `web_d06602c6.md` | Full baseline(50 sample,初版 scorer)|
| 3 | `web_1fa8eca0.md` | Prompt v2 优化(扩展 scorer + v2 样例)|
| 4 | `web_0f00dab5.md` | Prompt v3(契约式 Contract A–E)|
| 5 | **`web_623e2558.md`** | **v3.1 综合(本文主题来源,232 行)** |
| 6 | `web_75abdcf7.md` | `test_50_v2` frozen protocol(协议文档) |
| 7 | `web_67c44245.md` | v3 frozen test_50_v2 验证(自动 93.68%)|
| 8 | `web_dd6d8a0d.md` | Fine-tune baseline + 4 组实验设计 + QLoRA 闸门 |

---

## 🔗 关联知识入口

- **跨项目可借鉴**:泰玄小站 8 卦 prompt 设计(specs/prompts/*.yaml)是结构化契约 → **本案例的"分治策略"印证结构化适合填表任务**
- **bug 模式可参考**:`scorer negation awareness` 是通用模式,任何自动评估体系都该有(不只是 llm-lab Copilot)
- **数字一致性教训**:可融入 `paper-review-toolkit` 的 verify 框架(每次 report 自带 scorer_version 字段)

---

_本文件提炼于 2026-07-12 · 不复制原文,只抽象方法论 · source:`tmp/web_623e2558.md`_
