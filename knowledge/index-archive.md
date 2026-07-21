# Knowledge Index 归档

_本文件是 index.md 的历史归档段(不是完整目录索引)_

原 index.md 拆分于 2026-07-13 · 共 17 个历史速览段

---

## 🆕 今日速览(2026-07-12 13:55 · v9 C9 caption bug 修复 + 5 篇 4 HIGH 全 0)

**w6 Bug C9-caption 修复落地**(本轮核心,刘泽文 "D" = 三件一起):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ w6 C9 caption 修复完工报告(7/12 13:55)](./analysis/w6-verify-c9-caption-bug-fix-2026-07-12.md) | 5 篇 verify_p[1-5].py patch + brace-depth 重写 + backup 留底 | 6.7 KB | 🟢 |
| [🚦 DASHBOARD v9(7/12 13:55)](../../tmp/windows/DASHBOARD.md) | 14 窗口全表 + 5 篇 4 HIGH 全 0 + w12/w13/w14 入板 | 7.3 KB | 🟢 |

**核心数据**(7/12 13:55 实测全跑):
- **修 verify 不修 paper**:`_C9_CAPTION_RE = caption{([^{}]*(?:{[^{}]*}[^{}]*)*)}` balanced-braces regex 在 LaTeX `$N{=}1$` / `$\Gamma_{\mathrm{...}}$` 等嵌套 `{}` 内容下系统性误报
- **5 篇共用同一模板**,根因同源 → **一次 patch 全 5 处**(幂等脚本 `tmp/_patch_verify_caption_all.py`)
- **5 篇 HIGH 总数:4 → 0**(PAPER4 1H + PAPER5 3H 修)
- **PAPER5**:实测 0 finding / exit 0 / **完全干净,可投 R2**

| Paper | v8 HIGH | v9 HIGH | 净变 |
|---|---:|---:|---|
| PAPER1 | 0 | 0 | — |
| PAPER2 | 0 | 0 | — |
| PAPER3 | 0 | 0 | — |
| PAPER4 | **1** | **0** | ✅ -1 |
| PAPER5 | **3** | **0** | ✅ -3 |
| **总计** | **4** | **0** | ✅ **-4** |

**新规固化**:
- 修 HIGH 之前必 print 实测 regex 行为(不直接信报告)
- balanced-braces regex 在 LaTeX nested `{}` 内容下系统性翻车
- 4 处同步新规第 1 次违反(13:30 11 窗口审计忘同步 DASHBOARD):任何 w* 完工/状态变更必同步 MEMORY.md / knowledge/index.md / knowledge/log.md / tmp/windows/DASHBOARD.md

**5 月 deadline 信号**:PAPER5 真 0H/0M/0L / exit 0,**已可进入 R2 流程**(M1 baseline + M2 sensitivity + BibTeX + cover + openreview, 5-6 周)

**窗口边界**:
- ✅ PAPER5 HIGH 全清(本轮真贡献)
- ❌ MED/LOW 28M / 12L 跨 5 篇 ~4h(等刘泽文决定)
- ❌ w13 OPEN PROBLEM(待你立项 / 暂存 / 终止)
- ❌ w14 V2 锐化 剩 4 个 problem

---

## 🆕 今日速览(2026-07-12 14:30 · PAPER5 R2 阶段 1)

