# llm-lab Copilot Scorer 演进史 + 跨文档数字对齐表

> **生成时间**:2026-07-12 14:15
> **范围**:scorer 演进的**完整时间线** + **跨文档数字对齐**(P0 已知问题专项)
> **关联**:[Prompt 迭代方法论提炼](./contract-vs-natural-prompt-tradeoff-2026-07-12.md) · [8 份文档索引](./llm-lab-copilot-docs-index-2026-07-12.md)

---

## 🎯 这个文档解决什么问题

8 份文档里**至少有 3 个版本的 scorer**(旧 / 扩展 / 扩展+否定感知),但**跨文档直接比 uplift 不公平** —— scorer 覆盖度不同,数字会让人误读。这是 P0 已知问题。

本文件提供:
1. **Scorer 演进的完整时间线**(3 个版本 + 行号 + 行为差异)
2. **跨文档数字 vs scorer 版本对照表**(一张大表,所有数字映射到具体 scorer)
3. **否定感知算法细节**(可移植)
4. **公平比较的标准操作流程**(未来防御)

---

## 📅 Scorer 演进时间线

```
[Phase 0] 早期 scorer(intentionally conservative, ~早于 7/12 04:00)
  ├─ 来源:web_d06602c6.md §Scoring Caveat:"intentionally conservative"
  ├─ 行为:只检查基础 reference_checks(非空、长度、必含类)
  ├─ 漏覆盖:`must_not_claim_tamper_proof` 还是纯子串匹配,
  │         未感知"not a tamper-proof..."这种正确否认
  ├─ 影响数字:zero-shot 44.4% / few-shot 63.6%(web_d06602c6.md §Automatic Reference Checks)
  └─ 消失时机:被 Phase 1 替代,~7/12 04:00 左右

[Phase 1] 扩展 scorer(~7/12 04:00 ~ 12:58)
  ├─ 文件:`scripts/score_copilot_run.py`
  ├─ 升级:覆盖全 `reference_checks` 表面
  │       (must_include_any_keywords / must_include_all_keywords /
  │        must_answer_no / must_explain_surface_constraints /
  │        must_recommend_manual_or_semantic_eval /
  │        must_mention_rerun_or_reproducibility /
  │        must_not_claim_tamper_proof)
  ├─ 已知 bug:`must_not_claim_tamper_proof` 是纯子串匹配(旧版约 L225-L226),
  │           否定不感知 → 正确否认被误杀
  ├─ 影响数字:
  │   - 旧 zero-shot 重打分:47.97%(web_1fa8eca0.md §Re-scored Old Full Baselines)
  │   - 旧 few-shot v1 重打分:61.98%
  │   - few-shot v2 full:79.67%
  │   - few-shot v3 full:82.11%  ← reviewer_008 被误判挂
  └─ 暂停时机:v3.1 报告撰写期,~12:59 修复

[Phase 2] 扩展 scorer + 否定感知(2026-07-12 12:59 后)
  ├─ 文件:同 `scripts/score_copilot_run.py`(12:59 版本)
  ├─ 升级:
  │   - L120 `TAMPER_PROOF_PHRASES`(phrases list: ["tamper-proof", "防篡改", "不可篡改"])
  │   - L123 `denied_before(text, idx, window=48英/20中)`
  │   - L259 `must_not_claim_tamper_proof` 改为 negation-aware
  ├─ 行为差异:
  │   - 未否认的真实声称仍判挂(✅ 没放过坏人)
  │   - 含词但是否认的判过(✅ 没误杀好人)
  ├─ 影响数字:
  │   - v3 同批 outputs 重打分:82.11% → **82.93%(reviewer_008 改判过)**
  │   - 这是 v3→v3.1 公平比较的真正基线
  │   - test_50_v2 frozen:v3 自动 **93.68%**(178/190)
  └─ 当前状态:🟢 线上
```

### Phase 2 实现细节(可移植)

