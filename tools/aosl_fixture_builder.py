#!/usr/bin/env python3
"""
AOSL Fixture Builder (v1)

Purpose:
- Generate canonical fixture files from a single JSON spec.
- No git commands required; safe to run in GitHub Codespaces.
- Deterministic output paths and formats for reproducibility.

Usage:
  python tools/aosl_fixture_builder.py fixtures/aosl/v1/specs/p0002.json

Spec format (JSON):
{
  "prompt_id": "p0002",
  "category": "Constraint Compliance",
  "difficulty": "Low",
  "purpose": "...",
  "prompt": "...",
  "expected_stability_signal": ["...", "..."],
  "notes": ["..."],
  "outputs": {
    "good": "markdown text...",
    "bad": "markdown text..."
  },
  "violations": {
    "good": {
      "constraints": [
        { "id": "C1_...", "description": "...", "weight": 0.2, "violation": 0.0, "evidence": "..." }
      ],
      "notes": "..."
    },
    "bad": {
      "constraints": [
        { "id": "C1_...", "description": "...", "weight": 0.2, "violation": 1.0, "evidence": "..." }
      ],
      "notes": "..."
    }
  }
}
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


DATASET_ROOT = os.path.join("fixtures", "aosl", "v1")


@dataclass(frozen=True)
class Tier:
    tier: str
    label: str
    min_inclusive: float
    max_exclusive: float | None
    max_inclusive: float | None


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content.rstrip() + "\n")


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _load_baseline_tiers() -> List[Tier]:
    baseline_path = os.path.join(DATASET_ROOT, "meta", "baseline_threshold.json")
    baseline = _read_json(baseline_path)

    tiers: List[Tier] = []
    for t in baseline.get("tiers", []):
        tiers.append(
            Tier(
                tier=str(t["tier"]),
                label=str(t.get("label", "")),
                min_inclusive=float(t["min_inclusive"]),
                max_exclusive=float(t["max_exclusive"]) if "max_exclusive" in t else None,
                max_inclusive=float(t["max_inclusive"]) if "max_inclusive" in t else None,
            )
        )
    if not tiers:
        raise ValueError(f"No tiers found in {baseline_path}")
    return tiers


def _tier_for_divergence(d: float, tiers: List[Tier]) -> str:
    # d is assumed normalized to [0,1]
    for t in tiers:
        if d < t.min_inclusive:
            continue
        if t.max_exclusive is not None and d < t.max_exclusive:
            return t.tier
        if t.max_inclusive is not None and d <= t.max_inclusive:
            return t.tier
    # If none matched due to edge cases, return the highest tier
    return tiers[-1].tier


def _compute_divergence(constraints: List[Dict[str, Any]]) -> float:
    # D = Σ(w_i * v_i)
    d = 0.0
    for c in constraints:
        w = float(c["weight"])
        v = float(c["violation"])
        d += w * v
    # Clamp to [0,1] defensively
    if d < 0.0:
        d = 0.0
    if d > 1.0:
        d = 1.0
    # Round to 3 decimals for stable diffs
    return round(d, 3)


def _render_prompt_md(spec: Dict[str, Any]) -> str:
    pid = spec["prompt_id"]
    category = spec.get("category", "")
    difficulty = spec.get("difficulty", "")
    purpose = spec.get("purpose", "")
    prompt = spec.get("prompt", "")
    expected = spec.get("expected_stability_signal", [])
    notes = spec.get("notes", [])

    expected_md = "\n".join([f"- {line}" for line in expected]) if expected else "- (none)"
    notes_md = "\n".join([f"- {line}" for line in notes]) if notes else "- (none)"

    return f"""# Prompt ID: {pid}

## Category
{category}

## Difficulty
{difficulty}

## Purpose
{purpose}

## Prompt
{prompt}

## Expected Stability Signal
{expected_md}

## Notes
{notes_md}
"""


def _validate_spec_minimum(spec: Dict[str, Any]) -> None:
    required_top = ["prompt_id", "prompt", "outputs", "violations"]
    for k in required_top:
        if k not in spec:
            raise ValueError(f"Spec missing required key: {k}")

    pid = spec["prompt_id"]
    if not isinstance(pid, str) or not pid.startswith("p") or len(pid) != 5:
        raise ValueError("prompt_id must look like 'p0002' (5 chars)")

    if "good" not in spec["outputs"] or "bad" not in spec["outputs"]:
        raise ValueError("outputs must include 'good' and 'bad'")

    if "good" not in spec["violations"] or "bad" not in spec["violations"]:
        raise ValueError("violations must include 'good' and 'bad'")

    for variant in ["good", "bad"]:
        v = spec["violations"][variant]
        if "constraints" not in v or not isinstance(v["constraints"], list) or len(v["constraints"]) == 0:
            raise ValueError(f"violations.{variant}.constraints must be a non-empty list")

        # Lightweight checks for each constraint
        for c in v["constraints"]:
            for ck in ["id", "description", "weight", "violation", "evidence"]:
                if ck not in c:
                    raise ValueError(f"Constraint missing '{ck}' in {variant}")
            w = float(c["weight"])
            viol = float(c["violation"])
            if w < 0 or w > 1:
                raise ValueError(f"Constraint weight out of range [0,1] in {variant}: {c['id']}")
            if viol < 0 or viol > 1:
                raise ValueError(f"Constraint violation out of range [0,1] in {variant}: {c['id']}")

        # We allow weights to sum to ~1.0 but do not require exact.
        # (You may choose later to enforce strict normalization.)
    return


def build_from_spec(spec_path: str) -> List[str]:
    spec = _read_json(spec_path)
    _validate_spec_minimum(spec)

    pid = spec["prompt_id"]
    tiers = _load_baseline_tiers()

    # Paths
    prompt_md_path = os.path.join(DATASET_ROOT, "prompts", pid, "prompt.md")
    out_good_path = os.path.join(DATASET_ROOT, "outputs", pid, "good.md")
    out_bad_path = os.path.join(DATASET_ROOT, "outputs", pid, "bad.md")
    vio_good_path = os.path.join(DATASET_ROOT, "violations", pid, "good.json")
    vio_bad_path = os.path.join(DATASET_ROOT, "violations", pid, "bad.json")

    # Write prompt + outputs
    _write_text(prompt_md_path, _render_prompt_md(spec))
    _write_text(out_good_path, str(spec["outputs"]["good"]))
    _write_text(out_bad_path, str(spec["outputs"]["bad"]))

    # Write violations with computed divergence + tier
    written: List[str] = [prompt_md_path, out_good_path, out_bad_path]

    for variant, vio_path in [("good", vio_good_path), ("bad", vio_bad_path)]:
        constraints = spec["violations"][variant]["constraints"]
        divergence_value = _compute_divergence(constraints)
        tier = _tier_for_divergence(divergence_value, tiers)

        vio_obj = {
            "prompt_id": pid,
            "variant": variant,
            "schema_version": "aosl_violatio
