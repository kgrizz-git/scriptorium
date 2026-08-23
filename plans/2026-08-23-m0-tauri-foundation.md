# Plan: M0 — Tauri foundation

Last reviewed: 2026-08-23
Date: 2026-08-23
Author: bootstrap session
Status: draft
Linked issue/PR: n/a
Depends on: harness CI/hooks already on `main`
Blocks: [`2026-08-23-m1-scan-viewer.md`](2026-08-23-m1-scan-viewer.md)

## Goal

Stand up a **runnable Tauri 2 desktop shell** (Vite + React + TypeScript) and a **versioned book
package schema** so M1 can implement folder ingest and the flipbook without inventing project
layout mid-feature. Close remaining bootstrap harness leftovers that do not require app code.

## Out of scope

- Page-turn viewer, ingest UX, last-read page (→ M1)
- OCR, text layer, library, hotspots, web deploy (→ M2+)
- Full M0.5 CI matrix for TS/Rust (→ after this lands; tracked in roadmap M0.5)
- Visual polish / paper texture beyond a minimal chrome placeholder

## Approach

Create the app at **repo root** (standard Tauri layout: `src/`, `src-tauri/`) rather than a nested
monorepo package — one product, one app for now. Use **pnpm** + **React** (default; Svelte only if
explicitly requested). Document book package v1 in `docs/book-format.md` **before** writing Rust
I/O so schema and commands stay aligned.

Harness leftovers (`.envrc.example`, agent tooling contract) ship in the same PR stream as the
scaffold so agents and humans share one setup story.

### Alternatives considered

| Option | Why not chosen |
|---|---|
| `apps/desktop` monorepo | Overkill for a single-app MVP; revisit if a web-only package appears |
| Svelte | User OK with React default; avoid dual-framework churn |
| Defer book-format docs until M1 | Schema mistakes are expensive; document first |
| Symlink scans into package by default | Portability; default **copy** (confirm in M1) |

## Proposed file changes

```
package.json, pnpm-lock.yaml     — Vite + React + TS + @tauri-apps/cli/api
src/                             — React shell: App, empty home, routes stub
src-tauri/                       — Tauri 2: Cargo.toml, main.rs, tauri.conf.json, capabilities
index.html, vite.config.ts, tsconfig*.json
docs/book-format.md              — package schema v1 (renderMode, pages, ocr/, annotations)
.envrc.example                   — direnv: PATH hints for node/pnpm/rustc/cargo
AGENTS.md                        — paste agent-tooling contract block
README.md                        — prerequisites + pnpm tauri dev
.github/workflows/ci.yml         — minimal cargo check + (optional) pnpm typecheck if cheap
.gitignore                       — node_modules, dist, target, large fixtures
tests/fixtures/README.md         — how to place tiny sample pages (binaries gitignored if large)
```

## Phases & checklist

### Phase 0 — Harness closeout

- [ ] Add `.envrc.example` (Node, pnpm, Rust toolchain notes); document `direnv allow` in README
- [ ] Paste agent-tooling contract from `policies/agent-tooling-contract.md` into `AGENTS.md`
- [ ] Confirm `.agent-state/` already gitignored
- [ ] Update `scripts/validate-env.sh` / README with Tauri prerequisites checklist

### Phase 1 — Scaffold

- [ ] Create Tauri 2 + Vite + React + TypeScript app (official create flow or equivalent)
- [ ] `pnpm install` succeeds; `pnpm tauri dev` launches a window with placeholder UI
- [ ] Document run/build commands in README
- [ ] Pin Node via `.nvmrc` or `package.json` `engines` (current LTS)

### Phase 2 — Book format v1 (docs + stubs)

- [ ] Write `docs/book-format.md`: directory layout, `meta.json` fields, reserved `ocr/`,
      `annotations.json`, `renderMode` enum (`scan` default; future `text` / `hybrid`)
- [ ] Add empty Rust module(s) or types matching the schema (compile-only; full I/O in M1)
- [ ] Fixture instructions under `tests/fixtures/` (no large binaries in git)

### Phase 3 — CI smoke (minimal)

- [ ] CI: `cargo check` in `src-tauri/` on PR/push
- [ ] CI: `pnpm exec tsc --noEmit` if `tsconfig` exists (or document deferral to M0.5)
- [ ] Do **not** block M0 on full clippy/vitest matrix (roadmap M0.5)

## Verification

- [ ] Fresh clone path: install prereqs → `pnpm install` → `pnpm tauri dev` shows window
- [ ] `docs/book-format.md` reviewed against profile/roadmap (scan-first, OCR reserved)
- [ ] `cargo check` clean; CI green for new jobs
- [ ] `bash scripts/check-bootstrap.sh` findings explained or fixed

## Open questions

- [ ] Exact Tauri 2 create-app flags / template version at implementation time
- [ ] Whether book packages live under OS app-data dir vs user-chosen library root (decide in M1; document preference here)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Tauri/macOS signing noise for local dev | med | low | Document unsigned local-only first |
| Scaffold fights existing root files | med | med | Careful merge of package.json / gitignore |
| Over-building M0.5 into M0 | med | med | Explicit out-of-scope; checklist discipline |

## Completion steps

1. Status → `complete`; move to `plans/archive/completed/`
2. Changelog: user-facing “Tauri app scaffold” in `CHANGELOG.md`; harness bits in `CHANGELOG.dev.md`
3. Unblock M1 plan; update `to_do.md` and roadmap M0 checkboxes
4. Supersede leftover items in [`archive/superseded/2026-08-23-mvp-scaffold.md`](archive/superseded/2026-08-23-mvp-scaffold.md) (already archived)

## Related

- Roadmap: [`2026-08-23-product-roadmap.md`](2026-08-23-product-roadmap.md)
- Next: [`2026-08-23-m1-scan-viewer.md`](2026-08-23-m1-scan-viewer.md)
- Profile: `.context/project-profile.md`
- Prior combined draft: [`archive/superseded/2026-08-23-mvp-scaffold.md`](archive/superseded/2026-08-23-mvp-scaffold.md)
