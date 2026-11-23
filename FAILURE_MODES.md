# Failure modes

Counted results live in the root README and are recomputed by `make check`. This file says what those results do not prove. It is kept free of digits so a number cannot drift here.

## Tests

`make check` runs every `test_*.py` file under the Flask app, each in its own process, and runs the clean pair again in one process. A count changes only when that run changes and the README is updated to match. The check does not fix failures. A file that fails collection is an error, not a pass.

Passing the clean pair in separate processes does not mean they pass together. The combined run is recorded because it does not.

The lockout file lowers its lockout threshold and points the database at a temporary file. That is not a production lockout proof.

`test_app.py` still inserts a Windows path that is not this checkout. Pytest adds the app directory itself, which is why some imports still resolve. This check does not rewrite that path.

Signals in the test table are substrings of pytest output. They are not a complete cause for every failure.

## Benchmarks

The check rereads committed JSON files. It does not run `benchmark_llm.py` and it does not contact a model host. Empty model text scored at the bottom of the range is not an authentication failure. An authentication error on one backend is not a score for the other backend. A missing overall entry means that backend had no successful summary. Files disagree about which backend scores higher. That is not a ranking.

## Rules

`AGENT.md`, `RULE.md`, `MEMORY.md`, and `WORKFLOW.md` are documents. Nothing executes them.

## Provenance

License files under `tools/licenses/` are copies taken from one historical commit. The check hashes those copies and reads their headings. It does not walk git history, and it does not fetch upstream. The project trees are not in HEAD. They remain in git history. History was not rewritten. Pack size is not measured.

`knowledge/` is workspace notes. This check does not read those notes for copied prose. It only checks that the directory has no `LICENSE` file and is not labeled as a third-party code tree.

`tools/README.md` still names upstream repositories. The check only requires those URL strings to stay present. It does not open them.

## Secrets

The check rejects a tracked token that looks like `sk-` plus a long alphanumeric run. It does not run gitleaks, and it does not scan git history. Truncated key fragments remain in notes. Those fragments are not full tokens. Do not treat this as a secret-scanning audit of history.

## Versions and other documents

The check locks the app healthz version string to the first heading of the app changelog, and it requires that same token in the `app.py` module docstring. The analytics module still carries its own version label. This check does not reconcile that label.

The Flask app's own README is not regenerated. A banner points at the root README. Older sentences in that file are not gated.

GitHub About is outside git. The proposed text is the generated line in the root README. This repository cannot set About by itself.

The packaging and publish workflows do not run `make check`. They only need to use the same Python version string as the test workflows. A skipped package build is not a test result.

## Fresh clone

The check needs Python, pip, the requirements file, and git. It does not need an API key or a running model. It reads the HEAD tree. A shallow checkout is enough.
