# What the raw decodes show about *why* systems hedge (2026-08-20)

## Are responses logged before classification? Yes — all of them.

`results/raw/<run_id>/decodes.jsonl` stores every decode with full
`raw_text`, plus `parsed_label`, `parser_method`, `parser_confidence` and
`parse_failure_reason`. Nothing is discarded before classification:
7,160 decodes per open-weights model, 7,200 for `gemini_full139`.

## Are models choosing from the answer space, or are we mapping free text?

**They emit free text; we map it — but the mapping almost never has to
interpret.** The API-level JSON mode (`format: json` / `responseMimeType`)
forces well-formed JSON, not a valid label value, so the `label` field is an
unconstrained string. `src/parsing.py` then resolves it through a hierarchy:

| method | confidence | meaning |
|---|---|---|
| `strict_json` | 1.0 | `label` normalizes exactly onto the answer space |
| `json_alias` | 0.8 | off-space label rescued via schema aliases |
| `regex_label` | 0.5 | no JSON label; answer-space token found in prose |
| `regex_alias` | 0.4 | alias found in prose |
| `none` | 0.0 | parse failure, excluded |

Observed across 21,520 decodes:

| model | strict_json | regex_label | none |
|---|---|---|---|
| gemma4 | 100.00% | – | – |
| qwen3:8b | 100.00% | – | – |
| gemini-3-flash | 99.43% | 0.36% | 0.21% |

**`json_alias` fired zero times.** The fuzzy path is effectively unused, so
the labels are the models' own words, not our reconstruction of them.

## The mechanism: hedging is evidence-*selection* variance, not noise

F11 — "Is Tesla financially stable enough to weather an economic downturn?"
(gold `yes`). gemini-3-flash, trading agent, round 1, K=10, tau=0.7,
byte-identical prompt: **5 decodes `yes`, 5 decodes `mixed`.**

The two groups cite *disjoint, non-overlapping subsets of the same pack*:

| committed (`yes`) cites | hedged (`mixed`) cites |
|---|---|
| Momentum_20D = 0.1032 (+10.32% month) | RSI = 46.82 (below 50) |
| Medium-term momentum = 0.4374 | Momentum_5D = −0.0181 (negative) |
| MACD = 5.9422 (positive) | price < EMA_20 = 334.04 |
| Debt/Equity = 0.0925, Debt/Assets = 0.0562 | One_Day_Reversal = −0.0350 |

Every figure on both sides was verified present in the pack. Neither side
hallucinates; neither side is wrong. The long-horizon indicators support
stability and the short-horizon indicators do not, and the model is
inconsistent about **which horizon is decision-relevant** — not about the
facts.

### Why this matters for the paper

It supplies a mechanism for the categorical-uncertainty claim. The system is
not spreading probability over answers because it is unsure of the evidence;
it is switching between two internally coherent readings of the *same*
evidence, and one of those readings terminates in a non-committal label. That
is why the variance is invisible to entropy over answer strings and why
`p_nc` behaves as a discrete regime indicator rather than a confidence score.

It also predicts the FT-lane result: cross-signal questions are exactly the
ones offering two defensible horizons, and FT is the highest-hedging lane in
all five systems.

### Caveat

One question, one agent, one round, hand-read. The disjoint-citation pattern
should be measured across split cells before the paper asserts it as general
(there are 35 / 55 / 72 split cells in gemma4 / qwen3:8b / gemini-3-flash —
enough to quantify properly).
