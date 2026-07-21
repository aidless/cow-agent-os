# Awesome LLM Apps — 深度解析(2026-07-11)

> **⚫ 2026-07-11 历史快照** — 本页最后更新 2026-07-11 11:07,Shubhamsaboo/awesome-llm-apps 1751 文件深度解析。
> **7/11 之后未再访问**,本页**仅作历史参考**。GitHub 仓库本体仍活跃,可重激活。

> **仓库**:`Shubhamsaboo/awesome-llm-apps`(GitHub)
> **采集**:用户分享压缩包 `tmp/web_820918dd.zip`(68 MB,解压 83.8 MB,1751 文件)
> **定位**:100+ AI Agent / RAG / Voice / MCP 模板的"菜谱式"开源仓库
> **作者**:Shubham Saboo(blog:theunwindai.com)
> **许可证**:Apache-2.0

---

## 🎯 一句话定性

**不是 awesome-list(收藏清单),是 cookbooks(开箱即用模板)** — 每个项目独立运行、`pip install -r requirements.txt` 后 `streamlit run x.py`,单文件或 2-5 文件,大多 100-400 行代码,Apache-2.0 可商用 fork。

---

## 📊 全图盘点(1751 文件,78 项目,13 分类)

| 一级分类 | 子目录 | 项目数 | 文件数 | 代表作品 |
|---|---|---|---|---|
| `starter_ai_agents/` | 15 | **16** | 51 | ai_travel_agent · ai_meme_generator · xai_finance_agent |
| `advanced_ai_agents/multi_agent_apps/` | 14 | **16** | 432 | ai_home_renovation · multi_agent_researcher · ai_consultant |
| `advanced_ai_agents/single_agent_apps/` | — | **3** | 93 | (legacy single-agent templates) |
| `advanced_ai_agents/autonomous_game_playing_agent_apps/` | — | **1** | 11 | (game-playing agents) |
| `advanced_llm_apps/` | 10 | **10** | 193 | chat-with-tarots · llm_optimization_tools · cursor experiments |
| `agent_skills/` | 4 | **4** | 39 | project-graveyard · advisor-orchestrator-worker · self-improving |
| `ai_agent_framework_crash_course/` | 2 | **2** | 250 | google_adk_crash_course(115 文件)· openai_sdk_crash_course(135) |
| `always_on_agents/` | 1 | **1** | 11 | always_on_hn_briefing_agent(ADK + Agent Runtime) |
| `generative_ui_agents/` | 7 | **7** | 517 | ai-mcp-app-builder(158 文件,最大)· ai-shadcn(105)· generative-ui-starter(77) |
| `mcp_ai_agents/` | 6 | **6** | 20 | notion_mcp_agent · browser_mcp_agent · multi_mcp_agent_router |
| `rag_tutorials/` | 23 | **23** | 98 | agentic_rag_with_reasoning · knowledge_graph_rag · vision_rag |
| `voice_ai_agents/` | 4 | **4** | 25 | insurance_claim_live_agent_team · customer_support_voice_agent |
| **合计** | **87** | **~93** | **1751** | 涵盖 AI Agent 现代栈 |

> 注:13 个一级目录,78 个独立子项目(README 说 "100+" 含子项目变体,如云/本地双版本)。

---

## 🧬 三大技术栈解剖(代表性项目)

### 1️⃣ Starter 层 · `ai_travel_agent`(Agno + Streamlit 双 agent 流水线)

```python
# 核心模式:researcher → planner 显式串行
researcher = Agent(name="Researcher", tools=[SerpApiTools()], model=OpenAIChat(id="gpt-4o"))
planner = Agent(name="Planner", model=OpenAIChat(id="gpt-4o"))

# 用户触发 → 串行调用
research_results = researcher.run(f"Research {destination} for a {num_days} day trip")
response = planner.run(f"Research Results: {research_results.content}\n\nCreate itinerary")

# 配套能力:icalendar 生成 .ics 日历文件下载
ics_content = generate_ics_content(response.content)  # 正则切 Day 1/2/3
st.download_button("Download Itinerary as Calendar (.ics)", ics_content, "travel_itinerary.ics")
```

