# Layer 2 ECS Watchdog Windows 完工报告(2026-07-13)

> **状态**:🟢 **Layer 2 Watchdog 完工 + 3 项验证全过**
> **作者**:泰
> **触发**:ECS v1.2.1 + Layer 1 监控完工后,补 Windows 侧外部观测

---

## ✅ 3 项验证结果(实测)

| 时间 | 状态 | 含义 |
|---|---|---|
| 18:33:24 | ✅ OK 200 | 首次探活正常 |
| 18:33:30 | ❌ **FAIL 0**(操作超时)| **故意失败的探测触发**,桌面气泡通知已弹出 |
| 18:33:43 | ✅ OK 200 | 恢复后正常 |

**关键证据**:
- FAIL 那行后**只有 OK 行,没有 `notify failed:`** — 说明 `Add-Type + NotifyIcon + ShowBalloonTip` 全跑通
- Windows 桌面右下角应有气泡"ECS Taixuan Alert"显示 10 秒(用户已确认)

---

## 📦 完工产物

### 本机文件(`C:\Users\Administrator\cow\tools\`)

| 文件 | 大小 | 用途 |
|---|---|---|
| `watchdog_ecs.ps1` | 2.5 KB | 探活主脚本(ASCII only) |
| `install_watchdog_task.ps1` | 2.2 KB | 注册任务计划(以 SYSTEM 跑)|
| `WATCHDOG_README.md` | 2.7 KB | 安装 + 验证 + 卸载文档 |
| `logs/watchdog.log` | ~250 B | 探活日志(每 5 min 一行) |

### Windows 任务计划

| 字段 | 值 |
|---|---|
| 名称 | `WATCHDOG_ECS` |
| 触发 | 每 5 min |
| 身份 | SYSTEM(Highest) |
| 设置 | 网络可用就跑 / 不充电停 / StartWhenAvailable |
| 命令 | `powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File watchdog_ecs.ps1` |

---

## 🪤 本轮踩坑(已固化 RULE.md #5)

### 坑:PowerShell 5.x ASCII-only 才稳

**症状**:`install_watchdog_task.ps1` 包含 emoji(`✗` `ℹ`)和中文注释,parser 直接报
```
字符串缺少终止符: "。
```
第 21 行的 `}` 报"语句块或类型定义中缺少右"}"" — **整个脚本根本没跑**。

**根因**:PowerShell 5.x 默认 GBK codepage,多字节字符边界错位,parser 在某行提前终止。

**修法**:PowerShell 脚本**全部 ASCII**(注释也用英文)。
- 允许:变量名/字符串/注释纯英文 + ASCII 符号
- 不允许:emoji(✓ ✗ ℹ ⚠ ❌)、中文注释、中文字符串
- 真要中文:用 PowerShell 7+(`pwsh`),或把中文存到独立 `.txt` 文件再 Read

**已固化进 RULE.md 第 5 条,7/13 18:33 立**。

---

## 🎯 三层防御全景(完工)

| Layer | 在哪 | 干什么 | 状态 |
|---|---|---|---|
| **Layer 1** | ECS 上 | 进程级:healthcheck 失败 → supervisorctl restart | ✅ 7/13 18:25 完工 |
| **Layer 2** | Windows 上 | ECS 级:ECS 整个挂了 → 桌面通知 | ✅ **7/13 18:33 完工** |
| **Layer 3**(v2.0)| 微信 | 用户级:任何异常 → 微信告警 | 🟡 等 v2.0 用户系统 |

---

## 🎯 下一步

| # | 动作 | 触发 |
|---|---|---|
| 1 | 日常观测 | 任务计划自动跑,无需手动 |
| 2 | v1.2.1 → v2.0 RFC 实施(用户系统 + 微信告警) | 用户量起来后 |

---

## 📚 关联文档

- **Layer 1 监控 RFC**:`knowledge/analysis/taixuan-web-ecs-monitoring-rfc-2026-07-13.md`
- **ECS v1.2.1 完工**:`knowledge/analysis/taixuan-web-v121-completion-2026-07-13.md`
- **DASHBOARD v13**:`tmp/windows/DASHBOARD.md`
- **RULE.md 第 5 条**:PowerShell 5.x ASCII-only

---

*本报告于 2026-07-13 18:35 由泰在 3 项验证全过 + 桌面气泡通知成功后写。*