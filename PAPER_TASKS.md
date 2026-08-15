# PAPER_TASKS — TheWebConf 2027 (abstract 11 Oct, paper 18 Oct 2026)

Ordered by *risk-reduction per unit effort*. P0 = submission is unsafe
without it. P1 = materially improves accept odds. P2 = strengthens if time
allows. P3 = future work / rebuttal ammunition.

---

## P0 — must do before submitting

**1. Verify every GROUP B citation.** `refs.bib` splits established works
(GROUP A) from ones surfaced by literature search during the project
(GROUP B). The GROUP B entries currently have **no author fields** — left
blank deliberately rather than invented, so bibtex warns. Each arXiv ID,
title and author list must be checked against the actual listing. Do not
submit on search-result provenance. *(~1–2 h, blocking.)*

**2. Expand 5 pp → the CFP limit.** Check the exact TheWebConf 2027 limit
(historically ~9 pp + unlimited refs). Priority order for the added space:
Figures 1–2 (task 3), a worked example of each failure mode (task 5), a
proper Related Work expansion, and a reproducibility appendix.

**3. Decide the self-citation policy.** The benchmark paper is under review
at ACL ARR. Under double-blind, cite it as third-party work
(`\cite{fintradebench2026}` with neutral phrasing) and make sure no sentence
implies authorship. Also confirm ARR/TheWebConf dual-submission rules are
satisfied — this paper must be a clearly distinct contribution (it is: the
benchmark is an instrument here, not the contribution), but state that
explicitly in the response-to-reviewers if asked.

**4. Verify the CFP itself.** Page limit, anonymity rules, whether an
abstract is binding, appendix policy, artifact/reproducibility track.

---

## P1 — materially improves the paper

**5. ~~Build Figures 1 and 2.~~ DONE.**
- *Fig 1 — regime map* (`figures/fig1_regime_map.py`): sequential
  single-hue heatmap, 5 systems × 3 lanes, FT column boxed. Replaced the
  old lane table (same data + gemini row, strictly more informative).
- *Fig 2 — the interaction* (`figures/fig2_interaction.py`): error rate by
  $p_{\mathrm{nc}}$ stratum split by reference type, Wilson CIs, with
  **mechanically-forced cells marked hollow+crossed**. Built this way
  because the interaction turned out to be largely *definitional* — a smooth
  curve would have sold a definitional step as a discovered relationship.
  It now doubles as the visual proof of the "much of the signal is
  mechanical" claim.

**6. ~~Add a qualitative failure-mode figure or box.~~ DONE.** Table 2, a
two-column box with one worked question per mode, verbatim from the run
logs: F43 (hedge collision), F21 (wrong-direction), F40 (overcommitment),
F3 (correct non-commitment). The fourth row is the argument, not decoration —
it is *mechanically indistinguishable* from row 1 (same output shape, same
$p_{\mathrm{nc}}$, opposite correctness), which is the visual proof that a
hedging-rate monitor cannot separate them.
- The originally-planned exemplars were **all rejected on verification**:
  FT16 had an empty evidence pack, F50's reference is contradicted by its own
  evidence, T11/T2 are set-collapse artifacts. See
  `REFERENCE_QUALITY_AUDIT.md`. Verify exemplars against the released pack
  before using them.

