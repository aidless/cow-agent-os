---
name: arxiv-tracker
version: 0.1.0
status: live
description: |
  监控 arxiv 上与刘泽文研究主线(多 agent 协作 / 校准 / 偏好耦合)相关的
  新论文。每日/每周抓取 → LLM 中文摘要 + relevance 评分 → 写入 knowledge/
  下的 arxiv-watch 目录。
triggers:
  - "arxiv"
  - "抓 arxiv"
  - "最近有什么论文"
  - "看新论文"
  - "literature watch"
  - "研究监控"
requires:
  - OPENAI_API_KEY
  - OPENAI_API_BASE (default https://api.deepseek.com/v1)
  - python 3.10+
runtime:
  - http:    # 无 key 也跑(只 fetch)
  - llm:     # 需要 key
inputs:
  - --days (默认 30)
  - --max-results (默认 200)
  - --cats (默认 cs.CL,cs.AI,cs.LG)
  - --keywords (默认见 fetch_arxiv.py DEFAULT_KEYWORDS)
outputs:
  - JSONL (中间态)
  - Markdown vault 文件 (终态)
---

# arxiv-tracker

## 它做什么

抓 arxiv 最新论文 → 用 DeepSeek 写中文摘要 + 给 relevance 评分(基于你的研究主线)
→ 把高相关论文写入 `knowledge/concepts/arxiv-watch/arxiv-<YYYY-MM-DD>.md`。

## 何时用

- 你想知道"这周 arxiv 上有什么跟我研究主线相关的新工作"
- 想从最新论文里找新灵感 / 找新 baseline
- 想监控某个具体关键词(如 "multi-agent", "calibration")
- 写 TMLR R&R 之前需要快速 check 一下有没有新相关工作

## 工作流(三步,可独立运行)

```
┌────────────────────┐    ┌────────────────────────┐    ┌──────────────────────┐
│ 1. fetch_arxiv.py  │ →  │ 2. summarize_with_     │ →  │ 3. ingest_to_vault.py│
│ (零依赖)           │    │    llm.py              │    │ (knowledge-wiki 调用)│
│ 抓 arxiv 论文      │    │ DeepSeek 中文摘要      │    │ 写 vault + index     │
│ → JSONL            │    │ + 1-5 星 relevance    │    │ → markdown 终态     │
└────────────────────┘    └────────────────────────┘    └──────────────────────┘
```

### 阶段 1:抓取(无 LLM,可单独跑)

```bash
python skills/arxiv-tracker/scripts/fetch_arxiv.py \
    --days 30 --max-results 100 \
    --out tmp/arxiv_raw.jsonl
```

输出 schema(每行一个 JSON 对象):`arxiv_id / title / authors / abstract / categories / published / updated / pdf_url / html_url / matched_keywords / source`

**容错**:3 次重试 + 指数退避;分页间隔 3 秒防 arxiv 限流;`arxiv_id` 去重(保留首次出现,即较新版本)。

### 阶段 2:摘要(需要 LLM)

```bash
python skills/arxiv-tracker/scripts/summarize_with_llm.py \
    --in tmp/arxiv_raw.jsonl \
    --out tmp/arxiv_summarized.jsonl \
    --max-workers 4
```

**默认模型**:`deepseek-v4-flash`(`ARXIV_TRACKER_MODEL` 可改)。每篇添加三个字段:
- `zh_summary`:1-2 句中文
- `relevance`:1-5 星(relevance to 刘泽文的研究主线)
- `relevance_reason`:≤30 字评分理由

**并发**:默认 4 worker,总耗时 ≈ 4 seconds/paper × num_papers ÷ workers
**容错**:JSON 解析失败 / API 错误 → 行打 `[LLM call failed]`,不影响其它行;缺 key → 透传 input。

### 阶段 3:入 vault

```bash
python skills/arxiv-tracker/scripts/ingest_to_vault.py \
    --in tmp/arxiv_summarized.jsonl \
    --vault-root knowledge
```

按 `relevance >= 3` 过滤(可在脚本里改阈值),写 `knowledge/concepts/arxiv-watch/arxiv-<YYYY-MM-DD>.md`,
并更新 `knowledge/index.md` 加一行索引。同时跑过的日期打 `marker-file`避免重跑。

**vault 文件格式**:
- 头部:日期、抓取窗口、统计、高星论文 anchor
- 每篇:标题 + arxiv-id 链接 + authors + cats + zh_summary + relevance + reason

## 系统默认配置

| 项 | 默认值 |
|---|---|
| 时间窗 | 30 天 |
| 最大结果数 | 200 |
| 类目 | `cs.CL`, `cs.AI`, `cs.LG` |
| 关键词 | 多 agent / agent 协作 / 校准 / 偏好 / 共识 / agent 框架 |
| LLM | `deepseek-v4-flash` |
| 入 vault threshold | `relevance >= 3` |

## 自定义关键词 / 类目

CLI 覆盖即可,无需改代码:

```bash
python scripts/fetch_arxiv.py \
    --cats cs.MA,cs.CL \
    --keywords "agent calibration,communication efficiency" \
    --days 7
```

## 失败兜底

| 错误 | 兜底 |
|---|---|
| `OPENAI_API_KEY` 未配 | 阶段 2 透传,阶段 3 仍可跑(有 `zh_summary=""`) |
| arxiv 限流(429) | 脚本 3 次重试 + 指数退避,再不行写 stderr `[fetch_arxiv] FATAL` |
| DeepSeek 端超时 | 单行打 `[LLM call failed]`,其他行不受影响 |
| arxiv 一篇都没有命中关键词 | 仍产空 JSONL,vault 端会写"今日无高相关论文" |
| vault 目录不存在 | 脚本自动 `mkdir -p` |
| `knowledge/index.md` 不存在 | 脚本自动创建 |

## 实测验证

✅ `fetch_arxiv.py`:30 天 / cs.CL+cs.AI+cs.LG → **74 篇去重命中**
✅ `summarize_with_llm.py`:10 篇真实论文 → 完整 LLM 摘要(0 失败)

---

## 🆕 7/11 Self-Citation Filter(必读)

**问题**:7/11 给刘泽文做 PAPER5 must-cite 推荐时,arxiv-tracker 抓回来的论文里有
**他自己的 10 篇**(`liu_z_28` 主页可见),但 skill 没过滤,导致把 2606.20493 Contagion
Networks 等自我引用当外部论文推荐,反复确认浪费工时。

**修复**:任何为刘泽文做的 must-cite / related work / literature review 工作流,**第一步**
就是 fetch 自我的 arxiv 主页 + ORCID,标记 self-authored 论文,后续过滤掉。

```bash
# Step 0(a): fetch self-authored papers(必跑)
curl -s "https://arxiv.org/a/liu_z_28" | grep -oP 'arXiv:\d+\.\d+' | sort -u > tmp/self_arxiv_ids.txt

# Step 0(b): ORCID 交叉验证(可选,防 liu_z_28 主页疏漏)
# ORCID: 0009-0003-2981-9888 → /0009-0003-2981-9888/works
curl -s "https://pub.orcid.org/v3.0/0009-0003-2981-9888/works" \
  -H "Accept: application/json" | jq '.["activities-summary"]...'

# Step 0(c): Google Scholar(可选,同名作者去重)
# 警告:Scholar 上同名 "Zewen Liu" 可能多于 1 个,人工核对 ORCID + 邮箱
#        17353895263@163.com 才算 self

# Step 1-3: 正常抓 + 摘要 + 入 vault,但 ingest 阶段过滤 self-authored
python skills/arxiv-tracker/scripts/ingest_to_vault.py \
  --in tmp/arxiv_summarized.jsonl \
  --vault-root knowledge \
  --exclude-arxiv-ids tmp/self_arxiv_ids.txt \   # 🆕 7/11 新增参数
  --mark-self-cite                                # 🆕 7/11 新增参数(标记但不删除)
```

**两种处理模式**:
- `--exclude-arxiv-ids`:**完全过滤**,不写入 vault(默认用于 must-cite 推荐)
- `--mark-self-cite`:**保留但加 `🤚 SELF-CITE` 标记**,写入 vault(用于 related work,作者要看见自己的论文位置)

**刘泽文的 self-citation 锚点**(固化在 skill 里):
| 字段 | 值 |
|---|---|
| arXiv author ID | `liu_z_28` |
| ORCID | `0009-0003-2981-9888` |
| Email 锚 | `17353895263@163.com`(用于同名作者消歧) |
| 默认主页 | https://arxiv.org/a/liu_z_28 |

**未来扩展**:如果要把这个 skill 推广到其他用户,把 `liu_z_28` / ORCID / email 抽到
`skills/arxiv-tracker/config.yaml`,让每个用户单独配。

---

## 🆕 7/11 Review 章节 — 38 篇论文 LLM judgment

7/11 把 2026-07-10 抓的 38 篇 ≥3 星论文(分布在 `knowledge/concepts/arxiv-watch/arxiv-2026-07-10.md`)做了 LLM 5 字段判断 + cross-check:

| Judgment | 数量 | 含义 |
|---|---|---|
| **watch_deep** | **3** | 必读(PAPER1/2/3/4/5/6 之外的潜在新思路) |
| **watch_brief** | **9** | 简读,避免撞库即可 |
| **known_related** | **26** | related work 引用,跳过精读 |
| known_covered | 0 | (没命中 PAPER1-6 完整覆盖) |
| skip | 0 | (filter ≥3 星已经过滤) |

**3 篇 watch_deep(本周 deep dive)**:
- `2607.08700` — Citation Verifier Calibration(校准)
- `2607.07368` — Multi-Agent AI Control: Distributed Attacks(直接对应 PAPER1+2 监控场景)
- `2607.06855` — Geometric Self-Distillation(偏好漂移抑制,可迁移到多智能体偏好耦合)

**核心工具**(7/11 落地):
```
tmp/arxiv_review/
├── papers.jsonl                    38 篇元数据
├── judgments.jsonl                 38 篇 LLM 5 字段
└── ARXIV_WATCH_REVIEW_2026-07-11.md   132 行 dashboard
```

**下次自动跑**:
```bash
# 把 7/11 流程封装为脚本(下次开工可考虑)
python tmp/arxiv_review/extract_papers.py   # markdown → JSONL
python tmp/arxiv_review/judge_papers.py     # JSONL → LLM judgments
python tmp/arxiv_review/render_report.py    # judgments → dashboard
```

## 关联资源

- skill 主体:`C:\Users\Administrator\cow\skills\arxiv-tracker\`
- knowledge 索引:`C:\Users\Administrator\cow\knowledge\index.md`
- arxiv-watch 目录:`C:\Users\Administrator\cow\knowledge\concepts\arxiv-watch\`(首次运行后自动创建)
- DeepSeek API 文档参考:见 `references/deepseek_api.md`(首次运行后自动创建)
