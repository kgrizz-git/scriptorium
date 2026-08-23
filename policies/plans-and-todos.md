# Policy: Plans, TODOs, Archiving, and Completion

Last reviewed: 2026-08-23
Enforced by: convention + [`hooks/scripts/check_todo_limits.py`](../hooks/scripts/check_todo_limits.py)
+ [`prompts/todo-plan-audit.md`](../prompts/todo-plan-audit.md).

## Why

Agents and humans need a single place for “what’s next,” durable plans for non-trivial
work, and a clear done/archive path so the repo does not accumulate zombie checklists.

## Folders and files

| Path | Purpose |
|---|---|
| `plans/` | **Active** implementation plans (`YYYY-MM-DD-slug.md`) and the living roadmap. Optional `orchestration-state.md`. |
| `plans/deferred/` | Intentionally postponed plans (still discoverable; link from `to_do.md`). |
| `plans/archive/completed/` | Finished plans (`Status: complete`). |
| `plans/archive/superseded/` | Replaced or abandoned plans (`Status: abandoned`). |
| `to_do.md` or `TODO.md` (repo root) | Short living backlog — not a substitute for issues on large teams. |
| `assessments/` | Timestamped **durable** reviews (security, QI) when explicitly kept in-repo — do not rewrite in place. |
| `tmp/` (gitignored) | Scratch, spikes, and **plan reviews** by default. Do not commit; do not link from tracked docs. See [`tmp/README.md`](../tmp/README.md). |
| `.context/` | Scratch only (gitignored). Never the source of truth for plans. |

Use [`templates/plan.md`](../templates/plan.md) for new plans. Prefer GitHub/Linear issues
for cross-team tracking; keep `to_do.md` for agent-visible, in-repo backlog when that
helps the harness. Layout summary: [`plans/README.md`](../plans/README.md).

## Plan lifecycle

1. **draft** — written, not approved.
2. **approved** / **in-progress** — checklist drives work; mark `[x]` only when the item
   is fully done and verified (do not mark complete to “get past” a gate).
3. **complete** — all required checklist items done; verification section satisfied;
   status set to `complete`; **move to `plans/archive/completed/`**.
4. **abandoned** — explicitly stopped; note why; **move to `plans/archive/superseded/`**.
5. **deferred** — postponed on purpose; note why + target milestone if known;
   **move to `plans/deferred/`** (or keep in place only if still under active negotiation —
   prefer the folder so `plans/` stays executable).

### Marking plans done

- Update `Status:` in the plan header to `complete`, `abandoned`, or `deferred`.
- Move the file to the matching folder above. Do **not** delete archived or deferred plans.
- If `plans/orchestration-state.md` exists, set phase to `complete` / `blocked` and point
  “next action” at none / user.
- When superseding, leave a one-line pointer to the successor in the old plan’s header.

### Checklist honesty

- Mark `[ ]` → `[x]` only after the stated task is done **and** confirmed (tests, review,
  or explicit acceptance).
- If blocked, leave unchecked and add a comment under the item explaining the blocker —
  do not change the goal to something easier.

## Living `to_do` / `TODO` file

- Keep it short: prioritized bullets or a tiny table, not a novel.
- Soft line cap: **150** (warn). Hard cap: **300** (block) — see hook env vars.
- Each item should be actionable; link to a `plans/` file or issue when the work is large.
- Prune done items into a short "Recently done" section (max ~10) or delete them after
  they land in the changelog / git history.
- Stale `TODO`/`FIXME` in **source** are audited via [`prompts/todo-plan-audit.md`](../prompts/todo-plan-audit.md)
  and [`policies/garbage-collection.md`](garbage-collection.md) — not the line-cap hook.

## TODO completion workflow

When marking a TODO item complete:

1. **Remove it from `to_do.md`** (or move to "Recently done" section, max 10 items)
2. **Log the completion** based on work type:
   - **User-visible changes** → Add to `CHANGELOG.md` (public)
   - **Internal/harness changes** → Add to `CHANGELOG.dev.md`
   - **Maintenance/cleanup** → Add to `MAINTENANCE.md` (create if needed)
3. **Reference the source** - link to plan, issue, or commit that completed it
4. **Archive related artifacts** - move scratch notes from `.context/` to deletion

### Completion logging decision tree

```
User-visible impact?
├─ Yes → CHANGELOG.md + VERSION bump if appropriate
└─ No → Internal-only?
    ├─ Yes → CHANGELOG.dev.md
    └─ No → Maintenance/security?
        ├─ Yes → MAINTENANCE.md
        └─ No → Document only → No changelog needed
```

Use [`prompts/cleanup-completed-work.md`](../prompts/cleanup-completed-work.md) for systematic cleanup.

## File size relationship

Active plans and `to_do` files are documentation; they still respect doc soft caps in
[`file-size-and-counts.md`](file-size-and-counts.md). Prefer splitting a huge plan into
phased linked plans over one 2k-line checklist.

## Notes_and_Ideas vs this template

Personal research dumps, private API key bookmarks, and exploratory idea notes belong in
a Notes_and_Ideas (or similar) repo. This template keeps **durable, reusable** conventions
and inventory menus only.
