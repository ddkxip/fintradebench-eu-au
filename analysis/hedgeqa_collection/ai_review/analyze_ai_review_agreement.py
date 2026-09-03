"""Agreement analysis across the human reviewer and the two AI adjudicators.

Reads hedgeqa_core_review_merged.csv, writes AI_REVIEW_AGREEMENT_REPORT.md.

## What kappa does and does not mean here

Cohen's kappa corrects raw agreement for the agreement expected by chance
given each rater's marginal distribution. It is reported only where it is
meaningful:

  * on `gold_commitment` (3 categories) and `keep_or_exclude` (2), where
    the label set is small and shared;
  * NOT on `gold_label`, where the answer space differs per item -- 46
    distinct labels appear across the core, several unique to one question,
    so a chance-agreement baseline over a pooled label set is not defined.
    Raw agreement is reported there instead, and it is an OVERESTIMATE of
    skill because most items have 2-4 plausible labels.

Kappa is also unstable when one category dominates: if 95% of items are
`keep`, near-perfect raw agreement can yield a low kappa. Where that
happens the report says so rather than presenting the number bare.

## The correlation caveat that matters most

Gemini and ChatGPT are not independent readers. They share training data,
architecture family, and failure modes. High Gemini-ChatGPT agreement is
therefore weak evidence that an item is sound -- it is consistent with both
making the same mistake. The human-vs-AI columns carry more information than
the AI-vs-AI column, and the report is ordered to reflect that.

Usage: python analysis/hedgeqa_collection/ai_review/analyze_ai_review_agreement.py
"""

from __future__ import annotations

import collections
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

MERGED = HERE / "hedgeqa_core_review_merged.csv"
OUT = HERE / "AI_REVIEW_AGREEMENT_REPORT.md"

GEM, GPT = "gemini_antigravity", "chatgpt_codex"
MASKED = "evidence_masked_insufficient"


def norm(v):
    return (str(v).strip().lower() if v is not None else "")


def cohen_kappa(pairs):
    """pairs: [(a, b), ...] with both non-empty. -> (kappa, n, po)."""
    pairs = [(a, b) for a, b in pairs if a and b]
    n = len(pairs)
    if n == 0:
        return None, 0, None
    cats = sorted({x for p in pairs for x in p})
    if len(cats) < 2:
        return None, n, 1.0        # everyone used one category; kappa undefined
    po = sum(1 for a, b in pairs if a == b) / n
    ma = collections.Counter(a for a, _ in pairs)
    mb = collections.Counter(b for _, b in pairs)
    pe = sum((ma[c] / n) * (mb[c] / n) for c in cats)
    if abs(1 - pe) < 1e-12:
        return None, n, po
    return (po - pe) / (1 - pe), n, po


def raw_agreement(pairs):
    pairs = [(a, b) for a, b in pairs if a and b]
    if not pairs:
        return None, 0
    return sum(1 for a, b in pairs if a == b) / len(pairs), len(pairs)


def col(rows, name):
    return [norm(r.get(name, "")) for r in rows]


def pairwise(rows, a_col, b_col):
    return list(zip(col(rows, a_col), col(rows, b_col)))


def fmt(x, pct=True):
    if x is None:
        return "n/a"
    return f"{x:.1%}" if pct else f"{x:.3f}"


def section_agreement(rows, field, human_col, gem_col, gpt_col, use_kappa):
    """-> list of (comparison, n, raw, kappa)."""
    out = []
    for label, a, b in (("human vs Gemini", human_col, gem_col),
                        ("human vs ChatGPT", human_col, gpt_col),
                        ("Gemini vs ChatGPT", gem_col, gpt_col)):
        pr = pairwise(rows, a, b)
        ra, n = raw_agreement(pr)
        k = cohen_kappa(pr)[0] if use_kappa else None
        out.append((label, n, ra, k))
    return out


