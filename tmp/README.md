# tmp/

Scratch space for local runs, spikes, and agent-generated artifacts.

- Contents are **gitignored** (`tmp/*`); only this README is tracked.
- **Plan reviews** (advisor / TL critiques of `plans/*`) go here by default — e.g.
  `tmp/YYYY-MM-DD-*-plan-review.md`. Do **not** commit them and do **not** link to them
  from tracked docs (`AGENTS.md`, roadmap, `to_do.md`, etc.). Fold durable outcomes into
  the plans themselves or into ADRs.
- Do not put secrets or large scan corpora here long-term — use book packages outside the repo when possible.
- Safe to delete everything under `tmp/` at any time.
