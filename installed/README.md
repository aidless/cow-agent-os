# Installed Skills — 主动安装记录

**建立**: 2026-07-11 09:00
**目的**: 区分"主动安装" vs "自动继承"的 skill
**配合**: 7/10 已建立的 1273 个 symlink(`~/.cc-switch/skills/` → `~/.claude/skills/`)

---

## 🎯 这个目录存在的理由

7/10 你装了 1291 个 skill,其中绝大多数是**继承的**(从 cc-switch 的 marketplace 同步)。
其中**真正"主动挑"**的可能不超过 30 个。`installed/` 跟踪这批主动的 skill。

## 📂 目录结构

```
installed/
├── README.md              ← 本文件
├── _record_install.ps1    ← 幂等脚本(主动安装时调)
└── <skill-name>.md        ← 每个主动 skill 一份说明
```

## 🛠 使用方式

**主动装一个新 skill** 时:

```powershell
.\installed\_record_install.ps1 -SkillName "foo" -Reason "..."
```

**主动卸载时**:直接 `rm installed/foo.md` + `rm ~/.claude/skills/foo`

**审计所有主动 skill**: `Get-ChildItem installed/*.md | Where-Object Name -ne "README.md"`

## 📋 当前主动 skill 列表

(由 _record_install.ps1 自动维护)

| Skill | 首次记录 | 来源 | 用途 |
|---|---|---|---|
| `arxiv-tracker` | 2026-07-10 | 委托建设 | TMLR 论文每日 arxiv 抓取 + LLM 摘要 + relevance 评分 |
| `paper-changelog` | 2026-07-10 | 委托建设(部分) | 论文目录 commit-style changelog(等委托方交付完整) |
| `paper-review-toolkit` | 2026-07-10 | 委托建设 | 论文投稿前审阅(paper-writing-agent + tmlr-review-simulator) |
| `rr-responder` | 2026-07-10 | 委托建设 | R&R rebuttal 4 段 pipeline(review2queries / deep_critique / draft_response / render_latex) |
| `wechat-mp-validation` | 2026-07-10 | 委托建设 | 泰玄小站 v2.0.0 验证流水线(JS/JSON/spec/合规/包体积) |
| **`paper-graveyard`** | **2026-07-11** | **本地派生**(源自 `Shubhamsaboo/awesome-llm-apps/agent_skills/project-graveyard`,Apache-2.0) | **F:\Research 论文死亡分析(9 类 paper 死因 + 25 unittest + 与 paper-changelog 联动)** |

---

## 🔗 关联

- `~/.cc-switch/skills/` —— 权威源(1273+ 个 skill)
- `~/.claude/skills/` —— active 软链接(自动随 cc-switch 同步)
- `tmp/_quarantine.md` —— 清理决策
- `WORKFLOW.md` —— 工作流宪法