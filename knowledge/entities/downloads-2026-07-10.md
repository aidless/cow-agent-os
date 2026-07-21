# Downloads 2026-07-10 — 11 项目 30 秒说明

> **⚫ 2026-07-10 历史快照** — 本页最后更新 2026-07-11 00:01,11 项目 30 秒说明。
> **7/11 之后未激活任何一个项目**,本页**仅作历史参考**。归档目录 `C:\Users\Administrator\cow\downloads\2026-07-10\` 仍保留(可重激活)。

**目录**:`C:\Users\Administrator\cow\downloads\2026-07-10\`
**索引页**:`downloads/2026-07-10/INDEX.md`
**整理日**:2026-07-10

---

## 🎯 agent-frameworks/(3 项,143.63 MB)

### 1. `caveman/`(0.81 MB)
- **干什么**:让 AI 编程 agent 用"穴居人"语言回答(why use many token when few do trick)
- **声称收益**:**65% 更少 output token**,但脑容量不变
- **兼容性**:works with 30+ agents
- **场景**:跑大量 agent 任务时,**省 token 钱**;输出质量用户已多次验证
- **下一步**:试一下 `INSTALL.md`,挑 1 个 skill 改写成"穴居人风格"

### 2. `moyin-creator/`(17.13 MB,中文 README)
- **干什么**:**魔因漫创**(Moyin Creator)—— 中文 AI 影视生产级工具
- **声称收益**:AI 影视从剧本到成片**全流程批量化**,支持 **Seedance 2.0**
- **许可证**:AGPL-3.0
- **场景**:如果要做 AI 短剧/动画,**对接 Seedance 2.0 时用这个编排**
- **下一步**:读 `docs/WORKFLOW_GUIDE.md`,看是否适合泰玄小站"短视频内容"模块

### 3. `midscene-1.10.3/`(125.69 MB,主体项目)
- **干什么**:**Midscene.js** —— 自然语言写 UI 测试,vision-driven
- **npm**: `@midscene/web`,基于 UI-TARS-1.5-7B(字节开源)
- **场景**:泰玄小站 v2.0 的 **wxml 自动化测试**(替代手点)
- **下一步**:如果是给 mini-program 写 UI 测试,要的是 `@midscene/web` 还是 mini-program 适配版

---

## 🛠 claude-tools/(1 项,1.62 MB)

### 4. `taste-skill/`(Anti-Slop Frontend)
- **干什么**:**反烂尾前端**框架 —— 给 AI agent 用的 portable agent skills
- **声称改进**:layout、typography、motion、spacing(AI 烂尾 UI 的 4 个高发区)
- **附带**:**image-generation skills** for reference boards(配合 ChatGPT Images 生成参考)
- **场景**:泰玄小站 v2.0 页面的"避免 AI 烂尾风"
- **下一步**:对照 MEMORY 里"泰玄小站 v2.0 specs"看能不能直接套用 taste-skill 的风格规范

---

## 📚 reference/(2 项,10.93 MB)

### 5. `system-prompts-and-models/`(2.33 MB)
- **干什么**:**x1xhlol/system-prompts-and-models-of-ai-tools** 拷贝
- **内容**:各 AI 工具的完整 system prompts 与模型配置(Cursor, Aider, Cline...)

### 6. `system-prompts-leaks/`(8.6 MB)
- **干什么**:**asgeirtj/system_prompts_leaks** 拷贝
- **内容**:**实际泄露的 system prompts**(被报道过的,含 WaPo 报道)
- **覆盖**:Claude Opus 4.8 → Fable 5 / Sonnet 5 / Codex 5.5 / Claude Code (Glob + Grep) / Claude Design (Opus 4.8,48 tools,16 skills,9 starter sources)
- **场景**:**研究 AI 指令工程的真实样本**(比官方文档更接地气)
- **下一步**:研究 AI 指令对齐时,**配合 PAPER1-6 用**(避免我们造的提示词也是"烂尾")

---

## ⚙️ runtime/(2 项,23.72 MB)

### 7. `strix-1.0.4/`(4.73 MB)
- **干什么**:**开源 AI 安全 agent** —— 找并修 app 漏洞
- **PyPI**: `pip install strix-agent`
- **许可证**:Apache-2.0
- **场景**:泰玄小站上线前的**自动化安全审计**(微信审核虽然不是 web 攻击面,但 wxml 渲染器 + LLM 输出仍是攻击面)

### 8. `seedance-2.0/`(18.99 MB)
- **干什么**:**Seedance 2.0 Skill OS** —— "导演式"AI 影视调度
- **特点**:**28 sub-skills / 60 references / 126 evals**(版本 v6.6.0)
- **场景**:配合 moyin-creator 做"短视频生产"
- **下一步**:评估**字节 Volcengine Ark API 接入**(模型在 Volcengine 上的价格)

---

## 🕷 scraping/(已有,7/10 建)

### 9. `firecrawl-2.11.0/`(详见既有)
- **干什么**:Web scraper + 结构化 API
- **状态**:7/10 已建,本次发现 `firecrawl-main` 是其**字节级重复**,移到 `duplicates-removed/`

---

## 🗑 duplicates-removed/(3 项,49.76 MB)

| 项目 | 来源 | 与谁重复 | 处理 |
|---|---|---|---|
| `firecrawl-main_DUP_of_2.11.0/` | web_c4683a03 | scraping/firecrawl-2.11.0(README SHA256 完全相同) | **未删源 zip**,7/17 后可清 |
| `taste-skill_DUP/` | web_c7c1a699 | claude-tools/taste-skill(同一份) | **未删源 zip**,7/17 后可清 |
| `public-apis_TRUNCATED/` | web_ec199caa | 只有 scripts/,缺 README/INDEX | **未删源 zip**,7/17 后可清 |

---

## 🎯 用这批项目的"提问方式"

| 想做什么 | 看这里 |
|---|---|
| 写论文提示词 | reference/system-prompts-leaks + reference/system-prompts-and-models |
| 做一个短视频 | moyin-creator + seedance-2.0 |
| 自动测试小程序的 UI | midscene-1.10.3 |
| 减少 AI 浪费 token | caveman |
| 给前端反 AI 烂尾 | taste-skill |
| 给小程序做安全审计 | strix-1.0.4 |
| 爬公开网页 | scraping/firecrawl-2.11.0 |

---

## ⏰ 待办(下次想起来再说)

- [ ] 评估 seedance-2.0 是否要走字节火山方舟路线
- [ ] 试一下 caveman 的 INSTALL.md 看是否真的省 token
- [ ] strix 是否能给泰玄小站的 wxml 渲染器扫一次
- [ ] taste-skill 的 anti-slop 规范能否写成泰玄小站 v2.0 的 style guide
- [ ] system-prompts-leaks 是 awesome 资源 → 给 MEMORY 加一条 "📚 引用资料"