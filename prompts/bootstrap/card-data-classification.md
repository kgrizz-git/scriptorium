# Card: Data Classification (P0)

Gates everything else. Run it in Phase 0, before any scaffolding, and never infer the answer.

## Ask

1. What data can enter this repository — including fixtures, screenshots, logs, exports, and
   CI artifacts? (Ask about all five explicitly; people answer "just code" and then commit a
   debug log.)
2. Will it ever hold real customer data, credentials, financial records, or other
   business-confidential material?
3. If not: is that a rule (synthetic fixtures only) or just the current state?
4. Who is the named human owner for security exceptions and approvals?
5. Will the repo be public, private-but-shared, or private-solo?

## Branch

| Answer | Classification | Action |
|---|---|---|
| Code only, synthetic fixtures, rule is explicit | `public` / `internal` | Standard tier. Baseline pre-commit (gitleaks, private-key, file-size). Continue to P1. |
| No real data today, but no rule against it | `internal` → treat as `confidential` | Write the rule into `AGENTS.md` now, then standard tier plus explicit `.gitignore` for exports/logs. |
| Customer data, credentials, or business-confidential | `confidential` | Full GitHub hygiene tier: required secret scan, branch ruleset, `CODEOWNERS` on workflow/policy files, least-privilege Apps. See [`policies/github-repository-hygiene.md`](../../policies/github-repository-hygiene.md). |

When the answer is ambiguous, pick the **more protective** tier and say so. Downgrading later is
cheap; a leak in git history is not.

## Produce

- `Data classification` and `Repository data rule` filled in `.context/project-profile.md`.
- The named approval owner recorded in the profile (for confidential repos).

## Done when

- The profile's data fields are non-`TBD`.
- The classification is stated back to the user and they confirmed it.
- For `confidential`: required secret-scan CI job name is recorded for P3/P4, and sensitive
  workflow/policy paths have `CODEOWNERS` coverage.
