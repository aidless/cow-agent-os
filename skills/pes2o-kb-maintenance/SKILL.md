---
name: pes2o-kb-maintenance
description: Maintain and release the local peS2o / FAISS paper knowledge base in aidless/obsidian. Use when the user asks about KB health, pes2o, FAISS index, papers.db, kb_search --bibtex, generating citation bundles, VACUUM/freeing SQLite space, staging cleanup, or committing/pushing KB scripts/state to GitHub.
---

# peS2o KB Maintenance

Use this skill for the `aidless/obsidian` paper KB workflow: health checks, citation export, SQLite compaction, staging cleanup, and safe git release.

## Core principles

- **Verify before trusting stdout**: a command may print "saved to ..." before failing. Check exit code, file existence, and file size.
- **Prefer absolute paths on Windows**: avoid long `..\..\..\..\tmp\...` paths across drive roots; PowerShell can collapse them into stray `\\`.
- **Never commit large/regenerable artifacts**: keep DBs, indexes, backups, logs, and private agent state out of git unless the user explicitly chooses otherwise.
- **Do destructive or heavy work in two phases**: scan and present the plan first; execute only after user approval.

## Standard health snapshot

When asked "KB 状态 / health / 还能用吗", gather and report:

1. Repository and branch (`git status -sb`, remote URL).
2. DB size and SQLite stats:
   - `PRAGMA integrity_check;`
   - `SELECT COUNT(*) FROM papers;`
   - FTS/vector counts if project scripts expose them.
   - `PRAGMA page_count; PRAGMA freelist_count; PRAGMA page_size;`
3. FAISS/vector index size and vector count if available.
4. Latest freshness/growth state (`daily_grow_state.json`, `kb_growth_log.csv`, health JSON) when present.
5. Disk free space on the DB drive.
6. Final verdict: `HEALTHY`, `DEGRADED`, or `BLOCKED`, with the exact failing check.

## Citation / BibTeX export workflow

For `kb_search.py --bibtex`, `--json`, or similar output flags:

1. Use an absolute output path, preferably under workspace `tmp/` or a project `exports/` directory.
2. Ensure parent directories exist before invoking the command.
3. After running, validate all three:
   - process exit code is 0;
   - output file exists;
   - output file size is non-zero and content matches expected format.
4. If patching CLI path handling, use `pathlib.Path(...).expanduser().resolve()` where safe and always call `parent.mkdir(parents=True, exist_ok=True)` for user-controlled output paths.
5. Do not treat printed "Generating/Saved" messages as success without the checks above.

## SQLite VACUUM workflow

Use when freelist is large or user asks to reclaim space.

### 1. Preflight scan

Report before execution:

- DB absolute path and size.
- `integrity_check` result.
- key table counts before VACUUM.
- `page_count`, `freelist_count`, `page_size`, estimated reclaimable GB.
- `PRAGMA journal_mode;`.
- existing backup directory and size.
- free disk space; require enough room for at least one extra DB copy.
- whether scheduled jobs such as `daily_grow` may be running.

### 2. Backup

Create a same-drive backup such as `papers.db.bak_before_vacuum` or confirm an existing recent full backup. Verify backup size before proceeding.

### 3. Execute

Run `VACUUM;` with a timeout appropriate for multi-GB DBs. Warn that SQLite locks the DB while VACUUM runs.

### 4. Post-verify

Only declare success after:

- `integrity_check = ok`;
- key counts match preflight counts;
- `freelist_count = 0` or near-zero;
- DB file size decreased as expected;
- the project health check still passes.

Delete the temporary pre-VACUUM backup only after these checks pass and the user is comfortable with the risk. Keep long-term rebuild backups unless the user explicitly asks to remove them.

## Staging / temp cleanup workflow

Before deleting staging files:

1. List candidates with path, size, and reason.
2. Separate safe temp/log/cache files from source/data files.
3. Move to a quarantine folder first when possible; delete only after validation.
4. Report bytes reclaimed.

## Git release workflow

Use when fixing "Bug 1 git push" or releasing KB scripts/state.

### 1. Scan and classify

Run `git status --short` and classify files into:

- **Push**: source scripts, tests, CI workflow, scheduler/batch helpers, small non-sensitive state/checkpoint files if useful.
- **Ignore**: `.agent_data/`, `.experiments/`, `.memory/`, private memory JSON, server stderr logs, temporary test outputs.
- **Never push by default**: `papers.db`, FAISS indexes, raw corpora, rebuild/self-grow backups, huge logs, credentials, API keys.

### 2. Update `.gitignore`

Ensure it covers at least:

```gitignore
papers.db
papers.index
paper_ids.txt
rebuild_backups/
self_grow_backups/
*.log
*.bak
__pycache__/
.agent_data/
.experiments/
.memory/
.researcher_memory.json
kb_server*.err
test_*
```

Adjust to the repository's actual file names.

### 3. Credentials dry-run

Use a non-mutating check such as `git ls-remote <remote>` to confirm credentials before `git push`.

### 4. Commit and push

After user approval:

1. `git add` only the intended files.
2. Show staged summary.
3. Commit with a message that states the KB fix/release.
4. Push to the current branch.
5. Verify remote HEAD equals local HEAD and working tree is clean.

## Reporting template

End with a compact table:

| Area | Result |
|---|---|
| KB health | HEALTHY/DEGRADED/BLOCKED |
| DB size | before → after |
| Counts | before = after |
| Reclaimed | GB/MB |
| Git | commit hash / remote branch / clean? |
| Remaining bugs | list |

Flag uncertainties explicitly instead of smoothing over inconsistent disk-space readings or PowerShell rendering errors.
