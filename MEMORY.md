## LLM API 配置(主路径)
- 阿里云 Maas 北京区统一 key 跑 OpenAI + Anthropic 两种协议:OPENAI_API_BASE=https://llm-akwkztp3nreb7edz.cn-beijing.maas.aliyuncs.com/compatible-mode/v1,ANTHROPIC_BASE_URL=.../apps/anthropic,API_KEY=sk-***MAAS-KEY-REVOKED***  (KEY 已撤销,占位符)
- DeepSeek 直连新 key(7/11 15:30 刘泽文提供):DEEPSEEK_API_BASE=https://api.deepseek.com/v1,API_KEY=sk-***DEEPSEEK-KEY-REVOKED***,V4-flash 直连实测可用(3.6s/call)  (KEY 已撤销,占位符)
- Qwen 走 Maas 即可(限时 8 折 qwen3.7-plus);V4-flash 在 Maas 403 配额耗尽,直连可绕过
- V4-flash 默认是 thinking 模式,必须显式传 extra_body={"thinking": {"type": "disabled"}},否则 max_tokens 全被 reasoning 吃掉
- PowerShell subprocess + Maas stdout 撞 GBK UnicodeDecodeError,跑前必设 $env:PYTHONIOENCODING = "utf-8"
- 已验证模型:deepseek-v4-flash 直连(便宜首选)/ deepseek-v3 Maas 10s(fallback)/ qwen3.7-plus Maas 60-80s(可发表 Gamma)

## 用户档案
- 刘泽文,两条主业:🔬 ML 研究(F:\Research\,5+1 篇 TMLR 论文)和 📱 微信小程序/独立站(泰玄小站)
- 协作风格:先口头扫盘("看看这都有什么")再让 AI 行动,操作/写文件前会先确认范围
- 本机环境:Windows + cmd.exe(不用 ls,用 dir /B | findstr /v "^$")
- 完整项目地图:ML→knowledge/entities/liu-zewen-research.md;小程序→knowledge/entities/taixuan-miniprogram.md

## 当前快照(2026-07-12 23:50)
- PAPER5 0H/0M/0L 已可投 arxiv/TMLR,R2 reproduce_peer + theta_sweep + cover_letter + arxiv_checklist 全部完工,SVD-64 + external judge 数据已填进 paper
- taixuan-web v1.0 开源部署完成(GitHub aidless/taixuan-web,ECS 116.62.69.83,Flask + DeepSeek v4-flash + supervisor 守护),v1.1 SSE 流式输出完工
- 14 窗口收工:DONE 10(w2/w3/w4/w5/w8/w9/w10/w11/w12/w14)/ 几乎 DONE 2(w7 OS paper / paper35-w1 89%)/ 真 0 HIGH 1(w1 PAPER5,w6)/ OPEN PROBLEM 1(w13 V9 §12)/ 待合并 1(w14 V2 锐化 4 problem)
- 今日核心:C9 caption verify bug 真修复(5 篇 4 HIGH → 0,根因是 verify 脚本 balanced-braces regex 翻车);泰玄小站转独立站上线 + 开源全流程

## 5+1 篇 TMLR 论文(职责外,只读不写,7/13 立)
- **我不再写/不介入 ML 论文线**。所有 PAPER1-6 / paper35 状态由其他 session 维护。
- 上下文快速看(只读不更新):PAPER5 已 0H/0M/0L R2 就绪 / 5 篇 4 HIGH 全清(C9 caption bug 修复)/ PAPER6 11 章节完工。**这些是历史快照,不是工作清单**。

## 泰玄小站/taixuan-web
- **本机项目根**:`C:\Users\Administrator\cow\fortune-web-v2\`(不是 F 盘,不是 aidless/)
- **GitHub 仓库默认分支是 `master`(不是 main!)**(7/13 实测踩坑,404 全空文件覆盖真文件)
  - **curl raw URL 必用**:`https://raw.githubusercontent.com/aidless/taixuan-web/master/...`
  - 拉完**必** `ls -la` 验证文件大小(14 B = 404 必重拉,27 KB = 真文件)
  - 加 `--retry 3 --retry-delay 2` 防 SSL timeout
