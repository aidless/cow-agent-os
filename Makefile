.PHONY: check

# Recompute README.md from pytest and the committed benchmark JSON.
check:
	python3 scripts/check_claims.py
