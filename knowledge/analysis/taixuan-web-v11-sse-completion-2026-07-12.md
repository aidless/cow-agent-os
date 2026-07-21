# taixuan-web v1.1 流式 SSE 完工报告(2026-07-12)

## 一句话总结

v1.0 升级到 v1.1,8 派解读支持流式输出(SSE),用户提交表单后第 1 秒开始有字出现,体感延迟从 15 秒降到 0 秒(感知上)。

## GitHub commits

| Commit | 内容 |
|---|---|
| `188fba7` | v1.1 流式 SSE 实现(12 文件,+953/-250) |
| `bf31076` | docs: ROADMAP 标记 v1.1 完成 |

## 端到端验证(2026-07-12 23:50)

浏览器实测:
1. http://116.62.69.83/liupai/bazi → 强刷清缓存
2. 填表(1990-05-15 14:30 + 问题"今年事业如何")
3. 提交 → 看到 loading 转圈 1 秒
4. 之后文字开始 **逐 token 推出来**(打字机效果)
5. 内容:"根据您提供的八字排盘信息... 2025 年(乙巳年)的事业运势..."
6. 末尾"格局"、"逆反"、"审视"等专业术语完整

**结论**:流式 SSE 完整工作,DeepSeek v4-flash 真实 LLM,8 派共用。

## 实施细节

### 后端 llm_backends.py (+140 行)

4 个 chat_stream() 方法:

- **DeepSeekBackend.chat_stream()**:DeepSeek 流式 API,逐 chunk yield text
- **OllamaBackend.chat_stream()**:Ollama 流式 NDJSON 解析
- **MockBackend.chat_stream()**:逐字 yield 模拟打字
- **LLMRouter.chat_stream()**:主路 → 失败 → 兜底 → mock 流式调度

### 后端 app.py (+65 行)

`/api/v2/liupai/<liupai>/reading_stream` SSE 路由:

```
data: {"type": "start", "liupai": "bazi", "ts": ...}\n\n
data: {"type": "chunk", "text": "根"}\n\n
data: {"type": "chunk", "text": "据"}\n\n
...
data: {"type": "done", "full_text": "...", "latency_sec": 12.5}\n\n
```

### 前端 static/js/stream.js (新建 67 行)

公共流式客户端:fetch + ReadableStream 解析 SSE,暴露 window.streamReading。

### 前端 templates/liupai/*.html × 8

JS 段 fetch 改 streamReading,边收边渲染。

### ROADMAP.md (新建)

完整规划 v1.1 / v2.0 / v3.0。

## Bug 修复

1. **app.py: LIUPAI 名字错** → 改用 `LIUPAI_IDS`(LIUPAI 没定义)
2. **app.py: build_messages 参数错** → 改为 `(name, form_data)`(原调用 `(cfg, form_data, name)` 参数顺序错)

两个 bug 都在第一次部署后 curl 测试中暴露,30 分钟内修完。

## 踩坑汇总

1. **scp 子目录不自动创建**:`/var/www/taixuan/static/js/` 不存在时,scp 报错。修法:`mkdir -p` 先建目录再传
2. **浏览器缓存 v1.0 JS**:3 分钟没出文字,强刷 `Ctrl+Shift+R` 解决
3. **PowerShell 输出编码**:`Select-Object -First N` 在某些命令返回非 UTF8 时报错,但 git 命令实际成功,看 stderr 即可
4. **Flask `name not in LIUPAI`**:变量名混淆,统一用 `LIUPAI_IDS` set
5. **function call 参数错位**:从 3 参变 2 参,容易记错。修法:每次 commit 前跑真实测试

## 用户价值

| 维度 | v1.0 | v1.1 |
|---|---|---|
| 用户体感延迟 | 15 秒 | 0 秒(立即开始) |
| 总耗时 | 15 秒 | 15 秒(不变) |
| LLM 调用方式 | 同步 | 流式 |
| 浏览器体验 | 转圈 → 突然出 | 打字机效果 |
| 8 派覆盖 | 全 | 全 |

**核心收益**:同样的 15 秒等待,用户感知完全不同(等 vs 看)。

## 下一步

按 ROADMAP:
- v1.1.1:umami 自托管(2h)
- v2.0:用户系统 + SQLite(14h,等流量)
- v3.0:付费 + PWA + i18n(22h)

## 文件清单

- `app.py` - Flask 主入口
- `llm_backends.py` - LLM 路由器
- `static/js/stream.js` - 流式客户端
- `templates/liupai/*.html` - 8 派模板
- `ROADMAP.md` - 路线图
- `README.md` - 项目说明(展示级 23.5KB)
- `DEPLOY.md` - 部署文档
- `CHANGELOG.md` - 版本日志
- `LICENSE` - MIT

_作者:刘泽文 · 2026-07-12 v1.1 上线_