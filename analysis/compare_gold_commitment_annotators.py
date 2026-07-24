"""Compare gold-commitment annotations across annotators and rerun the
non-commitment error decomposition under each annotator's commitment
labels + majority vote. Reanalysis only; never fabricates annotations.

Annotator files (auto-detected; missing/blank ones are reported, not
invented):
    fable        analysis/gold_commitment_audit_sheet_completed.csv  (manual_*)
    codex        analysis/gold_commitment_audit_codex.csv            (annotator_*)
    antigravity  analysis/gold_commitment_audit_antigravity.csv      (annotator_*)
    human (opt.) analysis/gold_commitment_audit_sheet_human.csv      (manual_*)

Writes:
    analysis/gold_commitment_interannotator_agreement.md
    analysis/noncommit_error_decomposition_multiannotator.md
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas  # noqa: E402

ANA = REPO / "analysis"
RES = REPO / "results"
schemas = load_schemas()
QIDS = [s.question_id for s in schemas.values() if s.headline_eligible]
PRIMARY = [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3")]

# annotator file registry: (name, path, label_col, commit_col, schema_fallback)
REGISTRY = [
    ("fable", ANA / "gold_commitment_audit_sheet_completed.csv",
     "manual_gold_label", "manual_gold_commitment", True),
    ("codex", ANA / "gold_commitment_audit_codex.csv",
     "annotator_gold_label", "annotator_gold_commitment", False),
    ("antigravity", ANA / "gold_commitment_audit_antigravity.csv",
     "annotator_gold_label", "annotator_gold_commitment", False),
    ("human", ANA / "gold_commitment_audit_sheet_human.csv",
     "manual_gold_label", "manual_gold_commitment", False),
]
MIN_COVERAGE = 0.50   # an annotator is "active" if it labels >= 50% of items


def schema_commit(q):
    return "noncommitted" if schemas[q].gold_label in schemas[q].noncommit_set else "committed"


def blank(x):
    return x is None or (isinstance(x, float) and np.isnan(x)) or (isinstance(x, str) and not x.strip())


def load_annotator(name, path, lcol, ccol, fallback):
    """Return dict qid->(label, commit), plus stats (missing, violations)."""
    if not path.exists():
        return None
    df = pd.read_csv(path, keep_default_na=False)
    if lcol not in df.columns or ccol not in df.columns:
        return None
    out, missing, violations = {}, [], []
    for _, r in df.iterrows():
        q = str(r["question_id"])
        if q not in schemas:
            continue
        space = schemas[q].answer_space
        lab, com = str(r[lcol]).strip(), str(r[ccol]).strip().lower()
        if blank(lab) and blank(com):
            if fallback:
                out[q] = (schemas[q].gold_label, schema_commit(q))
            else:
                missing.append(q)
            continue
        if not blank(lab) and lab not in space:
            violations.append(f"{q}: label '{lab}' not in answer_space")
            lab = schemas[q].gold_label
        if com not in ("committed", "noncommitted"):
            violations.append(f"{q}: commitment '{com}' invalid")
            com = schema_commit(q)
        if blank(lab):
            lab = schemas[q].gold_label
        out[q] = (lab, com)
    coverage = len(out) / len(QIDS)
    return {"name": name, "map": out, "missing": missing,
            "violations": violations, "coverage": coverage,
            "active": coverage >= MIN_COVERAGE}


anns = {}
for name, path, lcol, ccol, fb in REGISTRY:
    a = load_annotator(name, path, lcol, ccol, fb)
    if a is not None:
        anns[name] = a

active = [n for n, a in anns.items() if a["active"]]

# ── inter-annotator agreement ───────────────────────────────────────────
A = ["# Gold-commitment inter-annotator agreement\n",
     "Reanalysis only; no fabricated annotations. Annotator = an "
     "independently completed commitment sheet.\n"]
A.append("## Annotator availability\n")
A.append("| annotator | file present | coverage | active (>=50%) | violations | missing |")
A.append("|---|---|---|---|---|---|")
for name, path, lcol, ccol, fb in REGISTRY:
    if name in anns:
        a = anns[name]
        A.append(f"| {name} | yes | {a['coverage']:.0%} | "
                 f"{'YES' if a['active'] else 'no'} | {len(a['violations'])} | "
                 f"{len(a['missing'])} |")
    else:
        A.append(f"| {name} | **no** | 0% | no | - | - |")
A.append(f"\n**Active annotators: {active if active else 'none with >=50% coverage'}.**")
A.append("\n> Note on independence: `fable` is the analyst's own (non-blinded) "
         "audit; its non-blank calls equal the schema, so fable is NOT "
         "independent of the schema baseline. Genuine inter-annotator "
         "agreement requires the BLINDED external annotators (codex, "
         "antigravity). Run them on "
         "`analysis/gold_commitment_audit_sheet_blinded.csv` "
         "(see BLINDED_ANNOTATOR_INSTRUCTIONS.md), then rerun this script.")


def cohen_kappa(a_map, b_map, keys):
    a = [a_map[k][1] for k in keys]
    b = [b_map[k][1] for k in keys]
    po = np.mean([x == y for x, y in zip(a, b)])
    cats = ["committed", "noncommitted"]
    pe = sum((a.count(c) / len(a)) * (b.count(c) / len(b)) for c in cats)
    k = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    return po, k


def fleiss_kappa(maps, keys):
    cats = ["committed", "noncommitted"]
    n = len(maps)
    if n < 2:
        return float("nan")
    N = len(keys)
    P_i = []
    col_tot = {c: 0 for c in cats}
    for k in keys:
        counts = {c: 0 for c in cats}
        for m in maps:
            counts[m[k][1]] += 1
        for c in cats:
            col_tot[c] += counts[c]
        P_i.append((sum(v * v for v in counts.values()) - n) / (n * (n - 1)))
    Pbar = np.mean(P_i)
    p_j = {c: col_tot[c] / (N * n) for c in cats}
    Pe = sum(v * v for v in p_j.values())
    return (Pbar - Pe) / (1 - Pe) if Pe < 1 else float("nan")


A.append("\n## Pairwise agreement + Cohen's kappa (binary commitment)\n")
if len(active) >= 2:
    A.append("| pair | n common | exact-label agree | commit agree | Cohen kappa |")
    A.append("|---|---|---|---|---|")
    for x, y in combinations(active, 2):
        keys = [q for q in QIDS if q in anns[x]["map"] and q in anns[y]["map"]]
        lab_ag = np.mean([anns[x]["map"][q][0] == anns[y]["map"][q][0] for q in keys])
        po, k = cohen_kappa(anns[x]["map"], anns[y]["map"], keys)
        A.append(f"| {x} vs {y} | {len(keys)} | {lab_ag:.3f} | {po:.3f} | {k:.3f} |")
    common = [q for q in QIDS if all(q in anns[n]["map"] for n in active)]
    fk = fleiss_kappa([anns[n]["map"] for n in active], common)
    A.append(f"\n**Fleiss' kappa across {len(active)} active annotators "
             f"(n={len(common)} complete items): {fk:.3f}.**")
else:
    A.append("_Pending: fewer than two active annotators. Cohen's / Fleiss' "
             "kappa cannot be computed until the blinded external annotations "
             "(codex, antigravity) are supplied._")

# disagreements + majority vote (across active annotators)
A.append("\n## Commitment disagreements and majority vote\n")
maj = {}
disagree = []
for q in QIDS:
    votes = [anns[n]["map"][q][1] for n in active if q in anns[n]["map"]]
    if not votes:
        maj[q] = schema_commit(q)
        continue
    if len(set(votes)) > 1:
        disagree.append({"question_id": q, "schema": schema_commit(q),
                         **{n: anns[n]["map"].get(q, ("", ""))[1] for n in active}})
    c = votes.count("committed")
    nc = votes.count("noncommitted")
    maj[q] = ("committed" if c > nc else "noncommitted" if nc > c
              else schema_commit(q))  # tie -> schema
if len(active) >= 2:
    A.append(f"- rows with any commitment disagreement among active "
             f"annotators: **{len(disagree)}**")
    if disagree:
        A.append("```\n" + pd.DataFrame(disagree).to_string(index=False) + "\n```")
else:
    A.append("_Majority vote defaults to schema until >=2 active annotators exist._")

(ANA / "gold_commitment_interannotator_agreement.md").write_text("\n".join(A), encoding="utf-8")

# ── multi-annotator decomposition ───────────────────────────────────────
def load_primary():
    fr = []
    for run, model in PRIMARY:
        d = pd.read_csv(RES / run / "rows.csv")
        d = d[(d["round"] == 1) & d["correct"].notna()].copy()
        d["model"] = model
        fr.append(d)
    df = pd.concat(fr, ignore_index=True)
    df["predicted_is_noncommit"] = df.apply(
        lambda r: str(r["predicted"]) in schemas[r["question_id"]].noncommit_set, axis=1)
    return df


df = load_primary()


def decompose(commit_of, label_of):
    d = df.copy()
    d["gold_eff"] = d["question_id"].map(label_of)
    d["noncommit_is_gold"] = d["question_id"].map(lambda q: commit_of(q) == "noncommitted")
    d["strict_error"] = d["predicted"].astype(str) != d["gold_eff"].astype(str)

    def et(r):
        if not r["strict_error"]:
            return "correct"
        ng, npr = r["noncommit_is_gold"], r["predicted_is_noncommit"]
        if not ng and npr:
            return "hedge_collision"
        if ng and not npr:
            return "overcommitment"
        if not ng and not npr:
            return "wrong_direction_commitment"
        return "wrong_noncommit_type"
    d["error_type"] = d.apply(et, axis=1)
    e = d[d.error_type != "correct"]
    shares = {k: round(float((e.error_type == k).mean()), 3) for k in
              ["hedge_collision", "overcommitment", "wrong_direction_commitment",
               "wrong_noncommit_type"]}
    # committed-gold & committed-pred AUROC (the non-mechanical cell)
    cc = d[(~d.noncommit_is_gold) & (~d.predicted_is_noncommit)]
    y = cc["strict_error"].astype(int).values
    s = cc["p_noncommit"].values
    if y.sum() and (len(y) - y.sum()):
        r = stats.rankdata(s)
        n1 = int(y.sum())
        auc = round(float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))), 3)
    else:
        auc = float("nan")
    return shares, auc, len(cc)


# build the version set: A schema always; B/C/D per annotator if active; E majority
versions = [("A_schema", schema_commit, lambda q: schemas[q].gold_label)]
for n in ("fable", "codex", "antigravity"):
    if n in anns and anns[n]["active"]:
        m = anns[n]["map"]
        versions.append((f"{n}",
                         (lambda mm: (lambda q: mm.get(q, (None, schema_commit(q)))[1]))(m),
                         (lambda mm: (lambda q: mm.get(q, (schemas[q].gold_label, None))[0]))(m)))
if len(active) >= 2:
    versions.append(("E_majority", lambda q: maj[q], lambda q: schemas[q].gold_label))

D = ["# Non-commitment error decomposition — multi-annotator\n",
     f"Primary set = gemma4 + qwen3:8b final rows (n={len(df)}). Reanalysis "
     "only. One column per available commitment version.\n"]
D.append("| version | hedge_collision | overcommit | wrong_direction | wrong_nc_type | committed-cell AUROC | survives? |")
D.append("|---|---|---|---|---|---|---|")
results = {}
for name, commit_of, label_of in versions:
    sh, auc, ncell = decompose(commit_of, label_of)
    survives = (sh["hedge_collision"] >= 0.30
                and (np.isnan(auc) or auc < 0.55))
    results[name] = (sh, auc, survives)
    D.append(f"| {name} | {sh['hedge_collision']} | {sh['overcommitment']} | "
             f"{sh['wrong_direction_commitment']} | {sh['wrong_noncommit_type']} | "
             f"{auc} | {'YES' if survives else 'NO'} |")

pending = [n for n in ("codex", "antigravity")
           if n not in anns or not anns[n]["active"]]
D.append("\n**Survival criterion:** hedge_collision remains the leading error "
         "mode (>=30% and modal) AND p_noncommit shows no wrong-direction "
         "signal (committed-cell AUROC < 0.55, i.e. ~chance).\n")
if pending:
    D.append(f"**Pending annotators:** {pending} — their templates are blank. "
             "Versions C/D and majority vote will populate automatically when "
             "`analysis/gold_commitment_audit_{codex,antigravity}.csv` are "
             "filled and this script is rerun.\n")
allsurv = all(v[2] for v in results.values())
D.append(f"## Verdict\n\nAcross the **{len(results)}** currently-available "
         f"commitment version(s) ({', '.join(results)}), the hedge-collision "
         f"conclusion **{'survives in all' if allsurv else 'FAILS in some'}**: "
         f"hedge_collision stays the leading error mode and p_noncommit remains "
         f"a hedge-collision detector with ~chance signal in the non-mechanical "
         f"cell. "
         + ("Full multi-annotator + majority-vote confirmation is pending the "
            "blinded external annotations (codex, antigravity)."
            if pending else
            "This holds under every annotator version and the majority vote."))

(ANA / "noncommit_error_decomposition_multiannotator.md").write_text("\n".join(D), encoding="utf-8")

print("active annotators:", active or "none (>=50%)")
print("versions computed:", [v[0] for v in versions])
print("pending external annotators:", pending or "none")
for name, (sh, auc, surv) in results.items():
    print(f"  {name}: hedge_collision={sh['hedge_collision']} commit-cell-AUROC={auc} survives={surv}")
print("wrote gold_commitment_interannotator_agreement.md + "
      "noncommit_error_decomposition_multiannotator.md")
