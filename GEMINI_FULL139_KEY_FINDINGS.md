# gemini-3-flash full-139 run — what it changed (2026-08-20)

Run: `gemini_full139`, `vertex:gemini-3-flash-preview`, **thinkingBudget=0**,
K=10 F/FT and K=20 T (G0 rule), rounds 0+1, 139/139 questions,
mean parse_rate 0.9996.

## Why thinking was disabled

`src/runner.py` sends `"think": False` to Ollama. The Vertex path had no
equivalent, so `gemini_subset16` ran with **extended thinking** — an
unmatched comparison in which test-time reasoning is confounded with model
identity. Probing showed only flash-tier models accept `thinkingBudget=0`:
`gemini-3.1-pro-preview` ignores it and `gemini-2.5-pro` returns HTTP 400.
That, not cost, is why the flash model was chosen.

## Finding 1 — debate DOES improve accuracy, for this system only

| system | R0 | R1 | Δ | rescued | lost | p (exact binomial) |
|---|---|---|---|---|---|---|
| gemma4 | 0.266 | 0.281 | +0.014 | 5 | 3 | 0.73 |
| qwen3:8b | 0.432 | 0.403 | −0.029 | 4 | 8 | 0.39 |
| qwen3.6-27b | 0.417 | 0.432 | +0.014 | 6 | 4 | 0.75 |
| gemma4-31b-it | 0.410 | 0.446 | +0.036 | 7 | 2 | 0.18 |
| **gemini-3-flash** | **0.504** | **0.590** | **+0.086** | **16** | **4** | **0.012** |

It is also the only system whose non-commitment *falls* across the round
(Δp_nc = −0.046; all four others rise).

**This qualifies the paper's headline.** "Debate buys stability, not
correctness" holds for the open-weights systems and is falsified for a
frontier API model. The paper now states it as a capability boundary
condition (§ Capability changes what debate does) rather than a universal.

What is NOT affected: the monitoring conclusion. gemini-3-flash's
non-mechanical-cell AUROC is 0.455 — still at chance, like every other
system. p_nc remains a non-answer detector, not a misinformation detector.

## Finding 2 — "hedge collision is modal in every model" needs a stated basis

Raw, all 139: gemini-3-flash **HC 0.421 vs WD 0.439** — wrong-direction is
nominally modal, the only system where that happens.

But the margin is one error (24 vs 25 of 57) and the HC CI is [0.30, 0.54].
And by lane the split is stark:

| lane | errors | HC | WD |
|---|---|---|---|
| F | 14 | 0.571 | 0.286 |
| FT | 22 | 0.682 | 0.136 |
| **T** | **21** | **0.048** | **0.857** |

The T lane carries it — exactly where set-collapse lives. Applying the
correction this repo already commits to (drop WD errors whose prediction the
reference's own justification endorses; see `REFERENCE_QUALITY_AUDIT.md`):

| system | errors raw | artifacts | HC | WD | modal |
|---|---|---|---|---|---|
| gemma4 | 100 | 8 | 0.728 | 0.174 | HC |
| qwen3:8b | 83 | 10 | 0.630 | 0.260 | HC |
| qwen3.6-27b | 79 | 9 | 0.600 | 0.214 | HC |
| gemma4-31b-it | 77 | 10 | 0.582 | 0.209 | HC |
| gemini-3-flash | 57 | 10 | **0.511** | 0.319 | **HC** |

Hedge collision is modal in all five under the corrected view. The claim
must be stated with its basis; it is not unconditional. Note the correction
was established *before* this run existed, so applying it here is not
post-hoc special pleading.

## Finding 3 — the FT-lane claim now rests on a matched system

Mean p_nc by lane: F 0.315, **FT 0.567**, T 0.038. FT is the highest-hedging
lane for gemini-3-flash as for every other system, so the abstract's
"highest-hedging lane in all five systems" no longer depends on the
unmatched `gemini_subset16`. The ordering survives even though this system
hedges least overall — a stronger form of the claim than previously stated.

## Data-integrity issues found and fixed during the run

- **FT36** triggered a latent bug: `run_question` emitted a different column
  set on the parse-failure branch, so its block was written with a different
  width and order under the existing header. Runner now pads both branches
  to a canonical schema; `tests/test_row_schema.py` pins it.
- **T9** failed entirely on HTTP 401 — the gcloud token expired ~2h in. The
  skip-no-parse guard wrote nothing rather than result-shaped empties, so it
  was cleanly re-runnable. **Long Vertex runs should expect this**; a Pro-arm
  run at ~4.3h would likely hit it more than once.
- Sweeping all shipped runs found `ec_interventions_gemma4` had one silently
  misaligned row (F22). Verified it changes nothing: already excluded by the
  `isinstance(arm, str)` guard, and the analysis uses `au_mm`/`eu_mm` not the
  corrupted raw `tu`/`au`. It did reveal the conflict arm is n=29, not 30;
  Limitations corrected.
