"""Local Streamlit app for the HedgeQA-Core-v0.1 human review.

Run:
    streamlit run analysis/hedgeqa_collection/review_app.py

## Blinding

The whole point of this review is an independent human judgement, so the app
must never show anything that would anchor it. Three sources of leakage are
closed here, and the first two are easy to miss:

1. **The candidate JSONL carries the pipeline's answers** -- `gold_label`,
   `gold_commitment`, `validation_status`, `schema_confidence`. Items are
   projected through `blind_item()` into a dict containing ONLY the allowed
   keys, so the blinded values never enter app state and cannot be rendered
   by any widget.

2. **The manual-review CSV carries `gold_label_auto` and
   `gold_commitment_auto`** (columns 10 and 13). These are dropped on load,
   and the in-progress working file is written WITHOUT them, so even opening
   the working CSV in a spreadsheet mid-review does not expose them. They
   are re-joined from the original CSV only at final export, where the
   downstream merger expects that schema.

3. **`derivation` restates the answer in prose.** For a directional item it
   reads "...the source answer -7.6 ... mapped to 'decreased'"; for a masked
   item it names the removed operands. Both are passed through the same
   sanitisers used for the AI blind batches, so the reviewer sees the source
   arithmetic (which they need to check operand order) but not our computed
   direction, and is told rows were removed but not which.

The app also never reads `ai_review/responses/`, `ai_review/reveal/`, or
`masked_content`, and computes no agreement.

## Files

reads   data/hedgeqa/hedgeqa_core_v0_1_candidates.jsonl        (never written)
reads   analysis/.../hedgeqa_core_v0_1_manual_review.csv        (never written)
writes  analysis/.../hedgeqa_core_v0_1_human_review_in_progress.csv
writes  analysis/.../review_backups/<timestamp>.csv
writes  analysis/.../hedgeqa_core_v0_1_manual_review_completed.csv (on export)
"""

from __future__ import annotations

import csv
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

CORE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_candidates.jsonl"
ORIG_CSV = HERE / "hedgeqa_core_v0_1_manual_review.csv"
WORK_CSV = HERE / "hedgeqa_core_v0_1_human_review_in_progress.csv"
DONE_CSV = HERE / "hedgeqa_core_v0_1_manual_review_completed.csv"
BACKUPS = HERE / "review_backups"

MASKED = "evidence_masked_insufficient"
DIRECTIONAL = "numeric_to_directional"

# Never enters app state.
BLINDED = ("gold_label", "gold_commitment", "validation_status",
           "schema_confidence", "masked_content", "exclusion_reason")
BLINDED_CSV_COLS = ("gold_label_auto", "gold_commitment_auto")

REVIEW_FIELDS = ["reviewer_gold_label", "reviewer_gold_commitment",
                 "evidence_sufficient_for_gold", "transformation_valid",
                 "masked_variant_valid", "keep_or_exclude",
                 "exclusion_reason", "notes"]
EXTRA_FIELDS = ["flags", "review_status", "reviewed_at"]

MASK_FLAGS = ["rollforward_reconstruction", "total_minus_components",
              "figure_repeated_elsewhere", "direction_stated_in_prose",
              "adjacent_period_proxy", "evidence_gutted", "other"]
DIR_FLAGS = ["operand_order_suspect", "question_presupposes_direction",
             "cross_sectional_not_temporal", "wrong_entity_or_period",
             "other"]

NEUTRAL_MASK_NOTE = (
    "Controlled-insufficient variant: some evidence rows were removed from "
    "the source document. You are not told which rows or which figures. "
    "Decide from the evidence below whether the question can still be "
    "answered."
)


def sanitize_derivation(text: str, transformation: str) -> str:
    """Strip our computed answer/label; keep what the reviewer must check."""
    if transformation == MASKED:
        return NEUTRAL_MASK_NOTE
    if transformation != DIRECTIONAL or not text:
        return ""
    marker = "Source derivation:"
    tail = text.split(marker, 1)[1].strip() if marker in text else ""
    if not tail or tail.lower().startswith("no source derivation"):
        return ("The source supplies no explicit derivation. Judge the "
                "direction from the evidence alone.")
    return "Source arithmetic as stated by the originating benchmark: " + tail


