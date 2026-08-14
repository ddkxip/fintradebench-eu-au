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

## Reporting position until the re-run lands

Report the **populated-pack** figures as headline (hedge collision 0.515) and
disclose the excluded questions, rather than quoting the inflated 0.572. Once
the re-run completes, the corrected full-139 numbers replace both.

## Lesson for the paper

This is worth a sentence in Limitations regardless of the re-run: an
entity-detection gap in evidence construction silently converts *appropriate
refusal* into a scored failure. Any benchmark that scores non-commitment
must audit whether the evidence was actually there.
