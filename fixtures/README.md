# AOSL Fixtures

This directory contains calibration fixtures for AOSL.

## Structure
- `cases/<case_id>/`
  - `prompt.md` – the test prompt
  - `good.md` / `bad.md` – example outputs
  - `score_good.json` / `score_bad.json` – violation vectors (0–1) for constraints C1–C10

## Scoring
Violation vectors map constraint IDs to values in [0,1].
Example:
```json
{ "C1": 0.0, "C2": 0.25, "...": 0.0 }
