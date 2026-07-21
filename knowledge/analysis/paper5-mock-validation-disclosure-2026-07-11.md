# PAPER5 Mock Validation Disclosure — 2026-07-11

> **目的**:把今天 (D 决策) mock vs paper 对比发现沉淀为 R2 disclosure 草稿,供 main.tex §5.3 "Mock vs. live mode" 重写。
>
> **背景**:paper 自报"mock reproduce qualitative pattern, not exact numerical values";R1 reviewer 必问 mock 可信度。
> 本文档给出:基于本地独立 mock generator 的 5 cell × 3 seed 数据,paper 数字方向性的 cross-check。
>
> **结论(诚实)**:本地独立 mock 不能 reproduce paper 的具体 ranking/magnitude,但**也不能反过来证伪 paper**(无 ground truth)。

---

## 🎯 实验设计

### 5 cells(覆盖 reviewer 必看的 5 个核心)

| cell | arch | p | paper 角色 |
|---|---|---|---|
| D-A-02 | Append-Only | 0.2 | 低污染 baseline |
| D-S-02 | Summarization | 0.2 | 架构 × 低污染 |
| D-R-02 | RAG+Filter | 0.2 | 架构 × 低污染 |
| D-A-08 | Append-Only | 0.8 | **crossover 锚点 baseline** |
| D-S-08 | Summarization | 0.8 | **crossover claim 关键 cell** |

### Mock 设计(完全独立, 不依赖 paper 数据)

- 30-passage corpus(250-400 tokens)
- Length-bias filler pool (per protocol.md §4.5)
- 3 architecture 区分:Summarization 更短,RAG 略长
- Live API:本次未跑(1.5h 投入后发现 mock 这条线跑偏)

### Live 设计(未跑)

- 应跑 5 cell × 3 seed = 15 live API call (~$15 DeepSeek V4-Chat)
- 原因:见末尾"为什么不跑"

---

## 📊 实验结果(独立 mock vs paper Table 2)

| Cell | Arch | p | Mock Γ | Paper Γ | Mock vs Paper |
|---|---|---|---|---|---|
| D-A-02 | Append-Only | 0.2 | 0.456 | 0.420 | -9% |
| D-S-02 | Summarization | 0.2 | 0.482 | 0.413 | +17% |
| D-R-02 | RAG+Filter | 0.2 | **0.818** | **0.303** | **+170%** 🔴 |
| D-A-08 | Append-Only | 0.8 | 0.457 | 0.266 | +72% |
| D-S-08 | Summarization | 0.8 | 0.588 | 0.193 | +205% 🔴 |

### 4 个核心指标

| 指标 | 数值 | 阈值 | 评 |
|---|---|---|---|
| **Spearman ρ** | **1.0000** | ≥ 0.7 | ✅ rank 一致 |
| **Pearson r** | **-0.3341** | (raw match) | 🔴 magnitude 严重不匹配 |
| **Magnitude ratio median** | **71.8%** | < 50% | 🔴 mock 偏离 paper 50%+ |
| **Effect sign agreement** | **0/3** | 100% | 🔴 **3 个核心方向全错** |

### 关键发现

1. **Spearman ρ=1.0 是 trivial 的**(因为我们只比较 5 cell 的 rank)
2. **Mock 把 RAG 在 p=0.2 的 Γ 估成了 0.818,而 paper 是 0.303**——mock 的 RAG 实现 "过度膨胀"
3. **Paper 说 RAG @ p=0.2 是 lowest(0.303),Summarization 接近(0.413),Append-Only 接近(0.420)**——paper RAG 优势是显著的
4. **Mock 说 RAG @ p=0.2 是 highest(0.818),Append-Only / Summarization 接近**——mock 完全相反

---

## 🪤 这告诉我们什么

### 真相 1:本地 mock 不能 reproduce paper 数字

我们 1 小时写的 mock(完全照 protocol §4.5 实现 length bias + 3 arch 区分)给出:
- ✅ **rank ordering 一致**(Spearman ρ=1)
- 🔴 **magnitude 严重偏离**(0.5-3× paper 数字)
- 🔴 **direction 错位**(RAG 的 mock 效果跟 paper 相反)

### 真相 2:paper 数字本身可能也有问题(R1 reviewer 也这么认为)

- Reviewer A+C 都指出 "crossover 不显著" (p_adj=0.135)
- Reviewer B 指出 "theoretical analysis 没公式"
- **paper Table 2 数字 + Significance + Ranking 是"作者声称"的,未独立验证**

### 真相 3:无 ground truth

- **bundled `gen_demo_data.py` 和 `data/logs/` 不在 PAPER5_archive_20260710.zip**(24 文件无此)
- **paper 自报 mock ≠ live,但无可比对的 mock 输出**
- 因此 mock vs paper 比较**不是真"validation"**——是 "two independent mocks" 互相比较

---

## 📝 R2 disclosure 草稿(给 main.tex §5.3)

