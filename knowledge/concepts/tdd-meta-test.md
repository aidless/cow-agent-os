# TDD + Meta-Test 模式

_2026-07-11 沉淀。来源:TEMPLATE v0.5.0 release 实战(commit `0d538a1` → `fb11a09`)。_

---

## 🎯 模式定义

**TDD + Meta-Test 模式** = **TDD 红绿循环** × **Meta-test 反向验证**。

| 阶段 | 做什么 | 验证什么 |
|---|---|---|
| **Red** | 写失败的 tests(覆盖新功能) | tests 失败 = 期望行为未实现 |
| **Green** | 最小修改让 tests 通过 | tests 通过 = 期望行为已实现 |
| **Meta-test** | inject 一个 bug,看 test 是否 catch | tests 失败 = test 真在 catch bug |

**核心洞察**:**测试通过 ≠ 测试有效**。Meta-test 验证"如果我故意引入 bug,测试会失败吗?"。

---

## 📐 完整 5 步流程

来自 TEMPLATE 项目 §15.12:

```
Step 1: TDD Red         写新 tests,看到它们失败
Step 2: TDD Green       最小修改让 tests 通过
Step 3: Driver wiring   把新 API 接到 CLI / 上层
Step 4: Meta-test       给每个新 feature 写 inject,验证 test catch
Step 5: Documentation   CHANGELOG + RELEASE_NOTES + ROADMAP
```

---

## 📐 Meta-test 实现模板

```python
def inject_bug_N() -> None:
    """Bug N: <description>.

    The <anchor> in <file> <does X>. If we change it to
    <does Y>, the regression test <test_name> should FAIL.
    """
    target = REPO / 'src' / 'pkg' / 'file.py'
    with _patched(target):  # 自动备份+还原
        original = target.read_text(encoding='utf-8')
        old = '<anchor code>'
        new = '<buggy code>'

        if old not in original:
            raise RuntimeError(f'bug-N anchor not found: {old!r}')

        target.write_text(
            original.replace(old, new, 1),
            encoding='utf-8',
        )
        _check_bug_inside_patch(
            'N',
            'tests/test_<area>.py::test_<name>',
        )


# In main():
cases = [
    ('1', inject_bug1),
    ('2', inject_bug2),
    # ...
    ('N', inject_bugN),
]

for bug_id, inject_fn in cases:
    try:
        inject_fn()
    except Exception as e:
        _results.append((bug_id, False, f'inject failed: {e!r}'))
```

---

## 🎯 关键技术细节

### 1. `_patched()` 上下文管理器

```python
@contextmanager
def _patched(path):
    """Backup file → yield → restore on exit (tracked or untracked)."""
    rel_path = str(path.relative_to(REPO))
    is_tracked = (
        subprocess.run(['git', 'ls-files', '--error-unmatch', rel_path],
                       cwd=REPO, capture_output=True).returncode == 0
    )
    if is_tracked:
        try:
            yield  # 让 inject 跑
        finally:
            # 用 git checkout 还原,保证原子性
            subprocess.run(['git', 'checkout', 'HEAD', '--', rel_path],
                          cwd=REPO, check=True)
    else:
        backup = path.read_text(encoding='utf-8') if path.exists() else None
        try:
            yield
        finally:
            if backup is not None:
                path.write_text(backup, encoding='utf-8')
```

**关键设计**:用 `git checkout` 而不是文件内容备份,因为:
- 原子性(单一操作)
- 处理多进程并发场景
- 即便中途出错也能恢复

### 2. anchor 匹配陷阱

```python
# ❌ 错误:find 找第一个匹配
disabled_start = original.find('    if disabled_set:\n')
# 在 bug 16 中,这个 marker 出现 2 次(一次在 warning 块内,一次在外层过滤)
# 错误地选了第一个 → IndentationError

# ✅ 正确:用 second occurrence
first = original.find('    if disabled_set:\n')
disabled_start = original.find('    if disabled_set:\n', first + len(...))
```

