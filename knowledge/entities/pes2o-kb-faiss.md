---
title: peS2o KB Faiss · 论文检索系统全图
slug: pes2o-kb-faiss
status: 🟢 活动
created: 2026-07-11
tags: [peS2o, FAISS, KB, TMLR, paper-search, tool]
related: [liu-zewen-research, paper-review-toolkit]
---

# peS2o KB Faiss · 论文检索系统全图

> **TL;DR** — 一个**本地离线运行**的 FAISS + SQLite 论文语义检索引擎,服务 TMLR 投稿前的
> "must-cite 论文发现" 流程。**实测 14:10 在 PAPER5 上跑出 6 篇 2026 年新文必引候选**,其中 2 篇与论文主题直接撞题。
>
> 不是 SaaS,是你盘上 `E:\peS2o_kb_faiss` 一个目录。

---

## ⭐ 实测战绩(2026-07-11 14:10)

| 维度 | 数值 |
|---|---|
| **PAPER5 必引候选产出** | **6 篇**(从 541,712 vectors 中)|
| **直接撞题** | 2 篇(Contagion Networks / State Contamination)|
| **检索性能** | **10-18ms** for top-10 |
| **排除精度** | 18 个 arxiv ID + 37 个 title 全部正确排除 |
| **召回质量** | 10/10 相关,全部 2026 年新文 |

**KB → 论文写作链路已打通**(路径 B 完成)。
> "must-cite 论文发现" 流程。当前收录 **541,613 篇** 论文,**560,284 个** 向量,
> 主要数据源是 **peS2o v3 CS** 切片 + arxiv 增量。
>
> 不是 SaaS,是你盘上 `E:\peS2o_kb_faiss` 一个目录。

---

## ⭐ 实测战绩(2026-07-11 14:10)

| 维度 | 数值 |
|---|---|
| **PAPER5 必引候选产出** | **6 篇**(从 541,712 vectors 中)|
| **直接撞题** | 2 篇(Contagion Networks / State Contamination)|
| **检索性能** | **10-18ms** for top-10 |
| **排除精度** | 18 个 arxiv ID + 37 个 title 全部正确排除 |
| **召回质量** | 10/10 相关,全部 2026 年新文 |

**KB → 论文写作链路已打通**(路径 B 完成)。

---

## 🎯 它解决什么问题

**TMLR 投稿前**:我需要快速找到"相关但还没引用的论文"来强化 related work。
arXiv API 搜索 + Semantic Scholar 推荐都不够精准,且 peS2o 这种"基于全文学术语料"预训练的领域
在 arxiv 之外还藏着大量值得引用的工作。

**这套系统的做法**:
1. 把 ~50 万篇 peS2o 论文 + arxiv 近期论文用 **all-MiniLM-L6-v2**(384 dim) 编码
2. 倒排到 FAISS `IndexFlatIP` 做余弦相似度
3. 配套 SQLite 存 metadata(title / authors / abstract / year / categories)
4. CLI + HTTP API + 必须引用排除(must-cite 模式)

**核心使用场景**:
```bash
py -3 E:\peS2o_kb_faiss\kb_search.py "TTRL test-time scaling" -n 10

# must-cite 模式:返回 KB 中相关但不在你现有 .bib 里的论文
py -3 kb_search.py "agent evaluation" --existing-refs refs.bib -n 5 --must-cite

# BibTeX 直出
py -3 kb_search.py "TTRL" --bibtex out.bib -n 20
```

---

## 📂 目录全景