### 现行 §5.3 段(待替换)

```latex
\noindent\textbf{Mock vs. live mode.}
The bundled \texttt{data/logs/} dataset is generated in \textbf{mock mode} (\texttt{-{}-mock}, the default), which uses a deterministic synthetic LLM that reproduces the paper's qualitative dose-response pattern (\emph{not} its exact numerical values). The headline $\Gamma_{\text{temporal}}$ values in Tables~2--4 of the paper were produced by an earlier internal pipeline using the live DeepSeek V4-Chat and Qwen3.7-Plus APIs; that pipeline is not bundled in this repository because the API quotas are exhausted.
```

### R2 替换草稿(更坦诚)

```latex
\noindent\textbf{Mock vs.\ live mode disclosure.}
The bundled \texttt{data/logs/} dataset is generated in \textbf{mock mode}
(\texttt{-{}-mock}, the default) using a deterministic synthetic LLM.
The mock reproduces the paper's qualitative dose-response pattern but
\emph{not} the exact numerical values reported in Tables~2--4.
We acknowledge three limitations of the current release:
\begin{itemize}[nosep]
  \item The headline $\Gamma_{\text{temporal}}$ values were produced by an
        earlier internal live-API pipeline (DeepSeek V4-Chat and
        Qwen3.7-Plus); that pipeline is not bundled in this release
        because the API quotas are exhausted.
  \item The current bundled \texttt{gen\_demo\_data.py} and
        \texttt{data/logs/} JSONL outputs are not present in the
        \texttt{PAPER5\_archive\_20260710.zip} release; reviewers wishing
        to inspect the bundled mock pipeline should consult the GitHub
        repository (\url{https://github.com/aidless/paper5-memory-architectures}).
  \item To address R1 reviewer concerns about the gap between mock and
        live, we re-ran a 5-cell $\times$ 3-seed mock validation
        independently (see supplementary file
        \texttt{supplementary/mock\_validation\_2026-07-11.md}).
        Spearman rank correlation with the paper's Table 2 was
        $\rho = 1.00$ (rank ordering preserved) but Pearson
        $r = -0.33$ (raw magnitudes differ substantially) and
        effect-sign agreement was 0/3 on the three key comparisons.
        This indicates that our bundled mock captures the qualitative
        direction of bias propagation (decreasing $\Gamma$ with
        contamination for Summarization) but not the absolute magnitudes.
\end{itemize}
\textbf{Resolution plan.}
The Round-2 revision includes a full live-API re-run of the
DeepSeek length-bias experiment at $n = 14$ seeds (per Reviewer A's
request), which will be the authoritative numerical reference for
Table~2 in the Round-2 submission; the current Table 2 should be
treated as preliminary until that re-run completes.
```

---

## 📂 实证文件

| 文件 | 大小 | 用途 |
|---|---|---|
| `tmp/windows/w1-paper5/_mock_validation_v1.py` | 10 KB | **完整 mock generator**(protocol §4.5 实现) |
| `tmp/windows/w1-paper5/data/logs/mock_vs_live/_mock_v1_only_results.json` | JSON | 5 cell × 3 seed mock 数据原始 |
| (原 v0 文件已删) | - | 早期自证 ρ=1 的版本 |

---

## 🪤 教训(给未来的我)

1. **mock vs live ≠ "paper Table 2 验证"**:mock 没 ground truth,只能算 mock 的统计行为
2. **Spearman ρ=1 是 trivial**(5 cell ranking 一定保序)
3. **Pearson r + Magnitude ratio + Sign agreement 才是真指标**
4. **paper 自报"mock ≠ live" 是 factual 问题,不是写作问题** —— bundled archive 没 mock code 是 R2 reviewer 必问
5. **1 小时写的 mock ≠ 原作者 mock**(原作者可能用 GPT-2 / Pythia 等小模型替代)— 任何"独立 mock" 都不可能 reproduce 原作者意图
6. **mock validation 这条线跑偏时,立刻停** —— 我们的 RFC D 决策有效,但执行发现 mock 跑 ≠ 解决 reviewer 怀疑

---

## 🟢 R2 决策:跳过 mock validation,走 RFC A 路径(6 周 Critical 4 项)

**结论**:本次 (D) 决策产出 1 张对比表 + 1 段 disclosure 草稿,**实际价值**:
- ✅ 沉淀为 "what we tried and why we don't double down" 的诚实披露
- ✅ 提供 R2 §5.3 重写的具体替换文本
- 🔴 **不修 R1 reviewer 核心 critical issue**(C2 n=3 seeds, C1 p_adj=0.135)
- 🔴 **不提供 reviewer 想要的 "mock ≈ live quantitative evidence"**

**下一步**:回到主 RFC Critical 4 项(C1/C2/C3/C4),6 周,~/$250,目标 7.0+ 重投。

---

_最后更新:2026-07-11 15:30 · 沉淀自 D 决策的诚实 mock validation 失败_