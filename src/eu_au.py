"""EU/AU decomposition engine.

Definitions (EU_AU_DECOMPOSITION.md): for agents i = 1..N with label
distributions p_i over answer space Y,

    p_sys = (1/N) sum_i p_i
    TU = H(p_sys);  AU = (1/N) sum_i H(p_i);  EU = TU - AU  (>= 0)

Distributions are self-consistency frequencies over K decodes.
Miller-Madow bias correction available for plug-in entropies.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

import numpy as np

EPS = 1e-12


def counts_to_dist(labels: list[str], answer_space: list[str]) -> np.ndarray:
    """Frequency distribution over answer_space from parsed labels.

    Labels not in the space are ignored (callers track them as parse
    failures before this point).
    """
    idx = {y: j for j, y in enumerate(answer_space)}
    c = np.zeros(len(answer_space), dtype=float)
    for lab in labels:
        j = idx.get(lab)
        if j is not None:
            c[j] += 1.0
    total = c.sum()
    if total == 0:
        raise ValueError("no in-space labels; cannot form a distribution")
    return c / total


def entropy(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    p = p / p.sum()
    q = np.clip(p, EPS, 1.0)
    return float(-(p * np.log(q)).sum())


def miller_madow(p: np.ndarray, k: int) -> float:
    """Plug-in entropy + Miller-Madow bias correction for K samples."""
    if k <= 0:
        raise ValueError("k must be positive")
    m = int((np.asarray(p) > EPS).sum())  # observed support size
    return entropy(p) + (m - 1) / (2.0 * k)


@dataclass
class Decomposition:
    tu: float
    au: float
    eu: float
    tu_mm: float | None
    au_mm: float | None
    eu_mm: float | None
    tu_norm: float
    au_norm: float
    eu_norm: float
    p_sys: np.ndarray = field(repr=False)
    agent_entropies: dict[str, float] = field(default_factory=dict)


def decompose(
    agent_dists: dict[str, np.ndarray],
    k_effective: dict[str, int] | None = None,
) -> Decomposition:
    """TU/AU/EU over uniform-weight agent mixture.

    agent_dists: agent name -> distribution over the shared answer space.
    k_effective: agent name -> number of decodes behind the frequency
        estimate (enables Miller-Madow); None disables the correction.
    """
    names = list(agent_dists)
    if len(names) < 2:
        raise ValueError("need >= 2 agents for a between-agent decomposition")
    P = np.array([np.asarray(agent_dists[a], dtype=float) for a in names])
    if P.ndim != 2 or len({p.shape[0] for p in P}) != 1:
        raise ValueError("agent distributions must share one answer space")
    P = P / P.sum(axis=1, keepdims=True)

    p_sys = P.mean(axis=0)
    h_agents = {a: entropy(P[j]) for j, a in enumerate(names)}
    tu = entropy(p_sys)
    au = float(np.mean(list(h_agents.values())))
    eu = max(tu - au, 0.0)  # clip -1e-16 artifacts only

    tu_mm = au_mm = eu_mm = None
    if k_effective is not None:
        ks = [k_effective[a] for a in names]
        au_mm = float(np.mean([miller_madow(P[j], ks[j]) for j in range(len(names))]))
        tu_mm = miller_madow(p_sys, int(np.sum(ks)))
        # EU as JSD is *less* biased than TU - AU_mm suggests; keep the raw
        # difference but floor at 0 and flag: MM primarily matters for AU
        # levels and lane comparisons, not for EU.
        eu_mm = max(tu_mm - au_mm, 0.0)

    logy = float(np.log(P.shape[1])) if P.shape[1] > 1 else 1.0
    return Decomposition(
        tu=tu, au=au, eu=eu,
        tu_mm=tu_mm, au_mm=au_mm, eu_mm=eu_mm,
        tu_norm=tu / logy, au_norm=au / logy, eu_norm=eu / logy,
        p_sys=p_sys, agent_entropies=h_agents,
    )


# ── ground-truth alignment ───────────────────────────────────────────────


@dataclass
class GoldMetrics:
    gold_prob: float
    predicted: str
    correct: bool
    brier: float
    nll: float


def gold_metrics(
    p_sys: np.ndarray,
    answer_space: list[str],
    gold_label: str,
    smoothing: float = 0.5,
) -> GoldMetrics:
    if gold_label not in answer_space:
        raise ValueError(f"gold label {gold_label!r} not in answer space")
    p = np.asarray(p_sys, dtype=float)
    p = p / p.sum()
    gi = answer_space.index(gold_label)
    onehot = np.zeros_like(p)
    onehot[gi] = 1.0
    pred = answer_space[int(np.argmax(p))]
    # Jeffreys-smoothed NLL so empty gold cells stay finite
    p_smooth = (p * len(p) + smoothing) / (len(p) + smoothing * len(p))
    p_smooth = p_smooth / p_smooth.sum()
    return GoldMetrics(
        gold_prob=float(p[gi]),
        predicted=pred,
        correct=pred == gold_label,
        brier=float(((p - onehot) ** 2).sum()),
        nll=float(-np.log(p_smooth[gi])),
    )


def bootstrap_ci(
    labels_per_agent: dict[str, list[str]],
    answer_space: list[str],
    n_boot: int = 500,
    seed: int = 42,
) -> dict[str, tuple[float, float]]:
    """Percentile bootstrap CIs (2.5/97.5) for TU/AU/EU by resampling each
    agent's K decodes with replacement."""
    rng = np.random.default_rng(seed)
    stats = {"tu": [], "au": [], "eu": []}
    names = list(labels_per_agent)
    for _ in range(n_boot):
        dists = {}
        ok = True
        for a in names:
            labs = labels_per_agent[a]
            res = [labs[i] for i in rng.integers(0, len(labs), len(labs))]
            try:
                dists[a] = counts_to_dist(res, answer_space)
            except ValueError:
                ok = False
                break
        if not ok:
            continue
        d = decompose(dists)
        stats["tu"].append(d.tu)
        stats["au"].append(d.au)
        stats["eu"].append(d.eu)
    return {k: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))
            for k, v in stats.items() if v}


def majority_vote(labels: list[str]) -> str:
    return Counter(labels).most_common(1)[0][0]