**亮点 / 坑**:
- ✅ 显式上下文传递(`research_results.content` 注入 planner prompt)
- ✅ 配套 `local_travel_agent.py` 用 Ollama llama3.2,**云/本对照**
- 🪤 **local 版有 bug**:`researcher` 定义但**未调用**,实际只跑单步生成 — 跟 cloud 版能力不对等
- 🪤 **设计一致性陷阱**:starter 层很多项目都"声明了 tool agent 但没接入流程",这是低门槛模板的常见问题

### 2️⃣ Advanced Multi-Agent · `multi_agent_researcher`(Agno `Team` 自动编排)

```python
# 3 个 specialized agent + 1 个 Team 容器
hn_researcher = Agent(name="HackerNews Researcher", tools=[HackerNewsTools()])
web_searcher = Agent(name="Web Searcher", tools=[DuckDuckGoTools()])
article_reader = Agent(name="Article Reader", tools=[Newspaper4kTools()])

# 关键:用 Team 而不是手写 pipeline,让 LLM 自己协调
hackernews_team = Team(
    members=[hn_researcher, web_searcher, article_reader],
    instructions=[
        "First, search hackernews for what the user is asking about.",
        "Then, ask the article reader to read the links for the stories to get more information.",
        # ↑ 自然语言指令定义执行顺序
    ],
    markdown=True,
    debug_mode=True,        # 调试模式:暴露中间步骤
    show_members_responses=True,  # 显示每个 agent 的输出
)
response = hackernews_team.run(query)
```

**亮点**:
- ✅ **Agno Team 模式** = OpenAI Swarm 的等价物 — instructions 用自然语言定义协调规则,LLM 当 orchestrator
- ✅ `debug_mode=True` + `show_members_responses=True` 让中间步骤透明,教学价值高
- ✅ 模型全用 `gpt-4o-mini`,成本低

### 3️⃣ RAG 代表 · `agentic_rag_with_reasoning`(Gemini + LanceDB + ReasoningTools)

```python
# 三件套:知识库 + Agent + 双面板 streaming
kb = Knowledge(
    vector_db=LanceDb(uri="tmp/lancedb", search_type=SearchType.vector,
                      embedder=OpenAIEmbedder(api_key=openai_key))
)
agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    knowledge=kb,
    search_knowledge=True,
    tools=[ReasoningTools(add_instructions=True)],  # ← 让 agent 强制 step-by-step 思考
    instructions=["Include sources in your response.", "Always search your knowledge before answering."],
)

# 双面板 streaming:reasoning + answer
for chunk in agent.run(query, stream=True, stream_events=True):
    if hasattr(chunk, 'reasoning_content') and chunk.reasoning_content:
        reasoning_placeholder.markdown(chunk.reasoning_content)
    if hasattr(chunk, 'content') and chunk.content:
        answer_placeholder.markdown(answer_text += chunk.content)
    if hasattr(chunk, 'citations') and chunk.citations:
        citations = chunk.citations.urls
```

**亮点**:
- ✅ **Gemini 2.5 Flash 作推理 + OpenAI Embedder 嵌入**(跨厂商组合,真·provider-agnostic)
- ✅ `ReasoningTools(add_instructions=True)` 强制 agent 走"先思考再回答"流程
- ✅ **流式 reasoning + 流式 answer 双面板** + citations 收集,UX 比 LangChain 的 chainlit 模板更好

---

## 🧩 Agent Skill 代表 · `project-graveyard`(质量天花板)

**与普通 prompt 模板的本质区别**:

```yaml
---
name: project-graveyard
description: >
  Scans the developer's machine for dead side projects, autopsies each one from
  its git history (died at the payments wall, killed by a newer project,
  finished but never shipped), surfaces their personal death patterns, and picks
  the corpse most worth resurrecting — then helps ship it.
license: Apache-2.0
metadata:
  author: "Shubham Saboo"
  version: "1.0.0"
  source: "https://github.com/Shubhamsaboo/awesome-llm-apps"
---
```

