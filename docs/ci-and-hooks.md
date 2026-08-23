# Scriptorium — CI & hooks

Last reviewed: 2026-08-23

## Recommendation (what runs where)

| Check | Pre-commit | Pre-push | CI fast (`ci.yml`) | CI slow (`security.yml`) |
|---|---|---|---|---|
| **File line count** | ✅ `check-file-size` | — | ✅ all tracked files | — |
| **Complexity** | ✅ ruff `C901` / PLR | — | ✅ same | — |
| **Secrets** | ✅ gitleaks + private-key | — | ✅ gitleaks full history | TruffleHog weekly (advisory) |
| **Lint** | ✅ ruff, markdownlint, shellcheck | — | ✅ same + actionlint | — |
| **Type check (Python)** | — | ✅ basedpyright | ✅ basedpyright | — |
| **Tests + coverage** | — | — | ✅ pytest-cov (report; gate later) | — |
| **SAST** | — | — | — | ✅ Semgrep on PR |
| **CodeQL** | — | — | — | later — [M0.5](../plans/2026-08-23-product-roadmap.md#m05--harness-follow-ups-after-tauri-scaffold--when-app-code-exists) |

**Later (M0.5), when Tauri/TS/Rust exist:** add `tsc` and `cargo clippy` to pre-push + CI; Vitest/cargo tests + coverage gates; optional CodeQL/Dependabot. See roadmap M0.5 and [`to_do.md`](../to_do.md).

## Quick start

```bash
pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type pre-push
pre-commit run --all-files
pre-commit run --all-files --hook-stage pre-push   # basedpyright
```

## Required GitHub checks (suggested)

After the first green `CI` run, set default-branch ruleset required checks to:

- `Policy (file size, docs, backlog)`
- `Lint & format`
- `Type check (Python)`
- `Tests & coverage`
- `Secret scan (gitleaks)`
- `SAST — Semgrep` (from Security workflow)

## Thresholds

- Source lines: soft **600** / hard **1000** — [`policies/file-size-and-counts.md`](../policies/file-size-and-counts.md)
- Complexity: cyclomatic **15**, branches **15**, statements **100** — `ruff.toml`
- Coverage: **reported** on `hooks/scripts` + `ci/scripts` today; raise `fail_under` after app tests (M0.5)

## Temp files

Use gitignored [`tmp/`](../tmp/) for scratch runs; never commit large scan corpora.
