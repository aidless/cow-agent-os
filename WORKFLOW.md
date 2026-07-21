# WORKFLOW.md - 我的工作流宪法

_提炼自 2026-07-10 一整天真实工作流的元规则。_

_这一篇是"为什么这样做"的元认知,不替代任何具体 skill / RULE.md / MEMORY.md。_

---

## 🎯 三条核心律令

### 律令 1:**契约先于实现**(Spec-First)

**做什么**:**先**把"应该怎么"**写下来**,**然后**才动手实现。

**来源证据**:
- 泰玄小站 v2.0 的 `specs/api/v2.endpoints.json` 提前 1 周写出来,然后才改后端
- ML 论文的 `protocol.md` 先写,然后才写 main.tex
- 11 个 zip 整理先 `.move_plan.json` 写出来,然后才 `Move-Item`

**反模式**:
- ❌ "边写边想" → 容易"实现完才发现契约不对"
- ❌ 直接动手 → 重构时找不到"原本的意图"
- ❌ 写完代码再补文档 → 文档永远和代码对不上

**判断标准**:
> 如果这个工作**会被复用 / 被验证 / 会被别人看** → 必须先有契约。
> 如果只是 1 次性的随手脚本 → 不强制,但**应该在脚本顶部加注释说明意图**。

### 律令 2:**人机双产物**(Markdown + JSON)

**做什么**:每个交付物都要**两份**:
1. **给人看的** `*.md`(叙事、表格、决策)
2. **给机器看的** `*.json` 或 schema(校验、自动化、二次利用)

**来源证据**:
- 泰玄小站 `specs/compliance/mingli_banned_words.json`(机器可读)+ 同名 `analysis/mp-ai-content-compliance.md`(人读)
- `downloads/2026-07-10/INDEX.md`(人读)+ `.move_plan.json`(机器读)
- `knowledge/index.md`(人读)+ 内部 cross-link 结构(机器读)

**反模式**:
- ❌ 只写人读的 markdown → 无法自动化校验
- ❌ 只写 JSON → 失去解释性,新人看不懂

**判断标准**:
> 如果这个产物的消费方**只有人** → 只 markdown。
> 如果**机器也要消费** → 必须 JSON。
> 如果**两者都消费** → 两份都写。

### 律令 3:**保留源 + 验证后清**(Preserve-then-Verify-then-Clean)

**做什么**:
- **任何破坏性操作前**,先**保留源**(即使源很占空间)
- **操作后**,逐项**验证非空 / 状态正确**
- **验证通过 + 等到回滚窗口到期**,才**询问是否清理**

**来源证据**:
- 7/10 教训:批量解压 + 立即删源,5 个项目"消失"(zip 解压失败但没报错)
- 7/10 决策:11 个 zip 解压完**保留源**,7/17 后再决定
- AGENT.md 里 5 条"我会主动说的不",保护这条不破

**反模式**:
- ❌ "解压完空间不够,删源" → 无回滚
- ❌ "脚本跑完应该没问题吧" → 没验证就清
- ❌ "几天了应该稳定了" → 无固定窗口

**判断标准**:
> 破坏性操作必须 3 步走:**保留 → 验证 → 询问**,缺一步不做。

---

## 📚 模式目录

### 模式 A:`specs/` 契约驱动(泰玄小站)

```
wx-miniprogram/
├── specs/
│   ├── README.md                 # 索引(人读)
│   ├── api/
│   │   ├── v1.endpoints.json     # 现有 API 契约
│   │   └── v2.endpoints.json     # 新 API 契约(加 $ref, $defs)
│   ├── schools/
│   │   └── bazi.result.schema.json
│   ├── compliance/
│   │   ├── ai_marker_rules.json
│   │   ├── mingli_banned_words.json   # 反模式 + remediation
│   │   └── disclaimer_templates.json
│   └── acceptance/
│       └── smoke.test.js         # 验证 specs/ 自洽
└── tests/
    └── audit-wxml-tone.js        # 读 specs/compliance/*.json,数据驱动
```

