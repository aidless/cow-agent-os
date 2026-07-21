# taixuan-web ECS 监控告警 RFC(v0.1)

**状态**:📋 设计阶段
**作者**:刘泽文
**日期**:2026-07-13
**目标**:让 ECS 挂了 / 资源爆 / API 异常**3 分钟内知道**

## 一、问题陈述

### 当前监控盲区

| 盲区 | 影响 |
|---|---|
| ECS 进程死了 | 用户访问 502,不知道 |
| 内存爆(2GB 临界) | OOM kill,服务停 |
| 磁盘满(40GB 临界) | SQLite 写入失败 |
| /healthz 失败 | LLM key 失效 / 代码 bug |
| LLM 调用持续报错 | 用户解读失败 |
| CPU 高 | 可能是被攻击 |

### 监控设计原则

- **3 分钟内知道**(不是天级)
- **轻量,不要被监控本身拖垮**(避免装 Prometheus + Grafana)
- **不要新依赖**(能 cron + curl 解决就不上工具)
- **优先级:进程 > 资源 > 业务**

## 二、3 层监控方案

### Layer 1 · ECS 内部 cron(基础)

**Workbench 跑**:

```bash
# 1. 创建监控脚本
mkdir -p /opt/taixuan-monitor
cat > /opt/taixuan-monitor/healthcheck.sh <<'EOF'
#!/bin/bash
LOG=/opt/taixuan-monitor/healthcheck.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === check start ===" >> $LOG

# 1. 进程检查
if ! sudo supervisorctl status taixuan | grep -q RUNNING; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: taixuan not running" >> $LOG
    sudo supervisorctl restart taixuan
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ACTION: restarted taixuan" >> $LOG
fi

# 2. healthz 检查
HEALTH=$(curl -s -m 5 http://127.0.0.1:80/healthz | head -c 200)
if ! echo "$HEALTH" | grep -q '"status":"ok"'; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: healthz failed: $HEALTH" >> $LOG
fi

# 3. 内存检查
MEM_PCT=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM_PCT" -gt 85 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: memory ${MEM_PCT}%" >> $LOG
fi

# 4. 磁盘检查
DISK_PCT=$(df -h /var/www/taixuan | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PCT" -gt 80 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: disk ${DISK_PCT}%" >> $LOG
fi

# 5. API 业务检查
STREAM=$(curl -s -m 5 -X POST http://127.0.0.1:80/api/v2/liupai/bazi/reading_stream \
  -H "Content-Type: application/json" \
  -d '{"question":"test"}' 2>&1 | head -c 200)
if echo "$STREAM" | grep -q '500 Internal'; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: stream API 500: $STREAM" >> $LOG
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === check done ===" >> $LOG
EOF

chmod +x /opt/taixuan-monitor/healthcheck.sh

# 2. 加 cron(每 5 分钟一次)
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/taixuan-monitor/healthcheck.sh") | crontab -

# 3. 验证
crontab -l
echo "==== 跑一次 ===="
/opt/taixuan-monitor/healthcheck.sh
cat /opt/taixuan-monitor/healthcheck.log
```

**期望看到**:日志里 4 个"=== check ==="段。

---

### Layer 2 · 你本地 Watchdog(主动)

Windows PowerShell 写个轻量 watcher,每天 3 次 curl ECS `/healthz`:

```powershell
# 加到 Windows 任务计划程序
$taixuan_url = "http://116.62.69.83/healthz"
$taixuan_log = "$env:USERPROFILE\Desktop\taixuan-watch.log"
$response = try {
    (Invoke-WebRequest $taixuan_url -UseBasicParsing -TimeoutSec 10).StatusCode
} catch {
    "ERROR: $_"
}
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$timestamp  status=$response" | Add-Content $taixuan_log
```

**每日 09:00 / 13:00 / 18:00** 自动跑。

**好处**:即使你**不去 ECS**,也能从 Windows 桌面日志看到 ECS 状态。

---

### Layer 3 · 微信通知(可选)

如果你想"被动收到告警",做最小微信通知:

**方案 A · 阿里云监控(免费)**:
- 阿里云 ECS 控制台 → 云监控 → 报警规则
- CPU > 80% 持续 5 min → 发短信(免费 1000 条/月)
- 缺点:只能监控 ECS 资源,**不能监控 Flask 业务**

**方案 B · 企业微信机器人**:
1. 建一个 1 人企业微信群
2. 群机器人 → Webhook URL
3. ECS 监控脚本 curl 这个 URL,带异常消息
4. 微信实时收到通知

**方案 C · 暂时不做**(等真出大事再说):
- 你目前流量小,v1.2 没真实用户
- ECS 挂了,supervisor 自动重启就行
- 监控是 v2.0 触发后再说

**我的推荐**:**先做 Layer 1 + Layer 2,Layer 3 等 v2.0 触发**。

## 三、监控指标分级

| 级别 | 指标 | 阈值 | 响应 |
|---|---|---|---|
| 🔴 P0 | 进程死了 | 自动重启失败 | 立即响应 |
| 🔴 P0 | /healthz 失败 | 持续 2 次 | 检查 LLM key |
| 🟠 P1 | 内存 > 85% | 持续 30 min | 排查泄漏 / 升级 |
| 🟠 P1 | /api 流式 500 | 持续 5 次 | 检查 LLM 调用 |
| 🟡 P2 | 磁盘 > 80% | 持续 1 天 | 清理 logs |
| 🟢 P3 | CPU > 60% 持续 1h | 持续 | 排查是否有攻击 |

## 四、不做(明确划线)

| 不做 | 原因 |
|---|---|
| Prometheus + Grafana | 太重,当前规模用不上 |
| 日志聚合(ELK) | 单机,grep 足够 |
| 业务指标(PV / 用户) | 已经有 SQLite readings.db |
| A/B 测试监控 | v2.0 之后再说 |
| 自动扩容 | ECS 单机够用,没需要 |

## 五、实施步骤

### Step 1 · Workbench 跑 Layer 1(15 min)

执行上面"Layer 1"那段 shell 脚本。

### Step 2 · 你 Windows 加 Layer 2(10 min)

把 PowerShell 脚本存到 `C:\Users\Administrator\cow\scripts\watch-taixuan.ps1`,
用任务计划程序每 4 小时跑一次。

### Step 3 · 验证(10 min)

```bash
# ECS 上
tail -20 /opt/taixuan-monitor/healthcheck.log

# Windows 上
Get-Content $env:USERPROFILE\Desktop\taixuan-watch.log -Tail 5
```

### Step 4 · 7 天观察(被动)

不要主动看,等真有事故再来看日志,验证监控真的有效。

---

## 六、风险

| 风险 | 缓解 |
|---|---|
| 监控脚本本身写错 | 用 shell 不用 Python(更简单,出错也直观) |
| cron 失败 | 看 `journalctl -u cron` |
| 健康检查本身拖垮服务 | `--max-time 5` 5 秒超时 |
| 日志无限增长 | `logrotate` 或定期清(`> 10MB` 清空) |

---

## 七、未来(v2.0 触发)

如果 v2.0 用户系统上线 + 流量起来,再升级:

- **Layer 3 微信告警**:企业微信机器人,实时推送到微信
- **业务指标 dashboard**:用 umami 看 PV / 转化 / 留存
- **错误率监控**:LLM 调用 5xx 比例超 10% 报警
- **响应时间监控**:P95 latency 超 30s 报警

---

_本 RFC 草案。Layer 1 + Layer 2 立刻做(~30 min),Layer 3 等 v2.0 触发。_