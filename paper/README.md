# paper/ — TheWebConf 2027 submission draft

**Target: ACM Web Conference (TheWebConf) 2027.** Abstract 11 Oct 2026,
paper 18 Oct 2026 (verify against the official CFP). Fallbacks if rejected:
ICML 2027 (~Jan) or KDD 2027 cycle 1 (~Feb).

`main.tex` — `acmart` `[sigconf,anonymous,review]` (double-blind, line
numbers on). Build:

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Status: compiles clean, **5 pages** — needs expansion toward the CFP limit.
Anonymization verified (no author/affiliation/repo strings in the PDF). CCS
concepts render. Copyright strip suppressed until the e-Rights form exists.

## The Web framing

Title: *Stable but Not Correct: Auditing Multi-Agent LLM Debate as a
Reliability Mechanism for High-Stakes Financial Information Access.*

The paper is positioned as a **reliability audit of a deployed web
mechanism**, not as a finance paper:

1. **High-stakes information access.** Financial QA now happens through
   web-facing LLM assistants; the cost of a confidently wrong answer is
   borne by the user and is invisible at consumption.
2. **Debate as a web-facing reliability mechanism.** Multi-agent debate is
   *adopted by operators* to make such systems trustworthy. Auditing whether
   it works is a Responsible-Web question about deployed infrastructure.
3. **Failure modes framed as user harms.** Hedge collision = a non-answer
   (unhelpful but honest); wrong-direction commitment = confident
   misinformation in a domain where users act on it; overcommitment =
   answering where refusal was correct. A single accuracy number conflates
   harms that differ in kind.
4. **Operator-facing conclusions** (§7): monitor non-commitment not entropy;
   don't route on uncertainty; configure panels for diversity not
   adversariality; score refusal as first-class.

**Honest risk, stated plainly:** "what makes this a Web paper?" is still the
most likely reviewer objection. The framing above is the strongest available
and is substantive rather than cosmetic — the mechanism audited is one
operators actually deploy, and the conclusions are operational. But the
artifacts are filings and market indicators, and no reviewer will mistake
this for a Web-systems paper. Budget rebuttal space for it.

## Section → evidence map

| section | source |
|---|---|
| §5.1 debate dynamics | `EA_FULL_FINDINGS.md`, `EB_CONTROLLED_FINDINGS.md`, `HF_GEMMA4_31B_FULL_FINDINGS.md` |
| §5.2 error decomposition | `analysis/noncommit_error_decomposition_allmodels.md` |
| §5.3 interaction / monitor limits | same, §E |
| §5.4 lane regimes | `HF_QWEN36_*`, `HF_GEMMA4_31B_*`, `analysis/model_comparison_table.csv` |
| §5.5 interventions | `EC_INTERVENTION_FINDINGS.md` |
| §5.6 agent design | `analysis/financebench/FINANCEBENCH_AGENTSET_CONTROL_FINDINGS.md` |
| §5.7 annotation | `INTERANNOTATOR_FINDINGS.md` |
| §5.8 + Fig 3 | `analysis/financebench/FINANCEBENCH_YESNO_ORACLE_FINDINGS.md` (note §10 retraction), `paper/figures/fig3_committed_cell.py` |

Figures: `figures/fig3_committed_cell.py` regenerates Fig 3 (forest plot,
Okabe-Ito CVD-safe, identity by shape+hue so greyscale-safe).

## Open tasks

See `PAPER_TASKS.md` in the repo root.
