# LangChain Deep Agents v0.6.12 vs. hermes-agent — 架构对比

> **触发**: 2026-07-11 22:34, 刘泽文发来 `tmp/web_f61a6454.zip` (LangChain Deep Agents v0.6.12, 20.9 MB / 1208 文件) — "学习这个 Deep Agents, 看看跟我们的对比"。
>
> **方法**: 解压到 `tmp/_inspect/deepagents-0.6.12/` (43.9 MB), 只读扫描 4 个核心模块 (graph / middleware / backends / profiles) + evals 目录, 不装、不跑。
>
> **核心定位**: Deep Agents 是 LangChain OSS 的 **agent harness** (电池装好的代理框架), 用 LangGraph 做 runtime, 内置 sub-agent / filesystem / 上下文管理 / skills / 持久 memory / HITL / MCP / sandbox.

---

## 1. 一句话定位

| | Deep Agents v0.6.12 | hermes-agent (我们的栈) |
|---|---|---|
| **本质** | 开源 agent harness (batteries-included) | 自研 AI 助手 runtime (按工具调用 + 记忆文件) |
| **底层** | LangGraph (StateGraph 流式 + checkpoint + delta channel) | hermes-agent 自研 dispatcher |
| **默认模型** | Claude Sonnet 4.6 (`_build_default_model`) | MiniMax-M3 (我们当前用的) |
| **打包方式** | monorepo (acp / cli / code / deepagents / evals / partners / talon) | 单进程 + skills/ 目录 + memory/ 文件夹 |
| **License** | MIT | 自用 |

---

## 2. 架构骨架 — `create_deep_agent()` 的 middleware 装配顺序

> 这是 Deep Agents 最值得借鉴的"工程化"设计。从 `graph.py:228-260` 抓到原文。

**Base stack** (7 层, 不可拆):
```
TodoListMiddleware
  → SkillsMiddleware            (if skills=[...])
  → FilesystemMiddleware        (强制的, 不可 exclude — "required scaffolding")
  → SubAgentMiddleware          (强制的, 不可 exclude)
  → SummarizationMiddleware
  → PatchToolCallsMiddleware
  → AsyncSubAgentMiddleware     (if async subagents)
```

**[USER MIDDLEWARE INSERTED HERE]** ← 这是扩展点

**Tail stack** (6 层):
```
profile.extra_middleware
  → _ToolExclusionMiddleware    (if profile.excluded_tools)
  → AnthropicPromptCaching      (unconditional, no-op for non-Anthropic)
  → BedrockPromptCaching        (if langchain-aws)
  → MemoryMiddleware            (if memory=[...])
  → HumanInTheLoopMiddleware    (if interrupt_on=...)
```

**关键 insight**:
- `_REQUIRED_MIDDLEWARE` 是**白名单**, 用户 exclude 时必须保留 `FilesystemMiddleware` + `SubAgentMiddleware`, 否则直接 `ValueError`。→ **这是把安全边界钉死在 API 层**
- "Additive merge" — user middleware 永远插在 base 后 / tail 前, 不允许替代, 只允许追加
- Prompt 装配也是 4 段式: `USER → (BASE|CUSTOM) → SUFFIX`, 顺序严格保证 USER 在最前 (用户指令优先)

**对比我们**:
- 我们没有显式 middleware stack — 工具调用是 `dispatcher → tool → result` 的扁平结构
- 工具是手动装载 (skills/ 目录 + 我在 prompt 里描述), 不是按需注入
- 没有"required vs optional"的边界控制

---

## 3. 中间件层对比 — `deepagents/middleware/` 13 个

> 按文件大小降序, 标记每个跟我们栈的对应。

