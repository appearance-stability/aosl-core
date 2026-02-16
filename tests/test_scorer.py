import pytest

from aosl.scorer import assign_tier, compute_divergence


def test_compute_divergence_uses_weighted_sum_with_defaults():
    scores = {
        "C1_format": 0.5,
        "C2_instruction": 1.0,
    }

    # Ten constraints total; missing constraints default to 0.0 violation.
    assert compute_divergence(scores) == pytest.approx(1.5)


def test_compute_divergence_supports_custom_weights():
    scores = {
        "C1_format": 0.5,
        "C2_instruction": 1.0,
    }
    weights = {
        "C1_format": 2.0,
        "C2_instruction": 0.5,
    }

    assert compute_divergence(scores, weights) == pytest.approx(1.5)


def test_compute_divergence_rejects_out_of_range_violations():
    with pytest.raises(ValueError, match=r"within \[0, 1\]"):
        compute_divergence({"C1_format": 1.2})


def test_assign_tier_thresholds():
    assert assign_tier(0.09) == "S3"
    assert assign_tier(0.10) == "S2"
    assert assign_tier(0.25) == "S1"
    assert assign_tier(0.45) == "S0"
