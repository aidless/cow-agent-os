# PAPER5 Mock vs Live API Validation — RFC (D)

> **目的**:用 5 cell × 2 model × 3 seed = **30 live API call** + 同等 mock cell = **30 mock call**,
> 验证 PAPER5 的 mock mode 数值结论是否在 live API 下**保序**(rank consistency)+ **方向一致**(effect sign)。
>
> **来源**:用户决策 D(7/11 14:58),[paper5-improvement-rfc-2026-07-11.md](./paper5-improvement-rfc-2026-07-11.md) "决策 D"。
>
> **投入**:~3 天 + ~$20 API + ~$0 LLM
>
> **产出**:1 张表(Table A "Mock vs Live Agreement")+ 1 段 main.tex §5.3 "Mock validation"

---

## 🎯 实验目标

**核心问题(PAPER5 R2 reviewer 必问)**:
> "你的 mock mode 是否能 reproduce live API 的 qualitative conclusions?如果不能,所有数字就要重跑。"

**可接受的回答**:
> "Mock vs Live 在 5 个核心 cell 上 **rank correlation ρ ≥ 0.7**,effect sign 100% 一致,absolute Γ magnitude 的 ratio 在 0.5-2.0× 区间内。这是 TMLR supplement 标准的 validation 实验。"

**不可接受的回答**(reviewer 会 reject):
> "我们相信 mock 跟 live 类似,因为我们的 mock 是 synthetic LLM"(太弱,无证据)

---

## 🔬 实验设计(科学严谨)

### 5 cell 选取(覆盖 reviewer 必看的全部情况)

| cell # | condition_id | model | architecture | bias | p | 理由 |
|---|---|---|---|---|---|---|
| 1 | D-A-02 | DeepSeek | Append-Only | length | 0.2 | **低污染 baseline** |
| 2 | D-S-02 | DeepSeek | Summarization | length | 0.2 | **架构 × 低污染** |
| 3 | D-R-02 | DeepSeek | RAG | length | 0.2 | **架构 × 低污染** |
| 4 | D-A-08 | DeepSeek | Append-Only | length | 0.8 | **高污染 baseline**(crossover 关键 cell) |
| 5 | D-S-08 | DeepSeek | Summarization | length | 0.8 | **crossover claim 锚点 cell** |

**为什么不跑 RAG @ 0.8**:5 cell 已经够 reviewer 看;6 cell = $24,边际信息不大。
**为什么不跑 Qwen**:Qwen 实验 Round-2 自己就有 reviewer 关注(n=3 seeds),Mock vs Live 在 Qwen 上 **重复** 同样的 methodology 验证,不强求一次过。

### Seeds

每个 cell 跑 **3 seeds**(不是 1,也不是 10)—— 3 seeds 给出 **rank ordering 是否稳定**,10 seeds 太贵。

### Mock 模式

按 `gen_demo_data.py --mock` 跑同样的 5 cell × 3 seeds。
- 论文承认 mock 是 deterministic synthetic,**有意 reproduce qualitative pattern**
- 我们要验证:**mock 真的做到了吗?**

### 数据格式

每个 cell 输出一个 JSONL:
```json
{"condition_id": "D-A-02", "seed_id": 0, "agent_id": "agent_A",
 "round": 1, "length": 234, "contamination": false,
 "source": "mock|live", "timestamp": "2026-07-XX"}
```

每 cell 30 round × 2 agent = 60 行,5 cell × 3 seed × 2 mode = 30 个 JSONL

### 量化指标(我们要算的)

| 指标 | 公式 | 阈值(reviewer 接受) |
|---|---|---|
| **Spearman ρ (per-cell)** | corr(mock_Γ, live_Γ) over 5 cells | **ρ ≥ 0.7** |
| **Effect sign agreement** | sign(Γ_arch1 - Γ_arch2) 在 mock 和 live 是否一致 | **100%** |
| **Magnitude ratio** | median(|live_Γ - mock_Γ| / live_Γ) | **< 50%** |
| **Architecture ranking stability** | arch 排序在 mock vs live 是否同序 | **100%** |

### 时间线

| Day | 动作 | 投入 |
|---|---|---|
| Day 1(上午) | 写幂等脚本 + corpus 准备(用 protocol.md 4.7 的 30-passage CNN/DailyMail 子集) | 半天 |
| Day 1(下午) | 跑 5 cell × 3 seed = 15 mock call(`gen_demo_data.py`) | ~1 min |
| Day 2 | 跑 5 cell × 3 seed = 15 live API call(DeepSeek, ~$15) | 1-2 小时(30 RPM) |
| Day 3(上午) | 跑同一 5 cell × 3 seed = 15 live API call(replicate, ~$15) | 1-2 小时 |
| Day 3(下午) | 算 4 个量化指标,写 Table A | 半天 |
| Day 4(可选) | 整合到 main.tex §5.3,加 Discussion 段 | 半天 |

