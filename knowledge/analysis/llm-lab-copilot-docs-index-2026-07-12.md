# llm-lab Copilot 8 份文档索引(长期版)

> **生成时间**:2026-07-12 14:05
> **来源**:2026-07-12 13:44:59 批量抓取的 `tmp/web_*.md` 8 份
> **范围**:长期沉淀,跟方法论提炼文档配对存在
> **临时版**:`tmp/web_index.md`(7 天滚窗)
> **关联**:[Prompt 迭代方法论提炼](./contract-vs-natural-prompt-tradeoff-2026-07-12.md)

---

## 🎯 文档集性质

这 8 份文档构成 llm-lab Copilot 项目的**完整 LLM 工作流时间线**(2026-07-12 单日完成)。是一个**独立工作流**,跟刘泽文主研究/泰玄小站项目**正交不重叠**,但有可借鉴的方法论(任务分类 / 否定感知 / 数字版本标注)。

---

## 📋 全景

| # | 文件 | 长度 | 角色 | 关键产出 |
|---|---|---:|---|---|
| 1 | `tmp/web_be7841d5.md` | 3.0 KB | **R1 smoke** | zero-shot vs few-shot 早期信号;first 5 YAML:46.2% → 76.9%(+30.7pp) |
| 2 | `tmp/web_d06602c6.md` | 3.2 KB | **Full baseline** | 50 sample 全量;zero 44.4% / few-shot 63.6%(旧 scorer);1 个 timeout |
| 3 | `tmp/web_1fa8eca0.md` | 3.8 KB | **Prompt v2** | 扩展 scorer + 8 例覆盖全 5 类;full 79.67%(98/123) |
| 4 | `tmp/web_0f00dab5.md` | 4.3 KB | **Prompt v3** | Contract A–E 契约式;full 82.11%(旧 scorer);2 类任务分化(+11.5/+14.3 vs −9.09)|
| 5 | `tmp/web_623e2558.md` | 13.7 KB | **🟢 v3.1 综合** | 取长补短决策;**已提炼为 [方法论文档](./contract-vs-natural-prompt-tradeoff-2026-07-12.md)** |
| 6 | `tmp/web_75abdcf7.md` | 1.2 KB | **`test_50_v2` 协议** | 50 条独立 frozen test set;SHA256 `087eb9f2...a7879577` |
| 7 | `tmp/web_67c44245.md` | 3.4 KB | **v3 frozen 验证** | test_50_v2 自动 93.68%(178/190);1 unsupported claim |
| 8 | `tmp/web_dd6d8a0d.md` | 3.9 KB | **Fine-tune 闸门设计** | 4 组实验 base/base_few_shot/fine_tuned/fine_tuned_few_shot;5 阈值 |

---

## 🔗 文档间引用关系(决策链)

```
[1] R1 smoke(zero vs few-shot 信号)
   ↓ few-shot > zero-shot 首次证明
[2] Full baseline(50 sample,旧 scorer,1 timeout)
   ↓ scorer 缺陷暴露 → 扩 scorer
[3] Prompt v2(扩展 scorer + 8 例 → 79.67%)
   ↓ 槽位任务(failure_diagnosis / reviewer_qa)不达标
[4] Prompt v3(Contract A–E → 82.11%)
   ↓ tamper-proof scorer bug 暴露 + 槽位强(+11.5/+14.3pp) + 叙述弱(−9.09pp)
[5] v3.1 综合(取长补短决策) —— 🟢 决策核心
   ↓
[6] test_50_v2 协议(冻结测试集,50 条新集 SHA256 锁定)
   ↓
[7] v3 frozen 验证(test_50_v2 自动 93.68%, 1 unsupported claim)
   ↓
[8] Fine-tune baseline + 4 组实验设计(QLoRA 闸门 5 阈值)
   ↓
[未来] QLoRA 真跑(目前未启动)
```

---

## 🪤 跨文档已知问题

### 1. 数字 scorer 版本不一致(最高优先级)

