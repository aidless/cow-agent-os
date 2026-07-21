# Ollama + qwen3:4b thinking 行为

> **用途**:泰玄小站 v2.0 本地兜底 LLM + 通用 LLM 部署经验
> **实测环境**:Windows 11 · RTX 3060 6GB · Ollama 0.24.0 · qwen3:4b(Q4_K_M)
> **实测日期**:2026-07-11

---

## 一句话总结

**qwen3:4b 是 reasoning 模型,默认开 thinking**。Ollama 0.24 上 `think=False` 字段不生效。**唯一稳定做法是大 `num_predict` + content 空 retry。**

---

## 行为解剖(实测)

### API 响应字段

调用 `/api/chat` 成功时返回:

```json
{
  "model": "qwen3:4b",
  "message": {
    "role": "assistant",
    "content": "...",          // ← 业务想要的输出在这里
    "thinking": "..."          // ← 思考过程(可空)
  },
  "done": true,
  "done_reason": "stop"|"length",
  "eval_count": 471
}
```

**关键洞察**:`thinking` 字段**有时是空字符串有时有内容**,但即使为空,模型可能在内部"消耗"了 token(就是 `eval_count` 用满但 `thinking.len()=0`)。

### `done_reason` 是关键信号

| done_reason | 含义 | 处理 |
|---|---|---|
| `stop` | 自然结束(可能 content 已有) | ✅ 返回 content |
| `length` | token 用光被截断 | ⚠️ content 可能空 → retry |

---

## 已知 bug:Ollama 0.24 + qwen3:4b 的 `think=False` 无效

测过 4 种 think 控制,**全部行为相同**:

```python
# options.thinking = False     → thinking 仍有, content 0
# options.think = False        → 同上
# options.think = "low"        → 同上
# 不设 think                   → 同上
# 都返回 done_reason=length, content=""
```

**唯一解锁方式(实测)**:用户 content 里塞 `/no_think` 前缀的话 **会让模型搞乱 token 序列**,反而更糟。

> 推测:Ollama 0.24 暂时未支持 qwen3 的 native thinking 控制(Qwen 后续版本才补上)。

---

## 实测稳态方案

### 后端代码模式

```python
class OllamaQwen3Backend:
    def chat(self, messages, temperature=0.7, max_tokens=800):
        messages = self._inject_system(messages)

        # 关键:思考至少占 1500 token,content 至少需要 max_tokens
        # 总 num_predict = max(max_tokens + 1500, 2000)
        desired_content = max(max_tokens, 400)
        num_predict = max(desired_content + 1500, self.default_num_predict)

        for attempt in range(self.retry_on_empty + 1):
            np_now = num_predict + (attempt * 1000)
            resp = self._do_chat_once(messages, temperature, np_now)
            content = resp["message"]["content"]
            thinking = resp["message"].get("thinking", "")

            if content.strip():
                return content
            if resp.get("done_reason") == "stop":
                return content or (thinking[:2000] if thinking else "")

        # 全 retry 失败,降级返回 thinking 前 2000 字
        if resp.get("message", {}).get("thinking"):
            return resp["message"]["thinking"][:2000]
        raise RuntimeError("空内容 + 无 thinking 兜底")
```

### 关键参数表

| 参数 | 推荐值 | 理由 |
|---|---|---|
| `num_ctx` | 4096 | 6GB 卡安全上限 |
| `default_num_predict` | 2000 | thinking 至少 1500 |
| `retry_on_empty` | 1 | 多 retry 意义不大,腾给其他后端 |
| `temperature` | 0.7 | 业务温度 |
| `timeout` | 120s | 6GB 卡最大等待 |

---

## 性能参考(RTX 3060 6GB)

| 任务 | num_predict | 实际耗时 | 输出长度 |
|---|---|---|---|
| 短答(50-100 字) | 2000 | 15-25s | 60-100 |
| 长答(500-800 字) | 2000 | 30-60s | 500-800 |
| 短答 + retry | 3000 | 50-80s | (触发 retry) |
| **首次 prewarm** | 50 | **30s**(加载到 VRAM) | 50 |

> 首次 prewarm **必须做**——否则用户首次请求等 30s+ 心理上像挂了。

---

## 何时该换 Qwen3 别的版本

| 场景 | 推荐 |
|---|---|
| 6GB 卡本地兜底(泰玄小站)| **qwen3:4b**(本方案,稳态)|
| 12GB+ 卡,有预算 | `qwen3:8b` 更好(慢但更强)|
| 24GB+ 卡(我) | `qwen3:14b` 推理强 |
| 4GB 卡(老机器) | `qwen3:1.7b` 勉强够 |
| 服务器级 | `qwen3:32b` 或更大 |

---

## 相关坑(MEMORY 链接)

- `RULE.md` · Ollama 部署铁律
- `RULE.md` · PowerShell UTF-8 BOM 铁律
- `concepts/deepseek-v4-flash-reasoning.md` · 对照的云端 reasoning 经验
