# Plans

Last reviewed: 2026-08-23

Optional folder for implementation plans. Adopt when the project uses plan-driven or
multi-agent work. Conventions: [`policies/plans-and-todos.md`](../policies/plans-and-todos.md).
Templates: [`templates/plan.md`](../templates/plan.md),
[`templates/orchestration-state.md`](../templates/orchestration-state.md).

**Scriptorium:** product roadmap [`2026-08-23-product-roadmap.md`](2026-08-23-product-roadmap.md);
active MVP [`2026-08-23-mvp-scaffold.md`](2026-08-23-mvp-scaffold.md); living index [`to_do.md`](../to_do.md).

## Layout

| Path | Purpose |
|---|---|
| `*.md` | Active feature/task plans (prefer `YYYY-MM-DD-slug.md`) |
| `orchestration-state.md` | Optional hub-and-spoke run state (orchestrator-owned) |
| `archive/` | Completed or abandoned plans (do not delete; move here) |

## Completion

1. Set plan `Status:` to `complete` or `abandoned`.
2. Mark checklist items `[x]` only when verified.
3. Move the file into `archive/`.
4. Clear or update `orchestration-state.md` if present.
