# Maintenance Log

Last reviewed: 2026-08-24

Copy to repo-root `MAINTENANCE.md` when needed. Tracks **operational** maintenance only
(infra upkeep, non-release rotations, recurring ops hygiene). Completion logging rules:
[`../policies/changelog-conventions.md`](../policies/changelog-conventions.md).

Do not put secrets, tokens, or private URLs here.

## [YYYY-MM-DD] - Session Type

### Completed
- [task description] - [impact/context] (ref: [plan/commit/issue])
- [task description] - [impact/context] (ref: [plan/commit/issue])

### Deferred
- [task description] - [reason for deferral] (filed as [issue/TODO])
- [task description] - [reason for deferral] (filed as [issue/TODO])

### Issues Found
- [issue description] - [severity] - [planned action/timeline]
- [issue description] - [severity] - [planned action/timeline]

### Operational security
- [non-release rotation, cert renewal, access audit, etc.] - [context] (ref: [commit/issue])
- [task] - [context] (ref: [commit/issue])

### Infrastructure/Tools
- [infrastructure change] - [impact] (ref: [commit/issue])
- [tool update] - [version] - [reason]

### Next Scheduled
- [date] - [focus areas/planned work]
- [date] - [focus areas/planned work]

---

## Usage Guidelines

Log each meaningful completion **once**. Public impact first.

### When to use this log (`MAINTENANCE.md`)
- Infra upkeep and environment/ops changes with no product release
- Non-release secret/cert rotation or access hygiene (no secret values in the log)
- Backup/restore testing and verification
- Compliance/audit ops tasks and recurring process hygiene
- Performance tuning that is ops-only (not a user-visible product change)

### When to use `CHANGELOG.dev.md` instead
- Agent harness, prompts, policies, or skills
- CI/CD workflows, hooks, SAST/secret-scan tooling (e.g. Semgrep, Action SHA pins)
- Documentation-only changes
- Test coverage improvements
- Code refactoring with no user impact

### When to use `CHANGELOG.md` instead
- User-visible features and changes
- Bug fixes that affect users
- Caller-facing security fixes or product security posture (`### Security`)
- Breaking changes or migration requirements
- Performance improvements users notice

### Entry format
Keep entries concise and actionable. Include:
- What was done
- Why it matters
- Reference to related commits, issues, or plans
- Any follow-up needed

### Rotation
Archive old entries to `docs/maintenance-archive/` or similar when this file grows beyond 200 lines. Keep at least the last 6 months of activity readily accessible.
