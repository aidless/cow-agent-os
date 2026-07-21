# 📦 `aidless/obsidian` 项目产物完整清单

> **生成时间**: 2026-07-11
> **最后更新**: 2026-07-11 13:30(清理行动后)
> **项目目录**: `E:\peS2o_kb_faiss\`
> **部署目标**: `https://github.com/aidless/obsidian`
> **项目本质**: **纯 Python 项目 + KB 数据驱动系统**
> **"build 产物"性质**: 源码即产物（`.py` 直接运行）+ 运行时数据（FAISS/SQLite/文本）
>
> 🧹 **清理状态**: 已完成 [KB 项目陈旧产物清理行动](./cleanup-stale-artifacts-2026-07-11.md),**释放 1.3 GB**(21 文件)。当前文件数已减少,详见文末「清理后变更」章节。

> ⚠️ **重要前提**:本项目**没有传统意义**的 build 产物 —— 没有 `make` / `CMakeLists.txt` / `Cargo.toml` / `pom.xml`、没有 binary、没有 `.a/.so/.dll`。
> Python 不需要编译（`.py` 直接运行）。`pip install -r requirements.txt` 装的是第三方依赖（numpy / faiss-cpu / sentence-transformers），装到 Python site-packages，跟本清单无关。

---

## 🎯 全局鸟瞰

| 类别 | 路径基数 | 总大小 | 进 GitHub? |
|------|----------|--------|-----------|
| **A. 项目源代码** | `E:\peS2o_kb_faiss\` | ~213 KB | ✅ **16 文件已 push** |
| **B. 运行时 KB 数据** | `E:\peS2o_kb_faiss\` | **~17.7 GB** | ❌ .gitignore 排除 |
| **C. 临时/缓存/日志** | `E:\peS2o_kb_faiss\` + `F:\temp\` | ~600 KB | ❌ |
| **总计** | 3 个盘符混合 | **~17.71 GB** | 仅 A 进 GitHub |

---

# 📦 A. 项目源代码产物（部署到 GitHub 的 16 个文件，~213 KB）

> **部署状态**: 3 个 commit, 16 文件, ~9 KB（其实是部署时只 push 了 `.py` + 配置 + 测试 + 文档，没把 `.bat` / LaTeX / 生产脚本 push 进去）

## A.1 核心 Python 脚本（5 个，源码即产物）

```
E:\peS2o_kb_faiss\dedup_and_reindex.py       (28,688 bytes)   🟢 dedup + reindex 主流程
E:\peS2o_kb_faiss\kb_health.py                (20,616 bytes)   🟢 KB 健康检查
E:\peS2o_kb_faiss\kb_search.py                (30,232 bytes)   🟢 KB 语义检索主入口
E:\peS2o_kb_faiss\merge_to_disk.py            (12,177 bytes)   🟢 增量 merge 到磁盘
E:\peS2o_kb_faiss\smart_rerank.py              (7,285 bytes)   🟢 Rerank 算法
```

**A.1 子合计**: **5 文件, ~99 KB**

## A.2 配置文件（3 个）

```
E:\peS2o_kb_faiss\.gitignore                                  (495 bytes)   🟢 git 排除规则
E:\peS2o_kb_faiss\requirements.txt                            (184 bytes)   🟢 Python 第三方依赖
E:\peS2o_kb_faiss\.github\workflows\ci.yml                  (6,917 bytes)   🟢 GitHub Actions CI
```

**A.2 子合计**: **3 文件, ~7.6 KB**

## A.3 测试套件（6 个文件）

```
E:\peS2o_kb_faiss\tests\__init__.py                          (33 bytes)
E:\peS2o_kb_faiss\tests\_mocks.py                        (6,875 bytes)
E:\peS2o_kb_faiss\tests\test_kb_search.py              (12,346 bytes)
E:\peS2o_kb_faiss\tests\test_kb_search_unit.py          (8,048 bytes)
E:\peS2o_kb_faiss\tests\simulate_ci_timeout.py          (8,766 bytes)
E:\peS2o_kb_faiss\tests\README.md                         (879 bytes)
```

**A.3 子合计**: **6 文件, ~36.9 KB**

## A.4 文档（2 个）

```
E:\peS2o_kb_faiss\CICD_DEPLOYMENT_CHECKLIST.md        (8,276 bytes)   🟢 部署 checklist
E:\peS2o_kb_faiss\CHANGELOG_2026-07-09.md             (5,662 bytes)   🟢 变更日志
```

**A.4 子合计**: **2 文件, ~14 KB**

### A 合计: **16 文件 / ~213 KB / 已 push GitHub**

---

# 💾 B. 运行时 KB 数据产物（本地，~17.7 GB，**.gitignore 排除**）

> **KB 系统产物** 通过 `merge_to_disk.py` / `dedup_and_reindex.py` 运行时生成，不是 `build` 出来的。

## B.1 KB 主索引（3 个文件，~9.17 GB）—— 🎯 核心运行时数据

```
E:\peS2o_kb_faiss\papers.index                       (831,916,077 bytes = 793.4 MB)   🎯 FAISS 索引
E:\peS2o_kb_faiss\papers.db                       (8,987,131,904 bytes = 8.37 GB)   🎯 SQLite metadata
E:\peS2o_kb_faiss\paper_ids.txt                        (5,972,869 bytes = 5.7 MB)   🎯 paper ID 列表
```

**B.1 子合计**: **3 文件, ~9.17 GB**

## B.2 Backup 目录（回滚用，~8.5 GB）

```
E:\peS2o_kb_faiss\rebuild_backups\                                      (目录)
├── E:\peS2o_kb_faiss\rebuild_backups\papers_20260710_172130.index     (533 MB)    🟠 gap merge 前的 backup
├── E:\peS2o_kb_faiss\rebuild_backups\paper_ids_20260710_172130.txt    (3.7 MB)   🟠 配套 ID 文件
└── E:\peS2o_kb_faiss\rebuild_backups\20260710_202232\                (目录)     🟠 dedup_and_reindex 后的完整 backup
    ├── E:\peS2o_kb_faiss\rebuild_backups\20260710_202232\papers.index  (793 MB)
    ├── E:\peS2o_kb_faiss\rebuild_backups\20260710_202232\papers.db    (8.37 GB)
    └── E:\peS2o_kb_faiss\rebuild_backups\20260710_202232\paper_ids.txt (5.7 MB)
