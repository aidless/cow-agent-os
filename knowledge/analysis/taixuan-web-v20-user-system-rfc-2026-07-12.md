# taixuan-web 用户系统 v2.0 RFC

**状态**:📋 RFC 草案
**作者**:刘泽文
**日期**:2026-07-12
**目标版本**:taixuan-web v2.0(预计 14h 工作量,2-3 天)

## 一、问题陈述

### 当前状态(v1.2)

- 完全匿名,无用户系统
- 解读历史所有人都能看到(`/api/v2/history` 无 filter)
- 无法识别回头客
- 无法做付费转化
- 无法做个性化(收藏、笔记)

### v2.0 目标

- 匿名用户 + 注册用户并存(向后兼容)
- 注册用户有个人历史 / 收藏 / 笔记
- 触发条件:日活 > 50 OR 月 PV > 1000(看 umami 数据)

## 二、用户分层设计

### 2.1 用户类型

| 类型 | 存储 | 权限 | 触发升级 |
|---|---|---|---|
| **匿名用户** | 无 | 浏览 + 解读(限流 10/min) | 注册 |
| **注册用户** | users 表 | + 历史保存 / 收藏 / 笔记 | 付费 |
| **付费用户** | users + subscriptions | + 无限解读 / 深度解读 | - |

### 2.2 注册 / 登录流程

```
匿名用户 → 点"注册" → 输入邮箱 + 密码
   ↓
服务端 bcrypt 哈希密码,生成 user_id
   ↓
返回 JWT(access_token, 14 天有效)
   ↓
前端 localStorage 存 token,后续请求带 Authorization header
```

**简化选择**:不做 OAuth / 微信登录 / 短信验证,**只做邮箱 + 密码**。简单可靠,够用。

## 三、数据库 Schema(SQLite 扩展)

### 3.1 新表

```sql
-- 用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,           -- bcrypt 哈希
    nickname TEXT,
    avatar_url TEXT,
    role TEXT DEFAULT 'user',              -- user / admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    is_active INTEGER DEFAULT 1
);
CREATE INDEX idx_users_email ON users(email);

-- 会话表(JWT 黑名单 + 主动登出)
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token_hash TEXT NOT NULL,              -- token 的 SHA256,不入原值
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX idx_sessions_token ON sessions(token_hash);

-- 收藏表(用户收藏的解读)
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    reading_id INTEGER NOT NULL,
    note TEXT,                             -- 用户笔记
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (reading_id) REFERENCES readings(id)
);
CREATE INDEX idx_favorites_user ON favorites(user_id);

-- 订阅表(v3.0 预留,v2.0 先建表不实现付费)
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan TEXT,                             -- 'monthly' / 'yearly' / null (free)
    started_at TIMESTAMP,
    expires_at TIMESTAMP,
    is_active INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 3.2 改造 existing readings 表

```sql
ALTER TABLE readings ADD COLUMN user_id INTEGER;  -- 匿名用户为 NULL
CREATE INDEX idx_readings_user ON readings(user_id);
```

**回退方案**:user_id 允许 NULL,匿名解读保留,平滑过渡。

## 四、API 设计

### 4.1 认证 API

```
POST /api/v2/auth/register
  Body: {email, password, nickname?}
  Resp: {user_id, access_token, expires_at}

POST /api/v2/auth/login
  Body: {email, password}
  Resp: {user_id, access_token, expires_at}

POST /api/v2/auth/logout
  Header: Authorization: Bearer <token>
  Body: {}
  Resp: {ok: true}     (token 加入 sessions 黑名单)

GET /api/v2/auth/me
  Header: Authorization: Bearer <token>
  Resp: {user_id, email, nickname, role, created_at}
```

### 4.2 用户历史 API(改造 existing)

```
GET /api/v2/history?limit=10
  Header: (可选) Authorization: Bearer <token>
  Resp: 匿名 → 公开所有解读
        登录 → 只看自己的(user_id 匹配)

GET /api/v2/history/<id>
  权限:公开 OR 自己的;他人 → 404
```

### 4.3 收藏 API

```
POST /api/v2/favorites
  Header: Authorization
  Body: {reading_id, note?}
  Resp: {favorite_id}

GET /api/v2/favorites
  Header: Authorization
  Resp: [{favorite_id, reading_id, note, created_at}, ...]

DELETE /api/v2/favorites/<id>
  Header: Authorization
  Resp: {ok: true}