| 文件 | 行数 | 字节 | 功能 | 我们对应 |
|---|---|---|---|---|
| `filesystem.py` | ~2900 | 107 KB | 文件系统中间件 (ls/read/write/edit/glob/grep) | ❌ 无对应, 我们用 `read`/`write`/`edit` 工具直接调 |
| `summarization.py` | ~2500 | 90 KB | 自动 + 手动压缩对话, offload 到 backend | 🟢 **同思路** — 我们 paper-review-toolkit v0.4 有 dynamic worker pool, 抄过它 |
| `skills.py` | ~1100 | 40 KB | 渐进披露 skill (Anthropic agent skills 模式) | 🟡 部分对应 — 我们的 `skills/<name>/SKILL.md` 是手抄它的格式 |
| `rubric.py` | ~900 | 33 KB | LLM-as-judge rubric grading | 🟢 **新洞察** — 我们 reviewer 模拟用类似思路, 但没结构化 |
| `subagents.py` | ~1000 | 37 KB | 同步 subagent dispatch via `task` tool | 🟡 部分对应 — 我们没显式 sub-agent 概念 |
| `async_subagents.py` | ~1000 | 38 KB | 远程/后台 subagent | ❌ 无 |
| `memory.py` | ~500 | 19 KB | AGENTS.md 文件加载到 system prompt | 🟢 直接对应 — 我们 `MEMORY.md` 是手写, 它是 YAML 多源合并 |
| `_state.py` | ~30 | 1.1 KB | private state fields | ❌ 无 |
| `_message_eviction.py` | ~200 | 6.8 KB | 消息逐出 | ❌ 无 |
| `_overflow_clip.py` | ~250 | 8.5 KB | 上下文溢出剪切 | ❌ 无 |
| `_fs_interrupt.py` | ~250 | 8.5 KB | 文件权限中断 | ❌ 无 |
| `_tool_exclusion.py` | ~70 | 2.3 KB | 按 profile exclude 工具 | ❌ 无 |
| `patch_tool_calls.py` | ~70 | 2.1 KB | 修补损坏的 tool_call | ❌ 无 |
| `permissions.py` | ~10 | 0.2 KB | (re-export 兼容) | ❌ 无 |

**重点**:
- **`skills.py` (40 KB) 借鉴价值最高**: 我们的 `knowledge-wiki` skill + `paper-review-toolkit` skill 都可以升级到"按需渐进披露"。当前是 `system_prompt` 里手动 list skills, 它是**按调用上下文动态注入**
- **`summarization.py` (90 KB)**: 我们的 `paper-review-toolkit v0.4` worker pool 的部分逻辑已经在抄它 (token counting + 压缩 + offload 到磁盘)
- **`rubric.py` (33 KB)**: **新洞察** — 我们 `rr-responder` skill 的 deep_critique.py 做的就是 LLM-as-judge, 但**没结构化为 CriterionPass/CriterionFail/CriterionEval**, 可以升级

---

## 4. 后端抽象 — `deepagents/backends/` 5 类

> 来自 `backends/__init__.py` + `backends/protocol.py`.

| Backend | 字节 | 做什么 | 我们对应 |
|---|---|---|---|
| `FilesystemBackend` | 49 KB | 本地文件系统, 真磁盘读写 + ripgrep 加速 | 🟢 直接对应 — 我们的工具就是这个 |
| `StoreBackend` | 29 KB | LangGraph Store 抽象 (跨 session 持久) | 🟡 部分对应 — 我们用 `MEMORY.md` + `memory/YYYY-MM-DD.md` |
| `StateBackend` | 14 KB | 内存中, 一次性 (测试 / 临时) | ❌ 无 |
| `CompositeBackend` | 29 KB | 多 backend 路由 (按 path prefix) | 🟢 **可借鉴** — 我们 wechat-mp-validation 的 plugin whitelist 思路一致 |
| `SandboxBackend` | 39 KB | 5 个 sandbox 集成 (Daytona/Modal/Runloop/Vercel/QuickJS) | ❌ 无 — 这是最大缺口 |
| `LangSmithSandbox` | 11 KB | LangSmith 云端 sandbox | ❌ 无 |
| `LocalShellBackend` | 16 KB | 本地 shell (有 timeout + ripgrep) | 🟡 部分对应 — 我们的 `bash` 工具 |
| `ContextHubBackend` | 13 KB | LangSmith Context Hub 检索 | ❌ 无 |

**关键 insight**:
- **`BackendProtocol` (~28 KB, abstract class)**: 这是核心。它定义了 `read/write/edit/ls/glob/grep/execute` 的统一接口, **每个 backend 实现一次**, 然后 `CompositeBackend` 按 path prefix 路由。比如:
  ```
  /workspace/*  →  FilesystemBackend(root_dir=/workspace)
  /sandbox/*    →  SandboxBackend(quickjs)
  /memory/*     →  StoreBackend(store=langgraph_store)
  ```
  → **这是我们当前最大的设计缺口** — 我们的工具是直接调 `read`/`write`/`edit`, 没有"按路径选后端"的统一抽象