**总投入**:3-4 天,~$30-40 API(2 replicate 跑)

---

## 📂 文件设计

### 脚本 1:幂等 validation 脚本

`tmp/windows/w1-paper5/_mock_vs_live_v1.py`(核心 200-300 行)

**功能**:
- [ ] 从 env 读 `DEEPSEEK_API_KEY`(不硬编)
- [ ] 加载 30-passage CNN/DailyMail corpus(用公开 huggingface dataset,无 key 需要)
- [ ] 跑 5 cell × 3 seed × 2 mode = 30 个 JSONL
- [ ] 算 4 个量化指标
- [ ] 输出 `_mock_vs_live_results.json` + `_mock_vs_live_table.txt`

### 脚本 2:幂等 LaTeX 段补丁

`tmp/windows/w1-paper5/_patch_apply_v3.py`

**功能**:
- [ ] 在 main.tex §5.3 末尾追加 Table A 和 Discussion 段
- [ ] 引用 `_mock_vs_live_results.json` 的实际数字

### 产出文件

```
F:\Research\PAPER5_CONSOLIDATED\data\logs\mock_vs_live\
├── mock_D-A-02_s0.jsonl ... mock_D-S-08_s2.jsonl  (15 mock JSONL)
├── live_D-A-02_s0.jsonl ... live_D-S-08_s2.jsonl  (15 live JSONL)
├── _mock_vs_live_results.json                     (quantitative)
└── _mock_vs_live_table.txt                        (human-readable)
```

---

## ⚠️ 关键风险

| 风险 | 缓解 |
|---|---|
| **DeepSeek API quota 又 exhausted** | (a) 用 DeepSeek-V3 (current default) + 显式标 snapshot;(b) 切换到 OpenAI gpt-4o-mini 做次选(更贵但 quota 多) |
| **mock 跟 live ρ < 0.7**(我们赌 ρ ≥ 0.7) | 这是**真实信号**,RFC 写明 "if ρ < 0.7, then we commit full Qwen n=10 + 重跑 mock calibration" |
| **live API 输出 variance 太大**(temperature=0 应该 deterministic 但可能有) | 2 replicate 跑,看 variance 是否稳定 |
| **corpus 找不到 / 不可下载** | 用 ~30 个手写 passage 作 fallback(降级但仍可做) |

---

## 🎯 决策(请勾)

- **(A)**:我立刻按 RFC 开工,3 天完成,~/$30
- **(B)**:先做 mock 跑(~1 min),看 mock 是否真的 reproduce paper 数字,**如果 mock 自己都跟 paper 不符,live 就不用跑了**(0 成本先验证 mock 端)
- **(C)**:跳过 mock vs live,**直接开工 Week 1-2 RFC(Qwen n=10 + C1 reframe)**,live data 后续再加
- **(D)**:跑全套,但**每个 cell 用 1 seed 而不是 3**(成本减半,精度低)
- **(E)**:用 **gpt-4o-mini 代替 DeepSeek**(成本可能持平,但更稳定 + 更"业内标杆")

**推荐 (B) → 如果 mock 不符 → (C)**:1 分钟验证 mock 端,**0 成本筛掉 mock 不对的可能**。

如果你不想做 D 决策(就是 R2 投出去,不管 mock vs live),那选 **(C)** — 直接进 6 周 RFC。

---

## 🪤 RFC 教训(给未来的我)

1. **mock vs live 是 TMLR R2 的隐藏必问** — paper 自报 "mock ≠ live",所以这问题 100% 来
2. **3 seeds / cell** 是 sweet spot(1 seed 不够看 variance,10 seeds 太贵)
3. **5 cell 覆盖 architecture × contamination × 关键 crossover** — 不是随机挑
4. **Spearman ρ 不 Pearson r**(我们要 rank ordering,不是 raw value match)
5. **幂等脚本 = 重跑不破坏** — 跑完后可能调整 corpus,需要能重跑

---

_最后更新:2026-07-11 15:05 · Draft v1 · 待用户 commit D / C / B 之一_
---

## D decision closed(7/11 15:35):杞?(伪)+(纬)

**User D** 鈫?mock 绔窇瀹?鈫?Spearman 蟻=1 浣?sign agreement 0/3 鈫?杞?disclosure銆?
璇﹁ [paper5-mock-validation-disclosure-2026-07-11.md](./paper5-mock-validation-disclosure-2026-07-11.md)銆?
涓嬩竴姝?涓?RFC Critical 4 椤?6 鍛?~$250,鐩爣 7.0+)銆?
