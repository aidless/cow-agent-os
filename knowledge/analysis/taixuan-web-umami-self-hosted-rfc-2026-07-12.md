# umami 自托管 RFC(taixuan-web v1.3)

**状态**:📋 设计阶段
**作者**:刘泽文
**日期**:2026-07-12
**目标版本**:taixuan-web v1.3(预计 2h 工作量)

## 一、为什么选 umami

| 工具 | 优 | 劣 |
|---|---|---|
| Google Analytics | 功能强 | 国内被屏蔽 + 数据出境 + GDPR |
| 百度统计 | 国内快 | 隐私差 + 数据出境 |
| 友盟 | 国内 | 数据出境 |
| **umami 自托管** | **隐私友好 + 轻量 + 免费 + 数据自己管** | 自维护 |

**核心需求**:知道多少人来、转化率、不涉及个人识别 → umami 完全够用。

## 二、架构

```
ECS (116.62.69.83)
├── Flask (taixuan-web)
│   └── base.html 嵌入 umami tracker.js
└── Docker
    ├── umami (127.0.0.1:3000)         # Web UI
    └── umami-db (Postgres 16)         # 数据库
```

**外部访问**:通过 nginx 反代 `umami.taixuan-web.xyz`(子域名)或 `/umami` 路径。

## 三、docker-compose.yml 增量

```yaml
version: "3.8"

services:
  # ... 现有 taixuan 服务 ...
  app:
    # 不变

  # 🆕 umami
  umami-db:
    image: postgres:16-alpine
    container_name: taixuan-umami-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: ${UMAMI_DB_PASSWORD:-changeme123}
    volumes:
      - umami-db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U umami"]
      interval: 10s
      timeout: 5s
      retries: 5

  umami:
    image: ghcr.io/umami-software/umami:postgresql-v2
    container_name: taixuan-umami
    restart: unless-stopped
    depends_on:
      umami-db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://umami:${UMAMI_DB_PASSWORD:-changeme123}@umami-db:5432/umami
      APP_SECRET: ${UMAMI_SECRET:-change-this-random-secret}
    ports:
      - "127.0.0.1:3000:3000"   # 只绑 localhost,通过 nginx 暴露
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  umami-db-data:
```

## 四、安装步骤

### Step 1 · Workbench 加依赖

```bash
cd /var/www/taixuan
# .env 加密码
echo "UMAMI_DB_PASSWORD=$(openssl rand -hex 16)" >> .env
echo "UMAMI_SECRET=$(openssl rand -hex 32)" >> .env

# 拉新镜像
docker compose pull umami umami-db
```

### Step 2 · 启动

```bash
docker compose up -d umami-db umami
sleep 10
docker compose logs umami | tail -20
```

**期望看到**:umami 启动 + 数据库连接成功。

### Step 3 · 首次配置

```
浏览器打开 http://127.0.0.1:3000
默认账号:admin
默认密码:umami
(强制要求立即改密码!)
```

### Step 4 · 加网站 + 拿 tracking code

1. 登录后 Settings → Websites → Add website
2. Name: `taixuan-web`
3. Domain: `wanxiangapp.xyz`(主域名)
4. 提交 → 拿到 tracking code:

```html
<script async defer data-website-id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        src="https://umami.taixuan-web.xyz/script.js"></script>
```

### Step 5 · 嵌入 base.html

`templates/base.html`(`<head>` 末尾):

```html
{% if umami_website_id %}
<script async defer
        data-website-id="{{ umami_website_id }}"
        src="https://umami.taixuan-web.xyz/script.js"></script>
{% endif %}
```

`app.py` 注入 `umami_website_id` 到所有模板上下文。

### Step 6 · nginx 反代(可选,但推荐)

`/etc/nginx/conf.d/taixuan-umami.conf`:

```nginx
server {
    listen 80;
    server_name umami.taixuanapp.xyz;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Step 7 · certbot SSL

```bash
sudo certbot --nginx -d umami.taixuanapp.xyz
```

### Step 8 · 验证

打开 http://116.62.69.83 浏览器访问几个页面 → 等 5 分钟 → 看 umami Dashboard 有访问记录。

## 五、ECS 资源评估

| 资源 | 当前 | 加 umami 后 |
|---|---|---|
| 内存 | 2GB | 2.8GB(umami + postgres 各 ~400MB) |
| 磁盘 | 40GB | 41GB(postgres 数据 ~10MB/天) |
| CPU | 2 核 | 偶尔峰值,无压力 |

**风险**:2GB 内存吃紧。**对策**:先观察,如果 OOM 加 swap 或升级 4GB。

## 六、监测指标

| 指标 | 含义 | 阈值 |
|---|---|---|
| 日 PV | 总访问 | > 100 → v2.0 用户系统 |
| 月独立 IP | 真实访客 | > 50 → v2.0 触发 |
| 派别点击 | 哪派最热 | 数据驱动运营 |
| 解读完成率 | 提交表单 / 提交后看到结果 | > 80% |
| 入口页 | 用户从哪个页面进 | 优化 SEO |
| 设备分布 | mobile vs desktop | 决定 UX 优先级 |

## 七、隐私合规

- umami **不收集 IP**(只 hash 后存)
- 不放 cookie
- 不放 fingerprint
- 符合 GDPR / 中国个人信息保护法
- `templates/base.html` 加隐私链接:

```html
<footer>
  <a href="/privacy">隐私政策</a>  ·  本网站使用 umami 自托管统计,数据全部在本机
</footer>
```

## 八、不做(明确划线)

| 不做 | 原因 |
|---|---|
| 事件追踪(自定义 event) | v1.3 只看 PV / 跳出率,事件追踪 v1.4 |
| 热力图 | 需要 Hotjar 类工具,复杂度高 |
| 漏斗分析 | 需要 A/B 测试,v3.0 再说 |
| 实时 Dashboard | umami 自带,够用 |

## 九、首次部署成本

| 项 | 工作量 | 备注 |
|---|---|---|
| 写 docker-compose | 20 min | 上面 YAML 直接用 |
| 部署 + 启动 | 20 min | docker compose up |
| 首次配置 + 加网站 | 10 min | UI 操作 |
| 嵌入 tracking 代码 | 10 min | 改 1 个模板 |
| nginx + certbot | 30 min | 如果要 SSL |
| **总计** | **~1.5h** | 比原计划 2h 快 |

---

_本 RFC 草案,ECS 上内存余量观察 1 周后再决定是否部署。_