**结构 = Claude Code / Codex Skill Spec**:
- `SKILL.md`(10.7 KB)— frontmatter + when-to-use + run-it + reading-the-report + writing-the-tombstone-report + the-autopsy-interview + the-resurrection + necromancer-mode
- `references/causes-of-death.md`(4.6 KB) — 9 类死因的 signal/confidence/resurrection-angle 知识库
- `scripts/graveyard.py`(24 KB) — 纯本地 git scan,never writes inside scanned repo,支持 `--days` `--json` `--me` `--include-foreign` `--state` 5 个 flag

**9 类死因**(完整复用价值极高):
| 死因 | 信号 | 复活策略 |
|---|---|---|
| `shiny_object` | 14 天内有更新的 sibling repo | 最健康,常成 chain-of-death |
| `deploy_fear` | README + 20+ commits 但无 deploy config | 最佳候选 — 工作已完成,ship 步骤只差 deploy |
| `payments_wall` / `auth_wall` | 最后 commit 触 stripe/oauth | 2024 的墙 2026 多被 managed service 吃掉 |
| `boilerplate_wall` | 60%+ touches 是 config 文件 | **复活 idea 而非 repo**,10 分钟 starter > 一周考古 |
| `rewrite_spiral` | 2+ rewrite/migrate commits | 复活计划第 1 步必须 freeze stack |
| `scope_explosion` | 100+ 文件、无 deploy、>1 月 | 复活 20% 那个 feature,其余埋葬 |
| `slow_fade` | 末 commit gap = median × 3+ | "兴趣死了,兴趣是 agent 不能 ship 的",closure 也是 feature |
| `unknown` | 都不匹配 | 读 README + 最后 commits 自己判 |

**墓碑卡片 ASCII 模板**(SKILL.md 直接给):

```
        .------------------------.
       /                          \
      |        tab-sensei          |
      |      Apr — May 2026        |
      |   54 commits · 12 days     |
      |                            |
      |   died of deploy fear      |
      |                            |
      |   "It worked. It just      |
      |     never shipped."        |
   ___|____________________________|___
      ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
```

**Epitaph 规则**(作者明文写出):
- ✅ 必 trace 回 evidence(例:"config ratio 78%"才能写 webpack 配置死)
- ❌ "too scared to ship"(刺人)— 接受 "It worked. It just never shipped"(刺模式)
- ✅ Dry beats wacky,One sentence,No puns unless earned
- ✅ 26-commit + finished README 但未 ship = small tragedy not punchline

---

## 🗣️ Voice Agent 代表 · `customer_support_voice_agent`(LLM-as-TTS-Instruction)

```python
# 3 个组件:TTS agent 生成 speech instructions + OpenAI TTS 音频化
tts_agent = Agent(
    name="Text-to-Speech Agent",
    instructions="""Convert processed documentation response into natural speech.
    Maintain proper pacing and emphasis. Handle technical terms clearly.""",
    model="gpt-4o-mini-tts"
)

# ↑ LLM 先生成 speech instructions(节奏、停顿、术语处理)
# ↓ 再用 gpt-4o-mini-tts 把 instructions + 文本 → mp3
audio_response = await async_openai.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice=st.session_state.selected_voice,  # 11 个 voice 选项
    input=processor_response,
    instructions=tts_response,  # ← LLM 生成的元指令
    response_format="mp3"
)
```

**架构特点**:
- ✅ **LLM-as-instruction-generator** — OpenAI TTS 的官方推荐用法(`instructions` 参数,模型是 gpt-4o-mini-tts)
- ✅ 11 个 voice 选项(alloy/ash/ballad/coral/echo/fable/onyx/nova/sage/shimmer/verse)
- ✅ RAG pipeline:Firecrawl 抓 → Qdrant 向量库 → Fastembed 本地嵌入 → OpenAI Embedding 后备
- ✅ Audio streamlit 内置播放 + 下载双按钮

