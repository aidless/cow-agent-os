# 知识库使用指南

_本 README 是知识库的"使用手册" + "快速导航"。_

---

## 🎯 这是什么?

刘泽文的**结构化长期知识库**(`knowledge/`),通过 `MEMORY.md` + `memory/*.md` 实现跨 session 连续性。

**核心理念**:
- **每次对话都可能失忆**,但文件不会
- 知识应该可发现、可审计、可复用
- 不在对话上下文里"强行记"——写入文件

---

## 🗂️ 目录结构与用途

```
knowledge/
├── README.md          ← 本文件(用法说明 + 统计)
├── index.md           ← 知识库目录(快速导航,精简版 1.7 KB)
├── index-archive.md   ← 旧版目录归档(46 KB,7/11 详细列表)
├── log.md             ← 操作日志(审计追溯,54 KB)
│
├── analysis/          ← 深度分析(71 个文件,1.1 MB)
│   ├── Agent OS 系列 (7)            architecture-full / vulnerabilities / red-team ×2 / v8-review / critical-11 / triage
│   ├── P0 借鉴落地 (3)              deepagents-vs-hermes / p0-1 / p0-2-p0-3
│   ├── Paper #35 USENIX 草稿 (12)   §1-§9 + appendix-b + complete + abstract + proposal
│   ├── PAPER5 R1+R2 (5)             review-r1 / qwen-n10-rerun / mock-* ×2 / improvement-rfc
│   ├── 泰玄完工报告 (11)            v1.1 / v1.2 / v1.2.1 / v2.0 Phase1-4 / deploy-readiness / ECS deploy / watchdog
│   ├── 泰玄 RFC / 设计 (4)          ECS monitoring / umami / user-system / v2-llm-backend
│   ├── 泰玄 + 微信合规 (3)          mp-ai-content / mingli-categories / spec-coding
│   ├── 论文盘点 / 库存 (4)          papers-local / project-artifacts / research-dir / changelog ×2
│   ├── 论文 idea (3)                from-agent-os / from-taixuan-dev / vulnerabilities
│   ├── window 完工 (5)              w4 / w5 / w6 ×2 / windows-progress
│   └── 基础设施 / 反思 / llm-lab (6) cleanup / inference-trap / llm-lab ×3 / reflection
│
├── concepts/          ← 概念定义(9 个,38 KB)
│   ├── a2a.md / calibration.md / trust.md
│   ├── multi-agent-collaboration.md / differential-privacy.md
│   ├── deepseek-v4-flash-reasoning.md / ollama-qwen3-thinking.md
│   ├── plugin-whitelist-pattern.md / tdd-meta-test.md
│   └── arxiv-watch/    ← 自动监控数据
│       └── arxiv-2026-07-10.md(37 KB,556 行,只 7/10 一份)
│
├── entities/          ← 实体档案(9 个,90 KB)
│   ├── liu-zewen-research.md   ⭐ 研究全图
│   ├── taixuan-miniprogram.md  ⭐ 微信小程序项目(7/12 16:55,v1.x 历史)
│   ├── fortune-web-v2.md       ⭐ v2.0 后端仓(7/11 13:35,已全完)
│   ├── pes2o-kb-faiss.md       ⭐ 论文 KB
│   ├── genesis-master.md       ⭐ master 工程
│   ├── tools-2026-07-10.md     ⚫ 40 项目速览(7/11 历史快照)
│   ├── downloads-2026-07-10.md ⚫ 11 项目 30 秒说明(7/11 历史快照)
│   ├── awesome-llm-apps-2026-07-11.md ⚫ 1751 文件解析(7/11 历史快照)
│   └── zcode-skill-discovery.md
│
├── research/          ← 论文写作素材(9 个,71 KB)
│   ├── index.md / papers-full-inventory.md
│   └── paper{1,2,3,4,5,6,35}.md  ⭐ 7 篇 CONSOLIDATED 论文实体
│
└── sources/           ← 原始资料(1 个,58 KB)
    └── agent-os-architecture-full-2026-07-11.md ⭐ 完整方案
```

---

## 🚀 快速入口

