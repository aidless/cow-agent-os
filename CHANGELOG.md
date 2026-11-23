# Changelog

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Offline `make check` reruns the Flask test files and rereads the committed
  benchmark JSON, then fails if the root README drifts. CI runs that command.
- Historical `LICENSE` files from the removed `tools/` trees are copied under
  `tools/licenses/`. The trees stay out of HEAD.
- Governance baseline: LICENSE, security policy, code of conduct, contributor and
  support guides, issue and pull-request templates, CODEOWNERS, dependabot, and
  `.editorconfig` added. No research content changed.
