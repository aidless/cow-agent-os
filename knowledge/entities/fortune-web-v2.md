# fortune-web-v2 · 泰玄小站 v2.0 后端仓全图

> **项目**:泰玄小站 v2.0 商业化后端
> **仓根**:`C:\Users\Administrator\cow\fortune-web-v2\`
> **与 wx-miniprogram 的关系**:**独立仓**,不在 `wx-miniprogram` 仓内(避免污染前端 git)
> **作者**:泰(刘泽文搭档)· 2026-07-11
> **当前状态**:Step 2 / 4 完成(LLM 接入层完成,业务路由待 Step 3)

---

## 一句话定位

**泰玄小站 v2.0 后端**,核心职责是**调 LLM 生成 8 派命理解读**。
前端 `wx-miniprogram` 不直接调 API,**通过这个后端取协议化的 5 段 JSON 输出**。

## 4 步路线

```
Step 1  ✅ Ollama + qwen3:4b 本地部署
Step 2  ✅ llm_backends.py + 路由器 + pytest + benchmark
        ⬇ (当前)
Step 3  ⬜ 接 8 派 prompt + /api/v2/reading + 合规过滤 + 端到端
Step 4  ⬜ Flask/FastAPI 部署 + 微信支付 + 上线
```

## 文件清单(2026-07-11)

| 文件 | 行数估算 | 用途 |
|---|---|---|
| `llm_backends.py` | ~280 | 2 个 backend class + 路由器 + Protocol + CLI |
| `prompts/qwen3_system.txt` | ~12 | 4B 减负 system prompt(严格 JSON 5 段)|
| `tests/test_llm_backends.py` | ~80 | pytest 套件 |
| `benchmark_llm.py` | ~200 | DeepSeek vs qwen3:4b 对比测试框架 |
| `_run_benchmark.py` | ~15 | 临时设 env + 跑对比(测试 helper)|
| `_diag_*.py` | 多个 | 临时诊断脚本(可清理)|
| `_patch_*.py` | 多个 | 一次性 patch 脚本(可清理)|
| `README.md` | ~80 | 用法 + 环境变量 |
| `benchmark_*.json/md` | 各 ~30 KB | 对比测试报告 |

## 架构

```
┌────────────────────────────────┐
│  wx-miniprogram 前端           │
│  POST /api/v2/liupai/{}/...    │
└─────────────┬──────────────────┘
              ↓ HTTPS
┌────────────────────────────────┐
│  flask/fastapi(待 Step 4)     │
│  ┌──────────────────────────┐  │
│  │  LLMRouter               │  │
│  │  ┌────────────────────┐  │  │
│  │  │ DeepSeek v4-flash  │─主路│  │
│  │  │ + reasoning buffer│  │  │
│  │  └────────────────────┘  │  │
│  │       ↓ 失败/超时        │  │
│  │  ┌────────────────────┐  │  │
│  │  │ Ollama qwen3:4b    │─兜底│  │
│  │  │ + thinking retry   │  │  │
│  │  └────────────────────┘  │  │
│  └──────────────────────────┘  │
└────────────────────────────────┘
```

## 关键设计决策(实测后)

| 决策 | 选什么 | 为什么 |
|---|---|---|
| **默认 model** | `deepseek-v4-flash` | 用户实测配置 + 中文命理强 |
| **DeepSeek `max_tokens`** | 默认 2000+ | reasoning 占 50%+ token,800 不够 |
| **Qwen3 thinking** | 接受 + 大 num_predict | Ollama 0.24 + qwen3:4b bug,`think=False` 无效 |
| **Qwen3 retry** | content 空则 retry 一次 | content 0 + done=length 时再给 1000 token |
| **架构主路/兜底** | DeepSeek 主路 + 4B 兜底 | 综合分 0.696 vs 0.597,延迟 11.6s vs 64.7s |
| **路由降级触发** | 5xx / 429 / timeout > 8s | 用户拍板(B 选项决策)|
| **env LLM_MODE** | "fallback" 强制本地 | 调试用 |

## 实测数据(2026-07-11 benchmark)

| 维度 | DeepSeek | qwen3:4b |
|---|---|---|
| 综合分(加权)| **0.696** | 0.597 |
| 合规分 | **0.975** | 0.875 |
| JSON 可解析率 | **12%** | 0% |
| 平均延迟 | **11.6s** | 64.7s |
| 成本 | ¥0.004/次 | ¥0 |
| 胜出维度 | 6/8 | 2/8 |

## 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `OPENAI_API_BASE` | `https://api.openai.com/v1`(实际要改 DeepSeek)| 业务环境应改为 `api.deepseek.com/v1` |
| `OPENAI_API_KEY` | — | **关键:实测 DeepSeek 平台接受此 OpenAI key(`sk-366c2f4fd05b...4ffb`)** |
| `DEEPSEEK_API_KEY` | `sk-b19084...689c` | **注意:已 401 失效,平台不再认可** |
| `RR_MODEL` | `deepse***chat` | 历史设置,实际用 `deepseek-v4-flash` |

> ⚠️ **MEMORY.md Trap 1 警告**:hermes-agent env_config 存的 key OS env 看不到,**生产环境部署要么走真实的 OS env 设置,要么换 hermes-agent API 注入。**

## 已知坑(Step 2 实测)

| 坑 | 详情 | 修法 |
|---|---|---|
| Qwen3 thinking bug | Ollama 0.24 + qwen3:4b,`think=False` 无效 | 大 num_predict=2000 + content 空 retry |
| Qwen3 首次加载 | 30s+ | prewarm(用 /api/chat + "你好")|
| DeepSeek v4-flash reasoning | reasoning_tokens 占 50%+ | max_tokens ≥ 2000 |
| DeepSeek 不支持 `response_format=json_object` | v4-flash 不支持 | 靠 prompt 强约束 + system prompt |
| Python 中文嵌套双引号 | " 术语 " 会 SyntaxError | 用「」单引号或单引号字符串 |
| PowerShell UTF-8 BOM | 中文脚本无 BOM → 乱码 | `New-Object System.Text.UTF8Encoding $true` 写 BOM |
| Ollama 0.24 serve/app 分裂 | app.exe 不带 serve,pull 报 timeout | 单独跑 `ollama serve`(后台窗口)|

## 待清理

- `_diag_*.py` / `_patch_*.py`(一次性 helper)
- 旧的 `tmp/*.err` / `tmp/*.jsonl`(从别的步骤遗留)
- benchmark 输出可以归档到 `analysis/benchmark-2026-07-11.md`

## 相关

- 上游:[泰玄小站 entity](taixuan-miniprogram.md)
- 方案:[v2 LLM 后端设计](analysis/v2-llm-backend-design.md)
- 概念:[Ollama qwen3 thinking](concepts/ollama-qwen3-thinking.md)、[DeepSeek v4-flash reasoning](concepts/deepseek-v4-flash-reasoning.md)
- Spec Coding 实践:[wechat-mp-spec-coding](analysis/wechat-mp-spec-coding.md)
