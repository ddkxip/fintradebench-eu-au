# ANSWER_SCHEMA_DESIGN

Every question gets a canonical `AnswerSchema` that reduces its gold
response to a finite, mutually exclusive label space. EU/AU are only
defined over such spaces. Design is grounded in the Phase-1 audit
(analysis/DATA_AUDIT.md) and a close read of 20 gold final-answer sections
(analysis/schema_pilot_excerpts.json).

## Empirical findings that drive the design

1. **F/FT questions reduce cleanly.** Golds are judgment conclusions with
   qualifications ("financially stable — yes", "priced for perfection —
   profitability real but valuation stretched"). A 3-way judgment space
   plus an explicit insufficiency label covers them.
2. **Gold responses sometimes conclude "cannot determine"** (F25: missing
   Disney data → no relative value judgment possible). `insufficient_data`
   must be a first-class label wherever the gold can land on it — it is a
   *correct* answer there, not an abstention.
3. **T-lane splits into three shapes:**
   - *judgment* T questions (fine, same as F);
   - *screening with a clear top-1* (T1 "strongest uptrends" → APP ranked
     first; T2 → INTC "leads decisively"; T10 → AAPL) → reduce to
     **constrained company choice**: answer_space = {gold top-1, the 2–4
     runners-up the gold names, distractor tickers}, gold_label = top-1,
     runners-up recorded as `acceptable_aliases` for a secondary lenient
     scoring;
   - *unordered list* screenings (T5 lists 20 tickers with no ranking;
     T30's gold cannot even rank) → **schema_uncertain**, excluded from
     headline EU/AU until schema validation passes or a set-valued scoring
     extension is designed. Do not force these.
4. **FT golds often land on "conditional/depends"** (FT25 cautious
   accumulation; FT31 depends on strategy). The judgment space therefore
   needs a real `conditional` label — and the class-imbalance risk (many
   FT golds conditional) must be tracked in SCHEMA_VALIDATION.md.

## Answer types (v1)

| answer_type | answer_space | used for |
|---|---|---|
| yes_no_mixed | yes / no / mixed / insufficient_data | "is X profitable/stable/…" |
| supportive_judgment | supportive / unsupportive / conditional / insufficient_data | "should I…", "is X a good…" (advice-shaped questions relabeled to evidence-support language) |
| company_choice | explicit ticker list (2–6) + insufficient_data | "which of A, B, C…" |
| screening_top1 | ticker shortlist (4–6) + none_clear | "which stocks show the strongest…" with ranked gold |
| direction_call | positive / negative / neutral | "has momentum turned positive" |
| valuation_judgment | expensive / fair / cheap / insufficient_data | valuation questions |
| open_summary_with_canonical_claim | claim_true / claim_false / mixed | "why…" questions, scored on the canonical claim |
| schema_uncertain | — | unreducible; excluded from headline |

Rules:
- The space must match the question; nothing is forced into
  bullish/neutral/bearish.
- Labels must be mutually exclusive and exhaustive *given the gold*
  (`mixed`/`conditional` absorb qualified conclusions; `insufficient_data`
  absorbs data-limited golds).
- `buy/sell/hold` never appear as labels unless the schema explicitly maps
  an advice-shaped question to support language (supportive_judgment).

## Schema fields (schemas/answer_schemas.jsonl)

question_id · lane · question · golden_indicators · answer_type ·
answer_space · gold_label · gold_label_evidence (verbatim quote from gold
response) · canonical_claim · aliases (per-label surface forms for the
parser) · label_parse_rules · ambiguity_notes · schema_confidence
(high/medium/low).

Low-confidence schemas are excluded from headline analyses unless manually
approved (validation tests enforce this).

## Derivation procedure

1. Read the gold response's final-answer section.
2. Choose the narrowest answer_type whose space the gold occupies.
3. gold_label = the label the gold's conclusion asserts; record the
   verbatim sentence as gold_label_evidence.
4. canonical_claim = one sentence restating the gold conclusion.
5. aliases: for each label, surface forms an agent might emit ("yes",
   "agree", "supported"; ticker names and company names for choices).
6. schema_confidence: high = gold conclusion unambiguous; medium = gold
   qualified but classifiable; low = forced or set-valued.

Phase 2 covers 20 questions (7F/7T/6FT) chosen to span all shapes,
including deliberately hard cases (F25 insufficient-data, T5 unordered
list, T30 degenerate gold). Scale to 150 only after SCHEMA_VALIDATION.md
passes on these 20.
