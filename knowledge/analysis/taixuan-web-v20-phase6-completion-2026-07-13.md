# taixuan-web v2.0 Phase 6 完工报告(2026-07-13)

> **状态**:🟢 **Phase 6 完工(密码找回流程,dev 模式)**
> **作者**:泰
> **触发**:刘泽文 "Phase 6 继续"

---

## ✅ E2E 8/8 本地验证

| # | 检查 | 结果 |
|---|---|---|
| 1 | forgot 现有用户 → reset_url | ✅ |
| 2 | forgot 未知邮箱 → 200 OK 但无 URL(防邮件枚举)| ✅ |
| 3 | forgot 邮箱格式错 → 400 | ✅ |
| 4 | 完整 reset 链路:旧密码失败,新密码 OK | ✅ |
| 5 | reset token 一次用完不能再用 | ✅ |
| 6 | 无效 token → 400 | ✅ |
| 7 | 弱新密码 → 400 | ✅ |
| 8 | reset 强制下线所有旧 session | ✅ |

## ✅ ECS 浏览器端到端验证(5/5)

| # | 检查 | 实测结果 |
|---|---|---|
| 1 | GET `/forgot` | ✅ 200 |
| 2 | GET `/reset` | ✅ 200 |
| 3 | POST `/api/v2/auth/forgot` | ✅ 返回 `reset_url` + `expires_in_sec: 3600` |
| 4 | POST `/api/v2/auth/reset` | ✅ `{"ok": true}` |
| 5 | POST `/api/v2/auth/login` 新密码 | ✅ user_id=3 + JWT |

**完整链路在 ECS 上跑通**!

---

## 🪤 关键发现 + 修复

### 发现:**`is_token_revoked` 反向 bug**(Phase 5 留的)
**症状**:JWT token 即使在 sessions 表被删除后,`require_auth` 仍认它有效。
**根因**:`is_token_revoked` 写成了 `return False` 始终 — sessions 表完全无用。
**修复**:改为 `return row is None`(sessions 表是白名单,不在表里 = 已撤销)。
**影响**:修了 Phase 5 的潜在安全问题(logout 和 reset 现在真生效)。

### 漏点:`/login` 没"忘记密码"链接
**症状**:用户登录页找不到 forgot。
**修法**:login.html 加 `<a href="/forgot">找回密码</a>`。

---

## 📦 Phase 6 交付物

| 文件 | 改动 |
|---|---|
| `user_system.py` | `request_password_reset` / `verify_reset_token` / `consume_reset_token` + `is_token_revoked` 反向 bug 修复 |
| `auth_routes.py` | `POST /api/v2/auth/forgot` + `POST /api/v2/auth/reset` + `send_reset_email` stub |
| `v20_schema.sql` | `password_resets` 表 |
| `app.py` | `/forgot` 和 `/reset` 页面路由 |
| `templates/forgot.html` | 新 2.5 KB |
| `templates/reset.html` | 新 3.3 KB |
| `templates/login.html` | 补 forgot 链接 |
| `tests/test_phase6_reset_flow.py` | 8 项测试 |

---

## 🎯 dev 模式 vs 生产 SMTP

**dev 模式**(当前):
- `forgot` API 返回 `reset_url` 在响应里
- `send_reset_email` 只 log,不真发
- 控制:`TAIXUAN_RESET_RETURN_URL=1`(默认)

**生产模式**(待接 SMTP 时):
- 不在 API response 返回 URL
- `send_reset_email` 改成 smtplib + 阿里云 / Mailgun / SendGrid
- 控制:`TAIXUAN_RESET_RETURN_URL=0`

---

## 📚 关联文档

- **v2.0 RFC**:`knowledge/analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`
- **Phase 1-5 完工**:`knowledge/analysis/taixuan-web-v20-phase{1,2,3,4,5}-completion-2026-07-13.md`
- **部署完工**:`knowledge/analysis/taixuan-web-v20-deployment-2026-07-13.md`
- **DASHBOARD v22**:`tmp/windows/DASHBOARD.md`

---

*本报告于 2026-07-13 22:00 由泰在 ECS Phase 6 浏览器链路验通 后写。*