```python
# Phase 2 修复版(scored at L259)
elif name == "must_not_claim_tamper_proof":
    phrases = TAMPER_PROOF_PHRASES  # L120 定义
    matched = [p for p in phrases if p in text]
    if not matched:
        add_check(result, name, True)
    else:
        # 仅当该词附近没有否定词时才判失败
        denied = all(_denied_before(text, text.index(p), window=12) for p in matched)
        add_check(result, name, denied)


def _denied_before(text: str, idx: int, window: int = 48) -> bool:
    """判断 text[idx] 位置前 window 字符内是否存在否定词。

    英文否定词:not / no / never / n't / cannot / can't / don't / ...
    中文否定词:不 / 非 / 未 / 没 / 别 / 莫
    """
    prefix = text[max(0, idx - window):idx].lower()
    return any(neg in prefix for neg in EN_NEGATIONS + CN_NEGATIONS)
```

**window 选择**:48 英 / 20 中 = 经验值。
- 太大:误识别(前面有没有不相关的否定)
- 太小:漏识别(短句被否定)
- 48/20 是**经验起点**,建议跑数据分布自适应

---

## 📊 跨文档数字 vs Scorer 版本对照表

> **关键约定**:任何 score 数字后附 `(scorer_version: <phase>)`,避免读者算错 uplift

| 数字 | 描述 | 出现的文档 | 用的 scorer | 公平比较? |
|---:|---|---|---|---|
| 44.4% (20/45) | zero-shot 自动参考检查 | web_d06602c6.md §Automatic Reference Checks | **Phase 0** | vs Phase 1+ ❌ |
| 63.6% (28/44) | few-shot 自动参考检查 | web_d06602c6.md 同上 | **Phase 0** | vs Phase 1+ ❌ |
| 47.97% (59/123) | zero-shot 重打分 | web_1fa8eca0.md §Re-scored Old Full Baselines | **Phase 1** | vs Phase 1 ✅ |
| 61.98% (75/121) | few-shot v1 重打分 | web_1fa8eca0.md 同上 | **Phase 1** | vs Phase 1 ✅ |
| 79.67% (98/123) | few-shot v2 full | web_1fa8eca0.md §Full v2 Baseline | **Phase 1** | vs Phase 1 ✅ |
| **82.11% (101/123)** | few-shot v3 full | web_0f00dab5.md §Score Progression | **Phase 1** ← bug 期间 | vs Phase 2 ❌ |
| **82.93% (102/123)** | v3 同批重打分 | web_623e2558.md §6.3 + §1 脚注 | **Phase 2** | vs Phase 2 ✅(公平基线) |
| 82.11% → 82.93% | v3 在两版 scorer 下差 | web_623e2558.md §6.3 | Phase 1 vs Phase 2 | — |
| 93.68% (178/190) | v3 frozen test_50_v2 | web_67c44245.md §Frozen Confirmation | **Phase 2 + test_50_v2** | 独立 frozen 集,不参与本表比较 |
| 86.21% (25/29) | v3 balanced smoke | web_0f00dab5.md §Balanced Smoke | **Phase 1** | smoke,样本少 |

### 表格使用规则

1. **同 Phase 内可比**(✅):v3 82.11% vs v2 79.67% 都是 Phase 1,可减 → +2.44pp 正确
2. **跨 Phase 不可比**(❌):v3 旧 82.11% vs v2 79.67% 不能直接比
3. **Phase 2 重打分是 ground truth**:v3 的"公平 v3"是 82.93% 不是 82.11%
4. **frozen 集独立**:test_50_v2 是新 SHA256,scorer 版本可能也不同,**不进上表**

---

## 🪤 已知 grader version bug(本案例独有)

### 重打分机制价值

v3 → v3.1 报告里展示了一个**很少见但很值钱的做法**:

> 用修复后 scorer 重打**同批 outputs.jsonl**,得到 v3 在新 scorer 下的真实分数。

这不是简单的 "re-run",而是 **re-grade** —— 输出文本没变,只是 grader 升级了。这个机制让 "v3 真的更差还是 grader bug?" 有了答案。

### 通用建议

任何 "v(N) vs v(N+1)" 对比前,先做 **re-grade**:

