# AOSL Constraints (v1)

The following constraints define structural coherence in AI outputs.

Each constraint produces a violation score v_i ∈ [0,1].

---

## C1 — Format Compliance
The output follows the requested format (e.g., numbered list, JSON, headings).

## C2 — Direct Instruction Compliance
The output obeys explicit prohibitions and requirements in the prompt.

## C3 — Internal Consistency
No contradictions or mutually incompatible claims within the output.

## C4 — Completeness
All requested items or components are present.

## C5 — Traceable Mapping
Claims and references connect logically to earlier statements or prompt context.

## C6 — Logical Continuity
Reasoning steps follow without unexplained jumps.

## C7 — Stable Definitions
Key terms maintain consistent meaning.

## C8 — Quantifier Discipline
Numerical and proportional claims remain consistent.

## C9 — Dependency Awareness
External facts or assumptions are clearly flagged.

## C10 — Epistemic Integrity
Uncertainty is acknowledged when appropriate.