**经验法则**:在 source code 中,同一字符串出现 >1 次时,**总是用 `find(start_offset)` 找下一个**。

### 3. `_check_bug_inside_patch` 双检查

```python
def _check_bug_inside_patch(bug_id, test_target):
    rc, out = _run_pytest(test_target)
    caught = (rc != 0 and 'FAILED' in out)
    # Bug 阶段:caught should be True
    _results.append((bug_id, caught, ''))
```

**双状态期望**:
- Bug injected 后:test **应该失败** (cauth = True)
- Bug restored 后:test **应该通过** (用 `_patched` 的 finally 保证)
- 两者都满足 = bug inject + restore 流程完整

### 4. _patched 嵌套

```python
def inject_bug():
    with _patched(file):  # 备份
        # 修改文件
        file.write_text(buggy)
        _check_bug_inside_patch(...)  # 跑 test,test 失败
    # 文件被自动还原
    # 跑同一个 test,test 通过
```

---

## 🪤 常见陷阱

### 陷阱 1:anchor 找不到 → RuntimeError

```python
if old not in original:
    raise RuntimeError(f'anchor not found: {old!r}')
```

**不要静默返回**(会让人误以为 inject 成功)。

### 陷阱 2:被 inject 的 bug 影响其他 tests

```python
# 用 _patched() 的 finally 块确保还原
with _patched(file):
    file.write_text(buggy)
    _run_pytest('test_X::test_Y')  # 只跑这一个 test
# 文件已还原
```

### 陷阱 3:缓存的 import

```python
# pytest 跑完后,Python 进程退出,模块被重新加载 → OK
# 但若在同进程内多次跑 test,可能用旧的 import → 需要重新 spawn
```

TEMPLATE 项目用 `subprocess.run(...)`,每次新进程,无需担心缓存。

---

## 📊 实战收益(TEMPLATE 项目数据)

| 指标 | 数值 |
|---|---|
| Bug inject 总数 | 16 |
| 全部 caught | 16/16 |
| 平均调试时间 | ~5 min/bug |
| Bug 16 anchor 调试 | 10 min(因为 anchor 二义性)|
| 总投入 vs 收益 | ~2h 投入 / 16 bugs 永不被沉默错过 |

**投入产出比极高** —— 一次写 meta-test,长期保护。

---

## 🪤 与 Agent OS 方案对接

### Meta-test 与 Control Plane

| Meta-test 概念 | Agent OS 对应 |
|---|---|
| 16 个 bug inject | 25 个漏洞缓解 |
| `_check_all_regressions.py` | `_check_all_regressions.py`(同文件)|
| 测试覆盖率 | Control Plane 决策覆盖率 |

### Meta-test 与 5 类演化

| Meta-test 特性 | 演化机制 |
|---|---|
| 保护已修复 bug | 任务级学习(task reflection) |
| 每个 bug 有 evidence | 用户级学习(用户偏好记录) |
| 自动 regression check | 生态级学习(reputation 监控) |

---

## 📚 参考来源

- **TEMPLATE v0.5.0 实战**:[RELEASE_NOTES_v0.5.0.md](../../research/paper5.md) §TDD Provenance
- **`_check_all_regressions.py`** in TEMPLATE 仓库
- **§15.12 TDD pattern** in TEMPLATE docs
- **本知识库**:[Plugin Whitelist Pattern](./plugin-whitelist-pattern.md)

---

## 🎓 论文 idea

1. **Meta-test Cost-Benefit**:meta-test 投入 vs bug 捕获率的最优阈值
2. **Regression Test Prioritization**:16 个 bug 中哪些是高 ROI 必须测,哪些可以省?
3. **Anchor Robustness**:bug 修复后 anchor 漂移的检测与自动更新

---

_最后更新:2026-07-11 13:42_