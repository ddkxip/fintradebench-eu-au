# EU_AU_DECOMPOSITION — definitions, estimators, and pitfalls

## Objects

Per question q, agent i ∈ {1..N}, round t, finite answer space Y from the
AnswerSchema:

- Agent distribution p_{q,i,t}(y): estimated by **self-consistency
  frequencies** over K independent decodes at τ=0.7 (G0 decision), with
  Jeffreys smoothing for NLL only (raw frequencies for entropies; see
  Estimator notes).
- System mixture: p_sys = (1/N) Σ_i p_i.
- TU_{q,t} = H(p_sys); AU_{q,t} = (1/N) Σ_i H(p_i);
  EU_{q,t} = TU − AU = generalized Jensen–Shannon divergence among the
  agents' distributions (with uniform weights). Base-e entropies; also
  reported normalized by log|Y| so questions with different label-space
  sizes are comparable (flagged `_norm`).

Identities enforced by unit tests: EU ≥ 0, AU ≥ 0, TU = AU + EU exactly;
identical agents ⇒ EU = 0; confident disagreeing agents ⇒ EU → log N
capped by log|Y|; TU ≥ AU always.

## Ground-truth alignment

gold label y*: from the schema. Per round:
G = p_sys(y*) · predicted ŷ = argmax p_sys · Correct = 1[ŷ = y*] ·
Brier = Σ_y (p_sys(y) − 1[y=y*])² · NLL = −log p̃_sys(y*) (smoothed).
Deltas across rounds: ΔEU, ΔAU, ΔTU, ΔG, ΔCorrect feed the transition
taxonomy (DEBATE_TRANSITION_TAXONOMY.md).

## Estimator notes (the honest part)

1. **Plug-in entropy bias.** Ĥ from K samples is biased low by
   ≈ (|Y|−1)/(2K) nats (Miller–Madow). With |Y|=4, K=10 the bias is
   ~0.15 nats — *material*. All headline entropies use the Miller–Madow
   correction; raw plug-in reported alongside. K=20 halves the bias
   (T-lane uses K=20 anyway per G0). Bias mostly cancels in ΔEU across
   rounds (same K), not in lane comparisons (different K!) — lane
   comparisons therefore use equal-K subsamples or the correction, never
   raw mixed-K values.
2. **EU is a difference of biased estimators.** Bootstrap over the K
   decodes gives a CI per question per round; the within-question CI is
   reported with every headline aggregate.
3. **Parse failures** shrink effective K. Rows record K_effective per
   agent; questions with parse rate < 80% for any agent are excluded from
   headline and analyzed separately (parse-failure sensitivity section of
   the stats plan).
4. **Screening spaces are larger** (|Y| up to 7) — normalized entropies
   and Miller–Madow matter most there.
5. **Verbalized probabilities** may be logged as a secondary diagnostic
   only (G0: heaped, weak).

## Why this replaces U3 and the B+W+R budget as the headline

EU here *is* the between-agent term (B) of the earlier budget, now defined
over schema labels with gold scoring; AU absorbs the within-agent
replicate term (W) and residual (R) at the label level. The old
frameworks×replicates split (B/W/R) remains available as a secondary
decomposition of AU (W = disagreement among an agent's own decodes is
exactly what the frequency entropy measures), but the paper leads with the
two-component form because it maps onto the *Epistemic Gain, Aleatoric
Cost* literature and onto actionability: EU is reducible by debate/
information; AU is what debate cannot fix at fixed evidence.
