# Scriptorium — CI & hooks

Last reviewed: 2026-08-23

## Recommendation (what runs where)

| Check | Pre-commit | Pre-push | CI fast (`ci.yml`) | CI slow (`security.yml`) |
|---|---|---|---|---|
| **File line count** | ✅ `check-file-size` | — | ✅ all tracked files | — |
| **Living backlog size** | ✅ `check-todo-limits` | — | ✅ `to_do.md` | — |
| **Backlog ↔ plans sync** | ✅ `check-todo-plan-sync` (advisory) | — | ✅ advisory (allowed to fail) | — |
| **Complexity** | ✅ ruff `C901` and `PLR0912` | — | ✅ same | — |
| **Secrets** | ✅ gitleaks + private-key | — | ✅ gitleaks full history | TruffleHog weekly (advisory) |
| **Lint** | ✅ ruff, markdownlint, shellcheck | — | ✅ same + actionlint | — |
| **Type check (Python)** | — | ✅ basedpyright | ✅ basedpyright | — |
| **Rust fmt / clippy / test** | — | — | ✅ required from **M0** once `src-tauri/` exists | — |
| **Tests + coverage** | — | — | ✅ pytest-cov (report; gate later) | — |
| **SAST** | — | — | — | ✅ Semgrep on PR |
| **CodeQL** | — | — | — | later — [M0.5](../plans/2026-08-23-product-roadmap.md#m05--harness-follow-ups-after-tauri-scaffold--when-app-code-exists) |

**Later (M0.5):** Vitest coverage gates, TS eslint pre-push, CodeQL/Dependabot. **Rust fmt/clippy/test belong in M0**, not M0.5 — see foundation plan.

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
- `Rust (src-tauri)` — **required from M0** once `src-tauri/` exists (`cargo fmt` / `clippy` / `test` / `check`; exact job name must match `ci.yml`)

Until M0 lands, omit the Rust job from the ruleset so the branch is not blocked on a missing check.

## Thresholds

- Source lines: soft **600** / hard **1000** — [`policies/file-size-and-counts.md`](../policies/file-size-and-counts.md)
- Complexity: cyclomatic **15**, branches **15**, statements **100** — `ruff.toml`
- Coverage: **reported** on `hooks/scripts` + `ci/scripts` today; raise `fail_under` after app tests (M0.5)

## Temp files

Use gitignored [`tmp/`](../tmp/) for scratch runs; never commit large scan corpora.