```

**B.2 子合计**: **2 文件 + 1 目录（含 3 文件）= 5 项目, ~8.51 GB**
> 🪤 **风险点**: 这俩 backup 时间戳相近，但根目录 .index 是 dedup **后**的（793 MB），`20260710_172130` 是 dedup **前**（533 MB）—— 533 MB 的 backup 其实已被 793 MB 取代，**理论上可清理**。

## B.3 历史 .bak 文件（rebuild 残留）

```
E:\peS2o_kb_faiss\papers.index.bak          (rebuild 前的 index 备份)
E:\peS2o_kb_faiss\paper_ids.txt.bak         (rebuild 前的 ids 备份)
```

**B.3 子合计**: **2 文件**
> 🪤 **风险点**: 已被 `rebuild_backups/` + 主数据覆盖，**属可清理残留**

## B.4 State / Checkpoint JSON（3 个）

```
E:\peS2o_kb_faiss\daily_grow_state.json                (1,069 bytes)   🟡 daily_grow 状态
E:\peS2o_kb_faiss\fill_gap_checkpoint.json               (42 bytes)   🟡 gap 填充 checkpoint
E:\peS2o_kb_faiss\checkpoint_old.json                (old checkpoint)   🟡 已过时
```

**B.4 子合计**: **3 文件, ~1.1 KB**

## B.5 JSONL 数据文件

```
E:\peS2o_kb_faiss\kaggle_new_papers.jsonl                (kaggle 来源论文)
```

**B.5 子合计**: **1 文件**

## B.6 KB 增长日志

```
E:\peS2o_kb_faiss\kb_growth_log.csv
```

### B 合计: **~17.7 GB**（绝大部分是 `papers.db` 8.37 GB + 主 index 793 MB + backup 8.5 GB）

---

# 🗑️ C. 临时 / 缓存 / 日志（本次会话期间 + 持续累积，~600 KB，**`.gitignore` 排除**）

## C.1 Python 编译缓存（8 个 .pyc，自动生成）

```
E:\peS2o_kb_faiss\__pycache__\
├── E:\peS2o_kb_faiss\__pycache__\kb_health.cpython-39.pyc     (581 bytes)
├── E:\peS2o_kb_faiss\__pycache__\kb_search.cpython-39.pyc     (984 bytes)
├── E:\peS2o_kb_faiss\__pycache__\kb_server.cpython-39.pyc     (460 bytes)
└── E:\peS2o_kb_faiss\__pycache__\smart_rerank.cpython-39.pyc (889 bytes)