- **`FilesystemPermission` 枚举**: read / write / edit / execute, 每个 backend 都支持, 在 `FilesystemMiddleware` 里统一 enforce。→ **可以原样抄到 hermes-agent**

---

## 5. Profile 系统 — `deepagents/profiles/`

> 这是 Deep Agents 最"工程化"的创新。从 `harness_profiles.py:75-100` 抓到核心。

### 5.1 两个 profile 类型

| 类型 | 做什么 | 注册函数 |
|---|---|---|
| `ProviderProfile` | 控制 **chat model 构造** (URL / key / headers / model_kwargs) | `register_provider_profile` |
| `HarnessProfile` | 控制 **agent runtime 行为** (system_prompt / excluded_tools / extra_middleware / general_purpose_subagent) | `register_harness_profile` |

### 5.2 `HarnessProfile` 字段 (来自 `harness_profiles.py`)

```python
@dataclass(frozen=True)
class HarnessProfile:
    name: str                                    # e.g. "anthropic-sonnet-4-6"
    base_system_prompt: str | None = None        # 替换 BASE 默认 prompt
    system_prompt_suffix: str | None = None      # 追加在最后
    excluded_tools: list[str] = field(...)       # 不暴露给 LLM 的工具名
    excluded_middleware: list[...] = field(...)  # 不装配的中间件 (但 protected 类不能 exclude)
    extra_middleware: list[AgentMiddleware] = field(...)
    general_purpose_subagent: GeneralPurposeSubagentProfile = field(...)
```

### 5.3 内置 5 个 HarnessProfile

来自 `profiles/harness/_*.py`:
- `_anthropic_opus_4_7.py` (3.4 KB)
- `_anthropic_sonnet_4_6.py` (3.2 KB)
- `_anthropic_haiku_4_5.py` (3.2 KB)
- `_openai_codex.py` (2.7 KB)

### 5.4 关键设计

- **Additive merge**: `register_harness_profile("anthropic-sonnet-4-6")` 后, **之前同名的 profile 字段不会被覆盖**, 新字段会 merge 上去
- **Protected scaffolding**: `FilesystemMiddleware` / `SubAgentMiddleware` 不能 exclude, API 层强制
- **匹配顺序**: 先精确匹配 model_name → 后 provider prefix → 后 fallback 到 base

### 5.5 跟我们对比

| | Deep Agents | 我们 paper-review-toolkit v0.4 |
|---|---|---|
| **profile 对象** | `HarnessProfile` dataclass | `WorkerTemplate` dataclass |
| **注册机制** | `register_harness_profile()` | `register_worker_template()` |
| **保护边界** | `_REQUIRED_MIDDLEWARE_NAMES` | ❌ 无 |
| **additive merge** | ✅ 是 | ✅ 是 (我们抄了) |
| **provider × harness 二维** | ✅ 解耦 | ❌ 一维 (worker 直接挂 model) |

**借鉴价值**: **高**。我们 worker profile 缺"protected scaffolding"概念 — 应该至少 hard-code 几个必备 worker 不允许 exclude.

---

## 6. Evals 体系 — `libs/evals/`

> 118 evals × 8 categories, 全在 `tests/evals/`.

### 6.1 8 个 category (来自 `EVAL_CATALOG.md`)

| Category | Evals 数 | 测什么 |
|---|---|---|
| `file_operations` | 13 | ls/read/write/edit/grep/glob |
| `retrieval` | 6 | 路径检索 + 内容定位 |
| `tool_use` | 53 | 单 tool / 2-6 tool 链 / 间接请求 |
| `memory` | 5 | cross-session recall |
| `conversation` | 4 | 多轮一致性 |
| `summarization` | 4 | 自动压缩 + offload |
| `unit_test` | ~30 | 框架内部 |
| `langchain/middleware` | ~5 | middleware 自身 |

### 6.2 4 个 model group (来自 `MODEL_GROUPS.md`)

