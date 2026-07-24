# Gold-commitment audit — summary

Sheet: `gold_commitment_audit_sheet_completed.csv`. Reanalysis only; schemas and existing findings untouched.

**Auditor note (limitation):** the manual adjudication was performed by the analyst (the same author who wrote the schemas), re-reading each gold's evidence against an explicit binary criterion, NOT by an independent third party. It is a criterion-based self-audit plus a hostile sensitivity bound, not an inter-annotator study.

**Commitment criterion.** COMMITTED iff the gold's operative conclusion selects a single answer-space direction a reader would act on (caveats on other dimensions allowed). NON-COMMITTED iff it (a) declines to determine, (b) is conditional on an unspecified external factor with no default, or (c) weights opposing conclusions on the same dimension equally.

- audited rows: **139** (37 high-risk cases adjudicated explicitly: all 22 non-committed golds + 15 hedge-adjacent committed golds; remaining 102 fall back to schema).
- exact gold_label agreement (audited vs schema): **1.000**
- commitment agreement (audited vs schema): **1.000**
- validation violations: 0

## Changed commitment assignments: 0
None. Every commitment call is confirmed under the criterion. The 15 hedge-adjacent committed golds all have a clear operative directional conclusion; their flagged hedge labels are defensible *alternative* labels (grading generosity), not non-commitment of the gold itself. The 22 non-committed golds are all genuine insufficiency/conditional/two-sided cases.

- questions flagged needs_schema_revision: ['FT28'] (FT28: operative conclusion is 'valuation not justified' = committed no, but it explicitly notes missing robotaxi evidence — the single most defensible insufficiency reclassification; retained committed).