| 文档 | 用的 scorer | 影响的数字 |
|---|---|---|
| `web_d06602c6.md` | 旧 scorer(保守,只检查基础 reference_checks) | zero 44.4% / few-shot 63.6% |
| `web_1fa8eca0.md` | 扩展 scorer(覆盖全 reference_checks 表面) | v2 full 79.67% |
| `web_0f00dab5.md` | 扩展 scorer | v3 full 82.11% |
| `web_623e2558.md` §1 表格 | 扩展 scorer | v3 82.11% |
| `web_623e2558.md` §6.3 | 扩展 scorer(12:59 修复后版本) | v3 **82.93%** |
| `web_67c44245.md` | test_50_v2 scorer(独立 frozen 集) | v3 frozen **93.68%** |

**问题**:跨文档直接比 uplift 不公平,因为 scorer 覆盖度不同。
**修复方向**:
- 任何 score 数字后附 `(scorer_version: YYYYMMDD-HHMM)`
- 任何"v(N) vs v(N+1)"对比表头加 `> 注:全部 baseline 用 same scorer 重打`

### 2. SHA256 不一致

- `web_75abdcf7.md` 协议文档**未印出** SHA256(只说"recorded in `test_50_v2.sha256`")
- `web_67c44245.md` §Frozen Confirmation 印了 `087eb9f2c86dd17608f957f2e8d7ea72e2964ee19ca9285a4a959b71a7879577`
- **建议**:协议文档正文加一行 `> SHA256: 087eb9f2c86dd17608f957f2e8d7ea72e2964ee19ca9285a4a959b71a7879577`,避免读者二次查证

### 3. QLoRA 阈值硬编码,缺 source

`web_dd6d8a0d.md` §Continue/Stop Criteria:
- YAML parse rate ≥ +20%
- schema pass rate ≥ +20%
- manual quality ≥ +0.5/5
- unsupported claims ≤ -30%
- failure diagnosis actionability ≥ 80%

**问题**:5 条阈值都是裸数字,没引用经验 / 文献 / 内部约定。

### 4. QLoRA 参数来源不清

`web_be7841d5.md` §Hardware Note:4-bit quantization / LoRA rank 8 / max seq 2048 / batch 1 / grad accum 16
**问题**:这套参数没引用 QLoRA 论文或本地 benchmark,直接拍脑袋。

---

## 📚 关键文件快速入口

| 想找 | 看 |
|---|---|
| v1→v2→v3→v3.1 决策 + 取舍日志 | `tmp/web_623e2558.md`(完整 232 行)|
| **方法论提炼(主题命名版)** | [`./contract-vs-natural-prompt-tradeoff-2026-07-12.md`](./contract-vs-natural-prompt-tradeoff-2026-07-12.md) |
| tamper-proof scorer bug 根因 + 双层修复 | `tmp/web_623e2558.md` §6 |
| 冻结测试集协议 | `tmp/web_75abdcf7.md` |
| v3 frozen 真跑结果 | `tmp/web_67c44245.md` |
| Fine-tune 4 组实验设计 | `tmp/web_dd6d8a0d.md` |
| QLoRA 闸门 5 阈值 | `tmp/web_dd6d8a0d.md` §Continue/Stop |

---

## 🔗 跨项目借鉴价值

| 借鉴点 | 适用场景 |
|---|---|
| **任务先分类**(填表 vs 叙述)再选 prompt 形式 | 泰玄小站 8 卦 prompt / paper-review-toolkit / 任何 LLM 应用 |
| **否定感知 = 自动检查必做项** | 任何 `must_not_X` 自动评估 |
| **跨迭代数字必标 scorer_version** | 任何 A/B uplift 报告 |
| **诚实承认自动评分不是人类质量** | 任何自动评估体系 |
| **冻结测试集协议**(`test_50_v2` 模式) | 任何需要严格 A/B 比较的工作 |
| **双层 bug 修复**(prompt 侧 + scorer 侧) | 任何 prompt + scorer 协同系统 |

---

## 📌 阅读建议

- **新读者**:先读方法论提炼文档(8.7 KB,15 分钟),再回 `web_623e2558.md` 看原文 YAML 合同
- **要复现实验**:从 `web_dd6d8a0d.md` §Copilot Evaluation Plan 开始,跟着 4 组实验跑
- **要审计 scorer**:从 `web_1fa8eca0.md` §Scoring Caveat 开始,看 scorer 扩展记录
- **要审计 prompt**:从 `web_623e2558.md` §4 取舍日志开始,逐条找 source

---

_最后更新:2026-07-12 14:05 · 长期索引,跟方法论提炼文档配对存在_