**6b. ~~A full reference-answer audit.~~ DONE.**
`analysis/reference_answer_audit.py`, all 139, four mechanical checks.
Result: **2/139 (1.4%)** state a superlative the released table falsifies
(F50, T9); 0 missing entities; 27/139 set-collapse (25 of them T-lane); 6
numeric flags of which 5 are window/derived artifacts. The reference set is
**broadly sound** — F50 was not the tip of an iceberg. Written into
§\ref{sec:robust} and Limitations. Detail in `REFERENCE_QUALITY_AUDIT.md`.
- Note: the checker's first version had 3 false positives out of 5 because
  composite superlatives invert indicator polarity ("strongest balance
  sheet" = *lowest* debt/equity). Hand-verify any new flag before believing
  it.

**7. Strengthen the Web framing in Related Work.** Currently thin. Add a
paragraph situating the work against trustworthy/responsible information
access and web-scale QA reliability. This is the section a sceptical
reviewer will check for "does this author know the venue".

**8. Reproducibility appendix.** Model digests, $K$, $\tau$, seeds, run
manifests (all already in `results/manifests/`), schema construction
procedure, and the released-artifact list. Cheap, and TheWebConf reviewers
increasingly ask.

**9. Tighten the abstract.** Currently dense and long. Lead with the
deployment claim ("debate buys stability, not correctness"), then the
mechanism, then the three harms. Aim for ~200 words.

---

## P2 — strengthens if time allows

**10. Pool the second benchmark's arms into the main narrative properly.**
Right now FinanceBench appears in §5.6 and §5.8 as separate threads. One
consolidated "external validity" subsection would read better.

**11. Statistical hardening.** Bootstrap CIs on the error-decomposition
shares (currently point estimates); a sensitivity table for the
$\varepsilon$ thresholds in the transition taxonomy; report the
majority-vote-commitment version of Table 1 in an appendix.

**12. A second model on the intervention suite.** The causal nulls (§5.5)
currently rest on one model at $n{=}30$. A second model would let you say
"replicated" rather than "scoped to one model" — the single most likely
reviewer complaint about that section.

**13. Lenient-scoring appendix.** Strict vs alias-credited accuracy,
especially for T-lane screening (0.43 → 0.78–0.85). Pre-empts "your
screening scoring is too harsh".

---

## P3 — future work / rebuttal ammunition

**14. Retrieval (RAG) arm.** Deliberately excluded from the headline to
avoid confounding. Reviewers *will* ask whether the findings hold with
retrieval. Having even a small arm ready for rebuttal is valuable; running
it fully is a follow-up paper.

**15. Identify the remaining driver of the §5.8 open question.** Agent
asymmetry is now identified; task format and answer space are not. Matched
runs varying one factor at a time.

**16. T-lane schema revision.** Both blinded annotators independently read
multi-entity screening references as non-committal (10 questions). A
set-valued scoring treatment would tighten the benchmark. Conclusions
already survive either labelling, so this is quality not rescue.

**17. Larger API-model coverage — IN PROGRESS.** The Gemini subset is 16
questions and should not be quoted as a result. A full 139-question run is
staged and ready:

```
python analysis/run_ea_full.py --model vertex:gemini-3.1-pro-preview \
    --run-id gemini_full139
```

**Blocked on credentials only.** `gcloud auth print-access-token` fails with
"Reauthentication failed. cannot prompt during non-interactive execution".
Run `gcloud auth login` in an interactive terminal, then launch the command
above. It is resumable per question, so an interrupted run continues where
it stopped. Expect ~3.5–4 h (the 16-question subset took 24 min at K=10; the
full run is K=10 F/FT and K=20 T per the G0 rule, ≈9.4x the sample budget).
Use a **new run id** — do not append to `gemini_subset16`, which used K=10
uniform and must stay intact for audit.

**18. Multi-round debate.** Everything here is one exchange round. Whether
the stability-without-correctness pattern compounds or reverses over more
rounds is open.

---

## Things NOT to do (tested and rejected)

- Do **not** revive the "residual hedge-mass variance" explanation for the
  §5.8 gap — refuted ($\rho = -0.03$, $p = 0.92$ within-benchmark); see
  `FINANCEBENCH_YESNO_ORACLE_FINDINGS.md` §10.
- Do **not** cite the FinanceBench "1 rescue / 10 losses" as a general
  debate effect — it is an artifact of the asymmetric skeptic pair (§11).
- Do **not** claim $p_{\mathrm{nc}}$ is a general error predictor, or that
  debate reduces AU unconditionally (both narrowed by our own data).
- Do **not** claim the FinanceBench arms differ pairwise — CIs overlap.
- Do **not** cite **F50** as a wrong-direction/model-error example — the
  reference's own justification ("APP has the highest ROA") is contradicted
  by the released table (NVDA 0.2131 > APP 0.1489). The models' unanimous
  NVDA is defensible there. Use **F21** instead.
- Do **not** report T-lane wrong-direction (77%) as clean model error —
  48.6% of those errors name an entity the reference itself endorses. Report
  it as an upper bound. See `REFERENCE_QUALITY_AUDIT.md`.
- Do **not** run `run_ea_full.py --model hf:<name>` — there is no `hf:`
  backend; it silently 400s against Ollama. The runner now aborts on a
  zero-parse question instead of writing empty rows.
