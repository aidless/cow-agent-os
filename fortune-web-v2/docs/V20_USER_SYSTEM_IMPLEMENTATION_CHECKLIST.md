# taixuan-web v2.0 用户系统 - 实施清单

> **状态**:🟡 实施就绪(代码骨架已写,详细 RFC 见 analysis 文件夹)
> **作者**:泰
> **总工作量**:14h / 2-3 天
> **触发**:不卡死触发条件,基础设施先建好,真用户来了直接能用

---

## ✅ 已完成(本轮)

| 文件 | 状态 | 说明 |
|---|---|---|
| `fortune-web-v2/v20_schema.sql` | ✅ 2.4 KB | 4 张新表(users/sessions/favorites/subscriptions)+ ALTER readings |
| `fortune-web-v2/user_system.py` | ✅ 11 KB | bcrypt + JWT + require_auth + CRUD + sessions + favorites |
| `fortune-web-v2/tests/test_user_system.py` | ✅ 4.0 KB | 6 测试类 / 17 测试用例 / 全 unittest 写,无外部依赖(只 pytest-runner) |

---

## 📋 实施阶段(2-3 天,~14h)

### Phase 1:基础设施接入(0.5h)

| # | 任务 | 工作量 | 谁 |
|---|---|---:|---|
| 1.1 | `app.py` 顶部 import `user_system` | 1 min | 我 |
| 1.2 | `init_db()` 启动时跑一次 | 5 min | 我 |
| 1.3 | 跑 pytest 验证 user_system.py | 30 min | 我 + 你跑测试 |
| 1.4 | bcrypt + 依赖装 ECS | 5 min | Workbench |

### Phase 2:Auth API + 前端(3h)

| # | 任务 | 工作量 |
|---|---|---:|
| 2.1 | `auth_routes.py`(register/login/logout/me 4 个)| 2h |
| 2.2 | `templates/login.html` | 30 min |
| 2.3 | `templates/register.html` | 30 min |

### Phase 3:接入现有路由(2h)

| # | 任务 | 工作量 |
|---|---|---:|
| 3.1 | 改造 `/api/v2/liupai/<liupai>/reading_stream` 接 user_id | 1h |
| 3.2 | 改造 `/api/v2/history` 按 user_id 过滤(匿名看公开,登录看自己)| 1h |

### Phase 4:收藏 + 个人中心(3h)

| # | 任务 | 工作量 |
|---|---|---:|
| 4.1 | `favorites_routes.py`(3 个)| 1h |
| 4.2 | `templates/me.html` 个人中心 | 2h |

### Phase 5:解读页收藏按钮(1h)

| # | 任务 | 工作量 |
|---|---|---:|
| 5.1 | `static/js/auth.js` token 管理 + 收藏按钮 | 30 min |
| 5.2 | 测试全套 | 30 min |

### Phase 6:加固(2.5h)

| # | 任务 | 工作量 |
|---|---|---:|
| 6.1 | 密码强度校验 + 暴力登录锁 | 1h |
| 6.2 | 密码找回流程(邮件重置)| 1h |
| 6.3 | 全链路测试 + bug 修复 | 30 min |

---

## 🎯 当前 session 还能做

### 高 ROI(~30 min)

| # | 任务 | 工作量 |
|---|---|---:|
| **A** | 跑本机 pytest 验证 `user_system.py` | 5 min |
| **B** | 写 `auth_routes.py` 完整版(register/login/logout/me) | 30 min |
| **C** | 写 `favorites_routes.py` 完整版 | 20 min |
| D | 写 bcrypt 安装命令 + ECS 集成检查清单 | 15 min |

---

## 🪤 本轮踩到的坑

- **(暂无)** — 代码骨架写得顺利,跟 RFC 设计一致
- **下一步**:Phase 1 接入 app.py 时,先跑 `pytest test_user_system.py` 确保 user_system.py 单测过

---

## 📚 关联文档

- **RFC**:`knowledge/analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`
- **本机代码根**:`C:\Users\Administrator\cow\fortune-web-v2\`(本轮所有新增都在这)
- **下一份完工**:v2.0 Phase 1 接入 + 验证(待跑)

---

*本清单于 2026-07-13 18:40 由泰在 user_system.py + v20_schema.sql + test_user_system.py 写完 时立。*
