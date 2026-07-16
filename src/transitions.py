"""Debate transition taxonomy (DEBATE_TRANSITION_TAXONOMY.md)."""

from __future__ import annotations

from dataclasses import dataclass

EPS_EU = 0.05   # normalized-scale material-change thresholds
EPS_AU = 0.05
EPS_G = 0.05


@dataclass
class RoundState:
    eu_norm: float
    au_norm: float
    gold_prob: float
    correct: bool
    agent_gold_probs: dict[str, float]  # per-agent p_i(y*)


@dataclass
class Transition:
    outcome: str
    flow: str
    persistent_rational_disagreement: bool
    correct_minority_suppression: bool
    d_eu: float
    d_au: float
    d_g: float


def classify(
    r0: RoundState,
    rf: RoundState,
    high_eu_threshold: float,
    eps_eu: float = EPS_EU,
    eps_au: float = EPS_AU,
    eps_g: float = EPS_G,
) -> Transition:
    d_eu = rf.eu_norm - r0.eu_norm
    d_au = rf.au_norm - r0.au_norm
    d_g = rf.gold_prob - r0.gold_prob

    # outcome family
    if not r0.correct and rf.correct:
        outcome = "DEBATE_RESCUE"
    elif r0.correct and not rf.correct:
        outcome = "CORRECTNESS_LOST"
    elif r0.correct and rf.correct:
        outcome = "STABLE_SUCCESS"
    else:
        outcome = "STABLE_FAILURE"

    # uncertainty-flow family (ordered)
    if d_eu <= -eps_eu and d_g >= eps_g:
        flow = "PRODUCTIVE_CONVERGENCE"
    elif d_eu <= -eps_eu and (d_g <= -eps_g or (r0.correct and not rf.correct)):
        flow = "FALSE_CONSENSUS"
    elif d_au >= eps_au and d_g <= -eps_g:
        flow = "ALEATORIC_DESTABILIZATION"
    elif d_au <= -eps_au and d_g >= eps_g:
        flow = "NOISE_REDUCTION"
    elif abs(d_eu) < eps_eu and abs(d_au) < eps_au and abs(d_g) < eps_g:
        flow = "NO_MATERIAL_CHANGE"
    else:
        flow = "MIXED_FLOW"

    prd = (rf.eu_norm >= high_eu_threshold
           and max(rf.agent_gold_probs.values()) >= 0.5)
    cms = (max(r0.agent_gold_probs.values()) >= 0.5
           and r0.gold_prob < 0.5
           and d_g <= -eps_g)

    return Transition(
        outcome=outcome, flow=flow,
        persistent_rational_disagreement=bool(prd),
        correct_minority_suppression=bool(cms),
        d_eu=float(d_eu), d_au=float(d_au), d_g=float(d_g),
    )
