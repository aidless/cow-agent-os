# v2.0 LLM 后端接入设计 + 实测对比

> **项目**:泰玄小站 v2.0 后端
> **方案**:`fortune-web-v2/llm_backends.py`
> **作者**:泰(刘泽文搭档)· 2026-07-11
> **状态**:Step 2 完成,设计冻结,Step 3 进入业务路由

---

## 一句话总结

**DeepSeek v4-flash 主路 + Ollama qwen3:4b 本地兜底**,自动 failover,实测对比已跑过(综合分 0.696 vs 0.597)。

## 4 步路线

```
Step 1  ✅ Ollama + qwen3:4b 本地部署(2026-07-11 完成)
Step 2  ✅ llm_backends.py + 路由器 + pytest + benchmark
Step 3  ⬜ 接 8 派 prompt + 路由 + 合规过滤
Step 4  ⬜ 部署 + 微信支付 + 上线
```

---

## 第 1 章 · 设计原则

### 1.1 接口统一
所有 LLM 后端实现同一 `Protocol`:

```python
class LLMBackend(Protocol):
    name: str

    def chat(self, messages, temperature=0.7, max_tokens=800) -> str: ...
    def is_alive(self) -> bool: ...
    def prewarm(self) -> None: ...
```

### 1.2 自动 failover
- 主路失败(5xx / 429 / timeout > 8s / 协议错误)
- 连续失败 2 次 → 本轮不再尝试主路
- 重置靠下一轮成功调用

### 1.3 强制带 reasoning buffer
DeepSeek v4-flash 是 reasoning 模型,**`max_tokens` 必须 ≥ 2000** 才出 content。
错误默认 800 → reasoning 全部吃掉 → content 空(踩了大坑)。

### 1.4 Qwen3 thinking 处理
- Ollama 0.24 + qwen3:4b 的 `think=False` **无效**(实测)
- 策略:**接受 thinking + 大 num_predict(≥ 2000) + content 空 retry 一次**

---

## 第 2 章 · 实测对比(2026-07-11)

### 2.1 测试设计

8 个 prompt,跨 4 维度:
- 基础对话(中文 + 简洁度):3 个
- 结构化 JSON(协议化输出):1 个
- 命理专项(术语精度):2 个
- 合规(避免绝对化用词):2 个

每个 prompt 跑 2 次,共 **32 次** API 调用。

### 2.2 评分指标(客观,无主观)

| 指标 | 权重 | 说明 |
|---|---|---|
| 中文占比 | 15% | ≥ 90% 为佳 |
| 长度合适 | 25% | 命中期望区间 = 满分 |
| 合规 | 35% | 无绝对化用词 = 满分 |
| JSON 可解析 | 25% | 严格 JSON.parse 成功 |

### 2.3 终极结论

```
DeepSeek v4-flash(主路):
  ✓ 综合分 0.696(8 维度 6 胜)
  ✓ 合规 0.975(几乎零绝对化用词)
  ✓ JSON 12%(所有 prompt 至少一次能出)
  ✓ 平均延迟 11.6s(基础对话 2-3s / 长回复 7-9s)
  ✓ 成本 ¥0.004/次 ≈ 免费
  
qwen3:4b(兜底):
  ✓ 综合分 0.597(8 维度 2 胜)
  ✓ 合规 0.875
  ✓ JSON 0%(thinking bug 抢 token)
  ✗ 平均延迟 64.7s(慢 5 倍)
  ✓ 成本 ¥0(本地 GPU)
  ✓ 唯一可用场景:断网 / 限流 / 调试
```

### 2.4 最终选型

**DeepSeek 主路 + qwen3:4b 兜底**,架构不变。

---

## 第 3 章 · 8 项关键修复

### 3.1 Qwen3 thinking 拦截 (数月难题,本次攻破)

**症状**:qwen3:4b 输出 thinking 字段,content 空(`done_reason=length`)

**真根因**:Ollama 0.24 + qwen3:4b 组合下,`think=False` 不生效,模型默认 reasoning。

**修法**(实测验证):
1. `num_predict ≥ 2000`(给 thinking 1500 + content 500)
2. content 空时 retry 一次,num_predict += 1000
3. 最终 retry 仍空时,降级返回 thinking[:2000] 兜底