E:\peS2o_kb_faiss\tests\__pycache__\
├── E:\peS2o_kb_faiss\tests\__pycache__\__init__.cpython-39.pyc
├── E:\peS2o_kb_faiss\tests\__pycache__\_mocks.cpython-39.pyc
├── E:\peS2o_kb_faiss\tests\__pycache__\test_kb_search.cpython-39.pyc
└── E:\peS2o_kb_faiss\tests\__pycache__\test_kb_search_unit.cpython-39.pyc
```

**C.1 子合计**: **8 文件, ~3 KB**

## C.2 运行时日志文件（24 个，~580 KB）

```
E:\peS2o_kb_faiss\daily_grow.log                       (16,131 bytes)
E:\peS2o_kb_faiss\daily_grow2_stderr.log                    (0 bytes)
E:\peS2o_kb_faiss\daily_grow2_stdout.log                  (808 bytes)
E:\peS2o_kb_faiss\daily_grow3_stderr.log                    (0 bytes)
E:\peS2o_kb_faiss\daily_grow3_stdout.log                  (814 bytes)
E:\peS2o_kb_faiss\daily_grow_ai.log                      (3,641 bytes)
E:\peS2o_kb_faiss\daily_grow_ai.err                            (file)
E:\peS2o_kb_faiss\daily_grow_cv.log                      (4,448 bytes)
E:\peS2o_kb_faiss\daily_grow_cv.err                            (file)
E:\peS2o_kb_faiss\daily_grow_stderr.log                   (582 bytes)
E:\peS2o_kb_faiss\daily_grow_stdout.log                  (4,447 bytes)
E:\peS2o_kb_faiss\daily_grow_w3a_stderr.log               (582 bytes)
E:\peS2o_kb_faiss\daily_grow_w3a_stdout.log              (3,841 bytes)
E:\peS2o_kb_faiss\daily_grow_w6.log                      (4,450 bytes)
E:\peS2o_kb_faiss\daily_grow_w6.err                            (file)
E:\peS2o_kb_faiss\kb_health.log                           (816 bytes)
E:\peS2o_kb_faiss\kb_server.log                             (0 bytes)
E:\peS2o_kb_faiss\kb_server.err                                  (file)
E:\peS2o_kb_faiss\kb_server_v2.log                          (0 bytes)
E:\peS2o_kb_faiss\kb_server_v2.err                               (file)
E:\peS2o_kb_faiss\rebuild.log                          (148,625 bytes)
E:\peS2o_kb_faiss\rebuild_run.log                       (14,338 bytes)
E:\peS2o_kb_faiss\rebuild_stderr.log                      (291 bytes)
E:\peS2o_kb_faiss\rebuild_stdout.log                   (137,053 bytes)
E:\peS2o_kb_faiss\run.log                              (25,575 bytes)
E:\peS2o_kb_faiss\self_grow.log                         (22,355 bytes)
```

**C.2 子合计**: **26 文件（含 .err）, ~390 KB**（含几个 0 字节）

> 🪤 **乱象预警**: `daily_grow*.log` 有 10+ 个变种（`_ai` / `_cv` / `_w3a` / `_w6` / `_stderr` / `_stdout` ...），说明日常调度有反复试错的历史。

## C.3 Windows 批处理脚本（4 个，调度用，**没 push GitHub**）

```
E:\peS2o_kb_faiss\daily_grow.bat
E:\peS2o_kb_faiss\post_daily_grow_check.bat
E:\peS2o_kb_faiss\setup_scheduler.bat
E:\peS2o_kb_faiss\start_kb_server.bat
```

**C.3 子合计**: **4 文件**

## C.4 LaTeX 测试文件（评估用，7 个，**没 push**）

```
E:\peS2o_kb_faiss\test_orch.bib
E:\peS2o_kb_faiss\test_orch.tex
E:\peS2o_kb_faiss\test_orch_fixed.tex
E:\peS2o_kb_faiss\test_v5.bib
E:\peS2o_kb_faiss\test_v5.tex
E:\peS2o_kb_faiss\test_v5_fixed.tex
E:\peS2o_kb_faiss\test_v6.tex
```

**C.4 子合计**: **7 文件**

## C.5 生产环境 Python 脚本（**非 deploy 范围，9 个**）

```
E:\peS2o_kb_faiss\daily_grow.py                       (17,779 bytes)   🟠 daily grow 系统
E:\peS2o_kb_faiss\self_grow.py                        (18,789 bytes)   🟠 self growth
E:\peS2o_kb_faiss\finalize_rebuild.py                 (5,223 bytes)   🟠 rebuild finalize
E:\peS2o_kb_faiss\fetch_specific.py                  (11,860 bytes)   🟠 fetch specific papers
E:\peS2o_kb_faiss\rebuild_kb_clean.py                (17,470 bytes)   🟠 rebuild cleaner
E:\peS2o_kb_faiss\watch_rebuild.py                    (2,915 bytes)   🟠 watch rebuild
E:\peS2o_kb_faiss\kb_server.py                       (13,077 bytes)   🟠 Flask? KB server
E:\peS2o_kb_faiss\kb_growth_log.py                    (2,446 bytes)   🟠 growth logger
E:\peS2o_kb_faiss\batch_must_cite.py                  (3,699 bytes)   🟠 must-cite batch
```

**C.5 子合计**: **9 文件, ~93 KB**

> 🪤 **风险点**: 这些是**生产系统核心**，但**没进 GitHub**。只 deploy 了 `dedup_and_reindex` / `kb_health` / `kb_search` / `merge_to_disk` / `smart_rerank` 这 5 个核心脚本，deploy 范围 ≠ 业务范围。

## C.6 隐藏目录 + 内部状态（**没进 GitHub**）

```
E:\peS2o_kb_faiss\.agent_data\                  (目录, agent 状态)
E:\peS2o_kb_faiss\.arxiv_cache\                 (目录, arxiv 缓存)
E:\peS2o_kb_faiss\.calibration\                 (目录, calibration 数据)
E:\peS2o_kb_faiss\.experiments\                 (目录, 实验数据)
E:\peS2o_kb_faiss\.long_term_memory\             (目录, 长期记忆)
E:\peS2o_kb_faiss\.memory\                       (目录, 短期记忆)
E:\peS2o_kb_faiss\.taste_learner\                (目录, taste learner)
E:\peS2o_kb_faiss\.git\                          (git 仓库, deploy 后生成的)
E:\peS2o_kb_faiss\.researcher_memory.json        (memory JSON)
E:\peS2o_kb_faiss\arxiv_updater_system\          (目录, arxiv updater)
```

**C.6 子合计**: **9 目录 + 1 JSON**

## C.7 已清理的 Checkpoint（部署时已清）

```
F:\temp\dedup_reindex_ckpt.json     (部署完成后已删除 ✅)
F:\temp\dedup_reindex_vecs.npy      (部署完成后已删除 ✅)
```

**C.7 子合计**: **2 文件, 已清理**

## C.8 本会话期间生成的临时文件（`F:\temp\`）

### C.8.1 临时 log 文件（24+ 个）

```
F:\temp\dedup_run.log                 (dedup_and_reindex 运行日志)
F:\temp\diff_full.log                (差异分析 log)
F:\temp\diff_investigate.log        (deep diff log)
F:\temp\diff_step1.log               (差集 step1 log)
F:\temp\final_check.log              (最终检查 log)
F:\temp\kb_search_after.log          (kb_search 跑完 log)
F:\temp\kb_search_timeout_test.log   (timeout 测试 log)
F:\temp\merge_full.log               (merge 完整 log)
F:\temp\pr_check.log                 (PR 检查 log)
F:\temp\push2.log                    (push 第 2 次 log)
F:\temp\push_retry.log               (push retry log)
F:\temp\simulate_ci.log              (CI 模拟 log)
F:\temp\test_run.log                 (test 跑 log)
F:\temp\test_stderr.log              (test stderr)
F:\temp\test_unit.log                (unit test log)
F:\temp\test_unit2.log               (unit test 2)
F:\temp\test_verbose.log             (test verbose)
F:\temp\test_verbose2.log            (test verbose 2)
F:\temp\test_post_dedup.log          (post dedup test)
F:\temp\timeout_test.log             (timeout test)
```

**C.8.1 子合计**: **20 文件**

### C.8.2 本会话脚本（7 个）

```
F:\temp\check_pr_html.py
F:\temp\check_pr_html2.py
F:\temp\check_specific.py
F:\temp\check_gap_data.py
F:\temp\direct_search.py
F:\temp\test_timeout.py
F:\temp\verify_merge.py
F:\temp\verify_post_dedup.py
F:\temp\_git_push_with_dns_retry.py  (F:\Research 借用的 push 工具)
```

**C.8.2 子合计**: **9 文件**

### C.8.3 CI 模拟相关

```
F:\temp\simulate_ci\                  (CI 模拟目录)
├── F:\temp\simulate_ci\install_step.log
├── F:\temp\simulate_ci\unittest_output.log
└── F:\temp\simulate_ci\downloaded_artifact.log
F:\temp\test-logs.zip                 (从 GitHub 下载的 artifact)
F:\temp\test-logs-extracted\          (解压目录)
```

**C.8.3 子合计**: **1 目录（含 3 log） + 1 zip + 1 解压目录**

### C.8.4 无关目录

```
F:\temp\tmaudit-build-wheel\          (其他项目的产物, 跟我们无关)
```

### C 合计: **~600 KB + 1 zip + 1 目录**

---

# ⚠️ 诚实声明：什么叫"build 产物"？

> 这份清单**刻意包含 2 类非传统产物**：
>
> **A. 项目源代码产物**（源码即产物，直接 deploy）
>
> **B. 运行时 KB 数据产物**（通过 `merge_to_disk.py` / `dedup_and_reindex.py` 运行时生成，不是 `build` 出来的）
>
> **严格意义上** "build 产物" 应该是 `pip install -r requirements.txt` 装到 Python site-packages 的第三方依赖：
>
> ```
> C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.9.25-windows-x86_64-none\Lib\site-packages\numpy\
> C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.9.25-windows-x86_64-none\Lib\site-packages\faiss\
> C:\Users\Administrator\AppData\Roaming\uv\python\cpython-3.9.25-windows-x86_64-none\Lib\site-packages\sentence_transformers\
> ```
>
> **但这些是第三方依赖**，跟本项目无关，**不列入本清单**。

---

# 📊 最终统计表

| 类别 | 文件数 | 大小 | 路径基数 | 进 GitHub? |
|------|--------|------|----------|-----------|
| **A. 项目源代码** | 16 文件 | ~213 KB | `E:\` | ✅ **16 push** |
| **B. KB 运行时数据** | ~20 文件+目录 | **~17.7 GB** | `E:\` | ❌ .gitignore 排除 |
| **C. 临时/缓存/日志** | ~100 文件 | ~600 KB | `E:\` + `F:\` | ❌ |
| **总计** | **~140 项** | **~17.71 GB** | 3 盘符 | 仅 A |

---

# 🪤 关键观察（给下一个 session 的我）

1. **KB 数据占 99.9%**：~17.7 GB / 17.71 GB —— 这是真"产物"。16 KB 的 GitHub 代码只是冰山一角。
2. **Backup 占 KB 数据的 ~48%**：`rebuild_backups/20260710_202232/` 完整备份了 ~8.5 GB（index + db + ids）。**回滚窗口很重要**，别轻易删。
3. **`daily_grow*.log` 乱象**：10+ 变种说明日常调度有反复试错。**7 天清理机制缺失**。
4. **生产脚本没进 GitHub**：`daily_grow.py` / `self_grow.py` / `kb_server.py` 等核心业务逻辑**只有本地**。**deploy 范围 ≠ 业务范围**——这是 GitHub repo 目前最大的 gap。
5. **`.bat` 没 push**：调度脚本（`daily_grow.bat` / `start_kb_server.bat`）是部署后的运维入口，**没进 GitHub**。
6. **`F:\temp\` 本会话 30+ 文件**全部可一次性清理（部署已稳定），保留最近的 `_git_push_with_dns_retry.py` 即可。

---

## 🧹 清理后变更(2026-07-11 13:30)

**详细报告**: 见 [cleanup-stale-artifacts-2026-07-11.md](./cleanup-stale-artifacts-2026-07-11.md)

| 清理项 | 文件数 | 释放空间 | 当前状态 |
|---|---|---|---|
| 0 字节 log | 4 | 0 KB | ✅ 已删 |
| backup 副本 → quarantine | 4 | 1,073.5 MB | 🛡️ 7 天回滚(至 7/18)|
| `daily_grow*.log/err` 变种 | 10 | ~23 KB | ✅ 已删(留主日志)|
| `kaggle_new_papers.jsonl` → tmp 归档 | 1 | 253 MB | 🛡️ 永久归档 |
| **总计** | **21** | **1,326.65 MB / 1.3 GB** | |

**清理后项目状态**:
- 项目总产物:~17.71 GB → **~16.38 GB**(**-1.3 GB**)
- KB 主数据(`papers.index/db/ids`):不动 ✅
- 最新完整 backup(`rebuild_backups/20260710_202232/`):不动 ✅

---

**归档完成**: `C:\Users\Administrator\cow\tmp\PROJECT_ARTIFACTS_INVENTORY.md`
**总长度**: ~270 行 / 完整 3 大类 + 诚实声明 + 关键观察
