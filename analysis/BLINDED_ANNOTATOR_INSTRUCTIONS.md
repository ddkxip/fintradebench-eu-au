# Blinded gold-commitment annotation — instructions

You are given, per row: the question, the finite `answer_space` (pipe-separated candidate labels), and the gold answer's own text (`gold_label_evidence`, `gold_final_answer_text`). You do NOT see any prior label or classification. Fill four columns per row:

- **annotator_gold_label**: the single label from `answer_space` that the gold answer asserts. Must be copied exactly from answer_space.
- **annotator_gold_commitment**: `committed` or `noncommitted`.
  - **committed** = the gold's operative conclusion selects one answer-space direction a reader would act on (caveats on *other* dimensions are allowed).
  - **noncommitted** = the gold (a) declines to determine / says the data is insufficient, (b) makes the answer conditional on an unspecified external factor with no default, or (c) weights opposing conclusions on the *same* dimension equally.
- **annotator_confidence**: high / medium / low.
- **annotator_notes**: one-line rationale (optional).

Judge only from the provided gold text. Do not use outside knowledge about the companies. Save your completed file as `gold_commitment_audit_codex.csv` or `gold_commitment_audit_antigravity.csv`.
