"""The 8 mandated unit tests for the EU/AU engine + transition classifier."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.eu_au import counts_to_dist, decompose, entropy, gold_metrics
from src.transitions import RoundState, classify

SPACE = ["yes", "no", "mixed"]


def dist(*p):
    return np.array(p, dtype=float)


def test_1_identical_agents_zero_eu():
    d = decompose({"f": dist(0.5, 0.3, 0.2), "t": dist(0.5, 0.3, 0.2)})
    assert abs(d.eu) < 1e-12
    assert abs(d.tu - d.au) < 1e-12


def test_2_deterministic_disagreement_high_eu():
    d = decompose({"f": dist(1, 0, 0), "t": dist(0, 1, 0)})
    assert abs(d.au) < 1e-9
    assert abs(d.eu - np.log(2)) < 1e-9  # two-agent max = log 2


def test_3_one_uncertain_one_certain_positive_au():
    d = decompose({"f": dist(1 / 3, 1 / 3, 1 / 3), "t": dist(1, 0, 0)})
    assert d.au > 0
    assert d.eu > 0
    assert abs(d.au - entropy(dist(1 / 3, 1 / 3, 1 / 3)) / 2) < 1e-9


def test_4_mixture_entropy_geq_au():
    rng = np.random.default_rng(0)
    for _ in range(200):
        a = rng.dirichlet(np.ones(4))
        b = rng.dirichlet(np.ones(4))
        d = decompose({"f": a, "t": b})
        assert d.tu >= d.au - 1e-12


def test_5_eu_equals_tu_minus_au():
    rng = np.random.default_rng(1)
    for _ in range(200):
        d = decompose({"f": rng.dirichlet(np.ones(5)),
                       "t": rng.dirichlet(np.ones(5)),
                       "j": rng.dirichlet(np.ones(5))})
        assert abs((d.tu - d.au) - d.eu) < 1e-10


def test_6_gold_probability():
    labels_f = ["yes"] * 6 + ["no"] * 2 + ["mixed"] * 2
    labels_t = ["yes"] * 3 + ["no"] * 7
    pf = counts_to_dist(labels_f, SPACE)
    pt = counts_to_dist(labels_t, SPACE)
    d = decompose({"f": pf, "t": pt})
    gm = gold_metrics(d.p_sys, SPACE, "yes")
    assert abs(gm.gold_prob - (0.6 + 0.3) / 2) < 1e-12
    assert gm.predicted == "yes" and gm.correct
    assert 0 <= gm.brier <= 2 and gm.nll > 0


def _rs(eu, au, g, correct, agent_g):
    return RoundState(eu_norm=eu, au_norm=au, gold_prob=g, correct=correct,
                      agent_gold_probs=agent_g)


def test_7_false_consensus_classifier():
    r0 = _rs(0.60, 0.30, 0.55, True, {"f": 0.8, "t": 0.3})
    rf = _rs(0.10, 0.30, 0.20, False, {"f": 0.2, "t": 0.2})
    tr = classify(r0, rf, high_eu_threshold=0.5)
    assert tr.flow == "FALSE_CONSENSUS"
    assert tr.outcome == "CORRECTNESS_LOST"
    assert tr.correct_minority_suppression is False  # r0 gold_prob >= .5


def test_7b_correct_minority_suppression():
    r0 = _rs(0.60, 0.30, 0.40, False, {"f": 0.9, "t": 0.1})
    rf = _rs(0.10, 0.30, 0.15, False, {"f": 0.2, "t": 0.1})
    tr = classify(r0, rf, high_eu_threshold=0.5)
    assert tr.correct_minority_suppression is True


def test_8_productive_convergence_classifier():
    r0 = _rs(0.55, 0.35, 0.45, False, {"f": 0.7, "t": 0.2})
    rf = _rs(0.15, 0.30, 0.80, True, {"f": 0.85, "t": 0.75})
    tr = classify(r0, rf, high_eu_threshold=0.5)
    assert tr.flow == "PRODUCTIVE_CONVERGENCE"
    assert tr.outcome == "DEBATE_RESCUE"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} tests passed")