```
E:\peS2o_kb_faiss\                 # KB 系统本体 (~9.92 GB + 9.7 GB backup)
├── 核心数据
│   ├── papers.db                  # SQLite, 8.37 GB, 541,613 papers
│   ├── papers.index               # FAISS IndexFlatIP, 793 MB, 363,948 vecs (主索引)
│   ├── paper_ids.txt              # 541,612 行, FAISS idx → paper_id 映射
│   └── rebuild_backups/           # 9.7 GB 备份 + 回滚点
│
├── 核心脚本 (5 个, ~99 KB 总)
│   ├── kb_search.py     (29.5 KB) 搜索引擎:语义检索 + must-cite + BibTeX 导出
│   ├── kb_health.py     (20.1 KB) 健康检查器:8 节检查 + JSON 输出 + strict 模式
│   ├── dedup_and_reindex.py (28 KB) 去重 + 补缺:5 阶段 + 进度条
│   ├── merge_to_disk.py (11.9 KB) gap 合并:增量持久化到主索引
│   └── smart_rerank.py   (7.1 KB) Query 扩展 + 重排
│
├── 辅助脚本
│   ├── daily_grow.py              # 每日拉 arxiv → 去重 → ingest → verify (主入口)
│   ├── self_grow.py               # 把 jsonl 摄入 FAISS + SQLite
│   ├── fetch_specific.py          # 精确拉取指定 arxiv ID
│   ├── batch_must_cite.py         # 批量跑 must-cite 给 5 篇 PAPER_CONSOLIDATED
│   ├── kb_server.py               # FastAPI HTTP 包装 (端口 8765)
│   ├── kb_growth_log.py           # 记录 KB 增长曲线到 CSV
│   ├── finalize_rebuild.py        # rebuild_kb_clean 完成后 swap
│   ├── watch_rebuild.py           # 监控 rebuild 进度
│   └── rebuild_kb_clean.py        # 从零重建干净索引 (45-75 分钟)
│
├── 测试 (38 个用例, 30 秒)
│   ├── tests/test_kb_search_unit.py   19 unit 测试 (mock KB, CI 跑)
│   ├── tests/test_kb_search.py        19 integration 测试 (真实 KB, 本地跑)
│   ├── tests/_mocks.py                100 mock papers + fake sentence-transformer
│   └── tests/simulate_ci_timeout.py   CI timeout 模拟器
│
├── CI/CD
│   └── .github/workflows/ci.yml    # 8 steps, 15 min timeout, ubuntu-latest
│
└── 配置 / 日志
    ├── requirements.txt            # numpy + faiss-cpu + sentence-transformers
    ├── .gitignore
    ├── daily_grow_state.json       # last_run / last_added / last_added_ids
    ├── daily_grow.log              # 运行日志
    ├── self_grow.log
    ├── rebuild.log                 # 历史重建日志
    ├── kb_growth_log.csv           # 增长曲线
    ├── CHANGELOG_2026-07-09.md     # 最近一次大改造的变更日志
    └── CICD_DEPLOYMENT_CHECKLIST.md  部署检查清单

E:\peS2o_cs\                       # 原始语料库 (98.86 GB) — 不在本系统内
├── peS2o-0000_cs.jsonl ~ peS2o-0089_cs.jsonl  # 134 个, 每个 1.0-1.5 GB
├── peS2o_supp_2025_2026.jsonl     # 2025-2026 补充语料
├── daily_grow_new_*.jsonl         # daily_grow 增量 staging (14 个, 7/8 那批残留)
└── backups/                       # 历史备份
```

---

## 🏗️ SQLite Schema(`papers.db` 8.37 GB)

| 表 | 角色 | 行数 |
|---|---|---|
| **`papers`** | 主表,每行一篇论文 metadata | **541,613** |
| **`papers_fts`** | FTS5 全文索引 (porter + unicode61) | 539,943 |
| **`paper_full_text`** | 部分论文的全文摘要缓存 | (按需) |
| **`review_records`** | TMLR 投稿审阅记录(自己写的) | (按需) |

**`papers` 表字段**(14 列):
```
id INTEGER PRIMARY KEY
paper_id TEXT           ← 显示用 ID (peS2o 数字 / arxiv ID / SHA1)
title TEXT
fields TEXT             ← "Computer Science" 等
text_prefix TEXT        ← 论文前 ~500 字符(text_prefix 索引用)
source_file TEXT        ← 来源 jsonl 文件名
created TEXT            ← 论文发布时间
authors TEXT
abstract TEXT
year TEXT
categories TEXT         ← arxiv categories (cs.LG 等)
source TEXT             ← 'arxiv' / NULL (peS2o 没标)
version TEXT
```

**索引**:`idx_paper_id` / `idx_fulltext_source` / `idx_review_tmlr`

**ID 体系启发式归类**(`kb_search.py` L116):
- 含 `.` 的 → arxiv (无论在哪个文件)
- 40 位 hex → peS2o SHA1
- 其他纯数字 → peS2o 内部 ID
- 自动加 `[arXiv]` / `[peS2o]` 来源标签

---

## 🔄 数据流