```bash
# 伪代码
for run_id in $ALL_RUNS:
  outputs=$(cat runs/$run_id/outputs.jsonl)
  for grader_version in $ALL_GRADER_VERSIONS:
    score=$(python score_copilot_run.py \
      --grader-version $grader_version \
      --inputs <(echo "$outputs"))
    echo "$run_id, $grader_version, $score"
done
```

**结果是一张 grid**:
- 行 = run
- 列 = grader version
- 对角线以外 = "如果用另一个 grader 重打,分数会怎么变?"

这能暴露 grader 自身的 false upgrades(grader 升级让分数自然涨,跟模型无关)。

---

## ✅ 公平比较的标准操作流程(SOP)

未来再写 "v(N) vs v(N+1)" 报告时,执行这套:

### Step 1:声明 scorer 版本
```markdown
> Scorer 版本:Phase 2(2026-07-12 12:59 后,含否定感知)
> SHA256:`git rev-parse HEAD:scripts/score_copilot_run.py`
```

### Step 2:re-grade 老 baseline
```bash
# 老 runs 用新 scorer 重打 → 数字统一
python score_copilot_run.py --grader-phase 2 \
  --inputs runs/<old_run>/outputs.jsonl
```

### Step 3:报告表中每行标 phase
```markdown
| baseline | 数字 | scorer_phase |
|---|---|---|
| zero-shot (2026-07-10) | 47.97% | Phase 1(7/12 04:00)+re-grade 验证 |
| few-shot v1 (2026-07-10) | 61.98% | Phase 1+re-grade 验证 |
| few-shot v2 (2026-07-11) | 79.67% | Phase 1+re-grade 验证 |
| few-shot v3 (2026-07-12) | **82.93%** | Phase 2(re-grade 后) |
| few-shot v3.1 (待跑) | ? | Phase 2 |
```

### Step 4:frozen 集独立成行
```markdown
| test_50_v2 frozen v3 | 93.68% | Phase 2 + test_50_v2(SHA256 `087eb9f2...`)|
```

---

## 🔁 跨项目借鉴

| 借鉴点 | 适用 |
|---|---|
| **scorer 演进必须有时间戳 + 行号** | 任何自动评估系统 |
| **re-grade 比 re-run 更值钱** | 任何 "v(N) vs v(N+1)" 比较 |
| **否定感知 window 经验值 48 英 / 20 中** | 任何自然语言 must_not check |
| **scorer 也有 false upgrades** | 任何 "升级 scorer 后分数涨了" 的报告 |
| **frozen 集 SHA256 + 协议文档必须配套** | 任何需要严格 A/B 的工作 |

---

## 🪤 给 llm-lab 项目的具体改进建议

1. **`test_50_v2` 协议文档加 SHA256**:`web_75abdcf7.md` §Reporting 加一行 `> SHA256: 087eb9f2c86dd176...`,免读者二次查证
2. **scorer 加版本字符串**:文件头加 `__version__ = "Phase2-2026-07-12-12:59"`,脚本启动时打印
3. **re-grade 工具化**:`scripts/regrade_all.py` 跑全 history 的 outputs 跨所有 scorer phase,产出 grid CSV
4. **数字表格统一格式**:每个对比表头加 `> Scorer: Phase X | Re-grade: yes/no`
5. **v3.1 真跑结果出来后,必先 re-grade Phase 2 后再报 vs v3 的 uplift** —— 防止"v3 真的更差"和"scorer 升级"被混淆

---

## 📚 关联入口

- **方法论提炼**(主题命名):[contract-vs-natural-prompt-tradeoff-2026-07-12.md](./contract-vs-natural-prompt-tradeoff-2026-07-12.md)
- **8 份文档索引**:[llm-lab-copilot-docs-index-2026-07-12.md](./llm-lab-copilot-docs-index-2026-07-12.md)
- **原文 8 份**:位于 `tmp/web_*.md`,SHA256 锁定的 `test_50_v2.jsonl` + `scripts/score_copilot_run.py`

---

_最后更新:2026-07-12 14:15 · 单独分析 scorer 演进,补 P0 已知问题的可操作细节_