| Group | Models | 用途 |
|---|---|---|
| `set0` | 29 models | 全量基线 (Anthropic 4 / OpenAI 4 / Google 4 / Baseten 6 / Fireworks 7 / Ollama 3 / Groq 0) |
| `set1` | 14 models | 中等覆盖 (去掉长尾模型) |
| `set2` | 10 models | 长尾 (Groq 4 / Ollama 4 / xAI 2) |
| `frontier` | 5 models | 顶级 5 个 (Claude Opus 4-6/4-7 / Gemini 3.1 Pro / GPT-5.4/5.5) |

### 6.3 关键 eval 设计 — `tool_use` 占 53 个

这一类**特别值得学**:
- `test_two_tools_*` / `test_three_tools_*` / `test_four_tools_*` / `test_five_tools_*` / `test_six_tools_*` — 不同 tool 链长度的覆盖
- `test_chain_search_then_email` / `test_chain_create_issue_then_notify` — 真实业务链
- `test_indirect_*` — 间接意图 (用户说 "schedule meeting" 但要拉 calendar / 找 oncall / 发邮件)
- `test_metric_ranking_*` / `test_alert_aggregation_*` — 数值推理

→ **这跟我们 paper-review-toolkit 的 worker pool ablation 思路一致**: 不是单 tool 测, 是测 tool **链** 的成功率 + cost。

### 6.4 跟我们对比

| | Deep Agents | 我们 paper-review-toolkit |
|---|---|---|
| **eval 数** | 118 | ~5 (verify_p[1-5].py) |
| **category 划分** | 8 类 | 无 |
| **model group** | 4 组 × 5-29 模型 | 2 模型 (Qwen + DeepSeek) |
| **chain 长度覆盖** | 1-6 tool | 1 (单 worker) |
| **radar 图** | `composite_radar.py` | ❌ 无 (我们做了 ablation_report 但静态 markdown) |

**借鉴价值**: **中**。`composite_radar.py` 可以抄 — 我们 worker pool 的 ablation 4 策略应该出雷达图。

---

## 7. 跟研究主线的 cross-cut

### 7.1 跟 paper #35 (USENIX Security — 行为回归)

**重叠点** (3 个):

1. **Sandbox 边界**: Deep Agents 的 `SandboxBackend` × `FilesystemPermission` × `HumanInTheLoopMiddleware` = 我们 #35 §6 (Defense Framework) 的 **"工具级信任 ≠ 模型级信任"** 分层思路
2. **`excluded_middleware` 白名单**: `_REQUIRED_MIDDLEWARE_NAMES` 强制保留 FS + SubAgent → 这是 #35 §3 (ABRTS Design) 想要的"安全契约"机制
3. **`summarization.py` 的 offload + 上下文压缩**: #35 §4 (Behavior Contract) 里的 "tiered memory" 原型

**新增 insight** (1 个):

- Deep Agents README 第 1 段明确写: **"Deep Agents follows a 'trust the LLM' model. The agent can do anything its tools allow. Enforce boundaries at the tool/sandbox level, not by expecting the model to self-police."** → **这就是 #35 §2 (Threat Model) 的核心论点**: 信任应该钉在工具/sandbox 层, 不是模型层。Deep Agents 自己也承认这个 → 给 #35 提供了**主流框架的实证支持**

### 7.2 跟 paper-review-toolkit (worker pool)

**重叠点** (3 个):

1. **Summarization Middleware**: 我们 w5 worker pool 抄过它的 token counting + 压缩 + offload
2. **HarnessProfile**: 我们的 `WorkerTemplate` 是精简版, 缺 protected scaffolding
3. **EVAL_CATALOG 8 类**: 我们 worker pool 的 ablation 应该按 8 类重新组织

**新增借鉴** (2 个):

1. **`CompositeBackend`**: 我们 worker pool 可以给每个 worker 配独立 backend (FS / State / 模拟)
2. **`RubricMiddleware`**: 我们 reviewer 模拟应该升级到结构化 CriterionPass/Fail/Eval + GraderResponse

### 7.3 跟 paper-graveyard (skill)

**重叠点** (1 个):