**规则**:
1. specs/ 是**一等公民**:契约变更**先改 spec**,再改代码,**最后**改叙事文档
2. spec 改了**没在代码体现** → 算 bug,优先级比"改完没跑通"更高
3. compliance 类 spec 必须含 **`remediation_playbook`** —— 不是只"指出错",要"建议怎么改"

### 模式 B:`protocol.md` 假设驱动(ML 论文)

```
F:\Research\paper5\
├── protocol.md                   # 假设 + 实验设计 + 验证清单
├── main.tex                      # 论文主体
├── main.tex.bak_<阶段描述>       # 7/10 学到的:用 .bak_<描述> 迭代
├── refs.bib
├── verify_p5.py                  # 跑 protocol.md 的实验,出 PASS/FAIL 报告
└── tmlr.bst/sty
```

**规则**:
1. protocol.md 必须先有 → main.tex 才有引用依据
2. `.bak_` 命名约定:**描述当前阶段**,不是"v1/v2/v3"
3. `verify_pN.py` 的"6/6 PASS"比论文写得好更重要

### 模式 C:`downloads/` 归档驱动(基础设施)

```
downloads/
└── <YYYY-MM-DD>/
    ├── INDEX.md                  # 人读索引
    ├── .move_plan.json           # 机器读搬运方案
    └── <分类>/<项目>/...          # 实际项目(从源解压/克隆出来)
```

**规则**:
1. **每个批次**一个目录,标日期
2. 归档脚本(`_apply_layout.ps1`)必须**幂等**
3. 源(zip/exe)在 `tmp/` 里再**保留 7 天**,quarantine.md 记录到期日

---

## 🔄 模式间的关系

```
                  ┌─────────────┐
                  │  USER 决策  │
                  └──────┬──────┘
                         │ (可能是反复的,7/10 已证)
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐      ┌─────────┐
   │  ML 研究 │      │ 小程序  │      │ 基础设施│
   │(protocol│      │ (specs) │      │ (archive│
   │  -first)│      │  -first)│      │  -first)│
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └────────────────┴────────────────┘
                         │
                  ┌──────▼──────┐
                  │  三模式共享  │
                  │ 的人机双产物 │
                  │   + 保留源  │
                  └──────┬──────┘
                         │
                  ┌──────▼──────┐
                  │   审计层    │
                  │  (verify_pN │
                  │  smoke.test │
                  │  quarantine)│
                  └─────────────┘
```

**关键**:**三个模式不是替代关系,是同一个"契约先于人"的律令,3 个不同应用**。

---

## 🎬 决策树(下次遇到新任务时)

| 任务特征 | 用哪个模式 |
|---|---|
| 需要跟别人(API/UI/契约)对齐 | A `specs/` |
| 需要可复现、可审计的实验 | B `protocol.md` |
| 需要从外部拉资源并归类 | C `downloads/` |
| 三者都不需要 | **不强制**,但记入 MEMORY.md 的小事件 |

---

## 🪤 律令 0:**先扫盘再动手**

虽然写在 AGENT.md 了,这里再强调:**这是律令 0**,比 1/2/3 都优先。

任何任务接到手,先:
1. `ls` 或 `dir /B` 看环境
2. `read` 看已有文档
3. `memory_search` 看有没有历史
4. **然后**才问 / 提议 / 动手

---

## 🧪 验证宪法本身(自检)

```bash
# 检查自己的"是否留痕"程度:
ls C:\Users\Administrator\cow\memory\*.md | wc -l     # 每日记忆数
ls C:\Users\Administrator\cow\knowledge\**\*.md | wc -l  # 知识页面数
cat C:\Users\Administrator\cow\MEMORY.md | wc -l       # MEMORY.md 行数
```

如果 MEMORY.md 行数 < 50 → 说明**没在工作**,宪法形同虚设。
如果 `memory/` 只有 1 天 → 说明**历史断了**,重建历史是 P0。
如果 `knowledge/` 空空如也 → 说明**没沉淀**,所有交付都是一次性。

**刘泽文的工作风格是"先口头扫盘再行动",所以**: 工作流宪法不应该是"我建议这样做",而是"我观察到刘泽文**已经**这样做,我只是命名它"。
