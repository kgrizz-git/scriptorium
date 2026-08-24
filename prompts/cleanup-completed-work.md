# Cleanup Completed Work

Run this when completing significant work or at session end to ensure proper logging and archival.

## Checklist

### TODO cleanup
- [ ] Remove completed items from **Next Up** and **Active plans** in `to_do.md`
- [ ] Verify no completed `[x]` items remain in `to_do.md`; it is an active queue, not history

### Completion logging
- [ ] Log every meaningful completion once: `CHANGELOG.md` (user-visible, incl. caller-facing
  security), `CHANGELOG.dev.md` (internal/harness/CI tooling, planning, or documentation), or
  `MAINTENANCE.md` (operational maintenance only — not product security releases)
- [ ] Use plan/issue/commit only for a truly trivial edit (such as a typo or formatting-only
  change)
- [ ] Reference the source (plan, issue, or commit) for each log entry

### Plan archival
- [ ] Move completed plans to `plans/archive/completed/` (superseded → `archive/superseded/`; deferred → `plans/deferred/`)
- [ ] Update plan status to `complete` or `abandoned`
- [ ] Update `orchestration-state.md` if present
- [ ] Verify no active plans remain in main `plans/` directory

### Scratch file cleanup
- [ ] Review `.context/` directory for old scratch files
- [ ] Delete scratch files older than 7 days (unless explicitly needed)
- [ ] Archive valuable research notes to appropriate docs location

### Source code cleanup
- [ ] Check for resolved TODOs/FIXMEs in source code
- [ ] Remove or update resolved markers
- [ ] Verify no orphaned TODO comments remain

### Verification
- [ ] Run `python hooks/scripts/check_todo_limits.py` to verify cleanup
- [ ] Run `python hooks/scripts/check_todo_plan_sync.py` (advisory) for Next Up / Active drift
- [ ] Run `python hooks/scripts/check_file_size.py` to check for bloat
- [ ] Verify git status shows only intended changes

## Logging decision tree

Use this tree to decide where to log completed work:

```
User-visible impact? (features, UX, caller-facing security)
├─ Yes → CHANGELOG.md + VERSION bump if appropriate
└─ No → Operational maintenance? (infra, non-release rotations, ops hygiene)
    ├─ Yes → MAINTENANCE.md
    └─ No → Meaningful internal, documentation, planning, or harness work?
        ├─ Yes → CHANGELOG.dev.md
        └─ No → Truly trivial edit → plan, issue, or commit only
```

### Examples

**User-visible feature:** "Added user authentication" → `CHANGELOG.md`
**Caller-facing security fix:** "Patched session fixation in login" → `CHANGELOG.md` (`### Security`)
**CI/SAST harness:** "Pinned Actions SHAs; Semgrep exclude scaffolds" → `CHANGELOG.dev.md`
**Internal tooling:** "Updated pre-commit hooks" → `CHANGELOG.dev.md`
**Operational security maintenance:** "Rotated staging API keys (no product release)" → `MAINTENANCE.md`
**Documentation:** "Updated API docs" → `CHANGELOG.dev.md`
**Bug fix:** "Fixed login redirect loop" → `CHANGELOG.md`

## Before declaring cleanup complete

- [ ] Every meaningful completion is logged once in the appropriate durable log
- [ ] No orphaned TODO items remain
- [ ] Plans are archived with correct status
- [ ] Scratch files are cleaned up
- [ ] Git status is clean (except for intended changes)
- [ ] Relevant policy checks pass

## Commit message guidance

When committing cleanup, use a descriptive message:

```
Cleanup: Log and archive completed work

- Logged [X] completions in CHANGELOG.md/dev.md
- Archived [Y] completed plans to plans/archive/completed/
- Cleaned up .context/ scratch files
- Removed resolved TODOs from source
```

This creates a clear audit trail and prevents accumulation of completed work artifacts.
