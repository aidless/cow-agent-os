# taixuan-web v2.0 部署就绪(2026-07-13)

> **状态**:🟢 **v2.0 一键部署脚本就绪**
> **作者**:泰
> **触发**:v2.0 RFC 14h 任务全部完工后,接 Workbench 一键部署

---

## 📦 部署交付物

| 文件 | 大小 | 用途 |
|---|---|---|
| `fortune-web-v2/deploy_v121_to_v20.sh` | 5.0 KB | ECS 一键升级脚本(Workbench 跑)|
| `fortune-web-v2/install_v20_deps.sh` | 2.0 KB | 单独装 bcrypt(可独立运行)|

---

## 🎯 部署脚本能力清单

`deploy_v121_to_v20.sh` 8 步自动化:

| # | 步骤 | 幂等 |
|---|---|---|
| 1 | 备份 v1.2.1 到 `/tmp/taixuan-backup-v12/` | ✅ |
| 2 | 停止 supervisor taixuan | ✅ `stop` + `true` |
| 3 | 从 GitHub master 拉 10 个新文件 | ✅ 已存在则跳过 |
| 4 | 运行 v20_schema.sql 创建 4 新表 | ✅ `CREATE IF NOT EXISTS` |
| 5 | 装 bcrypt via pip | ✅ |
| 6 | 生成 32 字节 hex JWT 秘密 | ✅ 写到 600 权限 |
| 7 | 更新 supervisor env + reread | ✅ 检查存在再添加 |
| 8 | 重启 supervisor + 冒烟测试 | ✅ /healthz + /api/v2/auth/register |

**预计执行时间**:2-5 min(取决于网络)
**回滚**:脚本自带 `Rollback` 章节,3 行恢复 v1.2.1

---

## 🚀 一键运行(Workbench)

```bash
bash /var/www/taixuan/deploy_v121_to_v20.sh
```

**或者直接 curl 拉脚本**:

```bash
curl -sSL https://raw.githubusercontent.com/aidless/taixuan-web/master/deploy_v121_to_v20.sh \
  -o /tmp/deploy.sh && bash /tmp/deploy.sh
```

---

## ⚠️ 已知限制

| # | 限制 | 解决 |
|---|---|---|
| 1 | 需要 ECS 上有 `sqlite3` CLI | `apt install sqlite3`(非 debian 系不同) |
| 2 | 需要 `pip` 可用 | 大多 Ubuntu 22.04 自带 |
| 3 | 需要 supervisor conf 路径是 `/etc/supervisor/conf.d/taixuan.conf` | 默认路径,如不是手动调整 |

---

## 📋 部署后 5 项必验

```bash
# 1. healthz OK
curl -s http://127.0.0.1:80/healthz

# 2. 注册(弱密码 → 400)
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"email":"smoke@test.com","password":"abc"}' \
  http://127.0.0.1:80/api/v2/auth/register

# 3. 注册(强密码 → 200 + token)
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"goodpass1"}' \
  http://127.0.0.1:80/api/v2/auth/register

# 4. 浏览器打开 /login
curl -s -o /dev/null -w "%{http_code}" http://116.62.69.83/login

# 5. 浏览器打开 /me(应跳 /login 因为未登录)
curl -s -o /dev/null -w "%{http_code}" http://116.62.69.83/me
```

---

## 🎯 下一步(7/13 晚)

| # | 任务 | 触发 |
|---|---|---|
| 1 | 真实流量触发后跑部署脚本 | 日 PV > 100 |
| 2 | Phase 5 密码强度 + 暴力登录锁 | 流量起来后 |
| 3 | Phase 6 密码找回 | 流量起来后 |

---

## 📚 关联文档

- **v2.0 RFC**:`knowledge/analysis/taixuan-web-v20-user-system-rfc-2026-07-12.md`
- **Phase 4 完工**:`knowledge/analysis/taixuan-web-v20-phase4-completion-2026-07-13.md`
- **DASHBOARD v19**:`tmp/windows/DASHBOARD.md`

---

*本报告于 2026-07-13 19:35 由泰写就。*