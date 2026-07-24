# INTERANNOTATOR_FINDINGS — the hedge-collision conclusion survives independent blinded annotation

Synthesis of the blinded multi-annotator gold-commitment study. Full
tables: analysis/gold_commitment_interannotator_agreement.md,
analysis/noncommit_error_decomposition_multiannotator.md. Reanalysis only;
external annotations produced by the user running Codex and Antigravity on
the blinded sheet (I did not fabricate them).

## Annotators

- **codex** and **antigravity**: the two genuinely blinded, independent
  external raters — 100% coverage, 0 validation violations. These are the
  scientifically meaningful annotators (they never saw the schema's label
  or my classification).
- **fable**: the analyst's own non-blinded self-audit (≈ schema); included
  for continuity, flagged as non-independent.
- **human**: partial (38/139, 27%) — below the 50% active threshold, used
  only as a low-power pairwise cross-check.

## Agreement — moderate on the label, by design

- **Independent blinded pair (codex vs antigravity): commitment agreement
  86.3%, Cohen's κ = 0.590.** Exact answer-label agreement 91.4%.
- **Fleiss' κ across the three active annotators = 0.531** (moderate).
- fable vs antigravity κ = 0.683; fable vs codex κ = 0.271 (codex diverges
  from the schema most). Human (n=38): κ = 1.00 vs fable, 0.834 vs
  antigravity, 0.271 vs codex.

Commitment is a genuinely borderline judgement at the margins, so moderate
(not near-perfect) κ is expected and honest. The important finding is that
the *downstream conclusion is insensitive to this subjectivity*.

## The two blinded raters disagree in OPPOSITE lane-directions

The 30 disagreement rows have a clean structure:

- **Codex reads F/FT "mixed" (two-dimension / two-timeframe) golds as
  committed** — F1, F6, F7, FT1, FT9, FT17, FT22, FT25, FT30, FT42, FT44,
  FT49, FT50, T7 (~14 cases). It treats "profitable-as-investment /
  not-as-business" style golds as picking a primary direction.
- **Antigravity reads T-lane screening golds as non-committed** — T4, T6,
  T11, T12, T20, T23, T37, T40, T42, T48 (~10 cases). It treats
  "which stocks show X" (a top-1 with a runner-up set) as a non-committal
  set answer, plus the hedge-adjacent committed golds (F16, FT3, FT5,
  FT35, FT10).

These are *opposite* stances (Codex stricter on F/FT hedges, Antigravity
stricter on T screenings), which is the ideal stress test: the conclusion
is squeezed from both sides at once.

## The conclusion survives every version

| version | hedge_collision share | committed-cell AUROC | survives |
|---|---|---|---|
| A schema | 0.617 | 0.421 | YES |
| B fable | 0.617 | 0.421 | YES |
| C codex | 0.618 | 0.457 | YES |
| D antigravity | 0.550 | 0.424 | YES |
| E majority vote | 0.574 | 0.429 | YES |
| F blinded consensus (codex∧antigravity agree, else schema) | 0.574 | 0.429 | YES |

Under all six commitment definitions:
1. **Hedge collision stays the single largest error mode** (55–62% of
   errors), never dislodged.
2. **p_noncommit stays a hedge-collision detector with no wrong-direction
   signal** — committed∧committed-pred-cell AUROC 0.42–0.46, i.e. ≈chance
   under every annotator.

## Plain-English verdict

**Yes — the hedge-collision conclusion survives independent blinded
annotation, majority vote, and strict blinded consensus.** Two independent
raters who never saw the schema, disagreeing with it and each other on 30
of 139 commitment calls (in opposite lane-directions, κ≈0.53–0.59), still
produce the same finding: the errors of these financial debate systems are
dominated by hedge collisions, and `p_noncommit` detects them without
carrying any wrong-direction signal. The conclusion depends only on the
coarse structure (F/FT hedge, T pick-wrong-ticker), not on the contestable
individual commitment labels — which is exactly the robustness a reviewer
would demand. The remaining honest caveat is that commitment agreement is
moderate, not high; the paper should report κ and show the conclusion is
invariant to it (this table), rather than claim the labels themselves are
objective.

## Cross-references

- Refines NONCOMMIT_ERROR_DECOMPOSITION_FINDINGS.md (single-audit) and the
  earlier gold_commitment_audit_summary.md (hostile bound). The hostile
  bound predicted hedge_collision could fall to ~49% under maximally
  adversarial relabeling; the *actual* independent annotators land at
  55–62%, comfortably above it.
