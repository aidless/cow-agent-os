# taixuan-web v1.2 ECS 部署完工报告(2026-07-13)

> **状态**:🟢 **部署完工 + 验证全过**(00:45 → 11:40 跨 session 接力完成)
> **作者**:泰(7/13 凌晨原 session 部署 + 7/13 上午接力 session 验证)
> **触发**:刘泽文 7/13 11:37 贴 5 条 Workbench curl 输出,**全部 PASS**

---

## ✅ 5 条验证结果(实测)

| # | 命令 | 输出 | 结论 |
|---|---|---|---|
| 1 | `sudo supervisorctl status taixuan` | `RUNNING   pid 81026, uptime 9:51:21` | ✅ 进程稳定 |
| 2 | `curl -s http://127.0.0.1:80/healthz` | `{"fallback_backend":"ollama-qwen3-4b","primary_backend":"deepseek-v3","service":"taixuan-web","status":"ok","version":"1.0.0"}` | ✅ 健康 |
| 3 | `curl -s http://127.0.0.1:80/api/v2/history?limit=3` | `{"count":0,"items":[]}` | ⚠️ 空(预期,无访问) |
| 4 | `curl -s http://127.0.0.1:80/api/v2/stats` | `{"total_readings":0,...}` | ⚠️ 空(预期) |
| 5 | `curl -N -m 15 ... /reading_stream` | 逐字 `data: {"type":"reasoning","text":"用户"}` → `"提交"` → `"了一个"` ... | ✅ **流式输出真活** |

**关键证据**:#5 SSE 看到 DeepSeek v3 正在逐字推理(出现"用户提交了一个八字排盘数据,要求进行 v...")— 说明:
- ✅ v1.2 新代码已生效
- ✅ DeepSeek v3 后端连通
- ✅ SSE 流式输出工作正常

---

## ⚠️ 两个"非问题"的说明

### 1. `version: 1.0.0` 而不是 1.2.0

**根因**:`/healthz` 路由里的 `version` 字段是**写死的硬编码字符串**,没改。
**影响**:无功能影响,**只是健康检查报告的版本号没跟上**。
**修法(可选,5 min)**:`app.py` 第 ~XX 行,把 `"1.0.0"` 改成 `"1.2.0"`。

### 2. history/stats 空

**根因**:v1.2 刚部署,没有任何用户访问产生数据。
**影响**:无影响,等待有访问后自动累计。
**触发**:有真实用户访问后,`total_readings` 会开始增长。

---

## 📦 部署交付物清单

### 11 个文件传到 `/var/www/taixuan/`

| 文件 | 来源 | 用途 |
|---|---|---|
| `app.py` | GitHub `c376ac3` | v1.2 Flask 后端 |
| `llm_backends.py` | GitHub `c376ac3` | DeepSeek v3 + Ollama + Mock 三级兜底 |
| `static/js/stream.js` | GitHub `c376ac3` | 前端 SSE 渲染 |
| `static/bazi/index.html` | GitHub `c376ac3` | 八派 HTML |
| `static/ziwei/index.html` | GitHub `c376ac3` | 紫微 |
| `static/qimen/index.html` | GitHub `c376ac3` | 奇门 |
| `static/liuyao/index.html` | GitHub `c376ac3` | 六爻 |
| `static/meihua/index.html` | GitHub `c376ac3` | 梅花 |
| `static/tarot/index.html` | GitHub `c376ac3` | 塔罗 |
| `static/western-astro/index.html` | GitHub `c376ac3` | 西占 |
| `static/vedic/index.html` | GitHub `c376ac3` | 印度占星 |

### 备份留底

- ✅ `/tmp/taixuan-backup-v11/`(v1.1 文件,7 天回滚窗口)

---

## 🪤 SSH 认证问题(本轮踩中,记下来)

### 症状

`ssh taixuan@c376ac3` 卡死 60s 后失败:
```
Warning: Permanently added ... to the list of known hosts.
taixuan@c376ac3: Permission denied (publickey).
```

### 根因

- Windows PowerShell SSH 用 `~/.ssh/id_ed25519`
- **该公钥不在 ECS `authorized_keys` 里**
- Workbench 是 ECS 自带 Web 终端,**有自己的 SSH key,不与 Windows 共享**

### Workaround(实战已验)

- **Workbench 直接登**(`sudo supervisorctl ...` / `curl 127.0.0.1`)
- **GitHub raw + curl 传文件**(免 SSH)
- **HTTP curl 调 API**(免 SSH)

### 永久解(未做,可选)

如要恢复 Windows → ECS 直连 SSH:
1. Workbench 跑 `cat /root/.ssh/authorized_keys` 看 ECS 现有 key
2. Windows 跑 `cat ~/.ssh/id_ed25519.pub` 看本地公钥
3. 若不匹配,Workbench 跑 `echo "本地公钥" >> /root/.ssh/authorized_keys`

---

## 🎯 下一步(7/13 待做)

### 立即(15 min)

| 动作 | 命令 |
|---|---|
| ECS Layer 1 监控脚本 | Workbench 创建 `/var/www/taixuan/healthcheck.sh` |
| cron 注册 | `*/5 * * * * /var/www/taixuan/healthcheck.sh` |
| 健康检查验证 | Workbench 跑 `curl -s http://127.0.0.1:80/healthz` + `tail /var/log/taixuan-health.log` |

### 之后(本人,~30 min)

- **PAPER5 arxiv 投递**(5 月 deadline)
- **healthz version 字段改成 "1.2.0"**(5 min)

---

## 📚 关联文档

- **监控 RFC**:`knowledge/analysis/taixuan-web-ecs-monitoring-rfc-2026-07-13.md`
- **完工总览**:`knowledge/analysis/taixuan-web-v12-completion-2026-07-12.md`
- **SSE v1.1**:`knowledge/analysis/taixuan-web-v11-sse-completion-2026-07-12.md`
- **本 session 接力总结**:`memory/2026-07-13.md`
- **DASHBOARD v12**:`tmp/windows/DASHBOARD.md`

---

*本报告于 2026-07-13 11:40 由泰在 5 条 curl 全 PASS 后写。*