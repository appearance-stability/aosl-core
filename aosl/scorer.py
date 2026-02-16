from typing import Dict, List
from .config import CONSTRAINTS


def compute_divergence(scores: Dict[str, float]) -> float:
    """Compute divergence as mean of constraint violations."""
    values = [scores.get(c, 0.0) for c in CONSTRAINTS]
    return sum(values) / len(CONSTRAINTS)


def assign_tier(D: float) -> str:
    if D < 0.10:
        return "S3"
    elif D < 0.25:
        return "S2"
    elif D < 0.45:
        return "S1"
    return "S0"
