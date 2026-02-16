# AOSL Pilot Results v1

## Objective
To test whether fluent but structurally unstable AI outputs can be detected using the AI Output Stability Layer (AOSL).

## Setup
- Prompts: 5
- Variants: Good vs Bad Fluent
- Constraints: C1–C10
- Scoring: Manual calibration

## Results

Mean D (Good): 0.00  
Mean D (Bad Fluent): 0.126  

Separation: 0.126

## Interpretation
The pilot demonstrates that structurally unstable outputs can be detected using constraint-based divergence scoring.

Even when outputs appear fluent, violations of format, instruction compliance, and logical integrity produce measurable divergence.

## Observations
Strongest signals:
- Format compliance (C1)
- Instruction adherence (C2)

Weaker signals:
- Logical continuity
- Quantifier discipline

## Conclusion
These results support the hypothesis that latent instability in generative AI outputs is measurable.

Further work will:
- Expand dataset
- Refine constraints
- Improve separation
- Automate scoring