### 📚 Agent OS Reference Architecture 系列(7/11 完成)
| 文档 | 用途 | 大小 |
|---|---|---|
| [V1→V8 完整方案](./sources/agent-os-architecture-full-2026-07-11.md) | 单文件回答"A2A 平台治理长什么样"(含 V8 §11-15 三刀闭合 + 红队 Harness) | 58 KB |
| [漏洞红队报告](./analysis/agent-os-vulnerabilities-2026-07-11.md) | 25 个真实漏洞 + 修复方案 | 28 KB |
| [研究 idea 挖掘](./analysis/research-ideas-from-agent-os-2026-07-11.md) | 15 个 paper 候选 | 22 KB |
| [idea 漏洞分析](./analysis/research-ideas-vulnerabilities-2026-07-11.md) | 第二轮红队 + 5 道筛子 | 19 KB |

### 📱 泰玄小站(7/12-13 完工系列)
| 文档 | 用途 |
|---|---|
| [v2.0 用户系统 RFC](./analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md) | 14h 任务分解,Phase 1-4 全完工 |
| [v1.2.1 + Layer 1 监控](./analysis/taixuan-web-v121-completion-2026-07-13.md) | ECS 自愈循环 |
| [Layer 2 Watchdog](./analysis/taixuan-web-watchdog-layer2-completion-2026-07-13.md) | Windows 桌面气泡通知 |
| [v2.0 部署就绪](./analysis/taixuan-web-v20-deploy-readiness-2026-07-13.md) | 部署脚本 + 10 项 checklist |
| [泰玄小程序 entity](./entities/taixuan-miniprogram.md) | v1.x 历史(7/12 后未更新) |

### 👤 个人 & 项目全图
| 文档 | 用途 |
|---|---|
| [刘泽文 — 研究系统全图](./entities/liu-zewen-research.md) | F:\Research 70 个子目录 + 5+1 篇 CONSOLIDATED 状态 |
| [泰玄小站 — 微信小程序](./entities/taixuan-miniprogram.md) | v1.x 历史快照(v2.0 完工报告在 analysis/) |
| [fortune-web-v2](./entities/fortune-web-v2.md) | v2.0 后端仓(已全完) |
| [peS2o KB](./entities/pes2o-kb-faiss.md) | 论文知识库 |
| [zcode skill discovery](./entities/zcode-skill-discovery.md) | skill 发现流程 |

### 📋 合规/上线专题
| 文档 | 用途 |
|---|---|
| [AI 内容合规 · 玄学赛道](./analysis/mp-ai-content-compliance.md) | AI 标识隐藏 + 禁词清单 + 备案模板 |
| [命理类目资质申请](./analysis/wechat-mp-mingli-categories.md) | 5 步硬门槛 + 双轨备案 |

### 🧪 实践/反思
| 文档 | 用途 |
|---|---|
| [Spec Coding 实践](./analysis/spec-coding-practice.md) | 泰玄小站 v2.0 体系总结 |
| [论文审阅工具箱](./analysis/paper-review-toolkit.md) | 3 工具 + 12 种审阅方式 |
| [基于推断踩坑反思](./analysis/inference-trap-2026-07-11.md) | AI 跨 session 失忆事件 |

### 🧬 概念速查(concepts/)
| 概念 | 文档 |
|---|---|
| Agent-to-Agent 协议 | [a2a.md](./concepts/a2a.md) |
| 校准(LLM) | [calibration.md](./concepts/calibration.md) |
| 信任体系 | [trust.md](./concepts/trust.md) |
| 多 Agent 协作 | [multi-agent-collaboration.md](./concepts/multi-agent-collaboration.md) |
| 差分隐私 | [differential-privacy.md](./concepts/differential-privacy.md) |
| DeepSeek V4-flash 推理 | [deepseek-v4-flash-reasoning.md](./concepts/deepseek-v4-flash-reasoning.md) |
| Ollama qwen3 thinking | [ollama-qwen3-thinking.md](./concepts/ollama-qwen3-thinking.md) |
| 插件白名单模式 | [plugin-whitelist-pattern.md](./concepts/plugin-whitelist-pattern.md) |
| TDD 元测试 | [tdd-meta-test.md](./concepts/tdd-meta-test.md) |

---

## 📖 使用规则

### ✅ 应该写入知识库的场景

1. **用户分享了文章/链接/文档** → `sources/<slug>.md`
2. **深度讨论产生了结论/方案** → `analysis/<topic>.md`
3. **重要实体(人物/项目/工具)** → `entities/<name>.md`
4. **技术概念/方法论** → `concepts/<topic>.md`
5. **论文写作素材** → `research/<paper>.md`