- **Skill format**: Deep Agents 的 `SKILL.md` (YAML frontmatter + markdown) ≈ 我们 `skills/<name>/SKILL.md` → **格式一致, 可以互读**

**新增借鉴** (1 个):

- **`progressive disclosure`** 模式: Deep Agents skills 按调用上下文动态注入 system prompt, **不是全量 list**。我们 skill 是手抄进 system prompt, 可以升级。

### 7.4 跟泰玄 v0.2 (wechat-mp)

**重叠点** (2 个):

1. **`CompositeBackend` × Plugin Whitelist**: 我们的 `policy.schema.json` (6 decision + 5 obligation) ≈ Deep Agents `BackendProtocol` × `CompositeBackend` 的 path-prefix 路由
2. **`FilesystemPermission` 枚举**: read / write / edit / execute → 我们的 scanner 检查清单可以直接对齐

**新增借鉴** (1 个):

- **StateBackend 用于测试**: 我们 v2.0 单元测试应该用 StateBackend 隔离, 不要直接写磁盘

---

## 8. 我们当前栈的 4 个最大缺口 (对比后)

| # | 缺口 | Deep Agents 的解 | 借鉴难度 | ROI |
|---|---|---|---|---|
| 1 | **没有统一的 Backend 抽象** — 所有工具直接调本地 FS | `BackendProtocol` + 5 backend + `CompositeBackend` 路由 | 中 (要重写工具层) | 🟢 高 |
| 2 | **没有 "protected middleware" 概念** — 用户可以关闭任何能力 | `_REQUIRED_MIDDLEWARE_NAMES` 白名单 + `ValueError` | 低 (10 行代码) | 🟢 高 |
| 3 | **没有真正的 sub-agent 机制** — 工具调用是扁平 | `SubAgentMiddleware` + `task` tool + `general_purpose_subagent` 默认 | 中 (要重写 dispatcher) | 🟡 中 |
| 4 | **没有 "trust the LLM" 边界模型** — sandbox 不存在 | `FilesystemPermission` + `SandboxBackend` + `HITL` | 高 (要建 sandbox) | 🟡 中 |

---

## 9. 我们栈的 4 个相对优势 (对比后)

| # | 优势 | Deep Agents 现状 | 备注 |
|---|---|---|---|
| 1 | **`MEMORY.md` + `memory/YYYY-MM-DD.md` 自动维护** | `MemoryMiddleware` 加载 AGENTS.md, 但**不自动写** | 我们更自动化 |
| 2 | **跨 session 接力** (DASHBOARD / STATUS.md / handoff) | ❌ 无 | 我们独有的协作模式 |
| 3 | **可审计脚本** (幂等 .ps1 + .json + .move_plan.json) | ❌ 无 | 我们有, LangChain 没有 |
| 4 | **多 LLM 真实对比** (Qwen n=10 live re-run) | `MODEL_GROUPS` 列表里有 29 个, 但只跑基线 | 我们的 verify-after-patch 是 ground truth 模式 |

---

## 10. 学到什么 — 5 条可立即抄的设计模式

| # | 模式 | 抄到哪 | 优先级 |
|---|---|---|---|
| 1 | **Middleware base + tail 装配顺序** + protected scaffolding | `hermes-agent` 的工具装载层 | 🟢 P0 |
| 2 | **`BackendProtocol` 抽象** + `CompositeBackend` 路由 | `paper-review-toolkit` 的 worker pool (每个 worker 配 backend) | 🟢 P0 |
| 3 | **`FilesystemPermission` 枚举** (read/write/edit/execute) | `wechat-mp-validation` 的 scanner 检查清单 | 🟢 P0 |
| 4 | **Skill progressive disclosure** (按调用上下文动态注入) | `knowledge-wiki` skill 升级 | 🟡 P1 |
| 5 | **`RubricMiddleware` 结构化评分** (CriterionPass/Fail/Eval + GraderResponse) | `rr-responder` skill 升级 | 🟡 P1 |

---

## 11. 学到什么 — 3 个**不**抄的反模式

