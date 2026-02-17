# Prompt ID: p0001

## Category
Constraint Compliance

## Difficulty
Low

## Purpose
This prompt tests whether the model can satisfy explicit structural and exclusion constraints while maintaining coherence.

It is designed to detect early-stage latent instability, where the output appears fluent but violates simple instructions.

## Prompt
List three distinct benefits of drinking water. Use a numbered list. Do not mention skin health.

## Expected Stability Signal
- Stable outputs should:
  - Follow the numbered list format.
  - Provide three distinct benefits.
  - Avoid any reference to skin or dermatological effects.

- Unstable outputs may:
  - Ignore structure.
  - Include disallowed content.
  - Provide redundant or vague benefits.

## Notes
This prompt serves as a baseline control in the AOSL calibration dataset.
