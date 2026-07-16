# SCHEMA_VALIDATION — Phase-2 pilot (20 schemas: 7F / 7T / 6FT)

Automated checks (tests/test_schema.py, all passing): 20 schemas, lane
counts 7/7/6, no duplicate ids, nonempty mutually-exclusive answer spaces
for all non-uncertain schemas, every gold_label ∈ answer_space, every
gold_label backed by a verbatim gold_label_evidence quote, alias keys ⊆
answer_space, low-confidence/schema_uncertain excluded from
`headline_eligible`.

## Feasibility verdict on finite answer schemas

**Viable, with a quantified T-lane carve-out.**

| | high | medium | low/uncertain | headline-eligible |
|---|---|---|---|---|
| F (7) | 4 | 3 | 0 | 7/7 |
| T (7) | 1 | 2 | 4 | 3/7 |
| FT (6) | 2 | 4 | 0 | 6/6 |
| total | 7 | 9 | 4 | **16/20 (80%)** |

Findings:

1. **F and FT reduce completely.** Judgment spaces (yes/no/mixed/
   insufficient_data; supportive/unsupportive/conditional/
   insufficient_data) absorbed every gold conclusion, including F25 whose
   *correct* label is insufficient_data.
2. **T-lane is the carve-out, and it is structural**: 4/7 pilot T
   questions have unordered-set or degenerate golds (T5: 20 tickers;
   T25: 6 tickers; T15: 4-way priority tie → forced low; T30: gold itself
   declines to rank). Extrapolating, expect roughly **20–30 of the 50 T
   questions to be headline-ineligible**. Consequences:
   - headline EU/AU set ≈ 115–130 of 150, with T underrepresented —
     report eligibility rates per lane and treat lane comparisons
     accordingly;
   - a set-valued scoring extension (precision/recall vs the gold set) is
     the natural follow-up for the excluded T items — documented as
     future work, not smuggled into headline classification.
3. **FT gold-label imbalance confirmed**: 3/6 pilot FT golds are
   `conditional`. If ~half of FT golds are conditional at scale, a
   trivial always-conditional baseline gets ~50% FT accuracy — the
   analysis must report per-label confusion and majority-class baselines,
   and gold-probability G (not just accuracy) is the primary outcome.
4. **Answer-type inventory used**: yes_no_mixed (3), company_choice (4),
   supportive_judgment (5), screening_top1 (4), open_summary_with_
   canonical_claim (1), schema_uncertain (3). direction_call and
   valuation_judgment weren't needed in this sample but stay in the
   design for the full 150.
5. **T30 upstream flag**: its gold concludes the question is unanswerable
   from its own generation context (single-stock coverage). Reported to
   benchmark maintainers as a data-quality note; excluded here.

## Scale-up rule (to 150)

Proceed lane by lane, F → FT → T. The 150-version validation flips
tests/test_schema.py constants to 150/50/50/50 and adds: per-label gold
distribution report (imbalance watch), screening shortlist symmetry check
(evidence pack must cover every candidate ticker), and a manual-approval
list for any medium schema whose ambiguity_notes flag a defensible
alternative label (F1, FT2, FT10 in the pilot — these three get a second
human pass before headline use).