def blind_item(raw: dict) -> dict:
    """Project a raw JSONL record onto the fields the reviewer may see."""
    return {
        "hedgeqa_id": raw.get("hedgeqa_id", ""),
        "source_benchmark": raw.get("source_benchmark", ""),
        "source_id": raw.get("source_id", ""),
        "transformation_type": raw.get("transformation_type", ""),
        "answer_type": raw.get("answer_type", ""),
        "question": raw.get("question", ""),
        "original_question": raw.get("original_question") or "",
        "answer_space": list(raw.get("answer_space", [])),
        "noncommit_labels": list(raw.get("noncommit_labels", [])),
        "oracle_evidence": raw.get("oracle_evidence", ""),
        "derivation": sanitize_derivation(raw.get("derivation") or "",
                                          raw.get("transformation_type", "")),
    }


@st.cache_data(show_spinner=False)
def load_items():
    out = {}
    with CORE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                d = blind_item(json.loads(line))
                out[d["hedgeqa_id"]] = d
    # hard guarantee: no blinded key survived the projection
    for d in out.values():
        leaked = [k for k in BLINDED if k in d]
        if leaked:
            raise RuntimeError(f"blinding failure: {leaked}")
    return out


def _blank_row(hid, item):
    return {
        "hedgeqa_id": hid,
        "source_benchmark": item["source_benchmark"],
        "source_id": item["source_id"],
        "evidence_hash": "",
        "transformation_type": item["transformation_type"],
        "answer_type": item["answer_type"],
        "question": item["question"],
        "original_question": item["original_question"],
        "answer_space": "|".join(item["answer_space"]),
        "noncommit_labels": "|".join(item["noncommit_labels"]),
        **{k: "" for k in REVIEW_FIELDS},
        "flags": "", "review_status": "unreviewed", "reviewed_at": "",
    }


def work_columns():
    return (["hedgeqa_id", "source_benchmark", "source_id", "evidence_hash",
             "transformation_type", "answer_type", "question",
             "original_question", "answer_space", "noncommit_labels"]
            + REVIEW_FIELDS + EXTRA_FIELDS)


def load_work(items):
    """Working rows: resume in-progress, else seed from the original CSV."""
    rows = {}
    if WORK_CSV.exists():
        with WORK_CSV.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                rows[r["hedgeqa_id"]] = r
    elif ORIG_CSV.exists():
        with ORIG_CSV.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                for c in BLINDED_CSV_COLS:      # never carried forward
                    r.pop(c, None)
                r.setdefault("flags", "")
                r.setdefault("review_status", "unreviewed")
                r.setdefault("reviewed_at", "")
                r.pop("oracle_evidence_preview", None)
                rows[r["hedgeqa_id"]] = r
    for hid, it in items.items():
        if hid not in rows:
            rows[hid] = _blank_row(hid, it)
        for c in work_columns():
            rows[hid].setdefault(c, "")
    return rows


def save_work(rows, make_backup=True):
    cols = work_columns()
    if make_backup and WORK_CSV.exists():
        BACKUPS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy(WORK_CSV, BACKUPS / f"in_progress_{stamp}.csv")
        keep = sorted(BACKUPS.glob("in_progress_*.csv"))
        for old in keep[:-40]:                  # keep the last 40
            old.unlink()
    tmp = WORK_CSV.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for hid in sorted(rows):
            w.writerow({c: rows[hid].get(c, "") for c in cols})
    tmp.replace(WORK_CSV)                        # atomic-ish


