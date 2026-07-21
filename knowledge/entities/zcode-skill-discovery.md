# ZCode Skill Discovery — `_diag_skills.py` 实体

> **来源**:`f:\TMLR\_diag_skills.py`(113 行,SHA-256 `EEA705937E236212D299E5140367BB145984DE6A8112F38D8541135FACAB5DD5`)
> **整理日**:2026-07-11
> **与 cow/skills/ 关系**:**完全不同的栈** —— 这是 ZCode CLI 体系,不是 hermes-agent 体系
> **状态**:🟡 归档(不激活,待刘泽文决定是否复用)

---

## 🎯 一句话定位

一个**完整可跑**的 Python 3 脚本,模仿 ZCode IDE 的 `zcode-guide/diagnosing-skills`,
扫描 **5 个 skill 发现根**,判断每个 `SKILL.md` 的 frontmatter 是否合法、是否被同名 skill 覆盖。

**唯一性**:本脚本**不读 `cow/skills/`** —— 它认的是 ZCode CLI 的 5 个根(见下)。

---

## 📂 5 个 Skill 发现根(优先级 P1 > P2 > P3 > P4 > P5)

| 优先级 | 路径 | 层级 |
|---|---|---|
| **P1** | `~/.zcode/skills` | 用户级 · ZCode 栈 |
| **P2** | `~/.agents/skills` | 用户级 · 通用 agents 栈 |
| **P3** | `~/ZCodeProject/.zcode/skills` | 工作区级 · ZCode 栈 |
| **P4** | `~/ZCodeProject/.agents/skills` | 工作区级 · 通用 agents 栈 |
| **P5** | `~/.zcode/cli/plugins/cache` | ZCode 插件缓存(技能以 `plugin:skill` 限定) |

> **优先级**:P1 > P2 > P3 > P4 > P5。**同名 skill** 时,优先级高的赢,其他的被 `[SHADOWED]` 标记。

---

## 🔍 5 段 Pipeline

| Step | 检查内容 | 输出 |
|---|---|---|
| **1** | `~/.zcode/cli/config.json` 的 subsystem 开关 + `plugins.enabledPlugins` + 顶层 `skills` key | 顶层 keys 列表 + enabled plugins |
| **2** | 扫 5 个根下所有 `SKILL.md`,解析 frontmatter | 每条:相对路径 + name + fm 状态(OK / NO_FM / FAIL_NO_NAME / FAIL_NO_DESC / FAIL_DESC_TOO_LONG)|
| **3** | **同名 skill 的优先级裁定** —— P1 > P2 > P3 > P4 > P5 | 被 shadow 的 skill 全列出 |
| **4** | **可加载集合** —— 只看 priority 最高的那个,分类 OK / NO_FM / FAIL | Totals: OK / NO_FM / FAIL / total_names |
| **5** | plugin cache 下 skill 的命名空间规则:`<plugin>:<name>` | 说明文字 |

**frontmatter 状态机**:
- `OK` — name + description 都齐全,description ≤ 1024 字符
- `NO_FM` — 没有 YAML frontmatter(默认 name = 目录名),**不会触发好**
- `FAIL_NO_NAME` / `FAIL_NO_DESC` / `FAIL_DESC_TOO_LONG` — **直接 drop**

---

## ⚙️ 依赖与运行

```python
# 标准库 only:json, os, re, sys, pathlib
# ROOT 硬编码为 Path(r"C:\Users\Administrator")
```

```bash
# 用 UTF-8 重定向避免 GBK 截断(RULE.md "Trap: PowerShell UTF-8" 的同款坑)
set PYTHONIOENCODING=utf-8
python _diag_skills.py > smoke.out 2> smoke.err
```

**注意**:`f:\TMLR\minimax-smoke.out` 和 `minimax-smoke.err` **都是 0 字节**(2026-07-10 00:08) —— 大概率是同一次执行,但 stdout/stderr 被吃了。可能是 Windows `>` 重定向 + 编码问题。

---

## 🆚 与 cow/skills/ 体系对比

| 维度 | ZCode(本脚本)| hermes-agent(cow/skills/)|
|---|---|---|
| **发现根** | `~/.zcode/skills`、`~/.agents/skills`、`~/ZCodeProject/{.zcode,.agents}/skills`、`~/.zcode/cli/plugins/cache` | `cow/skills/`(本工作空间)+ `cow/installed/`(主动安装登记) |
| **frontmatter 校验** | name + description ≤ 1024 chars(3 种 FAIL 状态) | name + description(由 description 触发 skill 匹配,长度阈值未硬编码)|
| **shadowing** | P1 > P2 > P3 > P4 > P5 同名优先级 | 主要靠 `installed/` 登记,无自动优先级裁定 |
| **插件命名空间** | `<plugin>:<name>` | 无此概念 |
| **诊断方式** | **静态扫描** + 输出 `[SHADOWED] [OK] [NO_FM] [FAIL]` | **运行时调用 + 验证脚本**(见 `installed/<skill>.md`)|

---

## 🪤 关联发现(同次扫盘产出)

- `f:\TMLR\default/` 是 **Firefox 9.0.6 + Zotero 9.0.0.SOURCE 真实 profile**,**不是 headless 测试**(有 922KB `retractions.json` + 20 个 shader-cache + devtools IDB)。某项目借了你的 Firefox 跑 web 测试。
- `f:\TMLR\tools/skill_diag_runner.py`(46 行)是 `_diag_skills.py` 的**截断版**(STEP 3-5 缺失),**价值低**,可删。
- `f:\TMLR\experiments/` 是空目录(2026-07-10 00:34 创建)。
- `.pytest_cache/` + `minimax-smoke.out/err`(0 字节)是**测试运行时残留**,无内容价值。

---

## 🚦 决策记录

- **2026-07-11**:刘泽文"以前做的项目,看看有没有有用的" → 扫盘,确认 `_diag_skills.py` 是唯一有代码价值的产物 → **写入 entity 归档**,**不激活**(等刘泽文决定是否要复用 ZCode 栈)。
- **2026-07-11 14:xx**:**物理归档完成** → 刘泽文 "没什么有用的那就归档吧" + "B" 模式 → 执行 `tmp/_archive_f_tmlr.ps1`(B2:留空骨架 + 7 天 quarantine)
  - **来源**:`f:\TMLR\`(7 顶层项 / 56 文件 / 2,481,784 bytes / 2.37 MB)
  - **目标**:`tmp/_archive/f-tmlr-2026-07-11/`(7 项搬入 + `manifest.json` + `RESTORE.md` + `DONE.txt`)
  - **SHA-256 验证**:`_diag_skills.py` = `EEA705937E236212D299E5140367BB145984DE6A8112F38D8541135FACAB5DD5`(归档前后一致,**未损坏**)
  - **f:\TMLR\ 现状态**:空骨架(目录保留,0 文件,防止路径 404)
  - **回滚窗口**:2026-07-11 → **2026-07-18**(7 天后若仍不需要,可彻底删 archive 目录)
  - **回滚命令**:`pwsh -File tmp/_archive_f_tmlr.ps1 -Restore`
- **未来动作**(待定,2026-07-18 后评估):
  - **彻底清理**:删除 `tmp/_archive/f-tmlr-2026-07-11/` 整棵,释放 ~3 MB,关掉所有噪音源
  - **保留 archive**:`tmp/_archive/` 区可作为长期历史项目归档池(类比 7/11 `cleanup-stale-artifacts-2026-07-11.md` 模式)
  - **复用**:`_diag_skills.py` 内容已完整入库,需要时从 archive 拉出复用或重新跑就够

---

_最后更新:2026-07-11 13:55 · 泰_