**RAG + Voice stack**:`Firecrawl` + `Qdrant` + `Fastembed`(本地嵌入模型)+ `gpt-4o-mini-tts`

---

## 🔌 MCP Agent 代表 · `notion_mcp_agent`(MCP + Memory + History 三件套)

```python
# 关键 5 行:stdio spawn npx Notion MCP server
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@notionhq/notion-mcp-server"],
    env={"OPENAPI_MCP_HEADERS": json.dumps({
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28"
    })}
)
async with MCPTools(server_params=server_params) as mcp_tools:
    agent = Agent(
        tools=[mcp_tools],
        db=SqliteDb(db_file="agno.db"),       # ← SQLite 持久化 memory
        enable_user_memories=True,            # ← 跨会话 user memory
        add_history_to_context=True,
        num_history_runs=5,
    )
    await agent.acli_app(user_id=user_id, session_id=session_id,
                         stream=True, exit_on=["exit", "quit", "bye", "goodbye"])
```

**生产级要素全到位**:
- ✅ **MCP**:stdio spawn `@notionhq/notion-mcp-server`(官方 Notion MCP)
- ✅ **Memory**:`SqliteDb` + `enable_user_memories=True` 跨会话持久化
- ✅ **History**:`add_history_to_context=True` + `num_history_runs=5` 最近 5 轮注入
- ✅ **Session**:`user_id` / `session_id` UUID 化,多用户隔离
- ✅ **CLI**:`acli_app()` 而非 streamlit — 终端版,适合 backend automation

---

## 🏠 架构最复杂 · `ai_home_renovation_agent`(Coordinator/Dispatcher + Sequential Pipeline)

**4 层嵌套 + 6 个 custom tools**:

```
Coordinator (Root Agent)
    ├── Info Agent (quick Q&A)            ← 快速分支
    └── Planning Pipeline (Sequential)
          ├── Visual Assessor (image analysis)
          ├── Design Planner (specifications)
          └── Project Coordinator (rendering + roadmap)
```

**技术栈**:Google ADK + Gemini 3 Flash/Pro multimodal + 6 个 custom tools(google_search + estimate_renovation_cost + calculate_timeline + generate_renovation_rendering + edit_renovation_rendering + versioned artifacts)。

**支持 4 种场景**:照片+预算 / 房间+灵感图 / 纯文本 / 迭代 refinement(改色、改地板、加灯)。

---

## 🎓 双 framework 教程(ADK vs OpenAI Agents SDK)

| | `google_adk_crash_course/` | `openai_sdk_crash_course/` |
|---|---|---|
| 文件数 | 115 | 135 |
| 章节 | Starter agent · Structured outputs · Tools · Memory · Plugins · Multi-agent | Starter · Function calling · Tools · Memory · Evaluation · Swarm orchestration · Routing |
| 模型 | Gemini / 任意 model-agnostic | OpenAI 全家桶 |
| 模式 | Plugin / Sequential / Parallel / Loop | Handoffs / Swarm / Routing |

**对比定位**:
- ADK 更工程化(Plugin 系统、adk web UI、Google Cloud 集成)
- OpenAI SDK 更轻量(function calling 原生、Agents SDK Swarm)

---

## 🎨 Generative UI 集群(本仓库独有的亮点)

`generative_ui_agents/` 517 个文件,**最大子目录**,7 个项目:
- `ai-mcp-app-builder` 158 文件(最大单一项目)
- `ai-shadcn-component-generator` 105
- `generative-ui-starter-project` 77
- `ai-dashboard-canvas-agent` 70
- `ai-financial-coach-agent` 38
- `ai-deep-research-agent` 29
- `mcp-apps-generative-ui-showcase` 39

