# taixuan-web v1.2 工程化优化完工报告(2026-07-12)

## 一句话总结

v1.1 基础上做 10 项工程化优化 + 6 个 bug 修复,GitHub commit `5405cee`,本地完整,ECS 待传。

## v1.2 改动统计

| 类别 | 改动 |
|---|---|
| **新文件** | `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `.env.example`, `tests/test_app.py`(5 个) |
| **修改文件** | `app.py`, `llm_backends.py`, `benchmark_llm.py`, `static/js/stream.js`, 8 派 HTML(11 个) |
| **代码量** | +600 行 / -200 行 |
| **GitHub commit** | `5405cee`(v1.2 feat) |

## 10 项工程优化详解

### 1. gzip 压缩
- `app.py` after_request 中 gzip_response 处理器
- 触发条件:文本 / JSON / JS + Content-Length > 1KB + 客户端支持 gzip
- 跳过 SSE 流式(实时性重要)
- 压缩级别 6(平衡 CPU 和压缩率)

### 2. 静态资源缓存
- `/static/*` → `Cache-Control: public, max-age=3600`(1 小时)
- `/api/*` → `Cache-Control: no-store`(API 不缓存)
- 其他不设

### 3. TEMPLATES_AUTO_RELOAD 关
- 生产模式默认关(避免每次请求检查 mtime)
- 仅 `FLASK_DEBUG=1` 时开

### 4. 日志轮转
- `taixuan-web.log`: 10MB × 5 backups
- `llm-audit.log`: 50MB × 3 backups(LLM 调用审计,体积更大)
- `logging.StreamHandler()` 保留(console)

### 5. CSP / HSTS / X-Frame 安全 headers
- `Content-Security-Policy`: default-src 'self' + script/style unsafe-inline(允许内联 JS)
- `X-Frame-Options: DENY`(防 clickjacking)
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: 关 geo/mic/camera`

### 6. 限流(防 LLM 滥用)
- 每 IP 每分钟 10 次(可配 `RATE_LIMIT_PER_MIN`)
- 内存字典实现(单进程,够用)
- 触发后返回 429 + `detail` 字段
- 应用到 `api_reading`, `reading_stream`, `liupai_form`

### 7. 客户端 abort 按钮
- 每个 HTML 模板 loading 区加"停止"按钮
- `stream.js` v3.0:返回 `AbortController`
- 用户中止不报错,优雅退出

### 8. SQLite 历史记录
- 新表 `readings`:liupai / client_ip / question / form_json / response_text / reasoning_text / backend / latency_sec / chunk_count / status / created_at
- 3 个 API:`/api/v2/history?limit=10` 列表 + `/<id>` 详情 + `/stats` 统计
- 索引:created_at + liupai
- 写入失败不抛异常(不影响主流程)

### 9. Docker 化
- `Dockerfile`:Python 3.11-slim 多阶段 + 非 root 用户 + 健康检查 + gunicorn 4 worker
- `docker-compose.yml`:单服务编排 + 可选 umami + 持久化 logs 目录
- `.dockerignore`:排除 .git / .env / venv / logs / db / _archive 等

### 10. .env.example 配置模板
- 注释完整,复制为 .env 填值即可
- 不提交到 git(.gitignore 已排除)

## 6 个 Bug 修复(严重度排序)

### 🔴 Bug 1:benchmark_llm.py UTF-8 BOM
- **症状**:`python benchmark_llm.py` 报 SyntaxError U+FEFF
- **原因**:PowerShell `New-Item -Encoding UTF8` 默认加 BOM
- **修法**:写脚本 `tmp/_strip_bom.py` 批量扫 + 去 BOM

### 🔴 Bug 2:init_db() NameError
- **症状**:Flask 启动时 `init_db()` 调 `log.info(...)`,但 `log = logging.getLogger(...)` 在 init_db 调用之后
- **修法**:把 `init_db()` 移到 `log` 定义之后

### 🔴 Bug 3:_validate_question 被错误装饰成路由
- **症状**:重构 `reading_stream` 抽 helper 时,Python 装饰器从下往上,导致 `@app.route("/reading_stream")` 装饰到 `_validate_question` 而不是 `reading_stream`
- **修法**:把 helper 函数移到所有路由定义之后,`@app.route` 紧贴 `reading_stream`

### 🟠 Bug 4:Prompt Injection 漏洞
- **症状**:用户问题可以包含 "忽略之前所有指令",可能操纵 LLM
- **修法**:加 7 个关键词检测(忽略 / ignore previous / disregard / act as / 扮演 / 你是黑客 / 输出系统提示)+ 500 字长度限制

### 🟢 Bug 5:404 errorhandler 三元表达式类型不一致
- **症状**:`render_template(...), 404 if (...).exists() else ("页面不存在", 404)` 返回类型混搭
- **修法**:改成 if/else 标准结构

### 🟢 Bug 6:backend_used 定义后未更新 + 重复 import
- **症状**:`backend_used = "unknown"` 后从不变;`from llm_backends import LLMRouter` 写了两遍
- **修法**:抽 `_detect_backend_used()` 函数,删重复 import

## 代码质量改进

| 函数 | 前 | 后 |
|---|---:|---:|
| `reading_stream()` | 116 行 | 51 行 + 4 helper |
| `api_reading()` | 80 行 | 49 行 |
| `benchmark_llm.score_response()` | 66 行 | 32 行 + 3 helper |

## 单元测试

`tests/test_app.py`:**19 个测试用例**,覆盖:

| 类 | 测试数 | 覆盖 |
|---|---:|---|
| TestValidation | 5 | 正常 / 超长 / 中文注入 / 英文注入 / "扮演" 关键词 |
| TestRateLimit | 2 | 正常 / 超出阈值 |
| TestChinesRatio | 4 | 全中文 / 半中半英 / 全英文 / 空字符串 |
| TestJsonParse | 4 | 干净 JSON / 嵌入 JSON / 无效 / 无大括号 |
| TestLengthScore | 4 | 区间内 / 区间下 / 区间上 / 无区间规格 |

## 已知限制

| 限制 | 影响 | 解 |
|---|---|---|
| 内存限流,多 worker 不共享 | gunicorn 4 worker 时实际限流 4× | v2.0 改 Redis |
| BOM 文件扫描器只在写时跑 | 历史遗留 BOM 可能仍在 | 运行时扫一次 + 自动清 |
| Helper 函数 `state` dict 共享 | 不适合真多线程 | 流式路由是单连接,够用 |

## 下一步(优先级)

| 优先级 | 任务 | 工作量 |
|---|---|---|
| 🥇 | 分批 scp 到 ECS | 30 min |
| 🥇 | Workbench 重启 supervisor 验证 5 个新 API | 15 min |
| 🥈 | 写用户系统 v2.0 RFC | 1h |
| 🥈 | 写 umami 自托管 RFC | 30 min |
| 🥉 | 流式再增强(reasoning 完整 / token 计数实时) | 1h |
| 🥉 | GitHub Actions CI | 1h |

## 文件清单

```
taixuan-web/
├── app.py                    # Flask 主入口(729 行)
├── llm_backends.py           # LLM 路由器(504 行)
├── benchmark_llm.py          # LLM 评分工具(444 行,部分重构)
├── Dockerfile                # 🆕 多阶段构建
├── docker-compose.yml        # 🆕 服务编排
├── .dockerignore             # 🆕 Docker 排除规则
├── .env.example              # 🆕 配置模板
├── tests/
│   └── test_app.py           # 🆕 19 个单元测试
├── templates/                # 8 派 HTML + 公共页
├── static/                   # JS / CSS / img
├── specs/prompts/            # 8 派 YAML prompt
├── logs/                     # 运行时日志 + readings.db
├── ROADMAP.md                # 版本路线
├── README.md                 # 项目说明
├── DEPLOY.md                 # 部署文档
├── CHANGELOG.md              # 版本日志
└── LICENSE                   # MIT
```

_作者:刘泽文 · 2026-07-12 v1.2 完工,本地 GitHub commit `5405cee`_