def main():
    if not MERGED.exists():
        raise SystemExit(f"{MERGED} not found — run merge_ai_reviews.py first")
    with MERGED.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    L, A = [], None
    A = L.append
    A("# HedgeQA-Core-v0.1 — AI-assisted review agreement report")
    A("")
    A("**These are AI-assisted audit labels, not human ground truth.** Gemini "
      "and ChatGPT are used to locate disagreement for a human to adjudicate. "
      "No item is promoted on the strength of AI agreement, and nothing in "
      "this pipeline sets `manually_validated`.")
    A("")

    n_all = len(rows)
    have_h = sum(1 for r in rows if norm(r.get("human_keep_or_exclude")))
    have_g = sum(1 for r in rows if norm(r.get(f"{GEM}__keep_or_exclude")))
    have_c = sum(1 for r in rows if norm(r.get(f"{GPT}__keep_or_exclude")))
    A("## Coverage")
    A("")
    A("| reviewer | items reviewed | of |")
    A("|---|---|---|")
    A(f"| human | {have_h} | {n_all} |")
    A(f"| gemini_antigravity | {have_g} | {n_all} |")
    A(f"| chatgpt_codex | {have_c} | {n_all} |")
    A("")
    if not (have_h and have_g and have_c):
        A("> **Incomplete.** Every figure below is computed only over items "
          "where both members of a pair recorded a label. Comparisons with "
          "zero overlap are reported as `n/a`, never as agreement.")
        A("")

    # ---------------------------------------------------------------- labels
    A("## 1. Agreement on `gold_label`")
    A("")
    A("Raw agreement only. Kappa is not defined here: the answer space is "
      "per-item and 46 distinct labels appear across the core, so there is no "
      "shared category set to compute chance agreement over. Raw agreement "
      "also **overstates skill**, because most items admit only 2-4 plausible "
      "labels.")
    A("")
    A("| comparison | n | raw agreement |")
    A("|---|---|---|")
    for lab, n, ra, _ in section_agreement(
            rows, "gold_label", "human_gold_label",
            f"{GEM}__reviewer_gold_label", f"{GPT}__reviewer_gold_label",
            use_kappa=False):
        A(f"| {lab} | {n} | {fmt(ra)} |")
    A("")

    # ----------------------------------------------------------- commitment
    A("## 2. Agreement on `gold_commitment`")
    A("")
    A("Three shared categories, so kappa is meaningful. This is the "
      "collection's load-bearing judgement; in the parent project two blinded "
      "human annotators reached only kappa 0.53-0.59 on it, so **moderate "
      "agreement here is the expected result, not a failure**.")
    A("")
    A("| comparison | n | raw agreement | Cohen kappa |")
    A("|---|---|---|---|")
    for lab, n, ra, k in section_agreement(
            rows, "gold_commitment", "human_gold_commitment",
            f"{GEM}__reviewer_gold_commitment",
            f"{GPT}__reviewer_gold_commitment", use_kappa=True):
        A(f"| {lab} | {n} | {fmt(ra)} | {fmt(k, pct=False)} |")
    A("")

    # ------------------------------------------------------ keep or exclude
    A("## 3. Agreement on `keep_or_exclude`")
    A("")
    kk = section_agreement(rows, "keep_or_exclude", "human_keep_or_exclude",
                           f"{GEM}__keep_or_exclude",
                           f"{GPT}__keep_or_exclude", use_kappa=True)
    A("| comparison | n | raw agreement | Cohen kappa |")
    A("|---|---|---|---|")
    for lab, n, ra, k in kk:
        A(f"| {lab} | {n} | {fmt(ra)} | {fmt(k, pct=False)} |")
    A("")
    keeps = collections.Counter(
        norm(r.get("human_keep_or_exclude")) for r in rows)
    if keeps.get("keep", 0) and keeps.get("exclude", 0) == 0:
        A("> Every reviewed item was kept, so kappa is undefined or "
          "degenerate on this field — with one category in use, chance "
          "agreement is 100%. Read the raw agreement, not the kappa.")
        A("")

    # ----------------------------------------------------------- by stratum
    A("## 4. Disagreement rate by stratum")
    A("")
    A("Disagreement = the two raters recorded different `gold_label`, over "
      "items where both recorded one.")
    A("")

    def dis_table(keyfn, title):
        A(f"### {title}")
        A("")
        A("| stratum | n | human-Gemini | human-ChatGPT | Gemini-ChatGPT |")
        A("|---|---|---|---|---|")
        groups = collections.defaultdict(list)
        for r in rows:
            groups[keyfn(r)].append(r)
        for g in sorted(groups):
            sub = groups[g]
            cells = []
            for a, b in (("human_gold_label", f"{GEM}__reviewer_gold_label"),
                         ("human_gold_label", f"{GPT}__reviewer_gold_label"),
                         (f"{GEM}__reviewer_gold_label",
                          f"{GPT}__reviewer_gold_label")):
                ra, n = raw_agreement(pairwise(sub, a, b))
                cells.append("n/a" if ra is None else f"{1 - ra:.1%} (n={n})")
            A(f"| {g} | {len(sub)} | " + " | ".join(cells) + " |")
        A("")

    dis_table(lambda r: r.get("source_benchmark", "?"), "By source benchmark")
    dis_table(lambda r: r.get("transformation_type", "?"),
              "By transformation type")

    A("### Masked variants specifically")
    A("")
    mk = [r for r in rows if r.get("transformation_type") == MASKED]
    A(f"{len(mk)} masked items. These carry a CONSTRUCTED gold, so the "
      "question is not only whether raters agree but whether any of them "
      "found a route to the answer.")
    A("")
    A("| comparison | n | disagreement on `masked_variant_valid` |")
    A("|---|---|---|")
    for lab, a, b in (("human vs Gemini", "human_masked_variant_valid",
                       f"{GEM}__masked_variant_valid"),
                      ("human vs ChatGPT", "human_masked_variant_valid",
                       f"{GPT}__masked_variant_valid"),
                      ("Gemini vs ChatGPT", f"{GEM}__masked_variant_valid",
                       f"{GPT}__masked_variant_valid")):
        ra, n = raw_agreement(pairwise(mk, a, b))
        A(f"| {lab} | {n} | {'n/a' if ra is None else f'{1 - ra:.1%}'} |")
    A("")
    anyno = [r for r in mk
             if any(norm(r.get(f"{who}__masked_variant_valid")) == "no"
                    for who in (GEM, GPT))
             or norm(r.get("human_masked_variant_valid")) == "no"]
    A(f"**{len(anyno)} masked item(s) had at least one reviewer report the "
      f"answer was still reachable.** Every one of these should be excluded "
      f"or re-masked; a single credible reconstruction route falsifies the "
      f"constructed gold.")
    A("")

    A("### numeric_to_directional specifically")
    A("")
    nd = [r for r in rows
          if r.get("transformation_type") == "numeric_to_directional"]
    A(f"{len(nd)} items. The failure mode here is a direction inverted by "
      "operand order, which produces a confidently wrong label.")
    A("")
    A("| comparison | n | disagreement on `transformation_valid` |")
    A("|---|---|---|")
    for lab, a, b in (("human vs Gemini", "human_transformation_valid",
                       f"{GEM}__transformation_valid"),
                      ("human vs ChatGPT", "human_transformation_valid",
                       f"{GPT}__transformation_valid"),
                      ("Gemini vs ChatGPT", f"{GEM}__transformation_valid",
                       f"{GPT}__transformation_valid")):
        ra, n = raw_agreement(pairwise(nd, a, b))
        A(f"| {lab} | {n} | {'n/a' if ra is None else f'{1 - ra:.1%}'} |")
    A("")

    # ------------------------------------------------------- flag frequency
    flags = collections.Counter()
    for r in rows:
        for who in (GEM, GPT):
            for fl in (r.get(f"{who}__flags") or "").split("|"):
                if fl.strip():
                    flags[fl.strip()] += 1
    if flags:
        A("## 5. Flags raised by AI reviewers")
        A("")
        A("| flag | count |")
        A("|---|---|")
        for k, v in flags.most_common():
            A(f"| `{k}` | {v} |")
        A("")

    # -------------------------------------------------- high-risk disagreements
    A("## 6. High-risk disagreements")
    A("")
    A("Ranked: a masked item any reviewer could answer, then a directional "
      "item whose transformation is challenged, then any three-way "
      "`gold_label` split, then commitment splits.")
    A("")
    risky = []
    for r in rows:
        hid = r["hedgeqa_id"]
        tt = r.get("transformation_type", "")
        labs = {norm(r.get("human_gold_label")),
                norm(r.get(f"{GEM}__reviewer_gold_label")),
                norm(r.get(f"{GPT}__reviewer_gold_label"))}
        labs.discard("")
        coms = {norm(r.get("human_gold_commitment")),
                norm(r.get(f"{GEM}__reviewer_gold_commitment")),
                norm(r.get(f"{GPT}__reviewer_gold_commitment"))}
        coms.discard("")
        if tt == MASKED and any(
                norm(r.get(f"{w}__masked_variant_valid")) == "no"
                for w in (GEM, GPT)):
            risky.append((0, hid, tt, "masked item reported answerable"))
        elif tt == "numeric_to_directional" and any(
                norm(r.get(f"{w}__transformation_valid")) in ("no", "unclear")
                for w in (GEM, GPT)):
            risky.append((1, hid, tt, "directional transformation challenged"))
        elif len(labs) >= 3:
            risky.append((2, hid, tt, f"three-way label split: {sorted(labs)}"))
        elif len(coms) > 1:
            risky.append((3, hid, tt,
                          f"commitment split: {sorted(coms)}"))
        elif len(labs) > 1:
            risky.append((4, hid, tt, f"label split: {sorted(labs)}"))
    risky.sort()
    if risky:
        A("| # | hedgeqa_id | transformation | issue |")
        A("|---|---|---|---|")
        for n, (_, hid, tt, why) in enumerate(risky[:60], 1):
            A(f"| {n} | `{hid}` | {tt} | {why} |")
        if len(risky) > 60:
            A("")
            A(f"…and {len(risky) - 60} more; the full list is the "
              f"`review_needed` rows of the merged CSV.")
    else:
        A("None recorded. With incomplete reviewer coverage this means "
          "*not yet computable*, not *no disagreement*.")
    A("")

    # ------------------------------------------------------ promotion classes
    A("## 7. Promotion classes")
    A("")
    cls = collections.Counter(r.get("promotion_class", "?") for r in rows)
    A("| class | items | meaning |")
    A("|---|---|---|")
    A(f"| `strong_keep` | {cls.get('strong_keep', 0)} | human + both AI kept, "
      f"commitment agrees — *eligible* for human promotion |")
    A(f"| `review_needed` | {cls.get('review_needed', 0)} | disagreement, "
      f"missing reviewer, low confidence, or an `unclear` flag |")
    A(f"| `exclude` | {cls.get('exclude', 0)} | human excluded, or both AI "
      f"reviewers excluded |")
    A("")
    A("`strong_keep` means **nobody objected**, which is weaker than "
      "verified. Two of the three raters are language models with correlated "
      "failure modes, so unanimity among them is not independent "
      "confirmation. A human still decides every promotion, and no item in "
      "this repository is `manually_validated`.")
    A("")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(L)} lines)")
    print(f"  coverage: human={have_h} gemini={have_g} chatgpt={have_c} "
          f"of {n_all}")
    print(f"  promotion: {dict(cls)}")
    print(f"  high-risk disagreements listed: {len(risky)}")


if __name__ == "__main__":
    main()
