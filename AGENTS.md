# AOSL — Codex Operating Instructions

## Role
Implement the AI Output Stability Layer (AOSL) as defined by the Appearance Stability Framework (ASF).

## Core definition
Divergence D = Σ(w_i * v_i), where each constraint violation v_i ∈ [0,1].

## Non-negotiables
- Deterministic scoring.
- Lightweight Python.
- Tests required.
- No changing definitions without instruction.

## Deliverables
- Constraint engine
- Scoring
- CLI
- Reports
- Dataset support
## Commands
- Run tests: pytest
- Lint: (none yet)

## Repo goals (current)
- Implement deterministic AOSL scoring + tiers
- Add pytest + CI
- Keep dependencies minimal
## Development priorities (current phase)

1. Deterministic constraint evaluation (C1–C4 first).
2. Automation of scoring pipeline.
3. Expansion of benchmark dataset.
4. Maintain reproducibility and clarity.