def validate(row, item):
    errs = []
    lab = (row.get("reviewer_gold_label") or "").strip()
    if not lab:
        errs.append("reviewer_gold_label is required")
    elif lab not in item["answer_space"]:
        errs.append(f"reviewer_gold_label {lab!r} is not in the answer space")
    if not (row.get("reviewer_gold_commitment") or "").strip():
        errs.append("reviewer_gold_commitment is required")
    if not (row.get("evidence_sufficient_for_gold") or "").strip():
        errs.append("evidence_sufficient_for_gold is required")
    if (row.get("keep_or_exclude") or "").strip() == "exclude" and not (
            row.get("exclusion_reason") or "").strip():
        errs.append("exclusion_reason is required when excluding")
    if item["transformation_type"] == MASKED and not (
            row.get("masked_variant_valid") or "").strip():
        errs.append("masked_variant_valid is required for a masked item")
    if item["transformation_type"] == DIRECTIONAL and not (
            row.get("transformation_valid") or "").strip():
        errs.append("transformation_valid is required for a directional item")
    return errs


def export_completed(rows):
    """Re-join the auto columns so the file matches the downstream schema."""
    if not ORIG_CSV.exists():
        return None, "original review CSV not found"
    with ORIG_CSV.open(encoding="utf-8", newline="") as f:
        orig = {r["hedgeqa_id"]: r for r in csv.DictReader(f)}
        cols = list(next(iter(orig.values())).keys())
    extra = [c for c in ("flags", "review_status", "reviewed_at")
             if c not in cols]
    with DONE_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols + extra, extrasaction="ignore")
        w.writeheader()
        for hid in sorted(rows):
            base = dict(orig.get(hid, {}))
            for k in REVIEW_FIELDS + EXTRA_FIELDS:
                base[k] = rows[hid].get(k, "")
            w.writerow(base)
    return DONE_CSV, None


# --------------------------------------------------------------------- app

st.set_page_config(page_title="HedgeQA-Core review", layout="wide")

items = load_items()
if "rows" not in st.session_state:
    st.session_state.rows = load_work(items)
    st.session_state.idx = 0
    st.session_state.msg = None
rows = st.session_state.rows

# ------------------------------------------------------------- sidebar
st.sidebar.title("HedgeQA-Core-v0.1")
st.sidebar.caption("Human review — blind. Pipeline and AI labels are hidden.")

st.sidebar.subheader("Filters")
f_unrev = st.sidebar.checkbox("Unreviewed only", value=True)
fam = st.sidebar.radio("Family", ["all", "masked only",
                                  "numeric_to_directional only",
                                  "natural only"], index=0)
f_noncommit = st.sidebar.checkbox("Has a non-committal label available")
benches = ["all"] + sorted({i["source_benchmark"] for i in items.values()})
f_bench = st.sidebar.selectbox("Source benchmark", benches)
f_status = st.sidebar.selectbox("Keep/exclude status",
                                ["all", "keep", "exclude", "unset"])
f_second = st.sidebar.checkbox("Needs second look only")


def visible_ids():
    out = []
    for hid in sorted(items):
        it, r = items[hid], rows.get(hid, {})
        status = (r.get("review_status") or "unreviewed")
        if f_unrev and status in ("reviewed",):
            continue
        if fam == "masked only" and it["transformation_type"] != MASKED:
            continue
        if (fam == "numeric_to_directional only"
                and it["transformation_type"] != DIRECTIONAL):
            continue
        if fam == "natural only" and it["transformation_type"] != "none":
            continue
        if f_noncommit and not it["noncommit_labels"]:
            continue
        if f_bench != "all" and it["source_benchmark"] != f_bench:
            continue
        ke = (r.get("keep_or_exclude") or "").strip()
        if f_status == "keep" and ke != "keep":
            continue
        if f_status == "exclude" and ke != "exclude":
            continue
        if f_status == "unset" and ke:
            continue
        if f_second and status != "second_look":
            continue
        out.append(hid)
    return out


vis = visible_ids()