**特点**:**Agents 渲染交互式 UI 组件(forms/cards/charts/editable plans)而非纯文本** — 这是 Anthropic / OpenAI 主推的 Generative UI 方向(Artifacts、Apps SDK),仓库已经系统化做了 7 个范式。

---

## 🏗️ 框架依赖谱(以出现频次计)

| 框架 | 估计覆盖 | 角色 |
|---|---|---|
| **Agno**(原 phidata) | ~60% | Agent + Team + Knowledge + LanceDB 整合,**默认框架** |
| **Streamlit** | ~85% | UI 层,几乎所有 starter/advanced 项目 |
| **OpenAI Agents SDK** | ~15% | voice 项目的 TTS 编排 |
| **Google ADK** | ~5% | 旗舰 multi-agent(ai_home_renovation) + crash_course |
| **CrewAI** | 1-2 项目 | ai_services_agency 等少数 |
| **LangGraph / LlamaIndex** | 几乎不用 | 仓库主推 Agno 而非 LangChain 生态 |
| **MCP**(`mcp` Python SDK) | 6 项目 | browser / notion / github / multi-router |

**战略观察**:**作者押注 Agno**(原 phidata),把它作为"agent framework 整合平台",Agno `Agent` / `Team` / `Knowledge` / `LanceDb` 4 件套覆盖 80% 模板需求。Google ADK 是 secondary,因为 Gemini 是核心 multimodal 推荐模型。

---

## 💰 Provider-agnostic 实测验证

README 声称 "switch between Claude, Gemini, GPT, Llama, Qwen, xAI with a config change",实测代码里确实如此:

```python
# travel_agent.py 默认 GPT-4o
model=OpenAIChat(id="gpt-4o", api_key=openai_api_key)
# local_travel_agent.py 换成 Ollama
model=Ollama(id="llama3.2")
# agentic_rag_with_reasoning.py 用 Gemini
model=Gemini(id="gemini-2.5-flash", api_key=google_key)
# home_renovation_agent 用 Gemini 3 Pro multimodal
```

**唯一的 provider 锁定**:`OpenAIEmbedder` 在 RAG 项目里几乎都用(text-embedding-3),这是隐性 lock-in —— 切换 Qwen / Llama 嵌入需要替换 embedder。

---

## 📐 模板代码的统一模式

每个 starter/advanced 项目平均 100-400 行,**4 文件标准布局**:

```
project_name/
├── xxx_agent.py          # 主程序(单文件 or 多 agent)
├── README.md             # 用法 + 教程链接
├── requirements.txt      # 3-10 个依赖
└── (optional) variant.py # 云/本版本对照
```

**Streamlit UI 标准模式**:
1. `st.text_input("OpenAI API Key", type="password")` — 顶部拿 key
2. `if openai_api_key:` 守卫后初始化 agent
3. `st.spinner("...")` 包裹长任务
4. `st.session_state` 存对话历史
5. 结果区:Markdown / Audio / Download button / 引用列表

---

## 🎁 对刘泽文研究/小程序主线的复用价值

### 对 arxiv-tracker / rr-responder 研究主线
- **⭐⭐⭐ `project-graveyard` 的 SKILL.md + causes-of-death.md** —— 是 **agent skill spec** 的范本,值得改造成 `paper-graveyard` 复用同样的结构(finished-but-never-shipped / rewrite_spiral / scope_explosion 三类映射到 paper 上完全成立)
- **⭐⭐⭐ RAG with Reasoning 模板** —— arxiv-tracker 摘要 + 引用 + reasoning 面板的范式
- **⭐⭐ `multi_agent_researcher` 的 Team 模式** —— advisor-orchestrator-worker 直接借鉴

### 对微信小程序泰玄小站
- ❌ **不直接复用** — 命名空间完全冲突(命理类目不允许 self-improving / always-on / multi-agent teams 模式)
- ✅ **借鉴 `generative_ui_agents/` 的渲染范式** — 八派命盘如果改成"用户可编辑的 cards/charts"而不是纯文本,UX 跳一个档次(对应 8 派 schema 的 title/content/tone 已写好,接 GenUI 是下一步)
- ✅ **借鉴 `ai_home_renovation_agent` 的 4 场景模式**(照片+预算 / 房间+灵感图 / 纯文本 / 迭代 refinement)— 命理 8 派也有同样的"4 输入模式"

