# FinanceBench agent-set control — the collapse was the skeptic, not debate

Full tables: `FINANCEBENCH_AGENTSET_CONTROL.md` (regenerate with
`analyze_agentset_control.py`). All three arms complete: qwen3:8b, oracle
`evidence_text`, K=10, 1 debate round, identical 37 yes/no schemas — **only
the agent pair differs**.

## Verdict: **skeptic-driven** (pre-registered rule, fired cleanly)

| arm | R0 acc | R1 acc | dCorrect | rescues / losses |
|---|---|---|---|---|
| skeptic (asymmetric) | 0.595 | 0.351 | **−0.243** (p=0.012) | 1 / 10 |
| neutral (heterogeneous, symmetric) | 0.595 | **0.649** | **+0.054** | 3 / 1 |
| homogeneous (identical) | 0.622 | 0.622 | **0.000** | 1 / 1 |

**Three-way decomposition.** Role *bias* does large harm (−0.243); role
*diversity* does small good (+0.054); role *duplication* does nothing at all
(0.000, and ΔpNC −0.005). The homogeneous arm is the cleanest null in the
programme — both identical analysts hold hedge rate at exactly 0.216 → 0.216
across the debate round. So the neutral arm's modest gain **requires genuine
perspective diversity**, not merely a second voice.

Identical round-0 accuracy (0.595) in both arms is a useful sanity check:
the shared Evidence Accountant behaves the same pre-debate, so the arms
diverge only through the debate exchange.

The interpretation rule was fixed **before** the run: *if the neutral arm's
drop largely disappears, the original collapse was an artifact of the
insufficiency-biased skeptic and must not be reported as a general debate
effect.* It disappeared and reversed. **The earlier "1 rescue / 10 losses"
result must not be cited as evidence that debate harms accuracy.**

## Mechanism: the skeptic dragged the analyst; the neutral partner did not

Per-agent, by round:

```
skeptic arm                  acc    pNC   hedge_rate
  evidence_accountant  R0   0.622  0.232     0.216
  evidence_accountant  R1   0.324  0.535     0.541   <- collapses
  skeptical_auditor    R0   0.243  0.676     0.676
  skeptical_auditor    R1   0.324  0.630     0.649   <- barely moves

neutral arm                  acc    pNC   hedge_rate
  evidence_accountant  R0   0.595  0.222     0.216
  evidence_accountant  R1   0.676  0.222     0.216   <- improves, hedge flat
  financial_analyst    R0   0.568  0.341     0.324
  financial_analyst    R1   0.568  0.295     0.297
```

In the skeptic arm the competent analyst is pulled onto the skeptic's
hedging (hedge rate 0.216 → 0.541, accuracy 0.622 → 0.324) while the skeptic
barely moves. In the neutral arm the same analyst's hedge rate is
**perfectly stable** (0.216 → 0.216) and its accuracy *rises*. Debate
transmitted the skeptic's insufficiency bias; it did not transmit anything
harmful between two substantive agents.

## Knock-on: the "debate increases hedging" result was also skeptic-driven

dNC: skeptic **+0.128 (p=0.020)** vs neutral **−0.023 (n.s.)**. On this
benchmark the hedging push is a property of the asymmetric pair, not of
debate. (The FinTradeBench dNC result stands on its own data — qwen3:8b
there used two substantive agents.)

## Knock-on: it partly explains the Figure 3 outlier

Committed-cell AUROC (the non-mechanical cell):

| arm | n | AUROC | 95% CI | includes chance? |
|---|---|---|---|---|
| skeptic | 18 | 0.815 | [0.631, 0.958] | no |
| **neutral** | 30 | **0.576** | **[0.360, 0.822]** | **yes** |
| FinTradeBench (4 models) | 50–78 | 0.403–0.446 | all straddle 0.5 | yes |

The arm methodologically comparable to FinTradeBench (symmetric substantive
agents, as in Fundamental vs Trading) behaves like FinTradeBench. The two
FinanceBench CIs overlap substantially, so **we cannot claim the arms
differ** — but the above-chance result appears only under the asymmetric
configuration, which makes agent design an identified source of instability
in that estimate rather than a purely benchmark-level mystery.

## Error composition

Errors fall from 24 to 13 under the neutral pair. Hedge collision remains
the modal type but loosens its grip: 0.792 → 0.538 (wrong-direction 0.208 →
0.462). The categorical-uncertainty story survives; its magnitude on this
benchmark was inflated by the skeptic.

## What this changes

1. **Retract** any "debate harms accuracy" reading of the FinanceBench probe.
   With symmetric agents, one debate round is mildly *beneficial*
   (+0.054, 3 rescues vs 1 loss).
2. **Scope** the Figure 3 / §5.7 open question: agent asymmetry is one
   identified driver; task format and answer space remain untested.
3. **Do not** generalize the skeptic arm's dNC or hedge-share figures.
4. Pending: the homogeneous arm (two identical accountants) separates role
   *diversity* from role *bias*; it will say whether the neutral arm's small
   gain needs two perspectives or merely two non-skeptical ones.

---

## Update — homogeneous arm complete (2026-08)

```
                    arm  R0_acc  R1_acc  dCorrect  resc/loss   dNC  commit_cell_AUROC        CI
     skeptic (asymm.)    0.595   0.351    -0.243      1/10   +0.128              0.815  [.63,.96]
    neutral (hetero.)    0.595   0.649    +0.054       3/1   -0.023              0.576  [.36,.82]
homogeneous (identical)  0.622   0.622    +0.000       1/1   -0.005              0.478  [.43,.50]
```

Per-agent, homogeneous arm — total inertia:

```
                         acc    pNC  hedge_rate
evidence_accountant_a R0  0.622  0.224     0.216
                      R1  0.622  0.219     0.216
evidence_accountant_b R0  0.595  0.224     0.216
                      R1  0.622  0.219     0.216
```

**Committed-cell consequence.** Two independent *symmetric* configurations
on FinanceBench (neutral 0.576, homogeneous 0.478) both sit at chance,
matching all four FinTradeBench models (0.403–0.446). Only the asymmetric
skeptic arm exceeds it (0.815). Since benchmark, model, questions, evidence
and K are held fixed across the three arms, **agent asymmetry — not
benchmark identity — is the identified driver** of the Figure 3 outlier.
This is a considerably stronger statement than the one-control version.

Caveat: adjacent CIs overlap, so no pairwise-significance claim is made; the
evidence is the pattern across three configurations. Also note that in the
homogeneous arm EU measures sampling divergence between two instances of the
same prompt, not framework disagreement, so its near-zero EU is expected by
construction rather than informative.
