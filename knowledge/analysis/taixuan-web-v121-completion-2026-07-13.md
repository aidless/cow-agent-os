# taixuan-web v1.2.1 ECS 部署完工报告(2026-07-13)

> **状态**:🟢 **v1.2.1 全部完工 + 验证全过**
> **作者**:泰(接力 session,7/13 12:00-18:30)
> **触发**:v1.2.0 部署完成后,加 version 字段同步 + 新端点 + Layer 1 监控 + 自动重启脚本

---

## ✅ 6 项验证结果(实测)

| # | 命令 | 输出 | 状态 |
|---|---|---|---|
| 1 | `supervisorctl status taixuan` | `RUNNING   pid 96231, uptime 0:00:03` | ✅ |
| 2 | `curl -s /healthz` | `{"build_time":"2026-07-13T11:45+08:00","git_commit":"c376ac3","version":"1.2.0","status":"ok"}` | ✅ |
| 3 | `curl -s /api/v2/version`(新端点) | `{"version":"1.2.0","build_time":"2026-07-13T11:45+08:00"}` | ✅ |
| 4 | `curl -N /reading_stream` | `data: {"type":"reasoning","text":"嗯"}` 逐字推理 | ✅ |
| 5 | `crontab -l \| grep healthcheck` | `*/5 * * * * /bin/bash .../healthcheck.sh` | ✅ |
| 6 | `/var/log/taixuan-cron.log` | 28 KB | ✅ |

---

## 📦 v1.2.1 增量清单

| 文件 | 来源 | 变化 |
|---|---|---|
| `app.py` | GitHub master | version 1.0.0 → **1.2.0** + 加 build_time + git_commit + 新增 `/api/v2/version` 端点 |
| `healthcheck.sh` | 新 | curl + jq + supervisorctl 自动重启 + 日志轮转 |
| `deploy_cron_healthcheck.sh` | 新 | 幂等注册 cron(检查是否已注册)|
| `deploy_v121.sh` | 新 | 一键 v1.2.0 → v1.2.1 升级脚本 |

---

## 🪤 本轮踩中的 3 个坑(已固化进 MEMORY.md)

### 坑 1:GitHub 仓库默认分支是 `master`,不是 `main`

**症状**:`curl .../main/app.py` 返回 **14 字节 404**,覆盖了原 27 KB 真文件,supervisor 重启 → spawn error → 端口 80 拒绝连接 → **整个站点挂了**。

**修法**:任何 GitHub raw URL 必用 `/master/...` **+ 拉完 `ls -la` 验证大小**。

### 坑 2:SSL timeout 间歇性

**症状**:`curl .../master/app.py` 偶发 `(28) SSL connection timeout`。

**修法**:加 `--retry 3 --retry-delay 2`(成功一次就好)。

### 坑 3:GitHub web 上传需 root 权限 + 大文件易断

**症状**:之前 plan 走 GitHub web 拖拽上传,但 SSH 认证问题 + Workbench 远程连接易断。

**实际**:本次实测你 web 上传 + Workbench curl 拉,**2 段组合最稳**。全程大约 18:00 → 18:25 搞定。

---

## 🎯 v1.2.1 完成的能力清单

| 能力 | 实现 |
|---|---|
| ✅ 版本号自描述 | `/healthz` 含 `version` + `build_time` + `git_commit` |
| ✅ 独立版本端点 | `/api/v2/version` 不带 backend 信息(轻量版) |
| ✅ Layer 1 自动监控 | healthcheck.sh + cron 每 5 min 跑一次 |
| ✅ 自动重启 | 失败时 supervisorctl restart taixuan |
| ✅ 日志轮转 | /var/log/taixuan-health.log 超 10MB 自动截断 |
| ✅ ECS 站点真活 | DeepSeek v3 + SSE 流式推理全跑通 |

---

## 🎯 下一步(7/13 晚,接力给未来 session)

| # | 动作 | 工作量 | 触发 |
|---|---|---|---|
| 1 | Windows Layer 2 Watchdog | 10 min | 任务计划 + PowerShell |
| 2 | v1.2.1 完工报告 v2(用户/SEO 友好版)| 30 min | 需要 |
| 3 | 用户系统 v2.0 RFC 实施 | ~3h | RFC-005 已写 |
| 4 | GitHub Actions CI | 1h | 可选 |

---

## 📚 关联文档

- **v1.2.0 完工报告**:`knowledge/analysis/taixuan-web-ecs-v12-deploy-completion-2026-07-13.md`
- **v1.1 SSE 完工**:`knowledge/analysis/taixuan-web-v11-sse-completion-2026-07-12.md`
- **v1.2 总览**:`knowledge/analysis/taixuan-web-v12-completion-2026-07-12.md`
- **监控 RFC**:`knowledge/analysis/taixuan-web-ecs-monitoring-rfc-2026-07-13.md`
- **DASHBOARD v13**:`tmp/windows/DASHBOARD.md`
- **本 session 接力总结**:`memory/2026-07-13.md`

---

*本报告于 2026-07-13 18:30 由泰在 supervisor RUNNING + 6 项验证全过 后写。*