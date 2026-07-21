# taixuan-web v2.0 Phase 4 完工报告(2026-07-13)

> **状态**:🟢 **Phase 4 全完工(★ 收藏按钮 + reading_id 链路)**
> **作者**:泰
> **触发**:Phase 3 完工后立即推进

---

## ✅ E2E 8 项验证(实测)

| # | 检查 | 结果 |
|---|---|---|
| 1 | `save_reading` 返回 int lastrowid | ✅ |
| 2 | 登录用户 save reading(user_id 入库)| ✅ |
| 3 | POST /favorites 创建 favorite | ✅ |
| 4 | favorite 行写入 DB(user_id + reading_id + note)| ✅ |
| 5 | 匿名 POST /favorites → 401 | ✅ |
| 6 | 重复收藏 → 400 | ✅ |
| 7 | GET /favorites JOIN readings 返回 liupai/question | ✅ |
| 8 | DELETE /favorites/<id> + 列表 count=0 | ✅ |

```
$ python tests/test_phase4_favorite_flow.py
PASS: save_reading returns int lastrowid (got 1)
PASS: saved reading_id=2 for user_id=1
PASS: POST /favorites -> favorite_id=1
PASS: favorite row verified in DB (user=1, reading=2)
PASS: anonymous POST /favorites returns 401
PASS: duplicate favorite returns 400
PASS: GET /favorites returns item with reading meta (liupai=bazi, question=meta test)
PASS: DELETE favorite flow works

All Phase 4 favorite flow checks passed.
```

---

## 🪤 本轮踩坑(已固化)

### 坑 1:SQL f-string 拼接语法错误
**症状**:`OperationalError: near "FROM": syntax error`,**当 readings 表没 summary 列时**(测试 fixture)。
**根因**:`select_summary = ""` 时,SQL 变成 `r.question, FROM` — 多余逗号。
**修法**:**if/else 两个完整 SQL**,不拼接。

### 坑 2:测试 fixture 多 DB 隔离
**症状**:favorites_routes.list_favorites 查不到 favorite(DB 不同)。
**根因**:`user_system.get_conn` 和 `app.get_db` 默认不同路径。
**修法**:fixture 强制 `app_module.get_db = unified_get_db(db_path)`,且自己创 readings 表。

### 坑 3:add_favorite 允许重复
**症状**:同一 reading 可被同一用户收藏多次。
**根因**:favorites 表**没 unique 约束**(user_id + reading_id)。
**修法**:`add_favorite` 函数体内先 SELECT 检查。

---

## 📦 Phase 4 交付物

| 文件 | 改动 | 用途 |
|---|---|---|
| `app.py` `save_reading` | 加 user_id 入库 + 返回 int | reading_id 给前端 |
| `app.py` `api_reading` / `reading_stream` | done 事件带 reading_id + user_id | 前端拿来收藏 |
| `app.py` `api_history` | scope 过滤(Phase 3 留存) | 历史按 user 隔离 |
| `user_system.py` `add_favorite` | 加去重 | 防重复收藏 |
| `user_system.py` `list_favorites` | 修 SQL 拼接 + summary 防御 | 鲁棒 JOIN |
| `static/js/favorites.js` | 新 3.5 KB | 收藏按钮 4 状态机 |
| `templates/liupai/*.html` | 8 文件 +316 bytes | 全部加 #favorite-section |
| `tests/test_phase4_favorite_flow.py` | 新 7.0 KB | 8 项端到端测试 |

---

## 🎯 四阶段累计完工

| 阶段 | 文件 | 测试 | 时间 |
|---|---:|---:|---|
| Phase 1(基础设施)| 7 | 35/35 | 18:50 |
| Phase 2(app.py + 前端)| 6 | 5/5 e2e | 19:00 |
| Phase 3(接业务流)| 2 | 8/8 e2e | 19:15 |
| **Phase 4(★ 收藏按钮)**| **9** | **8/8 e2e** | **19:30** |
| **合计** | **24** | **56/56** | — |

---

## 🎯 v2.0 完工度

**RFC 14h 任务已全部完工**:
- ✅ 基础设施(Phase 1)
- ✅ auth API + 3 页面(Phase 2)
- ✅ reading 接 user_id + history scope(Phase 3)
- ✅ ★ 收藏按钮端到端(Phase 4)

**未做的(明确划线)**:
- ⏸ 密码强度校验 + 暴力登录锁(可用)
- ⏸ 密码找回流程
- ⏸ 邮件验证

**触发条件**:日 PV > 100 / 月独立 IP > 50 / 重复访问率 > 20%
当前 v1.2.1 仍只有 ECS 上线,**真实流量触发后再补**。

---

## 📚 关联文档

- **RFC**:`knowledge/analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`
- **Phase 1 完工**:`knowledge/analysis/taixuan-web-v20-phase1-completion-2026-07-13.md`
- **Phase 2 完工**:`knowledge/analysis/taixuan-web-v20-phase2-completion-2026-07-13.md`
- **Phase 3 完工**:`knowledge/analysis/taixuan-web-v20-phase3-completion-2026-07-13.md`
- **DASHBOARD v18**:`tmp/windows/DASHBOARD.md`

---

*本报告于 2026-07-13 19:30 由泰在 e2e 8/8 PASS 后写。*