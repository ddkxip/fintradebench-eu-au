"""Phase 1 — data audit of FinTradeBench_Golden_Seed_150.csv.

Reports row/lane counts, missingness, indicator distribution, response
lengths, and heuristic answer-type candidates per question (input to the
answer-schema design). Writes analysis/DATA_AUDIT.md.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pandas as pd

SRC = Path(r"C:\Users\ddkxi\PycharmProjects\Contrastive learning\NASDAQ processed data"
           r"\Final_benchmark\final_dataset_release\FinTradeBench_Golden_Seed_150.csv")
OUT = Path(__file__).resolve().parent / "DATA_AUDIT.md"

df = pd.read_csv(SRC)


def lane(qid: str) -> str:
    q = str(qid).upper()
    return "FT" if q.startswith("FT") else ("F" if q.startswith("F") else "T")


df["lane"] = df["question_id"].map(lane)
df["n_ind"] = df["golden_indicators"].fillna("").map(lambda s: len([x for x in str(s).split("|") if x.strip()]))
df["resp_words"] = df["response"].fillna("").map(lambda s: len(str(s).split()))
df["q_words"] = df["question"].fillna("").map(lambda s: len(str(s).split()))


def answer_type_candidate(q: str) -> str:
    s = str(q).lower()
    if re.search(r"\bwhich (company|stock|one)\b|\bcompare\b|\bversus\b|\bvs\.?\b|\bor\b.*\?\s*$", s) and re.search(r"\b[A-Z]{2,5}\b", str(q)):
        pass  # fallthrough to finer checks below
    if re.search(r"\bstrongest\b|\bweakest\b|\bbest\b|\bworst\b|\bwhich .* (most|least)\b", s):
        return "choice_superlative"
    if re.search(r"\bwhich\b.*\b(company|stock)\b", s):
        return "company_choice"
    if re.search(r"\brank\b|\border\b.*\bby\b", s):
        return "ranking_choice"
    if re.search(r"\bis\b|\bare\b|\bdoes\b|\bdo\b|\bcan\b|\bshould\b|\bwas\b|\bhas\b|\bhave\b|\bwill\b", s) and s.rstrip().endswith("?"):
        return "yes_no_mixed"
    if re.search(r"\bhow (strong|weak|risky|volatile|healthy)\b|\bhow (is|are|did|has)\b", s):
        return "graded_judgment"
    if re.search(r"\bwhy\b|\bexplain\b|\bwhat does\b|\bwhat is driving\b", s):
        return "open_summary_with_canonical_claim"
    if re.search(r"\bovervalued\b|\bundervalued\b|\bcheap\b|\bexpensive\b|\bvaluation\b", s):
        return "valuation_judgment"
    return "unclassified"


df["atype_candidate"] = df["question"].map(answer_type_candidate)

# extract capitalized company-ish tokens and explicit dates for clustering hints
date_pat = re.compile(r"\b(?:Q[1-4]\s*20\d{2}|(?:January|February|March|April|May|June|July|August|"
                      r"September|October|November|December)\s+20\d{2}|20\d{2})\b")
df["date_mentions"] = df["question"].map(lambda s: date_pat.findall(str(s)))

ind_counter = Counter()
for s in df["golden_indicators"].fillna(""):
    for x in str(s).split("|"):
        x = x.strip()
        if x:
            ind_counter[x] += 1

lines = [f"# Phase 1 data audit — Golden Seed 150\n",
         f"- rows: **{len(df)}**, duplicate question_id: {df['question_id'].duplicated().sum()}",
         f"- lanes: {df['lane'].value_counts().to_dict()}",
         f"- missing values: " + ", ".join(f"{c}={int(df[c].isna().sum())}" for c in ["question", "golden_indicators", "response"]),
         f"- golden indicators per question: min={df.n_ind.min()}, median={df.n_ind.median():.0f}, max={df.n_ind.max()}",
         f"- indicators per lane (mean): {df.groupby('lane')['n_ind'].mean().round(2).to_dict()}",
         f"- response length (words): min={df.resp_words.min()}, median={df.resp_words.median():.0f}, "
         f"max={df.resp_words.max()}; by lane median: {df.groupby('lane')['resp_words'].median().to_dict()}",
         f"- question length (words): median={df.q_words.median():.0f}",
         f"- questions with explicit date mention: {int(df['date_mentions'].map(bool).sum())}/{len(df)}",
         "\n## Indicator vocabulary (top 25)\n"]
for ind, c in ind_counter.most_common(25):
    lines.append(f"- {ind}: {c}")
lines.append(f"\n(total distinct indicators: {len(ind_counter)})")

lines.append("\n## Heuristic answer-type candidates (to be refined manually)\n")
for lane_name, g in df.groupby("lane"):
    lines.append(f"- **{lane_name}**: {g['atype_candidate'].value_counts().to_dict()}")

lines.append("\n## Sample questions per lane (first 4 each)\n")
for lane_name, g in df.groupby("lane"):
    lines.append(f"### {lane_name}")
    for _, r in g.head(4).iterrows():
        lines.append(f"- `{r.question_id}` [{r.atype_candidate}] ({r.n_ind} ind): {r.question}")

OUT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
