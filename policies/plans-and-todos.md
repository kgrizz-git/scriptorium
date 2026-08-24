# Policy: Plans, TODOs, Archiving, and Completion

Last reviewed: 2026-08-23
Enforced by: convention + [`hooks/scripts/check_todo_limits.py`](../hooks/scripts/check_todo_limits.py)
+ [`hooks/scripts/check_todo_plan_sync.py`](../hooks/scripts/check_todo_plan_sync.py)
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

The root backlog is an **index + queue**, not a second copy of plan checklists.

### Sections (required shape)

| Section | Purpose | Rules |
|---|---|---|
| **`## Next Up`** | Default agent work queue | **3–5** pointer lines only; each links to a `plans/` file (or is labeled **unplanned**). No full checklists. |
| **`## Active plans`** | One row per active plan | Every `plans/*.md` except `README.md` and `orchestration-state.md` gets exactly one entry. Roadmap may live here as “living” horizon. |
| **`## Unplanned / small`** | Rare one-session work | Empty is fine. Graduate to a plan if work exceeds ~one session. |
| **`## Icebox`** | Deferred / someday | Pointers only. Prefer `plans/deferred/` for real designs. Soft cap **~20** lines. |

**Next Up ⊆ Active** in spirit: Next Up is the ordered subset agents should execute; do not
maintain a parallel task universe in the roadmap or plan bodies.

### Agent rules

1. **Start at Next Up.** If empty, stale, or contradictory, stop and fix `to_do.md` or ask the
   user — do not invent work from the roadmap alone.
2. **Creating a plan** → add an **Active plans** row and, when ready to execute, a **Next Up**
   pointer in the same change.
3. **Completing / deferring / superseding a plan** → remove or update its Next Up and Active
   entries in the same change; move the plan file per lifecycle above; link deferred work from
   **Icebox** or `plans/deferred/`. Do not retain completed work in `to_do.md` as history.
4. **Detail lives in plans.** Do not duplicate plan phase checklists into `to_do.md`.
5. **Plan reviews** stay in gitignored `tmp/` — never link them from `to_do.md`.

### Size and hygiene

- Keep it short: prioritized pointers, not a novel.
- Soft line cap: **150** (warn). Hard cap: **300** (block) — see hook env vars.
- Delete done items from `to_do.md` after their completion is logged. Log every meaningful
  completion once; an archived plan, issue, or commit alone is sufficient only for a truly
  trivial edit.
- Stale `TODO`/`FIXME` in **source** are audited via [`prompts/todo-plan-audit.md`](../prompts/todo-plan-audit.md)
  and [`policies/garbage-collection.md`](garbage-collection.md) — not the line-cap hook.

### Automated sync (advisory)

[`hooks/scripts/check_todo_plan_sync.py`](../hooks/scripts/check_todo_plan_sync.py) warns when:

- Next Up count is outside **3–5** (when the section exists and active plans remain)
- An active plan file is not linked from `to_do.md`
- `to_do.md` links to a missing plan path
- Archived/deferred plans appear in Next Up or Active
- A Next Up line has no `plans/` link (unless labeled unplanned)
- Icebox exceeds the soft cap

Runs in CI (advisory). Optional locally via pre-commit.

## TODO completion workflow

When marking a TODO item complete:

1. **Remove it from `to_do.md`**. The file is an actionable queue, not a completion log.
2. **Log every meaningful completion once** based on work type:
   - **User-visible changes** → Add to `CHANGELOG.md` (public)
   - **Internal/harness changes** → Add to `CHANGELOG.dev.md`
   - **Maintenance/cleanup** → Add to `MAINTENANCE.md` (create if needed)
   - Skip logging only for a truly trivial edit (for example, a typo or formatting-only change);
     the plan, issue, or commit is then sufficient.
3. **Reference the source** - link to plan, issue, or commit when a changelog or maintenance
   entry is created.
4. **Archive related artifacts** - archive a completed plan; delete stale `.context/` scratch
   notes or promote valuable findings to durable documentation.

### Completion logging decision tree

```
User-visible impact?
├─ Yes → CHANGELOG.md + VERSION bump if appropriate
└─ No → Maintenance/security work?
    ├─ Yes → MAINTENANCE.md
    └─ No → Meaningful internal, documentation, planning, or harness work?
        ├─ Yes → CHANGELOG.dev.md
        └─ No → Truly trivial edit → plan, issue, or commit only
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
