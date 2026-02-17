# AOSL Fixtures (v1)

This directory contains a **reproducible evaluation dataset** for AOSL (AI Output Stability Layer).

## Structure

- `meta/`
  - Dataset-wide configuration such as baseline thresholds.
- `prompts/`
  - Calibration prompts (human-readable, stable identifiers).
- `outputs/`
  - Canonical "good" and "bad-but-fluent" model outputs for each prompt.
- `violations/`
  - JSON scoring files that record constraint violations for each output artifact.

## Naming Rules (strict)
- Prompt IDs are fixed strings: `p0001`, `p0002`, ...
- Each prompt lives in: `prompts/<prompt_id>/prompt.md`
- Each output lives in: `outputs/<prompt_id>/<variant>.md` where `<variant>` is `good` or `bad`
- Each scoring file lives in: `violations/<prompt_id>/<variant>.json`

This dataset is designed to validate whether **latent instability** exists and is detectable via AOSL scoring.
