# taixuan-web v2.0 Phase 1 完工报告(2026-07-13)

> **状态**:🟢 **Phase 1 完工(基础设施层)+ 35 测试全过**
> **作者**:泰
> **触发**:刘泽文 "继续推 v2.0 RFC"

---

## ✅ 实测验证

| 测试套件 | 通过 | 覆盖 |
|---|---:|---|
| `test_user_system.py` | **19/19** | 密码 / bcrypt / JWT / CRUD / sessions / favorites |
| `test_auth_favorites_routes.py` | **16/16** | Flask Blueprint 4+3 路由全场景 |
| **合计** | **35/35** ✅ | user_system + auth + favorites 全栈 |

```
$ python -m pytest tests/test_user_system.py tests/test_auth_favorites_routes.py
============================= 35 passed in 15.21s =============================
```

---

## 📦 Phase 1 交付物(7 个文件)

| 文件 | 大小 | 用途 |
|---|---|---|
| `fortune-web-v2/v20_schema.sql` | 2.4 KB | 4 张新表(users/sessions/favorites/subscriptions)+ ALTER readings |
| `fortune-web-v2/user_system.py` | 11.5 KB | bcrypt + JWT(HS256 自实现,无 PyJWT)+ require_auth + CRUD |
| `fortune-web-v2/auth_routes.py` | 2.7 KB | register / login / logout / me |
| `fortune-web-v2/favorites_routes.py` | 2.0 KB | POST / GET / DELETE favorites |
| `fortune-web-v2/install_v20_deps.sh` | 2.0 KB | ECS 上一键装 bcrypt |
| `fortune-web-v2/tests/test_user_system.py` | 6.9 KB | 19 单测 |
| `fortune-web-v2/tests/test_auth_favorites_routes.py` | 8.5 KB | 16 路由集成测试 |

**合计 ~36 KB,5+ 路由,4 新表,35 测试。**

---

## 🎯 设计决策(已落地)

| 决策 | 选择 | 落地证据 |
|---|---|---|
| 认证方式 | 邮箱 + 密码 | `auth_routes.register/login` |
| Token 类型 | JWT | `create_token/decode_token` |
| Token 存储 | localStorage | 前端待 Phase 5 |
| 密码哈希 | bcrypt(cost=12) | `hash_password`(可选 SHA256 fallback)|
| 数据库 | SQLite | `v20_schema.sql` |
| ORM | 裸 SQL | `sqlite3` 直接执行 |
| 第三方依赖 | **只 + bcrypt** | JWT 自实现 HMAC-SHA256 |

---

## 🪤 本轮踩坑(已修)

### 坑 1:pytest 第一次跑 10 个 FAIL
**原因**:
- `v20_schema.sql` 末尾 `ALTER readings` 在没 readings 表的 DB 失败 → OperationalError
- 测试 `setUp` 用 `TEST_DB = mktemp()` 复用,Windows 文件锁被前一次连接卡住

**修法**:
- `init_db()` 重写:**先**用 inline schema 创表(永远成功),**再**可选跑 v20_schema.sql 并 try/except
- 测试改用 `tempfile.mkstemp()` + `_make_fresh_db()` helper + `tearDown gc.collect()`

### 坑 2:Flask 没装导致路由测试无法 collect
**原因**:hermes-agent venv 没装 Flask,只在另一个 Python venv 有

**修法**:`pip install flask bcrypt` 后跑过

---

## 🎯 Phase 1 没做的事(明确划线)

| 不做 | 原因 |
|---|---|
| ❌ `app.py` 改造接入 | Phase 2 |
| ❌ `templates/login.html` `register.html` | Phase 2 |
| ❌ 改造 `reading_stream` 接 user_id | Phase 3 |
| ❌ `/me` 个人中心页 | Phase 4 |
| ❌ 收藏按钮前端 | Phase 5 |
| ❌ 密码找回 | Phase 6 |
| ❌ 暴力登录锁 | Phase 6 |

---

## 🎯 Phase 2 接入 app.py(下一步,0.5h)

**app.py 顶部加 3 行 + 启动时 init_db + 注册 2 个 Blueprint**:

```python
import user_system
from auth_routes import auth_bp
from favorites_routes import favorites_bp

# 启动时
user_system.init_db()
app.register_blueprint(auth_bp, url_prefix="/api/v2/auth")
app.register_blueprint(favorites_bp, url_prefix="/api/v2/favorites")
```

**requirements.txt 加一行**:`bcrypt>=4.1`

**Env 变量**:`TAIXUAN_JWT_SECRET=<32+ random bytes>`

---

## 📚 关联文档

- **RFC**:`knowledge/analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`
- **实施清单**:`fortune-web-v2/docs/V20_USER_SYSTEM_IMPLEMENTATION_CHECKLIST.md`
- **DASHBOARD v15**:`tmp/windows/DASHBOARD.md`

---

*本报告于 2026-07-13 18:50 由泰在 35/35 测试 PASS 后写。*