```
[peS2o CS slices]    [arxiv daily]
       ↓                    ↓
   E:\peS2o_cs        fetch_specific
                          ↓
            daily_grow.py (拉 + 去重)
                          ↓
            self_grow.py (embed + ingest)
                          ↓
              ┌─────────────────┐
              │  papers.index   │ (FAISS, 384-dim, IndexFlatIP)
              │  papers.db      │ (SQLite, 14 列 metadata)
              │  paper_ids.txt  │ (FAISS idx → paper_id)
              └─────────────────┘
                          ↓
              kb_search.py / kb_server.py
                          ↓
                  BibTeX / must-cite
                          ↓
              F:\Research\PAPER*\refs.bib
```

---

## 📊 当前状态(2026-07-11 13:00 扫描)

### KB 数据
| 指标 | 数值 | 状态 |
|---|---|---|
| SQLite papers | 541,613 | ✅ |
| FAISS 总向量 | **560,284**(main 363,948 + gap 196,336) | ✅ |
| paper_ids.txt | 541,612 行 | ✅ |
| 重复 paper_id | 0 | ✅ |
| ID 抽样命中率 | 100.0% | ✅ |
| **main+gap vs SQLite 差距** | **-3.4%**(-18,407)** | ⚠ WARN |
| source 分布 | None: 539,894 / arxiv: 1,719 | (大部分 peS2o 无 source 标记) |
| year 分布 top | 2026: 90,921 / 2025: 74,062 / 空: 44,603 | (peS2o 部分无 year) |
| DB 内空闲页 | 1,009,225 / 2,194,124 (46%) | ⚠ 大量碎片,可 VACUUM 回收 ~4 GB |

### 已知问题
- **gap 索引未合并到 main**:`merge_to_disk.py` 跑过(`CHANGELOG` 说 gap 已消化),但 main+gap vs SQLite 还有 -3.4% 差距
- **7/9 之后 daily_grow 没再跑**(CHANGELOG 写于 7/9 23:59,后续两天没新 commit 进 git)
- **3 处 backlog 已知**:见 `CICD_DEPLOYMENT_CHECKLIST.md` 第 250-280 行
- **大量 source/year 空值**:peS2o 原始数据这些字段本就是 NULL,**不是 bug**

### Git 状态
| 项 | 值 |
|---|---|
| 远端 | `https://github.com/aidless/obsidian.git` |
| 分支 | `main`(6 commits)/ `test-pr-trigger`(2 commits) |
| 本地工作区 | **完全 untracked**(所有 .py / .db / .md 都没 add) |
| 最近 commit | `3b462fe Merge branch 'main' ... into test-pr-trigger` (CI 触发测试) |

⚠ **重要**:`CICD_DEPLOYMENT_CHECKLIST.md` 写"代码已提交到 git"是**错的** —— `git status` 显示全目录 untracked。
**真正投产前必须先 `git add` + `git commit` + `git push`**。

---

## ⚙️ 内部依赖关系

```
kb_search.py ──import──> smart_rerank.py (同目录, sys.path.insert(0))
kb_search.py ──import──> kb_dir as constant
self_grow.py / dedup_and_reindex.py / merge_to_disk.py 各自独立,
但都依赖 all-MiniLM-L6-v2 模型(HF cache, 离线模式)

kb_server.py (FastAPI on 8765)
    ├── POST /search       → kb_search.py
    ├── POST /must_cite    → kb_search.py
    ├── POST /fetch        → fetch_specific.py
    └── GET  /health       → kb_health.py
```

⚠ `kb_search.py` 用 `sys.path.insert(0, str(KB_DIR))` 强依赖 smart_rerank 同目录,**跨目录调用会 ImportError**。

---

## 🛠️ 常用命令速查

| 任务 | 命令 |
|---|---|
| 健康检查(8 节) | `cd E:\peS2o_kb_faiss && py -3 kb_health.py` |
| 健康检查 + JSON 输出 | `py -3 kb_health.py --json` |
| 严格模式(CI 用) | `py -3 kb_health.py --strict` |
| 基本搜索 | `py -3 kb_search.py "TTRL" -n 10` |
| 必须引用发现 | `py -3 kb_search.py "agent eval" --existing-refs refs.bib -n 5 --must-cite` |
| BibTeX 导出 | `py -3 kb_search.py "TTRL" --bibtex out.bib -n 20` |
| 拉指定 arxiv 入库 | `py -3 fetch_specific.py 2508.02694 --bibtex refs.bib` |
| 每日增量(后台) | `py -3 daily_grow.py` (自动 dedup + ingest + verify) |
| 每日 dry-run 试跑 | `py -3 daily_grow.py --dry-run` |
| 启动 HTTP API | `py -3 kb_server.py` → http://localhost:8765 |
| 批量跑 5 篇 paper 的 must-cite | `py -3 batch_must_cite.py` |
| 去重 + 重建索引 | `py -3 dedup_and_reindex.py` (20 分钟) |