### ❌ 不要写入

- API 密钥 / 令牌 / 密码
- 单次小讨论(不够"知识"密度)
- 临时调试信息

### ✏️ 写入方式

- **新建文档**:`write` 工具(单文件 < 10 KB)
- **追加内容**:`edit` 工具(oldText 留空)
- **修改内容**:`edit` 工具(oldText 精确匹配)
- **大文档**:先 write 骨架,再 edit 多次追加

### 🔗 跨文档链接

用相对路径,如 `[方案](./sources/agent-os-architecture-full-2026-07-11.md)`。

---

## 🛡️ 维护规则

### index.md / log.md 维护(强制)

每次新建/重命名知识页面后,**必须更新 `index.md`** 添加索引行。
每次写入操作后,**必须追加 `log.md`** 一行记录(操作类型/路径/触发/关键内容)。

### 文件命名规范

- `slug-YYYY-MM-DD.md`(带日期,可识别新旧)
- `slug` 用英文连字符(如 `agent-os-architecture-full`)
- 多个相同主题带后缀(`-full` / `-vulnerabilities` / `-ideas`)

### 体检(每月或大幅改动后)

跑一次 `dir /B /S knowledge\*.md | findstr /v "index-archive"` 对比 README 统计表。
最近一次:**2026-07-13 20:55**(`tmp/knowledge_audit_2026-07-13.md`)

---

## 🧠 知识库 vs 记忆系统

| 系统 | 文件 | 用途 | 检索方式 |
|---|---|---|---|
| **长期记忆** | `MEMORY.md` | 核心事实/偏好/决策索引 | 会话开始自动加载 |
| **每日记忆** | `memory/YYYY-MM-DD.md` | 当天事件 + 进展 | `memory_get` 读取 |
| **结构化知识** | `knowledge/` | 可复用、可审计的知识库 | `memory_search` 或 `read` |
| **操作日志** | `knowledge/log.md` | 所有写入操作追溯 | 人工查阅 |

---

## 📊 当前知识库统计(2026-07-13 20:55 实测)

| 分类 | 数量 | 总字节 |
|---|---|---|
| analysis | 57 + 1 ps1(已移 tmp) | ~880 KB |
| concepts | 9 + 1 arxiv-watch | ~75 KB |
| entities | 9(含 3 个 ⚫ 归档) | ~95 KB |
| research | 9 + paper35/drafts/ 12 | ~180 KB |
| sources | 1 | ~58 KB |
| 目录文件(README/index/log) | 4 | ~135 KB |
| **总** | **~103 md + 1 ps1** | **~1,420 KB(~1.4 MB)** |

**已知失同步(待 P1 修)**:
- ✅ **(7/13 21:05 已修)**paper35 12 草稿已迁到 `research/paper35/drafts/`
- ✅ **(7/13 21:05 已修)**3 个 7/11 历史 entity 已加 ⚫ 归档 banner
- ✅ **(7/13 21:05 已修)**`_append_rfc_d_close.ps1` 已移到 `tmp/`

---

## 🔮 未来规划

### 已建待深挖(不再是"待建")

所有 README "待建" 项目 7/11-7/13 期间均已落地:
- ✅ `concepts/`:trust / calibration / multi-agent-collaboration / a2a / differential-privacy 全部建好
- ✅ `research/`:7 篇 CONSOLIDATED 论文 entity 全建好(paper1/2/3/4/5/6/35)
- ✅ `arxiv-watch/`:7/10 抓取报告已落(concepts/arxiv-watch/arxiv-2026-07-10.md,556 行)

### 下一步可做

- ✅ **(7/13 21:05 已完)** paper35 草稿重定位 + 3 个 7/11 entity 归档 banner + ps1 脚本重定位
- 🟡 **arxiv-watch 增量策略** — 7/10 之后未再抓取,要么恢复 arxiv-tracker,要么归档
- 🟡 **entities/taixuan-miniprogram 重写或归档** — 已加 banner,可选整页重写为 v2.0 实体
- ⚪ **Obsidian 双源同步** — 95 文件已同步,健康

---

_最后更新:2026-07-13 20:55_
_作者:泰(刘泽文的长期搭档)_
_体检报告:`tmp/knowledge_audit_2026-07-13.md`_