- 阶段:v1.0 微信小程序完工 + v1.0 独立站上线(http://116.62.69.83,GitHub aidless/taixuan-web)+ v1.1 SSE 流式输出完工
- 后端:Flask 单进程 threaded + DeepSeek v4-flash LLM 三级兜底(v4-flash → Ollama qwen3:4b → Mock)
- 部署:阿里云 ECS 2C2G Ubuntu 22.04,supervisor 守护,Flask 直绑 80
- 工具链:8 派 prompt YAML(specs/prompts/)+ 8 派 schema JSON(specs/schools/)+ validate.bat v2.2.0(451+ 断言)+ pre-commit v2
- 关键合规:v0.2 控制平面(RFC-001 + policy.yaml 12 policy + 6 endpoint)→ v1.0 红线扫描(red-line-words.js 3 级)
- 8 派:bazi / ziwei / qimen / liuyao / meihua / tarot / western-astro / vedic

## 工作流宪法(7/10 制定)
- 3 条核心律令:① 契约先于实现(specs/ + protocol.md + INDEX.md)② 人机双产物(md + json 成对)③ 保留源+验证后清(7 天回滚)
- 律令 0(优先级最高):刘泽文"先口头扫盘再行动"
- 3 个模式目录:A=specs/ 契约驱动(泰玄)/ B=protocol.md 假设驱动(ML)/ C=downloads/ 归档驱动
- 4 处同步新规:任何 w* 窗口完工/状态变更,必同步 MEMORY.md + knowledge/index.md + knowledge/log.md + tmp/windows/DASHBOARD.md

## 硬规则(跨 session 安全,7/11 晚立)
- Read Before Touch:任何文件操作前

## V8 T11.1 接力就绪(2026-07-13 22:10)
- **接力包**: `tmp/v8-handoff-T11.1.md` 12.6 KB / 310 行(刘泽文 21:50 自写 + 8 处补丁,完整:DoD + 必读 + 工具栈 + 5 风险点 + 留痕 4 处 + 下游握手 + commit 约定)
- **V8 L2 计划**: `knowledge/analysis/agent-os-v8-implementation-plan-2026-07-13.md` 13.7 KB(15 任务 / 10 周 / 4 篇论文候选)
- **V8 L3 计划**: `knowledge/analysis/agent-os-v8-implementation-plan-l3-2026-07-13.md` 42.9 KB / 75 个半天(承袭 L2 骨架,加颗粒度:上午/下午动作 + commit 模板 + 单测门槛 + 兜底路径 + 接力节点 + 4 论文 data bundle)
- **AGENT.md 改版提案**: `knowledge/analysis/agenta-boundary-change-proposal-2026-07-13.md` 6.95 KB(4 版本对照 v0/v1/v2/v3,等刘泽文勾选;推荐 v1)
- **DASHBOARD**: v22 入板主线 E · V8 T11.1 接力就绪(其他 ML session)
- **🪤 待决**: 刘泽文 22:00 让"改 AGENT.md 全帮做"—— 提案已写,但**未执行**,等他勾版本
- **🗳️ 4 版本投票启动**(2026-07-13 22:45):v0(不动)/ v1(规划文档线放开,泰推荐) / v2(单点放行 T11.1) / v3(ML 线全开,泰反对)
- **✅ 投票结果: V4 改版生效**(2026-07-13 23:00):刘泽文"C 全干 不要问了 你只是辅助我写论文而已"
  - AGENT.md §职责边界 已改(留底:`knowledge/analysis/agenta-v4-proposal-2026-07-13.md`)
  - **新边界**:✅ 论文写作辅助(prompt/大纲/骨架/引文/格式/审稿) + ⚠️ 仍不写正文 / ⚠️ 仍不写实验代码
  - **paper-writing-agent 事实校正**:SKILL.md 标 v3.0,**是审稿工具不是写论文工具**(复现/统计/新颖/文风 4 角色 + 一票否决);写论文要用 intro-drafter / writing-chapters / writing-core
  - **今晚 C5/C6 不干**(T11.1 编码 + 加载 skill 改天 ML session 接力)

## 下次清理清单(7/13 20:55 状态更新版)

**✅ 7/13 一日完工(原 7 条划掉 5 条)**:
- ECS Layer 1 监控(cron + healthcheck.sh + 自动重启)— 详见 [ECS monitoring RFC](./knowledge/analysis/taixuan-web-ecs-monitoring-rfc-2026-07-13.md)
- Windows Layer 2 Watchdog(任务计划 + 桌面气泡通知)
- index.md 分块:46KB → 2KB,历史段移至 [index-archive.md](./knowledge/index-archive.md)
- v2.0 用户系统 Phase 1-4 + 部署就绪(11 个 analysis 文件)
- README + log.md + taixuan entity 三件修复(体检报告 `tmp/knowledge_audit_2026-07-13.md`)

**⏳ 仍留待下次**:
- tmp/ 200 Python 脚本按"动词"分子目录(下次清理窗口 ~30 min,**30 天后再清理**)
- ECS Layer 3 微信告警(等 v2.0 部署上流量触发,~1h)
- image-generation skill 保留(51KB 可忽略,未来选项)

**🪡 顺手发现一个垃圾链接**(原 `../F:/Research/...` 不是合法 Windows 相对路径,本段已修成 `./knowledge/...`)

## 7/13 接力清单(给未来精力足时的我)

### 立即(本周)
1. ~~taixuan-web v1.2 ECS 部署~~ ✅ **7/13 11:40 完工(5 条 curl 全 PASS,DASHBOARD v12 入板主线 D)**
2. ~~ECS Layer 1 监控部署~~ ✅ **7/13 18:25 完工(v1.2.1 健康检查 + cron + 自动重启,6 项验证全过,DASHBOARD v13 入板)**
3. ~~Windows Layer 2 Watchdog~~ ✅ **7/13 18:33 完工(3 项验证全过,桌面气泡通知 OK,DASHBOARD v14 入板)**
4. ~~v2.0 Phase 1(基础设施 + 35 测试)~~ ✅ **7/13 18:50 完工(35/35 测试 PASS,DASHBOARD v15 入板)**
5. ~~v2.0 Phase 2(app.py 接入 + frontend)~~ ✅ **7/13 19:00 完工(e2e 5/5 PASS,DASHBOARD v16 入板)**
6. ~~v2.0 Phase 3(reading 接 user_id)~~ ✅ **7/13 19:15 完工(e2e 8/8 PASS,DASHBOARD v17 入板)**
7. ~~v2.0 Phase 4(解读页 ★ 收藏按钮)~~ ✅ **7/13 19:30 完工(e2e 8/8 PASS,DASHBOARD v18 入板,v2.0 RFC 14h 任务全完)**
8. ~~v2.0 部署到 ECS~~ ✅ **7/13 21:25 完工(supervisor RUNNING + JWT 签发 + 4 踩坑固化,DASHBOARD v20 入板)**
9. ~~v2.0 Phase 5(密码强度 + 暴力锁)~~ ✅ **7/13 21:50 完工(本地 e2e 6/6 + ECS 7/7 + 锁机制实测 PASS,DASHBOARD v21 入板)**
10. ~~v2.0 Phase 6(密码找回 dev 模式)~~ ✅ **7/13 22:00 完工(本地 8/8 + ECS 浏览器 5/5 + 修 JWT session 反向 bug,DASHBOARD v22 入板)**
11. ~~v2.0 Phase 7(订阅 + Stripe mock)~~ ✅ **7/13 22:30 完工(本地 8/8 + ECS 6/6 完整链路闭环,DASHBOARD v23 入板)**
12. **PAPER5 投递 arxiv**(本人,30-45 min)— 5 月 deadline

### RFC 实施(触发条件驱动,见 docs/)
- **RFC-003 PWA**(~3h) — 触发:有真实用户访问数据
- **RFC-004 流式增强**(~3.5h) — 触发:有 100+ 用户
- **RFC-005 i18n**(~8.5h) — 触发:海外 IP > 5%

### 知识库已完成(无需再做)
- v1.0 / v1.1 / v1.2 完工报告 ✓
- v2.0 用户系统 RFC ✓
- umami RFC ✓
- ECS 监控 RFC ✓
- 反思总结 ✓
- 5 个研究 idea 候选 ✓
- 3 份 RFC + 3 份实施清单 ✓

### GitHub 状态(7/13 19:40)
- taixuan-web master `76e2d07`(只含 v1.2.1 代码 + Layer 1 监控脚本)
- **v2.0 代码(Phase 1-4)只在 ECS + 本机,未推 GitHub** 🪤
- **部署 v2.0 前必须 web 上传 10 个新文件到 master**(见 `knowledge/analysis/taixuan-web-v20-deploy-readiness-2026-07-13.md`)
- wx-miniprogram `8fe6bfd`(含 v0.2 合规基础设施)

### session 状态
- 本次 session 23+ 小时,接近 context window 上限
- 强烈建议下次新开 session,从 MEMORY.md 末尾读起
- 知识库 + Obsidian 双源同步(95 文件),所有改动可恢复