st.sidebar.subheader("Progress")
done = [h for h, r in rows.items() if r.get("review_status") == "reviewed"]
st.sidebar.metric("Reviewed", f"{len(done)} / {len(items)}")
st.sidebar.progress(len(done) / max(1, len(items)))
st.sidebar.write(f"Remaining: **{len(items) - len(done)}**")
st.sidebar.write(f"Matching current filters: **{len(vis)}**")

by_src, by_fam = {}, {"masked": 0, "directional": 0, "natural": 0}
ke_counts = {"keep": 0, "exclude": 0, "unclear/unset": 0}
for h in done:
    it = items[h]
    by_src[it["source_benchmark"]] = by_src.get(it["source_benchmark"], 0) + 1
    if it["transformation_type"] == MASKED:
        by_fam["masked"] += 1
    elif it["transformation_type"] == DIRECTIONAL:
        by_fam["directional"] += 1
    else:
        by_fam["natural"] += 1
    ke = (rows[h].get("keep_or_exclude") or "").strip()
    ke_counts[ke if ke in ("keep", "exclude") else "unclear/unset"] += 1

st.sidebar.caption("Reviewed by source")
for k in sorted(by_src):
    st.sidebar.write(f"- {k}: {by_src[k]}")
st.sidebar.caption("Reviewed by family")
st.sidebar.write(f"- masked: {by_fam['masked']}  ·  "
                 f"directional: {by_fam['directional']}  ·  "
                 f"natural: {by_fam['natural']}")
st.sidebar.caption("Decisions so far")
st.sidebar.write(f"- keep: {ke_counts['keep']}  ·  "
                 f"exclude: {ke_counts['exclude']}  ·  "
                 f"unset: {ke_counts['unclear/unset']}")
st.sidebar.write(f"- needs second look: "
                 f"{sum(1 for r in rows.values() if r.get('review_status') == 'second_look')}")
st.sidebar.write(f"- skipped: "
                 f"{sum(1 for r in rows.values() if r.get('review_status') == 'skipped')}")

st.sidebar.divider()
if st.sidebar.button("Export completed review", use_container_width=True):
    p, err = export_completed(rows)
    if err:
        st.sidebar.error(err)
    else:
        n_done = len(done)
        st.sidebar.success(f"Exported {len(rows)} rows ({n_done} reviewed) "
                           f"to {p.name}")
        if n_done < len(items):
            st.sidebar.warning(f"{len(items) - n_done} item(s) are still "
                               f"unreviewed; they exported blank.")

# --------------------------------------------------------------- main
if not vis:
    st.info("No items match the current filters.")
    st.stop()

st.session_state.idx = max(0, min(st.session_state.idx, len(vis) - 1))
hid = vis[st.session_state.idx]
item, row = items[hid], rows[hid]

if st.session_state.msg:
    kind, text = st.session_state.msg
    getattr(st, kind)(text)
    st.session_state.msg = None

top = st.columns([3, 1])
with top[0]:
    st.markdown(f"### `{hid}`")
    st.caption(f"{item['source_benchmark']} / {item['source_id']}  ·  "
               f"`{item['transformation_type']}`  ·  `{item['answer_type']}`  "
               f"·  evidence_hash `{row.get('evidence_hash', '')}`")
with top[1]:
    st.caption(f"Item {st.session_state.idx + 1} of {len(vis)} in view")
    st.caption(f"Status: **{row.get('review_status', 'unreviewed')}**")

if item["transformation_type"] == MASKED:
    st.warning("**Controlled-insufficient variant.** Evidence rows were "
               "removed. Decide whether the question can *still* be answered "
               "— actually try the arithmetic. If the mask is valid, "
               "`evidence_sufficient_for_gold` = **no** is the expected "
               "answer, and the gold should be a non-committal label.")
elif item["transformation_type"] == DIRECTIONAL:
    st.info("**Transformed item.** Derive the direction yourself from the "
            "source arithmetic. Check the **operand order** — a reversed "
            "subtraction inverts the answer — and confirm the question is "
            "**direction-neutral** and **temporal**.")

