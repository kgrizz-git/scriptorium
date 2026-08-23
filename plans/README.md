# Plans

Last reviewed: 2026-08-23

Implementation plans for plan-driven / multi-agent work. Policy:
[`policies/plans-and-todos.md`](../policies/plans-and-todos.md). Template:
[`templates/plan.md`](../templates/plan.md).

## Layout

| Path | Purpose |
|---|---|
| `*.md` (this directory) | **Active** plans and the living product roadmap |
| `orchestration-state.md` | Optional hub-and-spoke run state (orchestrator-owned) |
| `deferred/` | Plans intentionally postponed; still discoverable, not in progress |
| `archive/completed/` | Finished plans (`Status: complete`) — keep for history |
| `archive/superseded/` | Replaced or abandoned plans (`Status: abandoned` / superseded) |

Do **not** delete archived plans. Move them; do not rewrite history in place.

## Scriptorium active set

| Plan | Role |
|---|---|
| [`2026-08-23-product-roadmap.md`](2026-08-23-product-roadmap.md) | Product roadmap M0–M8 (stays active) |
| [`2026-08-23-m0-tauri-foundation.md`](2026-08-23-m0-tauri-foundation.md) | Tauri shell + book schema |
| [`2026-08-23-m1-scan-viewer.md`](2026-08-23-m1-scan-viewer.md) | First product milestone (depends on M0; pending review fixes) |

Superseded: [`archive/superseded/2026-08-23-mvp-scaffold.md`](archive/superseded/2026-08-23-mvp-scaffold.md).
Backlog index: [`to_do.md`](../to_do.md).

## Lifecycle (agents)

1. New work → `plans/YYYY-MM-DD-slug.md` with `Status: draft`.
2. On approval → `approved` / `in-progress`.
3. On finish → `complete`, move to `archive/completed/`.
4. On replace/stop → `abandoned` (note why), move to `archive/superseded/`.
5. On postpone → `deferred` (or keep Status and move to `deferred/`), link from `to_do.md`.

Mark checklist items `[x]` only when verified. See policy for TODO/changelog cleanup.
