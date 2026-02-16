"""Deterministic divergence scoring for AOSL."""

from __future__ import annotations

from typing import Mapping

from .config import CONSTRAINTS, DEFAULT_WEIGHT


def _validated_violation(name: str, value: float) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"Violation for {name!r} must be within [0, 1], got {value}.")
    return value


def _validated_weight(name: str, value: float) -> float:
    value = float(value)
    if value < 0.0:
        raise ValueError(f"Weight for {name!r} must be non-negative, got {value}.")
    return value


def compute_divergence(
    scores: Mapping[str, float],
    weights: Mapping[str, float] | None = None,
) -> float:
    """Compute divergence D = Σ(w_i * v_i) over configured constraints.

    Missing scores/weights default to 0.0 and DEFAULT_WEIGHT, respectively.
    """
    weights = weights or {}
    divergence = 0.0

    for constraint in CONSTRAINTS:
        violation = _validated_violation(constraint, scores.get(constraint, 0.0))
        weight = _validated_weight(constraint, weights.get(constraint, DEFAULT_WEIGHT))
        divergence += weight * violation

    return divergence


def assign_tier(divergence: float) -> str:
    """Assign a stability tier from divergence thresholds.

    Default thresholds:
    - S3: D < 0.10
    - S2: 0.10 <= D < 0.25
    - S1: 0.25 <= D < 0.45
    - S0: D >= 0.45
    """
    divergence = float(divergence)

    if divergence < 0.10:
        return "S3"
    if divergence < 0.25:
        return "S2"
    if divergence < 0.45:
        return "S1"
    return "S0"