st.markdown("#### Question")
st.write(item["question"])
if item["original_question"] and item["original_question"] != item["question"]:
    with st.expander("Original source question"):
        st.write(item["original_question"])
if item["derivation"]:
    st.markdown("#### Derivation / note")
    st.code(item["derivation"], language=None)

st.markdown("#### Oracle evidence")
st.text_area("evidence", item["oracle_evidence"],
             height=340, disabled=True, label_visibility="collapsed")

st.divider()
st.markdown("#### Your judgement")

nc = set(item["noncommit_labels"])
space = item["answer_space"]


def show(lbl):
    return f"{lbl}   ⟨non-committal⟩" if lbl in nc else lbl


cur = (row.get("reviewer_gold_label") or "").strip()
idx = space.index(cur) if cur in space else None
c1, c2 = st.columns([2, 1])
with c1:
    lab = st.radio("reviewer_gold_label", space, index=idx,
                   format_func=show, key=f"lab_{hid}")
with c2:
    st.caption("Non-committal labels for this item")
    st.write(", ".join(f"`{x}`" for x in space if x in nc) or "_none_")

suggested = ("noncommitted" if lab in nc else "committed") if lab else ""
com_opts = ["committed", "noncommitted", "ambiguous_exclude"]
com_key, sug_key = f"com_{hid}", f"_sugfor_{hid}"

# Auto-suggest has to be driven through session_state, not through `index`.
# Streamlit keeps a keyed widget's own state across reruns, so once the radio
# has been rendered once, recomputing `index` from a newly chosen label is
# ignored and the suggestion silently never fires. Writing the state directly
# -- and only when the label has actually changed since the last suggestion --
# makes it follow the label while still leaving a manual override intact.
if com_key not in st.session_state:
    saved = (row.get("reviewer_gold_commitment") or "").strip()
    st.session_state[com_key] = saved or suggested or "committed"
    st.session_state[sug_key] = lab
elif lab and st.session_state.get(sug_key) != lab:
    st.session_state[com_key] = suggested
    st.session_state[sug_key] = lab

com = st.radio(
    f"reviewer_gold_commitment  —  suggested from your label: "
    f"**{suggested or 'n/a'}** (override freely)",
    com_opts, horizontal=True, key=com_key)
if suggested and com != suggested:
    st.caption(f"Overriding the suggestion ({suggested}) — worth a note.")

g = st.columns(3)
yn = ["", "yes", "no", "unclear"]
with g[0]:
    cur_e = (row.get("evidence_sufficient_for_gold") or "")
    ev_suf = st.selectbox("evidence_sufficient_for_gold", yn,
                          index=yn.index(cur_e) if cur_e in yn else 0,
                          key=f"ev_{hid}")
with g[1]:
    tv_opts = ["", "yes", "no", "not_applicable", "unclear"]
    cur_t = (row.get("transformation_valid") or "")
    if item["transformation_type"] == DIRECTIONAL:
        tv = st.selectbox("transformation_valid  ← required", tv_opts,
                          index=tv_opts.index(cur_t) if cur_t in tv_opts else 0,
                          key=f"tv_{hid}")
    else:
        tv = st.selectbox("transformation_valid", tv_opts,
                          index=tv_opts.index(cur_t) if cur_t in tv_opts
                          else tv_opts.index("not_applicable"),
                          key=f"tv_{hid}")
with g[2]:
    mv_opts = ["", "yes", "no", "not_applicable", "unclear"]
    cur_m = (row.get("masked_variant_valid") or "")
    if item["transformation_type"] == MASKED:
        st.markdown("**masked_variant_valid ← required**")
        st.caption("yes = you tried and could NOT answer")
        mv = st.selectbox("masked_variant_valid", mv_opts,
                          index=mv_opts.index(cur_m) if cur_m in mv_opts else 0,
                          key=f"mv_{hid}", label_visibility="collapsed")
    else:
        mv = st.selectbox("masked_variant_valid", mv_opts,
                          index=mv_opts.index(cur_m) if cur_m in mv_opts
                          else mv_opts.index("not_applicable"),
                          key=f"mv_{hid}")