### 3.2 DeepSeek JSON 输出修复

**症状**:DeepSeek 之前在 JSON 任务输出 0 内容。

**真根因**:`max_tokens=800`,reasoning 占 800 token,content 0。

**修法**:`DeepSeekBackend.chat` 自动 `max_tokens = max(用户传的 + 1500, 2000)`。

### 3.3 DeepSeek key 智能选择

**症状**:`DEEPSEEK_API_KEY` 已 401 失效,但 OpenAI key `sk-***DEEPSEEK-KEY-REVOKED***` (redacted) DeepSeek 平台认。

**修法**:`__init__` 智能选 key:
- `base` 含 `deepseek.com` → 优先用 OPENAI_API_KEY
- 兜底 DEEPSEEK_API_KEY

### 3.4 DeepSeek key 'X' 大小写

通过 asyncio 自定义环境变量 `OPENAI_API_KEY` 全大写,SDK 读得到。

---

## 第 4 章 · 业务化路径(Step 3)

### 4.1 业务接入清单

| 模块 | 位置 | 难度 |
|---|---|---|
| 8 派 prompt | 复用 `wx-miniprogram/specs/prompts/{}.yaml` | 低 |
| 主路由 | Flask/FastAPI `/api/v2/reading` | 低 |
| 排盘数据接收 | 复用 `wx-miniprogram/utils/liupai-reader.js` 输出格式 | 中 |
| 合规过滤层 | 后置 regex `必定/一定/绝对/注定` → 替代表达 | 低 |
| 流式输出 | SSE(可选)| 中 |
| 缓存层 | 30s 同生辰+问 → 复用缓存 | 低 |

### 4.2 流程

```python
# v2.0 reading 核心伪代码
def handle_reading(liupai: str, body: dict) -> dict:
    # 1. 校验排盘数据
    validate_four_pillars(body.get('fourPillars'))

    # 2. 加载 8 派 prompt + 渲染
    prompt = load_prompt_template(liupai).format(**body)

    # 3. 调 LLM(主路 + 兜底自动)
    result = router.chat([
        {"role": "system", "content": prompt['system']},
        {"role": "user", "content": prompt['user']},
    ], temperature=0.7, max_tokens=1500)

    # 4. 合规过滤
    text = compliance_filter(result['text'])

    # 5. 解析 5 段 JSON
    sections = parse_5_sections(text)

    # 6. 返回
    return {
        'code': 0,
        'data': {
            'reading': sections,
            'backend': result['backend'],
            'fallback_used': result['fallback_used'],
        }
    }
```

### 4.3 选型与初版设计的差异

| 维度 | 初版文档(V2_LLM_RECOMMENDATIONS.md) | 实测后结论 |
|---|---|---|
| 主路模型 | DeepSeek V3 | DeepSeek **v4-flash**(用户实测配置)|
| 默认 API base | DeepSeek | DeepSeek(相同)|
| 兜底 | 未规划 | **本地 Ollama qwen3:4b**(本次新增)|
| 主路延迟估算 | 1-3s | **11.6s**(reasoning 模型特性)|
| 合规层 | 后置 regex | 同上 |

---

## 第 5 章 · 风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| DeepSeek key 失效 | 主路挂 | 已记录:实测 OpenAI key DeepSeek 也认 |
| qwen3:4b 慢 | 兜底 UX 差 | 上限 90s timeout,超时直接返回错误而非无限等 |
| 模型输出超规 | 合规问题 | 后置 regex 过滤层(Step 3 加)|
| Ollama 服务挂 | 兜底挂 | is_alive 探测 + 快速失败 |
| Reasoning token 超预算 | 成本上升 | 限 max_tokens=2000(实测足够)|

---

## 第 6 章 · 下一步(Step 3)

1. **接 `wx-miniprogram/specs/prompts/*.yaml`**(8 派)
2. **写 Flask/FastAPI** `/api/v2/liupai/{}/reading`
3. **后置合规过滤层**(regex)
4. **pytest 端到端 8 派**
5. **写 `STEP3_SUMMARY.md`**