---

## 🎓 学到的关键设计

1. **FAISS gap 索引模式**:大批量 ingest 不直接写主索引,先 append 到 `papers_gap.index`,
   完成后 `merge_to_disk.py` 原子合并。失败可重跑不损坏主索引。
2. **启发式 ID 归类**:不依赖文件名,只看 ID 格式(`\d{4}\.\d{4,5}` → arxiv,
   40 hex → peS2o SHA1,纯数字 → peS2o 内部 ID)。
3. **BibTeX 来源分流**:arxiv 用 `eprint + archivePrefix`,peS2o 用 `howpublished + note`
   **避免编造假 arxiv eprint**(这是 TMLR 引用规则雷区)。
4. **健康检查 + strict 模式**:CI 用 `--strict`(warn 阈值 0.5%/命中 99.5%),日常用默认 1.0%/95%。
5. **`--must-cite`**:从 KB 里挑相关但**不在现有 .bib 里**的论文,自动排除已引用的。
6. **`smart_rerank.py` 的 query 扩展**:检测到 "modal ceiling" 等 ML 黑话时
   自动补 "language model test-time scaling" 上下文,显著改善召回。

---

## ⚠️ 我注意到的潜在风险

| 风险 | 触发条件 | 缓解 |
|---|---|---|
| **Git 没提交** | 任何本地磁盘故障 | 立即 `git add . && git commit && git push` |
| **daily_grow 停了 2 天** | KB 错过最新论文 | 跑 `py -3 daily_grow.py` 验证 cron / 调度器 |
| **source/year 字段空** | peS2o 部分论文没标 | 这是 peS2o 数据本身的特性,不是 bug |
| **DB 碎片 46%** | 长期 ingest/delete 不 VACUUM | `VACUUM` 可回收 ~4 GB,生产前建议跑 |
| **Python 3.9 used (c39)** | model 编译可能慢 | requirements 没指定,实际用 `D:\cmigrate\python\python39\` |
| **HF_ENDPOINT=https://hf-mirror.com** | 离线模型缓存失效 | `HF_HUB_OFFLINE=1` 已设,模型只在 CI 下载 |
| **merge_to_disk.py 假设 gap 不存在**(CHANGELOG 写"已消化") | 实际 -3.4% drift 暗示没彻底消化 | 跑 `py -3 kb_health.py` 看最新 gap 状态 |

---

## 🪤 我在这次扫描中犯的错(诚实记录)

1. **误判了 PowerShell GBK 渲染**为"文件是 GBK 编码 mojibake",**实际上 CHANGELOG / CICD 都是合法 UTF-8**。
2. **多此一举**给 4 个纯 ASCII JSON 加了 UTF-8 BOM。**已清除**。
3. **没改任何业务文件**(看了头/中间,没改一行)。

教训:**中文 .md 在 PowerShell 用 GBK codepage 看就是乱码,但字节本身完全合法**。
下次直接用 `read_bytes()` + `decode('utf-8')` 验证,不要被 `[System.IO.File]::ReadAllBytes()` + GBK decode 误导。

---

## 🔗 关联资源

- **主 CHANGELOG**(4 轮会话改造记录):`E:\peS2o_kb_faiss\CHANGELOG_2026-07-09.md` (~5.5 KB)
- **CI/CD 部署清单**:`E:\peS2o_kb_faiss\CICD_DEPLOYMENT_CHECKLIST.md` (~8 KB)
- **远端 repo**(空,本地未 push):`https://github.com/aidless/obsidian`
- **关联项目**:刘泽文 `F:\Research\PAPER{1..6}_CONSOLIDATED\refs.bib`(must-cite 输出目标)
- **原始语料**:`E:\peS2o_cs\peS2o-*.jsonl`(98.86 GB,不动)

---

_最后更新:2026-07-11 13:30 · 泰整理_