# family-specific flags
flag_opts = (MASK_FLAGS if item["transformation_type"] == MASKED
             else DIR_FLAGS if item["transformation_type"] == DIRECTIONAL
             else [])
chosen_flags = []
if flag_opts:
    st.caption("Flags (tick any that apply)"
               + (" — a reconstruction route means the mask is invalid"
                  if item["transformation_type"] == MASKED else ""))
    have = set((row.get("flags") or "").split("|"))
    fcols = st.columns(len(flag_opts))
    for i, fl in enumerate(flag_opts):
        with fcols[i]:
            if st.checkbox(fl, value=fl in have, key=f"fl_{hid}_{fl}"):
                chosen_flags.append(fl)

k1, k2 = st.columns([1, 2])
with k1:
    ke_opts = ["", "keep", "exclude"]
    cur_k = (row.get("keep_or_exclude") or "")
    keep = st.radio("keep_or_exclude", ke_opts,
                    index=ke_opts.index(cur_k) if cur_k in ke_opts else 0,
                    horizontal=True, key=f"ke_{hid}")
with k2:
    excl = st.text_input("exclusion_reason  (required if excluding)",
                         value=row.get("exclusion_reason", ""),
                         key=f"ex_{hid}")
notes = st.text_area("notes", value=row.get("notes", ""), height=80,
                     key=f"nt_{hid}")


def collect():
    return {"reviewer_gold_label": lab or "",
            "reviewer_gold_commitment": com or "",
            "evidence_sufficient_for_gold": ev_suf or "",
            "transformation_valid": tv or "",
            "masked_variant_valid": mv or "",
            "keep_or_exclude": keep or "",
            "exclusion_reason": excl.strip(),
            "notes": notes.strip(),
            "flags": "|".join(chosen_flags)}


def commit(status, advance):
    row.update(collect())
    errs = validate(row, item) if status == "reviewed" else []
    if errs:
        # The message banner is rendered near the top of the script, which has
        # already run by the time a button callback fires. Without an explicit
        # rerun the error is stored but never shown, so a blocked save looks
        # exactly like a button that does nothing.
        st.session_state.msg = ("error", "**Not saved.** " + "; ".join(errs))
        st.rerun()
    row["review_status"] = status
    row["reviewed_at"] = datetime.now().isoformat(timespec="seconds")
    save_work(rows)
    st.session_state.msg = ("success", f"Saved `{hid}` as {status}.")
    if advance:
        st.session_state.idx += 1
    st.rerun()


st.divider()
b = st.columns(6)
if b[0].button("Save", use_container_width=True):
    commit("reviewed", advance=False)
if b[1].button("Save and Next", type="primary", use_container_width=True):
    commit("reviewed", advance=True)
if b[2].button("Previous", use_container_width=True):
    st.session_state.idx = max(0, st.session_state.idx - 1)
    st.rerun()
if b[3].button("Next", use_container_width=True):
    st.session_state.idx = min(len(vis) - 1, st.session_state.idx + 1)
    st.rerun()
if b[4].button("Skip for later", use_container_width=True):
    row.update(collect())
    row["review_status"] = "skipped"
    save_work(rows)
    st.session_state.idx += 1
    st.rerun()
if b[5].button("Needs second look", use_container_width=True):
    row.update(collect())
    row["review_status"] = "second_look"
    save_work(rows)
    st.session_state.idx += 1
    st.rerun()

st.caption(
    "Autosaves to `hedgeqa_core_v0_1_human_review_in_progress.csv` on every "
    "button; a timestamped backup is written to `review_backups/` before each "
    "overwrite. The candidate JSONL and the original review CSV are never "
    "modified. Pipeline gold labels, AI reviews and reveal files are not "
    "loaded by this app.")
