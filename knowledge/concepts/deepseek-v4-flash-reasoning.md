# DeepSeek v4-flash · Reasoning 模型特性

> **用途**:泰玄小站 v2.0 主路 LLM + 通用 reasoning 模型调用经验
> **实测环境**:Windows · Python 3.11 · urllib(不依赖 openai SDK)
> **实测日期**:2026-07-11

---

## 一句话总结

**DeepSeek v4-flash 是 reasoning 模型**,**`max_tokens` 必须 ≥ 2000**,因为 reasoning 占 50%+ token。不支持 OpenAI 的 `response_format=json_object` 字段,只能靠 prompt 强约束。

---

## API 响应字段

```json
{
  "id": "...",
  "model": "deepseek-v4-flash",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "...",               // ← 业务想要的输出
      "reasoning_content": "..."       // ← thinking 过程(不暴露给用户)
    },
    "finish_reason": "stop"|"length"
  }],
  "usage": {
    "prompt_tokens": 92,
    "completion_tokens": 1940,
    "total_tokens": 2032,
    "completion_tokens_details": {
      "reasoning_tokens": 1532         // ← 关键:reasoning 占 1532 / 1940 ≈ 79%
    }
  }
}
```

### `usage.completion_tokens_details.reasoning_tokens`

**这是 reasoning 模型最重要的字段**——告诉你 thinking 占多少。

实测占比:
| 任务 | reasoning_tokens | total | 占比 |
|---|---|---|---|
| 简单 ping | 10 | 15 | 67% |
| 基础对话(一句话) | 200-300 | 300-500 | 60-70% |
| 长内容(2000 字) | 800-1500 | 1500-2200 | 50-65% |
| JSON 结构化 | 800-1500 | 1500-2000 | 50-75% |

> **保守估计:always 给 max_tokens = 期望 content × 2**

---

## max_tokens 调优实测

### 业务场景调优表

| 业务需求 content | max_tokens 建议 | 备注 |
|---|---|---|
| 100 字短答 | **500-800** | reasoning 至少 400 |
| 500 字长答 | **1500-2000** | reasoning 至少 800 |
| 800-1500 字输出 | **2500-3000** | reasoning 至少 1200 |
| JSON 5 段 2000 字 | **3000-4000** | reasoning 至少 1500 |

### 不调优会怎样

```python
# ✗ 错:以为 max_tokens=800 给的是"输出 800 字"
resp = call(max_tokens=800)
# 实测:reasoning 拿 800 token 思考, content = 0 字
# finish_reason="length"
# 返回用户一个空字符串
```

→ **这就是泰玄小站刚开始的坑**。

### 修法

```python
def chat(self, messages, temperature=0.7, max_tokens=800):
    # 用户传的 max_tokens 是"想要的 content"
    # reasoning 至少 1500
    # 实际请求给 max(用户 + 1500, 2000)
    effective_max = max(max_tokens + 1500, 2000)
    payload = {"max_tokens": effective_max, ...}
```

---

## 不支持的特性

### `response_format={"type": "json_object"}` ❌

实测返回:`HTTP 400 Bad Request`

> v4-flash 尚未支持这个字段。`v3` 系列可能支持,但实测都是 v4。

**应对**:不用 `response_format`,靠 system prompt 强约束(已实测成功):

```python
system_msg = """你是资深命理师,严格输出合法 JSON,不要任何额外文字。
格式:
{"summary":"...","sections":[{"title":"...","content":"..."}]}"""
```

### 流式输出

未实测(本项目当前用 SSE planned for Step 4),但理论上支持。

### Function Calling

未实测(泰玄小站暂不需要)。

---

## 关键 Bug 与修法

### Bug 1:默认 base URL 的 OpenAI 平台不可达

**症状**:`base=https://api.openai.com/v1` + OpenAI key → `WinError 10060` timeout

**真根因**:你机器在国内网络环境,OpenAI 官方直接连不上。

**修法**:把 `OPENAI_API_BASE` 改为 `https://api.deepseek.com/v1`。**DeepSeek 平台同时接受 OpenAI key**(实测 `sk-366c2f4fd05b...4ffb` 直接 200)。

### Bug 2:DEEPSEEK_API_KEY 实际失效

**症状**:`base=DeepSeek` + `DEEPSEEK_API_KEY`(`sk-b19084...689c`) → `HTTP 401 invalid`

**真根因**:DeepSeek 平台对这个 key 报 invalid,推测过期 / 余额 0。

**修法**:**不要用 DEEPSEEK_API_KEY**,用 `OPENAI_API_KEY`(实测有效)。

### Bug 3:为什么 `OPENAI_API_KEY` 在 DeepSeek 平台也认?

**推测**:DeepSeek 跟某些 OpenAI 兼容平台做 key 池互通。这条经验值得记入长期记忆——**任何 OpenAI 兼容平台的 key,试试 DeepSeek 能不能认**。

---

## 与 qwen3:4b reasoning 的对比

| 维度 | DeepSeek v4-flash | qwen3:4b (Ollama) |
|---|---|---|
| 端点 | `/v1/chat/completions` | `/api/chat` |
| reasoning 字段 | `reasoning_content` | `thinking` |
| Reasoning 控制 | 没字段控制(全开)| `think=False` Ollama 0.24 不支持 |
| max_tokens 行为 | 共享 content + reasoning | 共享 content + thinking |
| 速度(本机)| 1-3s 起,平均 11.6s(基础对话) | 30-60s(6GB GPU 慢)|
| 成本 | ¥0.004/次 | ¥0 |

---

## 调用代码模式(纯净 Python)

```python
import urllib.request
import json
import os

def call_deepseek(messages, max_tokens=800, temperature=0.7,
                  api_base=None, api_key=None):
    api_base = (api_base or os.environ.get("OPENAI_API_BASE") or
                "https://api.deepseek.com/v1").rstrip("/")
    api_key = (api_key or os.environ.get("OPENAI_API_KEY") or
               os.environ.get("DEEPSEEK_API_KEY"))

    # ★ 关键:补 reasoning buffer
    effective_max = max(max_tokens + 1500, 2000)

    payload = {
        "model": "deepseek-v4-flash",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": effective_max,
        "stream": False,
    }

    req = urllib.request.Request(
        f"{api_base}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))

    msg = body["choices"][0]["message"]
    return msg.get("content") or msg.get("reasoning_content", "")[:2000]
```

---

## 相关

- 上游: [v2 LLM 后端设计](../analysis/v2-llm-backend-design.md)
- 孪生: [Ollama qwen3 thinking](../concepts/ollama-qwen3-thinking.md) — 本地 reasoning
- 实测报告: `fortune-web-v2/benchmark_report_*.md`(每次跑都生成)
