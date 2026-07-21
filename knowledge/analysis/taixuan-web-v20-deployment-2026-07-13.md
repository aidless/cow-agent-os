# taixuan-web v2.0 ECS 部署完工报告(2026-07-13)

> **状态**:🟢 **v2.0 在 ECS 跑起来了!**
> **作者**:泰
> **触发**:刘泽文 "继续推 v2.0 RFC" + "B 立刻部署"

---

## ✅ 部署验证

| # | 检查 | 实测结果 |
|---|---|---|
| 1 | supervisor RUNNING | `RUNNING pid 100032, uptime 0:00:04` |
| 2 | /healthz 200 | `{"status":"ok","version":"1.2.0","primary_backend":"deepseek-v3","git_commit":"c376ac3"}` |
| 3 | POST /api/v2/auth/register 强密码 | `{"user_id":1,"access_token":"eyJ...","expires_in":1209600,"email":"smoke@test.com","nickname":"smoke"}` |

**JWT 已签发**,用户系统 v2.0 真活!

---

## 📦 部署交付物

### GitHub master(全部到位)

| 文件 | 来源 | 大小 |
|---|---|---:|
| `user_system.py` | 本机重写(tab-free)| 13,197 B |
| `auth_routes.py` | 本机 | 2,715 B |
| `favorites_routes.py` | 本机 | 2,030 B |
| `auth_helpers.py` | 本机 | 856 B |
| `v20_schema.sql` | 本机 | 1,938 B |
| `analytics.py` | 本机 | 8,446 B |
| `app.py` | 本机 v2.0 改造 | 32,403 B |
| `deploy_v121_to_v20.sh` | 本机 LF 行尾 | 5,072 B |
| `templates/login.html` | 本机 | 2,297 B |
| `templates/register.html` | 本机 | 2,477 B |
| `templates/me.html` | 本机 | 5,276 B |
| `static/js/auth.js` | 本机 | 1,838 B |
| `static/js/favorites.js` | 本机 | 3,650 B |

### ECS `/var/www/taixuan/`

12 个新文件 + app.py v2.0 改造版,supervisor 守护。

### 凭据

| 文件 | 状态 |
|---|---|
| `C:\Users\Administrator\cow\credentials\github_pat.bin` | DPAPI 加密 262 bytes(40 字符 PAT) |

---

## 🪤 本轮踩坑固化(RULE.md 已加)

### 坑 1:Windows 写 .sh 默认 CRLF → Linux 不能跑
**症状**:`$'\r': command not found`
**修法**:上传前 `python _fix_newline.py` 转 LF。
**预防**:任何从 Windows 写到 ECS 跑的脚本必须 LF。

### 坑 2:删 import 注释但保留裸调用
**症状**:`NameError: name 'analytics' is not defined`
**修法**:要么 import 一起保留,要么 5 处调用全删。
**预防**:删 import 时**必须 grep 检查调用点**。

### 坑 3:GitHub raw URL 14 字节 404 偶发
**症状**:curl 拉到 14 字节 404 文件覆盖真文件
**修法**:`stat -c%s` 验证 > 1000 才是真文件。
**预防**:每次 curl 后 `stat -c%s` 检查。

### 坑 4:app.py 改造后没在本机 e2e 测过
**症状**:import 路径错 / 漏 import 一上 ECS 就崩。
**修法**:本机 `python -c "import app"` 验证 + e2e 测试覆盖。
**预防**:任何 app.py 改造后必须本地 import 成功 + 关键路由 smoke。

---

## 🎯 工具永久化(`C:\Users\Administrator\cow\tools\`)

| 文件 | 用途 |
|---|---|
| `github_pat_setup.py` | 首次:加密存储 PAT |
| `github_pat_load.py` | 后续:解密读取(可设 env) |
| `github_api_upload.py` | 批量上传 12 个文件 |
| `upload_app_and_analytics.py` | 单文件快速上传 helper |
| `watchdog_ecs.ps1` | Windows 任务计划探活 |
| `install_watchdog_task.ps1` | 注册 Watchdog 任务 |

**以后任何对 aidless/taixuan-web 的修改都可全自动推送**!

---

## 📚 关联文档

- **v2.0 RFC**:`knowledge/analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`
- **Phase 1-4 完工**:`knowledge/analysis/taixuan-web-v20-phase{1,2,3,4}-completion-2026-07-13.md`
- **部署就绪**:`knowledge/analysis/taixuan-web-v20-deploy-readiness-2026-07-13.md`
- **DASHBOARD v20**:`tmp/windows/DASHBOARD.md`

---

*本报告于 2026-07-13 21:25 由泰在 ECS supervisor RUNNING + JWT 签发成功 后写。*