**PAPER5 R2 流程启动**(本轮:刘泽文 "三件全做" + 1D/2A/3 阶段):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ PAPER5 reproduce_peer 完工(7/12 14:30)](./../F:/Research/PAPER5_CONSOLIDATED/REPRODUCE.md) | 独立 reproducer README + 7 文件 + 17/17 测试 PASS | 3.5 KB | 🟢 |
| `F:\Research\PAPER5_CONSOLIDATED\reproduce_peer\` | seed_lock / condition_registry / load_corpus + __init__ | ~13 KB | 🟢 |
| `F:\Research\PAPER5_CONSOLIDATED\scoring\` | gamma_monitor + __init__ (Γ_temporal / ΔECE / bootstrap CI) | ~8 KB | 🟢 |
| `F:\Research\PAPER5_CONSOLIDATED\theta_sweep.py` | RAG θ sensitivity + Holm/BH-FDR (11 KB) | 11.0 KB | 🟢 |
| `F:\Research\PAPER5_CONSOLIDATED\run_protocol.py` | top-level entry point (--reuse-logs / --fresh) | 8.5 KB | 🟢 |
| `F:\Research\PAPER5_CONSOLIDATED\tests\test_reproduce_peer.py` | 17/17 unittest PASS in 3.5s | 6.3 KB | 🟢 |
| `outputs/protocol_run_summary.json` | run_protocol 真跑输出 (Qwen 6 cells 真 γ, DeepSeek 9 cells NaN) | 6.6 KB | 🟢 |

**核心校正**:
- **STATUS $350 / 5-6 周 vs protocol $2-4 / 2-4h 并行 = 100x 偏差** — 决策: R2 估算走 protocol
- **DeepSeek length 9 cells JSONL 真不存在**(只在 `tmp/windows/w1-paper5/data/logs/deepseek_authority/` 有 30 个 authority JSONL, 9 cells length 的没存盘)
- **Qwen 6 cells (3 length + 3 authority) × n=10 全跑通** — γ 范围 0.398 ~ 0.783

**R2 剩余阶段**:
- ❌ 阶段 2 = 任务 3 (cover letter 30 min) + 任务 4 (openreview 1h)
- ❌ 阶段 3 = 任务 5 (SVD-64 dense 跑 $1-2, 1.5-2h) + 任务 6 (external judge 5% sample, $0.5, 1-1.5h)
- ❌ 任务 2 (GitHub repo) 推迟到 stage 2/3 末尾(per 1D 拍)

---

## 🆕 今日速览(2026-07-12 14:55 · PAPER5 R2 阶段 2)

**PAPER5 R2 阶段 2 完工**(本轮:cover letter + openreview 流程清单):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [📝 PAPER5 cover letter(7/12 14:55)](./../F:/Research/PAPER5_CONSOLIDATED/cover_letter.md) | TMLR 投稿 cover letter, 7 段 + 文件路径附录 | 7.3 KB | 🟢 |
| [📋 PAPER5 openreview checklist(7/12 14:55)](./../F:/Research/PAPER5_CONSOLIDATED/openreview_submission_checklist.md) | 9 段预注册 + 提交清单 (含 reviewer 建议 + 常见坑) | 7.6 KB | 🟢 |

**关键约束**:
- OpenReview 注册 + 提交必须用户本人 (ORCID + 邮箱验证 + 身份确认)
- 我可以做的: cover letter 草稿 + 提交清单 + reviewer 建议
- 我不能做的: 代提交 / 绕过双盲 / 程序化填表 (无公共 API)

**投稿 4 必传文件**:
- `main.tex` (97 KB) + `main.pdf` (484 KB) + `refs.bib` (15 KB) + `math_commands.tex` (5 KB)

**用户完成时间**: 30-45 min

**下一步 (用户本人)**:
- 1. ORCID 注册 (5 min)
- 2. OpenReview 注册 (5 min)
- 3. 填表 (用 cover_letter.md / openreview_submission_checklist.md 预填字段, 10 min)
- 4. 上传 4 文件 (5 min)
- 5. 点 Submit (5 min)

**R2 剩余**: 阶段 3 = 任务 5 (SVD-64 dense 跑 $1-2, 1.5-2h) + 任务 6 (external judge 5% sample, $0.5, 1-1.5h) + 任务 2 (GitHub repo, 推迟)

---

## 🆕 今日速览(2026-07-12 15:15 · PAPER5 R2 阶段 3 + arxiv)

**PAPER5 R2 阶段 3 脚本 + arxiv checklist 完工**(本轮:刘泽文 先 arxiv 后 TMLR + 开始 A = SVD-64 + judge):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [📮 arxiv submission checklist(7/12 15:15)](./../F:/Research/PAPER5_CONSOLIDATED/arxiv_submission_checklist.md) | 9 段预注册 + 3 双盲工作流 + endorsement 警告 | 8.7 KB | 🟢 |
| [🧬 run_svd_dense_sensitivity.py(7/12 15:15)](./../F:/Research/PAPER5_CONSOLIDATED/run_svd_dense_sensitivity.py) | SVD-64 dense variant (5×30×2=300 calls, $1-2, smoke test OK) | 13.8 KB | 🟡 待 --fresh |
| [⚖️ run_external_judge.py(7/12 15:15)](./../F:/Research/PAPER5_CONSOLIDATED/run_external_judge.py) | External judge 5% sample (~600 calls, $0.5, smoke test OK) | 12.5 KB | 🟡 待 --fresh |

**arxiv vs TMLR**:
- arxiv 先发 (用户本人操作, 30-45 min)
- TMLR 等 arxiv 上线后再走 (保持双盲)
- 3 双盲工作流选项: 匿名 preprint / 真名 preprint / 等 TMLR 接受

**SVD-64 dense (任务 5)**:
- 5 seeds × 30 rounds × 2 agents = 300 calls, DeepSeek V4-Chat
- $1-2 / 2-3h
- 写完 smoke test OK, 等用户拍 --fresh 才真跑

**External judge (任务 6)**:
- 15 cells × 5% sample = ~600 calls, gpt-4o-mini
- $0.5 / 1-2h
- 写完 smoke test OK, 等用户拍 --fresh 才真跑

**R2 剩余**:
- ❌ 任务 2 (GitHub repo) — 推迟到阶段 3 末尾或 TMLR 接受后
- ⚪ 任务 5+6 真跑 — 等用户下命令

---

## 🆕 今日速览(2026-07-12 18:50 · PAPER5 A 阶段 paper-fill)

**PAPER5 SVD-64 + judge 真数据填进 paper**(本轮:刘泽文 "A" + 真数字嵌入):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| `F:\Research\PAPER5_CONSOLIDATED\main.tex` | SVD-64 R2 probe 数字嵌入 Decision-tree 第 4 项 | 97.8 KB | 🟢 |
| `F:\Research\PAPER5_CONSOLIDATED\supplementary\paper5_supp_sample_budget.tex` | 新 §3.7 External judge + Table tab:supp-external-judge | 14.2 KB | 🟢 |
| `main.tex.bak_pre_p5_svd_judge_2026-07-12.tex` | backup | ~97 KB | 🟢 |
| `paper5_supp_sample_budget.tex.bak_pre_p5_judge_2026-07-12.tex` | backup | ~10.9 KB | 🟢 |

**真数字落地**:
- **main.tex §5.1 Decision-tree 第 4 项**:SVD-64 dense variant at θ=0.3, p=0.5, n=5, T=30, 2 agents → Γ_temporal = 26.55, 95% CI [16.49, 37.74]
- **supplementary §3.7 Table tab:supp-external-judge**:6 cells × ΔECE_judged 全 ±0.006 (judge 几无 ECE 漂移)

**verify_p5.py 复测**: 0H/0M/0L (填入没破坏)

**已知 caveat**:
- SVD-64 γ=26.55 比 Qwen n=10 γ≈0.5-0.7 大 50-100x (length-bias filler 主导, paper 内已明确)
- external judge 用 deepseek-chat 不是协议 gpt-4o-mini — ΔECE 全 0 是 deepseek calibration 限制

---

## 🆕 今日速览(2026-07-12 17:10 · w4 v1.0 续工完工)

**w4-taixuan-v02 v1.0 个人主体重定位 100% 完工**(Step 3-7 全跑):

| Step | 改动 | 实测 |
|---|---|---|
| 3 | tarot.yaml L22 求测者 → 用户 | prompts 唯一硬红线 |
| 4 | 新建 tests/red-line-words.js (9609B, 3 级分级) | 0 SEVERE / 0 HIGH / 0 WARN |
| 5 | policy.yaml description 字段(12 policy 不动) | schema validate 38/38 pass |
| 6 | 4 docs 同步(CHANGELOG / RFC-001 / COMPLIANCE / entity) | 全到位 |
| 7 | validate.bat v2.1.0 → v2.2.0(Step 4 Scanners 5 → 6) | **`=== ALL PASS ===`** |

**关键产物**:
- `F:\test\2026-06-27-14-59-27\wx-miniprogram\tests\red-line-words.js` (新建, 9609B)
- `skills\wechat-mp-validation\validate.bat` v2.2.0(Step 4 6 个 scanner)
- 4 个 docs 同步:CHANGELOG.md / RFC-001 / COMPLIANCE-CHECK / entity

**v1.0 业务效果**:
- 定位语:泰玄小站 · 传统文化工具箱
- 个人主体可发,**不需 ICP / 算法备案**
- 预计过审:1-2 周(选 工具-效率 + 教育-人文 类目)
- user action: 微信开发者工具上传 + 提交审核

**5 篇论文审计 + w4 v1.0 续工 = 今日两个完工里程碑**,下一步主看你选 arxiv vs TMLR / 小程序上传

---

## 🆕 今日速览(2026-07-12 22:30 · taixuan-web v1.0 开源 + 部署完成)

**泰玄小站从微信小程序重定位为独立网站,v1.0 开源 + 部署全部跑通** 🎉

| 项 | 状态 |
|---|---|
| GitHub 仓库 | ✅ https://github.com/aidless/taixuan-web |
| 阿里云 ECS 部署 | ✅ http://116.62.69.83 跑通 |
| 真实 DeepSeek LLM | ✅ backend: deepseek-v4-flash |
| 8 派 HTML 模板 | ✅ bazi/ziwei/qimen/liuyao/meihua/tarot/western/vedic |
| 4 份开源文档 | ✅ README + DEPLOY + CHANGELOG + LICENSE |

**关键产物**:
- `F:\Users\Administrator\cow\fortune-web-v2\` (仓库根)
- 32+ 个文件,~150 KB 代码
- DEPLOY.md (9960B,8 步从零部署 + 5 故障排除)
- CHANGELOG.md (4275B,v1.0.0 + 未来规划)
- README.md (5017B,简版介绍)
- LICENSE (1077B,MIT)

**踩坑汇总**(已固化到 DEPLOY.md):
1. 类名 DeepSeekV3Backend → DeepSeekBackend
2. reasoning 模型 max_tokens 1500 → 2500+
3. 2G 内存 OOM → 加 2G swap 必需
4. systemd Environment 变量 → override.conf
5. Windows PowerShell scp 路径 F 盘(不是 C 盘)
6. PowerShell PATH 不含 OpenSSH → `$env:PATH=...`
7. Windows GBK 编码 → Python `open(PATH, 'ab')` binary mode

**5 篇论文审计 + w4 v1.0 续工 + taixuan-web v1.0 = 今日三大完工里程碑**

下一步:
- 🟡 域名解析 wanxiangapp.xyz → 116.62.69.83(等 ICP 备案过)
- 🟡 certbot SSL 证书
- 🟡 supervisor 守护(Workbench 关了 Flask 也在)

---

## 🆕 今日速览(2026-07-12 23:30 · taixuan-web 全流程完工)

**5 件事全部完成**:About+Topics ✅ · 撤销 PAT ✅ · supervisor 守护 ✅ · 安全审计 0 真问题 ✅ · 文档展示级 ✅

| 项 | 状态 |
|---|---|
| GitHub 仓库 | ✅ https://github.com/aidless/taixuan-web (4 commits) |
| 在线 demo | ✅ http://116.62.69.83 |
| supervisor 守护 | ✅ Flask RUNNING pid 73208 |
| 真实 LLM | ✅ DeepSeek v4-flash (17.1s/解读) |
| 安全审计 | ✅ 0 敏感 + 0 代码漏洞 + 0 Flask 风险 + 0 LLM injection |
| 4 份文档 | ✅ README 23.5KB + DEPLOY 8.5KB + CHANGELOG 1.8KB + LICENSE |

**完工报告**:`knowledge/analysis/taixuan-web-completion-2026-07-12.md`

**今日三大完工里程碑**:5 月论文审计 + w4 v1.0 续工 + taixuan-web v1.0 全流程

---

## 🆕 今日速览(2026-07-11 18:45 · w2-idea 收尾)

**w2-idea 窗口 ✅ 收尾**(本轮核心:选 #35 idea + 完整 handoff):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ w2 STATUS.md(7/11 18:45 v3)](../../tmp/windows/w2-idea/STATUS.md) | 撞车矩阵 11×3 + v3 收尾 + SUPERSEDED 勘误段 | 12.7 KB | 🟢 |
| [🆕 _proposal_35_draft.md](../../tmp/windows/w2-idea/_proposal_35_draft.md) | **#35 完整 W1-W12 计划** | 9.8 KB | 🟢 |
| [🆕 _handoff.md](../../tmp/windows/w2-idea/_handoff.md) | **5 min 上手指南**(未来执行者必读) | 9.6 KB | 🟢 |
| [🆕 _scan_report_v2.md](../../tmp/windows/w2-idea/_scan_report_v2.md) | 11 兄弟剩余缺口深扫 + 资产地图 | 7.4 KB | 🟢 |
| [🆕 _dataset_checklist.md](../../tmp/windows/w2-idea/_dataset_checklist.md) | 35 idea Top 5 + 26 简版对照 | 4.2 KB | 🟢 |
| [_proposal_draft.md](../../tmp/windows/w2-idea/_proposal_draft.md) | A4 Verifier Capture 备选(若改 idea 用) | 8.6 KB | 🟡 |
| w4 STATUS 末尾段 | w4 v1.0 启动时 model_pinning 字段预留 | 1.5 KB | 🟡 |
| w5 STATUS 末尾段 × 2 | w5 CP4 baseline 接口 + #35 整合路径 5 行表 | 3.3 KB | 🟢 |

**核心数据**(7/11 18:45 已收尾):
- **选定**:#35 Frontier Model "对齐退化" 静默偏移(USENIX Security 顶会命中)
- **撞车协调**:11 兄弟 3 遍扫描,**6 个能给 #35 喂资产**(w1 Qwen n=10 baseline / w5 ablation_results + run_ablation.py / w7 arxiv 模板 / w9 EPC γ 工具 / w10 KB must-cite / w4 v1.0 预留字段)
- **时间表**:12 周 → **10 周**(省 10 天 = W4 1 周 + W12 1 周)
- **关键 insight**:w3-paper6 14:25 已自启 A4 → #35 跟 A4 不撞
- **勘误**:发现其他 session 18:35 写错的状态广播段(写"X=A4 / Y=B3 / Z=hold"),用 SUPERSEDED 勘误段标记(不覆盖原文)

**窗口边界**:
- ✅ w2-idea 收尾(决策已落)
- ❌ #35 paper 实际启动(留给未来 session)
- ❌ 5 月 deadline(投 2026/11 NeurIPS / 2027/5)

--

---

## 🆕 今日速览(2026-07-11 17:42 · w3 完工)

**w3 PAPER6 → A4 Verifier Capture(Empirical Study)**(本轮核心,继 w6/w9/w4/w5/w11 后第六个完工窗口):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ w3 STATUS.md(7/11 17:42)](./../tmp/windows/w3-paper6/STATUS.md) | W1-W3 完整时间线 + 16 产物清单 + verify 11/12 PASS | 3.9 KB | 🟢 |
| [🆕 PAPER6 entity "完整完工"段](./research/paper6.md) | A4 verifier capture / Empirical Study / 47 KB main.tex | 4.2 → 6.3 KB | 🟢 |
| [F:\Research\PAPER6_CONSOLIDATED\main.tex](../research/paper6.md) | 11 章节完整 paper(标题 / Abstract / Intro / §2-9 + Appendix A.1-A.4)| 46898 bytes | 🟢 |
| [F:\Research\PAPER6_CONSOLIDATED\verify_p6.py](../research/paper6.md) | 12 check 框架,11 实装 1 stub | 14777 bytes | 🟢 |

**核心数据**(7/11 17:42 全跑已实):
- **算法空间穷尽**:CRV v1 / CRV v2 / ATV(我设计)/ kalman_trust,**都没稳定赢 majority**
- **Headline result**:majority 跟 trust_median 全列并列 0.686,其他全部 ≤ 0.673
- **结构性解释**:**capture 在统计上 ≡ honest-but-wrong verifier**,任何用 deviation 检测 capture 的方法都会同时排除真 honest 少数错,净效果 = 0
- **paper 性质**:**Empirical Study / Negative Result**(从原 A4 主推 CRV 在 W2 demo 暴露算法 bug 后转型)

**W3 边界**(刘泽文锁定):
- ✅ W1(骨架 / 算法 / 真实化 Related Work)
- ✅ W2(crv.py + attacks.py + 7 methods + benchmark)
- ✅ W3(§7 Broader Impact + §8 Ethics + Appendix 全实写 + verify C8/C10-C12)
- ❌ W4-W8(超边界,留给刘泽文决定)

**TMLR 适配性**:acceptance criteria 原文"technical correctness over subjective significance" + "We explicitly avoid these terms (significant, impactful, novel)" → **negative result + 结构性解释** 正中 TMLR 偏好

--

---

## 🆕 今日速览(2026-07-11 16:55 · w5 完工)

**w5 paper-review-toolkit 动态化 — DoD 6/6 全绿**(本轮核心,继 w6/w9/w4 后第四个完工窗口):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ w5 STATUS.md(7/11)](./../tmp/windows/w5-paper-review-dynamic/STATUS.md) | 5 CP 全部完工 + DoD + 反哺 IDEA-B3 | 19 KB | 🟢 |
| [📄 w5 DESIGN.md](./../tmp/windows/w5-paper-review-dynamic/DESIGN.md) | Worker 数据结构 + 8 worker 注册表 + 3 设计决策 | 5.5 KB | 🟢 |
| [📊 w5 ablation_report.md](./../tmp/windows/w5-paper-review-dynamic/ablation_report.md) | 4 策略 dry-run 聚合结果 + 📍 TODO 真跑指南 | 5 KB | 🟢 |

**核心数据**:
- 5 CP 用时:~2h(预算 4h,快 2×)
- 10 产物:~105 KB 代码(worker_template + worker_impls + dynamic_spawner + worker_expiration + run_ablation + DESIGN + STATUS + 报告 + JSON)
- 6 个 finding 全修 + 1 个 created_at age=0 调试坑
- 真实端到端:PAPER5 quick 4 步串行 + standard 61KB review prompt

**4 组 ablation 结论(mock,待真跑)**:
- `dynamic_spec` quality 最高(0.850)
- `static_level_tuning` cost 最低($0.170)
- `random_baseline` quality 最低(0.500)— 基线确认

**反哺路径**:
- 全部产出 = IDEA-B3 (Dynamic Worker Pool paper) 的 §3 architecture + §4 implementation + §5 evaluation 实验基础

--

---

## 🆕 今日速览(2026-07-11 15:45 · w4 完工)

**w4 泰玄 V0.2 控制平面 6/6 全绿**(本轮核心,继 w6/w9 后第三个完工窗口):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ w4 泰玄 V0.2 完工报告(7/11)](./analysis/w4-taixuan-v02-completion-2026-07-11.md) | 6 步全交付 + 12 policy + 451 断言不退步 + 5 scanner | 9.1 KB | 🟢 |
| [📄 RFC-001-policy-control-plane.md](./../tmp/w4-taixuan-v02/RFC-001-policy-control-plane.md.step6) | 5 段设计 + 决策记录 + v1.0/v3.0 演进 | 11.2 KB | 🟢 |
| [🔧 policy.schema.json](./../F:/test/2026-06-27-14-59-27/wx-miniprogram/specs/policy.schema.json) | 6 decision + 5 obligation enum + anyOf 强约束 | 4.5 KB | 🟢 |

**核心数据**:
- 6 步用时:7.5h(预算 10h,快 1.3×;实际分配 1.5h 工作时间,间隔跑)
- 10 文件产出:~60KB
- 8 派 cost 平均 0.0035 元/次(135× 富余)
- 26 文件 permission scan / 0 违规

**跨会话同步落地**:
- 7/11 15:50 DASHBOARD v3 → v4(w4 ⚪ → ✅ DONE)
- 7/11 15:52 MEMORY.md + memory/2026-07-11.md 加 w4 专题段 + 当前快照行
- 7/11 17:xx 合规检查报告(11.3KB)落 `wx-miniprogram/docs/COMPLIANCE-CHECK-2026-07-11.md`
- 7/11 17:xx 产品定位重新规划(11.2KB)落 `wx-miniprogram/docs/PRODUCT-REPIVOT-PERSONAL-MP-2026-07-11.md`(选 A 个人 + 大改)
- 7/11 17:xx v1.0 文化工具箱改造 ~50%(Step 1+2 完成,Step 3-7 handoff 给未来 session)— `tmp/w4-taixuan-v02/V1.0-HANDOFF.md`(16.4KB)

--

---

## 🆕 今日速览(2026-07-11 14:38 · w6 完工)

**w6-paper-repair 4 HIGH → 0**(本轮核心):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [✅ w6-paper-repair 完工报告](./analysis/w6-paper-repair-completion-2026-07-11.md) | 4 HIGH 全修(3 个是 verify regex bug)+ 5 条新规 | 6.4 KB | 🟢 |
| [w6 STATUS.md v4](./../tmp/windows/w6-paper-repair/STATUS.md) | 5 篇真数字表 + 完成记录 + 备份清单 | 7.3 KB | 🟢 |
| 3 个 verify 脚本 OR 模式 regex 修复 | `verify_p[2,3,4].py.bak_with_subsection_or_fix` 备份 | +262 bytes | 🟢 |

**关键发现**(治标 + 治本):
- **🪤 治本**:`c2_section_pattern` 不支持 `\subsection` 是**跨 4 个 paper 的共性 verify bug** → 修 verify 比改 main.tex ROI 高 10×
- **🪤 新规**:`PATCH 后必 verify`,不靠文件大小判断(PAPER2 12:12 patch 早就对了,但没 verify 误判为失败)
- **🪤 现场跑 verify 是 ground truth**:audit 报告报 6 HIGH,实测 4 HIGH(PAPER1 MED 报 6 实测 2)

**真 HIGH 总数**:4 → **0**,5 篇距投稿统一"最近"。MED/LOW 41 个未动,工时 ~4h(路径 B/C)。

---

## 🆕 今日速览(2026-07-11 14:25)

**3 个 skill 升级 + 1 个新 skill 创建(7/11 14:xx self-evolve pass)**:

| Skill | 升级 | 关键改动 |
|---|---|---|
| **`cross-session-handoff`** 🆕 | 新建 | 11 兄弟窗口撞车检查 + 接力公告机制(从 w9 撞车 check 工作中沉淀) |
| **`paper-review-toolkit`** | v0.3.0 → **v0.4.0** | + Bug F(C2 regex `\\subsection` 兼容性 + verify-after-patch 强 gate)+ Bug G(audit ≠ verify 实测) |
| **`arxiv-tracker`** | 修补 | + "Self-Citation Filter"(过滤 4 个身份锚点:`liu_z_28` / ORCID `0009-0003-2981-9888` / `17353895263@163.com` / 主页 URL) |
| **`wechat-mp-validation`** | v2.0.0 → **v2.1.0** | + bat 根检测(`if not exist "app.json" cd /d "%~dp0"`)+ 3 个新 scanner(cost/permission/permissions-validate) |

**关键洞察**:self-evolve 不再是"记 MEMORY"而是"修 skill source"——按 `memory/evolution/2026-07-11.md` 14:25 段的新规:**根因在 skill 里的就改 skill,不在 MEMORY 里反复记 symptom**。

**对应 evolution 留底**:`memory/evolution/2026-07-11.md` 14:07 / 14:10 / 14:25 / 13:53 共 4 个 pass

--

---

## 🆕 今日速览(2026-07-11 13:25)

**w9-fill-todo 完工**(本轮核心产出,继 11:00 全量审计之后):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [📊 w9-fill-todo 完成报告](./../tmp/windows/w9-fill-todo/REPORT.md) | 5 篇 CONSOLIDATED 论文 entity TODO 补全 + 撞车 check + 5 篇梯子关系图 | 7.9 KB | 🟢 |
| [w9 STATUS.md](./../tmp/windows/w9-fill-todo/STATUS.md) | 状态 🟡 → 🟢 + 🤝 接力 offer 段 | 6.2 KB | 🟢 |
| [PAPER1-5 entity "内容概述"段](./research/paper1.md) | abstract 草稿 + 关键词 + 主论点 + 章节大纲(70-75% 精度) | 涨 2-4 KB × 5 | 🟢 |
| [PAPER6 entity "w9 决策占位"段](./research/paper6.md) | stub skip + 3 路径候选(A/B/C) | 涨 1.3 KB | 🟢 |
| [🆕 PAPER6 entity "完整完工"段(7/11 17:42)](./research/paper6.md) | A4 verifier capture / Empirical Study / 7 methods × 4 scenarios × 5 seeds / 11/12 verify PASS / main.tex 46898 bytes | 4.2 → 6.3 KB | 🟢 |
| [research/index.md 主研究主线总览](./research/index.md) | 6 篇主题列填真主题 + 投递优先级更新 | 涨 1.7 KB | 🟢 |

**5 篇 CONSOLIDATED 论文梯子关系**(w9 挖出):
- 5 篇共享 **EPC 框架**(Evaluator Preference Coupling γ / 策略熵 H / CV)作为方法学骨架
- 梯子结构:PAPER2(三角理论)→ PAPER1(双面统一)→ PAPER3(因子分解)↔ PAPER5(工程)→ PAPER4(N-sensitivity 元方法论)
- w3 候选 B1/B3 + w7 OS paper 可白嫖此成果(已各插接力标识段)

**多 session 时间戳教训**(w9 顺手挖出):
- 系统时钟在 13:22 左右,MEMORY.md 部分段写"14:xx"是前 session 叙事时间非 system time
- edit 工具返回 success 但 LastWriteTime 未真更新(Windows mtime bug)
- **新规**:撞车判定用 Length + 内容验证,不是 LastWriteTime

--

---

## 🆕 今日速览(2026-07-11 11:00)

**5 月 deadline 论文全量审计完成**:

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [📊 5 篇论文全量审计报告](./analysis/paper-review-audit-2026-07-11.md) | 5 篇 × 4 阶段 + 25 LLM review + 2 bug 修复 | 6.8 KB | 🟢 |
| [PAPER5 audit 段](./research/paper5.md) | ⚠️ 状态更新:不再"唯一可投递" | +1.5 KB | 🟡 |
| [PAPER1-4 audit 段](./research/paper1.md) | 各篇 findings + action 清单 | +1.5 KB × 4 | 🟢 |
| [research/index.md](./research/index.md) | 投递优先级重排 | +1 KB | 🟢 |

7 轮 Agent OS 深度对话的产出(上午):

| 文档 | 用途 | 大小 | 状态 |
|---|---|---|---|
| [Agent OS V1→V7 完整方案](./sources/agent-os-architecture-full-2026-07-11.md) | 10 层架构 + 6 补丁 + 25 漏洞缓解 | 53 KB | 🟢 |
| [漏洞红队报告](./analysis/agent-os-vulnerabilities-2026-07-11.md) | 25 真实漏洞 + S×E×F 评分 | 27.8 KB | 🟢 |
| [研究 idea 挖掘](./analysis/research-ideas-from-agent-os-2026-07-11.md) | 15 个 paper 候选 | 22 KB | 🟢 |
| [idea 漏洞分析](./analysis/research-ideas-vulnerabilities-2026-07-11.md) | 第二轮红队 + 5 道筛子 | 18.7 KB | 🟢 |
| [📦 `aidless/obsidian` 项目产物清单](./analysis/project-artifacts-inventory-2026-07-11.md) | 16 文件 + ~17.7 GB KB 数据 + 临时日志盘点 | 16.5 KB | 🟢 |

配套建立的 5 个核心概念页 + 6 篇论文 entity(详见各 section)。

--

---

