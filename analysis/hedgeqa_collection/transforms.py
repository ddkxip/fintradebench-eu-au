"""Question transformations shared by the TAT-QA / FinQA / ConvFinQA builders.

TAT-QA, FinQA and ConvFinQA are numeric-answer datasets. A free-form numeric
answer has no finite answer space, so none of the hedging metrics are
computable on it as written: there is no "non-committal label" for a number.

Two transformations give these items a finite space while preserving the
original question and the derivation that licences the rewrite:

  numeric_to_directional
      A question whose gold answer is a *change* becomes a direction
      question over {increased, decreased, roughly_unchanged,
      insufficient_data}. Licensed only when the source question is already
      asking about a change, so we are not inventing a new task.

  comparison_to_choice
      A question comparing named entities becomes pick-one over those
      entities plus a non-committal label.

Both record `original_question` and `derivation`, which the schema validator
requires. Items that do not cleanly fit either pattern are skipped -- a
forced transformation would silently change what the question asks.
"""

from __future__ import annotations

import re

DIRECTIONAL_SPACE = ["increased", "decreased", "roughly_unchanged",
                     "insufficient_data"]
DIRECTIONAL_NONCOMMIT = ["roughly_unchanged", "insufficient_data"]

# Direction-NEUTRAL phrasings only. The sign of the source answer may be
# read as a direction only when the question itself does not already assert
# one.
CHANGE_CUES = ("change in", "net change", "changes in", "percentage change",
               "percent change", "growth rate", "change of", "change from",
               "change between", "what was the change")

# Phrasings that PRESUPPOSE a direction. Datasets report the magnitude of
# such a quantity as a POSITIVE number ("what percentage decrease occurred"
# -> 96.55), so a sign-based mapping yields exactly the wrong label. These
# are rejected outright rather than sign-flipped: the convention is not
# consistent across the corpora, and guessing it would trade a visible skip
# for an invisible wrong gold.
DIRECTION_PRESUPPOSING = (
    "increase in", "decrease in", "decline in", "drop in", "growth in",
    "reduction in", "percentage decrease", "percentage increase",
    "percent decrease", "percent increase", "rate of increase",
    "rate of decrease", "how much did", "rose by", "fell by", "grew by",
    "declined by", "increased by", "decreased by",
)

# Cross-sectional comparisons: "difference between A and B" is not a change
# over time, so no direction label applies.
CROSS_SECTIONAL = ("difference between", "difference in", "gap between",
                   "variance between", "compared with the", "as opposed to")

COMPARE_CUES = ("compared to", "versus", " vs ", "higher", "lower",
                "greater", "larger", "smaller", "more than", "less than")

# A change smaller than this (relative) reads as "roughly unchanged".
FLAT_BAND = 0.005


