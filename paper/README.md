# paper/ — initial draft

`main.tex` (ACM `sigconf`) + `refs.bib`. Build:

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

`nonacm` is set for internal drafting; remove it for the real submission and
add the venue's rights commands.

## Venue: read before committing to TheWebConf

The draft is written venue-neutral on substance. **My honest assessment is
that ACM Web Conference is not the most natural home for this work**, and
you should weigh that before we invest in a Web framing.

- **The fit problem.** Nothing here is about the Web. The artifacts are
  SEC-derived filings and market indicators; the object of study is LLM
  agent reliability. TheWebConf reviewers routinely ask "what makes this a
  Web paper?", and the honest answer is "the data was originally scraped".
  That is a weak answer and a likely reject-driver even if the science is
  sound.
- **Where it does fit at TheWebConf**, if you still want it: the
  Responsible/Trustworthy Web track (uncertainty, reliability, and failure
  modes of deployed LLM systems) is the only credible route, and the paper
  would need reframing around *trustworthy automated decision support* with
  the finance benchmark as the testbed rather than the subject.

**Stronger-fit alternatives, roughly in order:**

1. **ACM ICAIF** (International Conference on AI in Finance) — an ACM venue,
   directly on-topic; the evaluation/UQ angle is well received there.
2. **EMNLP / ACL (main or Findings)** — the categorical-vs-distributional
   uncertainty result is an NLP-evaluation contribution; FinNLP is the
   natural workshop fallback with a fast path.
3. **NeurIPS Datasets & Benchmarks** — if the schemas + intervention suite
   are released as the headline artifact.
4. **CIKM / AAAI** — reasonable middle ground if you want a broad CS venue.

If the goal is "an ACM venue in this cycle", **ICAIF is the better ACM
target than TheWebConf**. If the goal is TheWebConf specifically (e.g.
institutional reasons), say so and I will rewrite the intro and related-work
framing around trustworthy Web-scale decision systems — it is doable, just
not the paper's natural shape.

Check the current CFP for page limits and deadlines; TheWebConf research
papers have historically been due in **October** for the following spring,
which would leave runway, but verify against the official CFP rather than
this note.

## Status of the draft

Written from verified results; every number traces to a findings doc in the
repo root or `analysis/`. Sources per section:

| section | source |
|---|---|
| §5.1 error decomposition | `analysis/noncommit_error_decomposition_allmodels.md` |
| §5.2 interaction | same, §E |
| §5.3 lane regimes | `HF_QWEN36_*`, `HF_GEMMA4_31B_*`, `analysis/model_comparison_table.csv` |
| §5.4 debate dynamics | `EA_FULL_FINDINGS.md`, `EB_CONTROLLED_FINDINGS.md` |
| §5.5 interventions | `EC_INTERVENTION_FINDINGS.md` |
| §5.6 annotation | `INTERANNOTATOR_FINDINGS.md` |
| §5.7 boundary | `analysis/financebench/FINANCEBENCH_YESNO_ORACLE_FINDINGS.md` |

## Before submission — required

1. **Verify every GROUP B citation** in `refs.bib` against the arXiv
   listing. They came from literature search during this project and the IDs
   have not been checked against the published record. Do not submit on
   search-result provenance alone.
2. **Add figures.** Three are planned in
   `RECOMMENDED_PAPER_DIRECTION_EU_AU.md` §5; Figure 3 (committed-cell AUROC
   vs residual-hedge-mass variance) is the one that converts the §5.7
   boundary from a caveat into a result.
3. **Finish the FinanceBench neutral-agent control** (running). Until it
   lands, §5.7 must stay framed as an auxiliary probe and the debate arm of
   that benchmark must not be used for any general claim — the original pair
   was asymmetric by design.
4. Decide the self-citation/anonymization policy for the benchmark paper.
5. Reproducibility appendix: model digests, $K$, $\tau$, seeds, run
   manifests (all already in `results/manifests/`).
