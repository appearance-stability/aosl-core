from aosl.scorer import compute_divergence, assign_tier


def test_divergence():
    scores = {
        "C1_format": 1.0,
        "C2_instruction": 0.0,
    }
    D = compute_divergence(scores)
    assert D > 0


def test_tier():
    assert assign_tier(0.05) == "S3"
    assert assign_tier(0.20) == "S2"