### ✅ 实际落地印证 — 7/11 paper-graveyard 已派生(2026-07-11 11:15 完工)

**派生路径**:`Shubhamsaboo/awesome-llm-apps/agent_skills/project-graveyard`(Apache-2.0)
→ `F:\Research\.graveyard\`(本地 4 phase 落地)

| 复用维度 | awesome-llm-apps 提供 | paper-graveyard 落地 |
|---|---|---|
| SKILL.md 骨架 | 13 段结构 + frontmatter 模板 | **完全复用,改 paper 适配**(name/description/example/flag) |
| causes-of-death.md | 8 类 code 死因 + signal/confidence/angle | **派生 9 类 paper 死因**(原版 8 类适配 + 新增 reviewer_killed / deadline_missed) |
| ASCII 墓碑卡片 | `tab-sensei` 范例 | **完全复用,字符级一字未改** |
| epitaph 规则 | 4 条(traceable/punch-pattern/dry/respect) | **完全复用 + paper-specific example** |
| `--days/--json/--state` flag | 5 个原版 flag | **复用 + 新增 `--paper-dir/--min-files/--include-hash/--include-ids`** |
| Python stdlib scanner | 540 行原版 | **精简 ~31 KB paper 版**(纯 pathlib,无 git subprocess 强制依赖) |
| noise filter | 无(原版靠 git commit 历史过滤) | **v0.2 新增**:3 regex + file-count gate,96→33 真实 paper |
| 测试 | 无(原版无 unittest) | **v0.2 新增**:25 unittest 全过 |
| 联动 | 无 | **v0.2 新增**:`combine_reports.py` × paper-changelog |

**关键验证**(2026-07-11 10:00-11:15 实际跑通):
- ✅ 4 phase 全部 user-driven(每次"继续"驱动 1 phase),决策密度高
- ✅ Apache-2.0 合规:SKILL.md frontmatter 显式标 `source` + `source_license`
- ✅ **25/25 unittest 全过**(unittest 走 stderr,需 redirect 2>&1 才能看到)
- ✅ 与 paper-changelog 联动产出 `paper_dashboard.md`(.json)+ 高优先级复活候选表
- ✅ noise filter 把 96 个原始目录筛到 33 个真实 paper(剔除 arxiv-id / hash / crawler cache)

**v0.2 改进点(留给下次)**:
1. mtime fallback 下 lifespan 估算失真(都成 1 day)— 需要真实 git log
2. reviewer_killed / deadline_missed 检测纯靠 commit message 关键字
3. paper-changelog 的 🟠/🔴 列表和 graveyard noise filter 后交集空 — 后续可对齐分类

---

## 🪤 已识别的仓库质量问题

1. **🪤 local 版 bug 不少** — `local_travel_agent.py` 定义 researcher 但不调用,等价于少了 search 能力(对比 cloud 版验证)
2. **🪤 requirements 漂移** — 部分项目缺 `streamlit`(虽然代码用),如 `rag_tutorials/rag_chain/`
3. **🪤 README "100+" 包含双版本** — 实际独立项目 78 个,云/本各算 +1
4. **🪤 Crash Course 路径混乱** — `ai_agent_framework_crash_course/` 下 google_adk 和 openai_sdk 各自 100+ 文件,新手分不清

---

## 🔗 关联知识

- [arXiv-tracker 论文摘要流程借鉴](../concepts/arxiv-watch/arxiv-2026-07-10.md)— RAG with Reasoning 模板可改造
- [RR-responder 4 段 pipeline](../rr-responder SKILL.md)— 多 agent 协调模式可借鉴
- [泰玄小站 GenUI 升级路径](taixuan-miniprogram.md)— Generative UI agents 是下一阶段重点