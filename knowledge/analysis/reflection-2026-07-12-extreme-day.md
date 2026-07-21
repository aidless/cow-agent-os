# 2026-07-12 极端工作日反思

## 一句话总结

**17+ 小时连续高强度输出,完成 5 篇论文审计 + taixuan-web v1.0/v1.1/v1.2 + 6 个 bug 修复 + 2 份 RFC + 7 份完工报告**。

---

## 📊 产出清单(今日)

| 类别 | 数量 | 详情 |
|---|---:|---|
| **代码 commit** | 4 | v1.0 / v1.1 流式 / v1.2 工程化 / docs |
| **新建文件** | 11 | Dockerfile / compose / 测试 / RFC / 完工报告 |
| **修改文件** | 20+ | app.py / 8 派 HTML / stream.js / ROADMAP 等 |
| **代码行数** | ~6000 行 | 含 prompts(8 派 YAML) |
| **Bug 修复** | 6 | 包括 1 个 🔴 路由错装饰 |
| **完工报告** | 3 | v1.0 / v1.1 SSE / v1.2 工程化 |
| **RFC** | 2 | 用户系统 v2.0 / umami 自托管 |
| **记忆同步** | 5 | MEMORY.md / knowledge/ / Obsidian / log.md |

---

## 🪤 今日最关键的 5 个学习

### 1. Python 装饰器从下往上应用 ⚠️

```python
@app.route("/path", methods=["POST"])
def _validate_question():  # ← 这被装饰了!不是 def reading_stream()
    ...

def reading_stream():
    ...
```

**症状**:重构抽 helper 时,把 `@app.route` 装饰的紧贴下一个函数定义,但中间插了 helper,导致装饰器装饰错对象。

**教训**:**重构 helper 时,先写 helper(无装饰器),再写 `@app.route` 装饰的主函数**。**最后跑一次 `app.url_map` 校验路由**。

**新规**:**写完 route 立刻用 `python -c 'from app import app; print(app.url_map)'` 校验**。

---

### 2. UTF-8 BOM 看不见摸不着但毒死人 ⚠️

```python
# PowerShell New-Item 默认加 BOM
# 头 4 字节 EF BB BF 22 22 22  (BOM + """)
# Python 解析时第一字符 U+FEFF → SyntaxError
```

**症状**:本地能跑, ECS 上 `python benchmark_llm.py` 报 SyntaxError U+FEFF。

**教训**:**写任何 .py 文件必查头 3 字节**。**统一用 `open(path, 'w', encoding='utf-8')` + 不带 BOM**。

**新规**:**PowerShell 写 .py 必显式 `New-Item -Encoding utf8NoBOM`**(或用 Python 写)。

---

### 3. 客户端 abort 用 AbortController,简单且优雅 ✨

```javascript
// 流式响应 fetch 加 signal
const controller = streamReading(url, formData, callbacks);
// 用户点"停止":controller.abort()
```

**不需要**额外的 fetch 包装、cancel token、EventSource 关闭逻辑。

---

### 4. 流式 SSE 的 4 步握手(开 / 推 / 结 / 存) 🤝

```
data: {"type": "start", "ts": ...}        # 开
data: {"type": "content", "text": "根"}   # 推(token-by-token)
data: {"type": "content", "text": "据"}
...
data: {"type": "done", "full_text": "..."} # 结
```

**SSE 协议简单但状态机明确**:每条 message 一行 `data: {...}\n\n`。

**配合 generator(Flask `Response(stream_with_context(generate()), mimetype="text/event-stream")`)完美**。

---

### 5. 限流先内存字典,gunicorn 多 worker 再说 🔒

```python
_rate_buckets = defaultdict(list)  # ip -> [ts1, ts2, ...]
```

**单进程**(dev server / 单 worker gunicorn)够用,代码 10 行。

**多进程**时换 Redis(`SET key EX` + `INCR`)。

**先做对,再做大**。**别提前优化**。

---

## 🪤 踩过的坑(必记)

| 坑 | 症状 | 修法 |
|---|---|---|
| scp 子目录不存在 | 12 文件只传 11 个 | `mkdir -p` 先建 |
| 浏览器缓存 v1.0 JS | 流式按钮不工作 | Ctrl+Shift+R 强刷 |
| `init_db()` 提前调用 | NameError | 移到 log 定义之后 |
| PowerShell `select -First` | 输出乱码但命令 OK | 看 stderr |
| Windows PowerShell `rm` | 不识别 | `Remove-Item` |
| Long line in PowerShell heredoc | shell 解析成 heredoc 输入 | 单行命令 |
| 装饰器错位 | 路由错绑到 helper | 写完路由必校验 |

---

## 🎯 今日核心数字

| 项 | 数值 |
|---|---|
| 总工作时 | **17h+** |
| GitHub commit | **5** 个(v1.0 / v1.1 / v1.2 / 2 个 docs) |
| 流式响应真实跑通 | ✅ |
| ECS 服务运行 | ✅(v1.1 上, v1.2 本地) |
| 浏览器实测 | ✅(流式 + 思考状态 + abort) |
| 安全审计 | ✅(0 漏洞) |
| Bug 总数修复 | 6 个 |
| 代码测试覆盖 | 19 个 unittest |

---

## 💡 反思:为什么能 17+ 小时持续

1. **目标分解**:每个小时有明确交付物(v1.0 / v1.1 / v1.2 / docs / RFC)
2. **反馈循环**:每步验证(浏览器 / curl / 单元测试)
3. **即时归档**:每个里程碑写完工报告 + 同步 Obsidian,**避免记忆负担**
4. **专注单一项目**:整个 day 聚焦 taixuan-web,没切换 ML 主线
5. **优先级清晰**:**先流式(用户感知)> 后优化(代码质量)> 再文档(沉淀)**

---

## ⚠️ 明日 / 下次必须做

1. **ECS 部署 v1.2**(分批 scp + supervisor restart + 5 个新 API 验证)
2. **如果 umami 部署**,先观察 ECS 内存余量(2GB 紧张)
3. **GitHub Actions CI** 写 lint + test(质量门禁)
4. **写"认真审阅项目"工具脚本**作为长期实践(每周一次)

---

## 🪤 自我警告(给未来的我)

| 警告 | 原因 |
|---|---|
| **17h 极端输出不可持续** | 身体需要休息,不是常态 |
| **代码 review 不能跳过** | 这次发现 6 个 bug,审计是必要的 |
| **写完代码必跑测试** | 单元测试今天才补,应该从一开始就写 |
| **完工报告 = 一次性记忆** | 不写报告 = 不记忆 = 浪费 |
| **不要"先做 v3.0"** | 用户系统 RFC 是触发条件驱动的,不是立即做 |

---

## 📈 长期价值

虽然今天累,**长期产出是真的**:

| 产出 | 价值 |
|---|---|
| taixuan-web v1.2 完整工程化 | **可部署的开源产品** |
| 流式 SSE | **可复用的 AI 推理体验** |
| SQLite 历史 | **未来用户系统的基础** |
| 用户系统 v2.0 RFC | **流量到达后的实施蓝图** |
| umami RFC | **数据驱动的决策依据** |
| 6 个 bug 修复 | **质量提升** |

---

_17h 极端工作日记 · 2026-07-12 23:50 · 反思沉淀完毕_

_结论:今天值得。明天休息。_