---
name: cross-session-handoff
description: 多窗口/多 session 并行任务的撞车检查与接力公告工作流。Use when the user asks to check whether another window/session/task overlaps, says "别和他们撞车", "接力", "通知 w3/w7", "把这个给另一个窗口", "多窗口状态", "兄弟窗口", "handoff", or when editing tmp/windows/*/STATUS.md across sessions.
---

# Cross-Session Handoff

用于在 `tmp/windows/<window>/STATUS.md` 之间做低风险协作：先查撞车，再写接力，不替别的窗口做决策。

## Core Rules

1. **先扫盘再动手**：读取相关 `STATUS.md` 末尾和任务标题，确认主题、状态、DoD、阻塞点。
2. **不要用 LastWriteTime 单独判断新旧**：多 session 下可能出现叙事时间漂移或 edit 后 mtime 不更新。以 **Length + 内容验证** 为准，timestamp 只作辅助。
3. **只追加接力段，不重写对方内容**：跨窗口写入时默认 append 一个小段；不改对方决策表、DoD、正文草稿。
4. **接力段讲三件事**：对方需要什么、我这里已有哪份产物、怎么直接使用。
5. **长度克制**：每个接力段通常 2-3 KB 以内；链接到本窗口产物，不复制大段正文。
6. **留底**：如果实际写入了接力段，同步在本窗口 `STATUS.md` 或当日 memory 里记录“已接力到哪些窗口”。

## Workflow

### 1. Identify windows

- 当前窗口：用户正在推进的 `tmp/windows/<name>/STATUS.md`。
- 目标窗口：用户点名的窗口，或所有 `tmp/windows/*/STATUS.md`。
- 若用户只是问“撞不撞”，只读并报告；不要写文件。

### 2. Collision check

对每个目标窗口给出分类：

| 分类 | 判断 | 动作 |
|---|---|---|
| 无重叠 | 主题/文件/交付物都不同 | 不写 |
| 互补 | 对方阻塞点正好需要本窗口产物 | 可写接力 notice |
| 低风险共享主题 | 研究对象相同但问题不同 | 只报告风险，谨慎写 |
| 真撞车 | 同文件同段落同交付物 | 停止，要求用户决策 |

检查优先级：
1. `STATUS.md` 的任务名/DoD/当前状态
2. 最近完成段、阻塞段、待办段
3. 文件大小与关键内容
4. timestamp（仅辅助）

### 3. Handoff notice template

追加到目标 `STATUS.md` 末尾：

```markdown

## 🤝 接力 from <source-window>

> 写入时间：<system-time if verified> · 目的：避免重复扫盘/提供现成素材。

### 对本窗口有用的现成产物

| 本窗口需求/阻塞点 | <source-window> 已有产物 | 怎么用 |
|---|---|---|
| ... | `path/to/file.md` / section name | copy/参考/验证 |

### 边界
- 本段只提供素材/撞车判断，不替本窗口做最终决策。
- 如本窗口已有更新，以本窗口 DoD 和负责人判断为准。
```

写入前先 `read` 末尾，选择 append 或精确插入；写入后再次 `read` 或检查 Length + 内容关键词验证。

### 4. Report back

最终报告包含：

- 哪些窗口无重叠 / 互补 / 真撞车
- 写了哪些接力段，写在哪里
- 哪些地方刻意没动，为什么
- 下一步选择（如需要用户决策）

## 状态广播(Broadcast)— DASHBOARD 同步专用

接力模式是**窗口间定向**("我这里有 X 你需要"),广播模式是**窗口到 DASHBOARD 的被动上报**("我刚改了什么,DASHBOARD 维护者下次刷新请扫这里")。

**触发场景**:用户说"为什么多窗口不同步"、"多窗口状态脱节"、"DASHBOARD 滞后"、"每个窗口无法同步计划"。

### 何时用广播 vs 接力

| 模式 | 方向 | 用途 | 谁触发 |
|---|---|---|---|
| 🤝 接力 | 窗口 A → 窗口 B(定向)| 交付可复用素材 | A 发现自己产物对 B 有用 |
| 📡 广播 | 窗口 A → DASHBOARD 维护者(广播)| 汇报自己状态变化 | A 刚改完 STATUS.md,怕 DASHBOARD 滞后 |

**不要混用**:接力段里塞广播字段会让 B 窗口困惑(他不需要知道你下次刷新 DASHBOARD)。

### 广播段 schema

追加到本窗口 `STATUS.md` 末尾(通常在接力段、教训段之后):

```markdown

## 📡 状态广播(<date> <approx-time>, <agent> 跨窗口同步)

> 跨窗口协作接口 — DASHBOARD 维护者下个刷新时直接对照本段 + `tmp/windows/DASHBOARD.md` 当前行。

| 字段 | 值 |
|---|---|
| **当前状态** | 🟡 / 🟢 / ✅ / ⚪ (照 STATUS 原文) |
| **本 STATUS.md 大小** | XXXX B(从 v0/前次到现在) |
| **本次变化** | 一句话讲清本 STATUS.md 比上版本多了什么 |
| **下一个动作** | 具体可执行任务 |
| **是否阻塞其他窗口** | 是/否 + 哪个 |
| **DASHBOARD 当前版本是否已纳入** | ✅ 已 / ⚠️ 待刷新 |
```

### 广播段写入规则

1. **幂等保护**:写之前先 `grep` 本 STATUS.md 是否有 `📡` 段,有了就跳过(避免重复 append)
2. **追加位置**:STATUS.md 末尾(接力段、教训段之后);用 `edit` 工具找末尾最后一段的锚点 append
3. **DASHBOARD 维护者下次刷新时**:grep 11 个 STATUS.md 的 `📡 状态广播`,对照 DASHBOARD 当前表格,"DASHBOARD 是否已纳入"列 = ⚠️ 的窗口立刻能看出滞后
4. **广播段不带决策**:和接力段一样,不替别的窗口或 DASHBOARD 维护者做选择,只报事实

### 批量加广播段的幂等脚本模式

当用户要"给所有窗口加广播段"(典型多窗口同步需求):

1. **先扫盘**:列 `tmp/windows/*/STATUS.md` 全部路径,读头部 5 行确认状态
2. **写一次性 Python 脚本**(`tmp/_add_<verb>_segments.py`),参数化 6 字段,从顶部状态行自动提取
3. **跑前必 dry-run**:先 print 不写,确认 EXPECTED 行数 = 实际文件数
4. **跑后验证**:用 `Get-Item ... | Select Length` + `Select-String "📡"` 双重确认
5. **删一次性脚本**:不留临时文件(已经在 memory/evolution 留底)

### 广播 vs DASHBOARD 维护的边界

- 广播段**只写自己窗口的 STATUS.md**,不直接改 DASHBOARD.md
- 升级 DASHBOARD 是别人 session 的责任,除非用户明确授权
- 如果检测到 DASHBOARD 明显滞后(w9 案例),在广播段里加一栏"⚠️ DASHBOARD v5 状态脱节"提示,但不替维护者写 v6

## Anti-Patterns

- 不要因为看到旧 timestamp 就断言对方没改。
- 不要把本窗口大段报告复制进对方文件。
- 不要替目标窗口选择候选方案，除非用户明确授权。
- 不要修改全局 dashboard，除非它本来就是当前任务交付物。
- 不要在广播段里塞接力内容(混用会让 DASHBOARD 维护者和目标窗口都困惑)。
