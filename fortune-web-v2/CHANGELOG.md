# Changelog

## v1.2.0  2026-07-13

ECS 上跑的版本,主要从 v1.0.0 把 SSE 流式输出串起来。

新增:

- 流式输出:`/api/v2/liupai/<school>/reading_stream` 端点,SSE 协议
- 前端 `static/js/stream.js`,逐字渲染 reasoning + content
- ECS Layer 1 监控脚本 `healthcheck.sh`,cron 每 5 min 自动重启
- 8 派 HTML 模板统一接入流式接口

修复:

- `healthz` version 字段从 "1.0.0" → "1.2.0"(7/13 11:45 同步)
- DeepSeek v3 在 ECS 实测连通(thinking reasoning 模式 SSE 逐字回流)

线上表现:

- 5 条 curl 全过:`/healthz` / `/api/v2/history` / `/api/v2/stats` / `/reading_stream`
- supervisor `RUNNING pid 81026, uptime 9:51:29`(7/13 11:37 实测)
- DeepSeek v3 单次解读 SSE 流式 4-6 秒

部署时间线:

- 7/13 00:45 开始传 11 文件到 `/var/www/taixuan/`
- 7/13 02:50 SSH 认证失败,改用 GitHub raw + curl
- 7/13 11:37 5 条 curl 全过

---

## v1.0.0  2026-07-12

第一个开源版本。从微信小程序改成独立网站。

新增:

- app.py Flask 主入口,8 派路由加 healthz
- llm_backends.py LLM 路由器,三级兜底(DeepSeek 主、Ollama 兜底、Mock 开发用)
- 8 派 HTML 模板:bazi、ziwei、qimen、liuyao、meihua、tarot、western、vedic
- base.html、index.html、privacy.html、terms.html
- 8 派 prompt YAML,从 wx-miniprogram 移植到 specs/prompts/
- 8 派结果 schema 在 specs/schools/
- specs/compliance/ 里有 mingli_banned_words、tone_rules、disclaimer
- static/css/style.css 样式
- tests/test_llm_backends.py 测试
- deploy_ecs.sh 一键部署脚本
- 文档:README、DEPLOY、CHANGELOG、LICENSE

修复:

- DeepSeekV3Backend 类名问题,改成 DeepSeekBackend
- max_tokens 默认从 1500 调到 2500,因为 v4-flash 是 reasoning 模型需要更多 buffer
- Ollama 兜底改静默失败,不抛错

变了:

- 从 wx-miniprogram 拆出来,改用 Flask
- 后端从 wx.request 改成 fetch
- 登录从 wx.login 改成浏览器 localStorage(还没接)

线上表现:

- 1 worker 加 threaded,5 到 10 并发
- DeepSeek 一次解读 2 到 5 秒
- 单次成本大概几厘钱
- 2C2G 加 2G swap 占 600MB

已知问题:

- 单 worker,高并发会排队
- 没用户系统
- 没支付
- 没统计
- 没 SSL,要先域名解析再做 certbot

部署时间线:

- 09:00 决定改网站
- 10:00 写代码
- 11:00 上传到 ECS
- 12:00 改类名 bug
- 13:00 换有效的 key
- 14:00 改 max_tokens
- 15:00 加 swap
- 16:00 跑通
- 22:30 开源

---

## 之后想做但还没做的

- GitHub Actions 自动跑 pytest
- Dockerfile 一键部署
- 域名绑定加 SSL 证书
- supervisor 让 Workbench 关了也能跑
- 访问统计
- 支付
- 历史记录(后端存 SQLite)
- 登录(邮箱、短信)
- PWA
- i18n 英文版