```

## 五、安全设计

| 风险 | 措施 |
|---|---|
| 密码明文存储 | **bcrypt**(cost=12) |
| 弱密码 | 注册时要求 ≥ 8 位 + 含数字 |
| JWT 泄露 | 14 天过期 + sessions 黑名单支持主动失效 |
| CSRF | API 全部 POST,要求 `Authorization` header(非 cookie) |
| 暴力登录 | 同一 IP 失败 5 次后锁 15 min(类似限流) |
| SQL 注入 | 全用参数化 query(SQLite ? 占位符) |
| XSS | Flask 模板自动转义;前端不直接 innerHTML |

## 六、前端设计

### 6.1 顶部导航加菜单

```
[首页] [8 派卡片] ... [登录 / 注册]
```

### 6.2 个人中心页 `/me`

```
我的解读历史
我的收藏
我的笔记
个人设置(改昵称 / 改密码 / 登出)
```

### 6.3 解读页加"收藏"按钮

解读完成后,显示 ★ 收藏按钮(登录用户可点)。

## 七、文件结构(增量)

```
taixuan-web/
├── app.py                     # 加 auth 路由(register/login/logout/me)
├── user_system.py             # 🆕 用户系统模块
│   ├── hash_password()
│   ├── verify_password()
│   ├── create_token()
│   ├── decode_token()
│   ├── require_auth() 装饰器
│   └── User 表 CRUD
├── auth_routes.py             # 🆕 4 个 auth 路由
├── favorites_routes.py        # 🆕 3 个 favorites 路由
├── templates/
│   ├── login.html             # 🆕
│   ├── register.html          # 🆕
│   └── me.html                # 🆕 个人中心
├── static/js/
│   └── auth.js                # 🆕 token 管理
├── tests/
│   └── test_user_system.py    # 🆕 单元测试
└── docs/
    └── USER_SYSTEM_RFC.md     # 本文档
```

## 八、实施步骤(2-3 天)

### Day 1:基础设施(6h)

| # | 任务 | 工作量 |
|---|---|---:|
| 1 | bcrypt + JWT 依赖装 | 10 min |
| 2 | 写 user_system.py(密码 hash + token 创建) | 1h |
| 3 | 写 auth_routes.py(register/login/logout/me) | 2h |
| 4 | ALTER readings 表加 user_id | 30 min |
| 5 | 改造 api_reading/reading_stream 接 user_id | 1h |
| 6 | 前端 login.html / register.html | 1h |
| 7 | 单元测试 test_user_system.py | 30 min |

### Day 2:个人中心 + 收藏(5h)

| # | 任务 | 工作量 |
|---|---|---:|
| 1 | favorites_routes.py | 1h |
| 2 | /me 个人中心页 + 模板 | 2h |
| 3 | 解读页加 ★ 收藏按钮 | 1h |
| 4 | 改造 /api/v2/history 按 user_id 过滤 | 30 min |
| 5 | 测试 + 修 bug | 30 min |

### Day 3:完善(3h)

| # | 任务 | 工作量 |
|---|---|---:|
| 1 | 密码强度校验 + 暴力登录锁 | 1h |
| 2 | 邮箱验证(可选,先做密码找回流程) | 1h |
| 3 | 全链路测试 | 1h |

## 九、不做(明确划线)

| 不做 | 原因 |
|---|---|
| 微信扫码登录 | 复杂度高,用户基数小不值得 |
| 短信验证 | 国内短信 API 贵 + 备案麻烦 |
| OAuth / GitHub 登录 | 目标用户群体用不上 |
| 邮箱验证(发邮件) | 第三方邮件服务要钱,先用密码找回 |
| 实名认证 | KYC 复杂度高,v2.0 不做 |
| 头像上传 | 用 Gravatar 简化,不做本地存储 |

## 十、风险与对策

| 风险 | 严重度 | 对策 |
|---|---|---|
| bcrypt 慢导致 API 慢 | 中 | 单实例同步,200ms 内可接受;预留 worker 线程 |
| SQLite 单文件并发限制 | 中 | 单写多读够用;v3.0 改 PostgreSQL |
| 用户增长后限流失效 | 低 | v2.0 后期改 Redis 共享计数 |
| JWT 无法主动失效 | 高 | sessions 表 + 黑名单机制 |
| 用户忘了密码 | 中 | Day 3 密码找回流程 |

## 十一、触发指标

从 v1.2 → v2.0 的升级触发条件(基于 umami 数据):

| 指标 | 阈值 | 含义 |
|---|---|---|
| 日 PV | > 100 | 有真实访问量 |
| 月独立 IP | > 50 | 有真实用户 |
| 重复访问率 | > 20% | 用户有粘性 |
| 单次解读后停留 | > 30 秒 | 内容有价值 |

未触发 → 继续 v1.x 优化,不升级。

## 十二、v2.0 与 v1.x 的兼容

**保留所有现有功能**(不破坏性改动):
- 匿名解读完整保留
- `/api/v2/history` 匿名 → 看公开记录,登录 → 看自己
- 8 派页面 URL 不变
- API 路由前缀不变(继续 `/api/v2/...`)

**新增功能**(增量):
- 4 个 auth API + 3 个 favorites API
- 3 个新页面(/login /register /me)

## 十三、关键决策记录

| 决策 | 选项 | 选择 | 理由 |
|---|---|---|---|
| 认证方式 | OAuth / 邮箱密码 / 手机 | **邮箱密码** | 简单可靠,够用 |
| Token 类型 | Session cookie / JWT | **JWT** | 无状态,移动端友好 |
| Token 存储 | localStorage / httpOnly cookie | **localStorage** | 纯前端,简单 |
| 密码哈希 | SHA256 / bcrypt | **bcrypt(cost=12)** | 行业标准,慢哈希抗彩虹表 |
| 数据库 | SQLite / PostgreSQL | **SQLite** | 单机够用,零运维 |
| ORM | SQLAlchemy / 裸 SQL | **裸 SQL** | 简单,无学习成本 |

---

_本 RFC 草案,等流量触发指标到达后再启动实施。代码暂不写,先沉淀设计。_