| # | 反模式 | Deep Agents 怎么做的 | 为什么不该抄 |
|---|---|---|---|
| 1 | **依赖 LangSmith** | tracing / eval / deploy 全走 LangSmith | 我们有自研 toolchain, 切过去亏 |
| 2 | **prompt caching 平台锁** | Anthropic / Bedrock 双 middleware | 我们 MiniMax provider 不支持 cache, 抄了也没用 |
| 3 | **CLI / Code / ACP 三个独立 binary** | `deepagents_code` / `cli` / `acp` 重复造轮子 | 我们单一 runtime, 不需要这么多入口 |

---

## 12. 对研究主线 (PAPER1-6 + #35) 的具体建议

### 12.1 立即可加进 paper-review-toolkit 的引用

- **§3 Background — Agent harness 主流方案**: 引用 Deep Agents 作为"主流框架代表", 强调他们也承认 "trust the LLM" 模型
- **§4 Methodology — Worker profile 设计**: 引用 `HarnessProfile` 的 6 字段 + protected scaffolding, 对比我们精简的 4 字段
- **§5 Evaluation — Ablation 分类**: 借鉴 EVAL_CATALOG 8 类, 但**只挑 3 类 (file_ops / summarization / chain)** 因为我们 paper 是单 worker 不是 framework

### 12.2 加进 paper #35 的引用

- **§2 Threat Model**: 引用 Deep Agents README 第 1 段 + `_REQUIRED_MIDDLEWARE_NAMES` 设计, **作为"主流框架也承认"** 的证据
- **§3 ABRTS Design**: `FilesystemPermission` 枚举 + `excluded_middleware` 白名单 → 直接作为我们 §3.4 "Protected Action Surface" 的设计依据
- **§6 Defense**: `SandboxBackend` × `CompositeBackend` 路由 → 作为 §6 "Defense-in-Depth" 的实证

### 12.3 加进 paper-graveyard 的引用

- **skill format**: Deep Agents `SKILL.md` 是公开标准 (Anthropic agent skills), 我们 paper-graveyard 用的 `SKILL.md` 格式**已经一致**, 可以 cite "compatible with Anthropic agent skills spec"

---

## 13. 落地决策 (待刘泽文点头)

### 选项 A — 只读不抄 (最保守)
- ✅ 已读懂架构
- ❌ 不改任何 skill / agent
- 📦 把 `tmp/_inspect/deepagents-0.6.12/` 物理归档到 `tmp/_archive/`

### 选项 B — 抄 3 个 P0 设计到现有 skill
- ✅ 抄 1 (protected scaffolding) → `paper-review-toolkit` 升级 v0.5
- ✅ 抄 2 (BackendProtocol 抽象) → `paper-review-toolkit` worker pool
- ✅ 抄 3 (FilesystemPermission 枚举) → `wechat-mp-validation` scanner
- 📅 工时: ~6h / 1-2 天

### 选项 C — 全量升级 hermes-agent runtime
- 5 个 P0 + P1 全抄, 重写 dispatcher
- 📅 工时: ~3-5 天
- ⚠️ 风险: 改太多, 可能影响主线上所有 skill

**我的建议**: B — 性价比最高, 风险可控, 工时合理。

---

## 14. 副产品

- **解压路径**: `tmp/_inspect/deepagents-0.6.12/deepagents-deepagents-0.6.12/` (1208 文件 / 43.9 MB)
- **扫描耗时**: ~5 min (read 8 个核心文件 + powershell 扫 7 个目录)
- **写入**: 1 个 knowledge page (本文)
- **索引更新**: `knowledge/index.md` 加 1 行
- **MEMORY**: 不写 (这是参考资料, 不是工作进展)

---

## 15. 待回答的问题 (留给刘泽文)

1. **是否要全量升级 hermes-agent 的 middleware stack?** (建议先抄 3 个 P0)
2. **`BackendProtocol` 抽象是否要在 `paper-review-toolkit` 实现?** (我的建议: 实现, ~2h)
3. **`FilesystemPermission` 是否要成为 `wechat-mp-validation` v2.2 的新字段?** (我的建议: 加, ~1h)
4. **物理归档还是留着?** (建议归档, 留 7 天 quarantine)
5. **是否要把 Deep Agents 加进 arxiv-watch 的引用源?** (不建议, 它不是 paper)

---

*最后更新: 2026-07-11 22:55 · 泰 · 只读学习完毕, 未跑任何代码 / 未装任何依赖*