def _to_float(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "").replace("$", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()").rstrip("%")
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def is_change_question(q: str) -> bool:
    """True only for direction-NEUTRAL temporal change questions.

    Rejects (a) questions presupposing a direction, whose magnitude is
    reported positive regardless of which way it moved, and (b)
    cross-sectional differences, which are not changes over time at all.
    """
    ql = (q or "").lower()
    if any(c in ql for c in DIRECTION_PRESUPPOSING):
        return False
    if any(c in ql for c in CROSS_SECTIONAL):
        return False
    return any(c in ql for c in CHANGE_CUES)


def change_question_reject_reason(q: str) -> str:
    """Why a question was not usable, for the builders' stats."""
    ql = (q or "").lower()
    if any(c in ql for c in DIRECTION_PRESUPPOSING):
        return "presupposes a direction (magnitude reported positive)"
    if any(c in ql for c in CROSS_SECTIONAL):
        return "cross-sectional difference, not a change over time"
    if not any(c in ql for c in CHANGE_CUES):
        return "not a change question"
    return "other"


def is_comparison_question(q: str) -> bool:
    ql = (q or "").lower()
    return any(c in ql for c in COMPARE_CUES)


def numeric_to_directional(question: str, answer, derivation: str = "",
                           scale: str = ""):
    """Map a numeric change answer onto a direction label.

    Returns (answer_space, noncommit, gold_label, derivation_text) or None
    when the item does not qualify.
    """
    if not is_change_question(question):
        return None
    val = _to_float(answer)
    if val is None:
        return None

    if abs(val) == 0:
        gold = "roughly_unchanged"
    elif val > 0:
        gold = "increased"
    else:
        gold = "decreased"

    # A percentage answer near zero is "roughly unchanged" rather than a
    # direction; for absolute magnitudes we have no denominator, so we only
    # apply the band when the source says the answer is a percent.
    if (scale or "").lower() in ("percent", "percentage", "%"):
        if abs(val) < FLAT_BAND * 100:
            gold = "roughly_unchanged"

    text = (f"numeric_to_directional: the source answer {answer!r}"
            + (f" (scale={scale})" if scale else "")
            + f" is a change, mapped to {gold!r}. "
            + (f"Source derivation: {derivation}" if derivation else
               "No source derivation supplied."))
    return DIRECTIONAL_SPACE, DIRECTIONAL_NONCOMMIT, gold, text


def comparison_to_choice(question: str, entities, gold_entity: str,
                         derivation: str = ""):
    """Map an entity comparison onto pick-one over the named entities."""
    ents = [e for e in dict.fromkeys(entities) if e]
    if len(ents) < 2 or gold_entity not in ents:
        return None
    space = list(ents) + ["none_clear", "insufficient_data"]
    nc = ["none_clear", "insufficient_data"]
    text = (f"comparison_to_choice: the source compares {ents}; the gold "
            f"answer identifies {gold_entity!r}. "
            + (f"Source derivation: {derivation}" if derivation else
               "No source derivation supplied."))
    return space, nc, gold_entity, text


def table_to_text(table) -> str:
    """Render a TAT-QA / FinQA style list-of-rows table as aligned text."""
    if not table:
        return ""
    rows = []
    for r in table:
        if isinstance(r, (list, tuple)):
            rows.append(" | ".join(str(c).strip() for c in r))
        else:
            rows.append(str(r))
    return "\n".join(rows)


def clean_ws(s: str) -> str:
    return re.sub(r"[ \t]+", " ", (s or "")).strip()


def stratified_sample(items, key, target, seed=20260820):
    """Seeded, label-balanced subsample.

    Two reasons this is not just `items[:target]`:

    * **Document order is not random.** These corpora group questions by
      filing and company, so a head slice over-represents a handful of
      documents.
    * **The direction labels are skewed.** TAT-QA eligible items are ~62%
      "increased", FinQA ~64%. Sampling proportionally would carry that
      prior into the collection, where a system that always answers
      "increased" would score ~63% without reasoning at all -- a degenerate
      baseline that makes the diagnostic easy to pass for the wrong reason.

    So: take every item from scarce classes, then fill the remainder equally
    from the abundant ones. The realised composition is returned rather than
    assumed, since perfect balance is usually impossible (TAT-QA has only 76
    "roughly_unchanged" items in total, FinQA only 9).
    """
    import collections
    import random

    rng = random.Random(seed)
    buckets = collections.defaultdict(list)
    for it in items:
        buckets[key(it)].append(it)
    for v in buckets.values():
        v.sort(key=lambda x: getattr(x, "hedgeqa_id", str(x)))

    chosen, remaining = [], target
    # scarce classes first: anything that cannot fill its equal share
    order = sorted(buckets, key=lambda k: len(buckets[k]))
    for i, k in enumerate(order):
        share = remaining // (len(order) - i)
        take = min(share, len(buckets[k]))
        chosen.extend(rng.sample(buckets[k], take) if take < len(buckets[k])
                      else list(buckets[k]))
        remaining -= take
    chosen.sort(key=lambda x: getattr(x, "hedgeqa_id", str(x)))
    realised = collections.Counter(key(it) for it in chosen)
    return chosen, dict(realised)
