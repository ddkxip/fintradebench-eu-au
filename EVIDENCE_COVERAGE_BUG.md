# Evidence-coverage bug (found 2026-08) — impact and correction

## What happened

While pulling verbatim rationales for the qualitative failure-mode figure,
several models justified a non-committal answer with *"the context is
completely empty"*. Checking the evidence packs confirmed it: **21 of the 139
headline-eligible questions built EMPTY evidence packs** (zero tickers
detected, 0 characters of context).

Root cause: `src/evidence.py`'s `NAME_TO_TICKER` alias map contained only 27
company names. Questions naming Starbucks, Cisco, PayPal, Adobe, Texas
Instruments, Pepsi, Palo Alto Networks, Comcast (and others) matched no
ticker, so no context was built. For F/FT questions the answer space contains
no ticker candidates either, so there was no fallback.

**Why it matters:** with no evidence, answering `insufficient_data` is
*correct behaviour*. The error taxonomy scored it as a **hedge collision** —
inflating the paper's headline failure mode.

## Impact (measured, before the fix)

| | rows | hedge-collision rate | mean $p_{nc}$ |
|---|---|---|---|
| empty packs | 84 | **0.690** | 0.936 |
| populated packs | 472 | 0.288 | 0.410 |

- 58 of 194 hedge collisions (**29.9%**) occurred on empty packs.
- Hedge-collision share of all errors: **0.572 → 0.515** when empty-pack
  questions are excluded.

**The central claim survives**: hedge collision remains the modal error mode
(51.5%). But the headline number was inflated by ~6 points, and a reviewer
who checked would have found it.

## Fix

1. `NAME_TO_TICKER` extended with 38 verified aliases (every added ticker
   confirmed to have a data file). Empty packs: **21 → 4 (2.9%)**.
2. The 4 remaining are legitimate and now allow-listed:
   - `F23`, `F45`, `F49` — sector/category questions naming no entity; the
     evidence builder is entity-based.
   - `FT19` — Moderna, which genuinely has no data file. Its reference
     answer *is* `insufficient_data`; an empty pack is correct here.
3. `tests/test_evidence_coverage.py` pins the invariant: no unexpected empty
   packs, every alias resolves to a real data file (with an explicit
   allow-list for the deliberate Walmart/Disney absences behind F31/F25),
   and empty-pack rate ≤ 5%.
4. Re-running the 17 now-fixed questions on all four models
   (`--only` flag added to `analysis/run_ea_full.py`, results to
   `evfix_<model>` run ids, originals preserved for audit).

## RESOLVED (2026-08-14) — final reporting position

The re-run completed for the two locally-servable models. The two HF models
(`qwen3.6-27b-fp8`, `gemma4-31b-it`) were run on external infrastructure and
**cannot be re-run with current tooling** — `run_ea_full.py` has no `hf:`
backend. (An attempt to force it produced a run in which every decode
returned HTTP 400; that run is quarantined under `results/_quarantine/`, and
the runner now aborts on a zero-parse question rather than writing
result-shaped rows. See PAPER_TASKS "Things NOT to do".)

**Headline is therefore the 122-question populated-pack subset**, which is
bug-free for all four models and apples-to-apples:

| model | acc | HC | WD | OC | WN |
|---|---|---|---|---|---|
| gemma4 | 0.320 | 0.663 | 0.277 | 0.036 | 0.024 |
| qwen3:8b | 0.418 | 0.493 | 0.408 | 0.085 | 0.014 |
| qwen3.6-27b | 0.492 | 0.484 | 0.371 | 0.129 | 0.016 |
| gemma4-31b-it | 0.500 | 0.443 | 0.393 | 0.131 | 0.033 |
| **pooled** | 0.432 | **0.531** [0.43, 0.63] | 0.357 | 0.090 | 0.022 |

**The bug did not drive the finding.** Add-back check on the two re-runnable
models, comparing 122q subset → corrected 139q → buggy 139q:

| model | 122q subset | 139q corrected | 139q with bug |
|---|---|---|---|
| gemma4 | 0.663 | 0.681 | 0.670 |
| qwen3:8b | 0.493 | 0.519 | 0.554 |

The correction moves hedge collision by ≤3.5 points and **in opposite
directions** for the two models. Hedge collision remains modal in every model
under every treatment. The original inflated pooled figure (0.572) and the
interim populated-pack figure (0.515) are both superseded by **0.531**.

## Lesson for the paper

This is worth a sentence in Limitations regardless of the re-run: an
entity-detection gap in evidence construction silently converts *appropriate
refusal* into a scored failure. Any benchmark that scores non-commitment
must audit whether the evidence was actually there.
