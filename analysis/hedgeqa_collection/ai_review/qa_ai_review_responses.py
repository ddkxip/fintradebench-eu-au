"""Blind-safe structural QA over collected AI reviewer responses.

## Blind-safety contract

The human review is not complete. Anything this script emits could reach the
human reviewer before they form their own judgement, so it reports **only
structure**: whether files parse, whether fields exist, whether enum values
are legal, whether batches line up.

It never emits:
  * `reviewer_gold_label` values
  * `rationale_short` text
  * per-item `keep_or_exclude` / commitment decisions
  * any count that reveals a reviewer's overall stance (e.g. "Gemini
    excluded 40 items")

Rule-consistency checks are reported as VIOLATION COUNTS only. "3 rows have
`exclude` with an empty `exclusion_reason`" is a structural defect; "Gemini
excluded 40 items" is a finding about content and is withheld.

The one deliberate exception is the low-confidence-keep count, which the QA
spec asks for explicitly. It is a review-workload indicator, not a verdict,
and is reported without per-item detail or reviewer attribution beyond the
totals needed to plan the work.

## Normalisation

`masked_answer_recoverable` is not in the schema enum; it is a plausible
paraphrase of `answer_reconstructible` that a reviewer may emit. Occurrences
are rewritten in place and counted. No other value is ever rewritten --
silently repairing a reviewer's output would destroy the signal this whole
exercise collects.

Usage: python analysis/hedgeqa_collection/ai_review/qa_ai_review_responses.py
       [--no-write]   report without applying the normalisation
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

RESP = HERE / "responses"
SCHEMA = HERE / "ai_review_schema.json"
MANIFEST = HERE / "batch_manifest.json"
OUT = HERE / "AI_REVIEW_RESPONSE_QA.md"

REVIEWERS = ["gemini_antigravity", "chatgpt_codex"]
MASKED = "evidence_masked_insufficient"
DIRECTIONAL = "numeric_to_directional"

BAD_FLAG = "masked_answer_recoverable"
GOOD_FLAG = "answer_reconstructible"

# Fields whose VALUES must never leave this script.
SENSITIVE = ("reviewer_gold_label", "reviewer_gold_commitment",
             "rationale_short", "exclusion_reason", "keep_or_exclude")


def load_schema():
    s = json.loads(SCHEMA.read_text(encoding="utf-8"))
    props = s["properties"]
    enums = {k: set(v["enum"]) for k, v in props.items() if "enum" in v}
    flag_enum = set(props["flags"]["items"]["enum"])
    return set(props), set(s["required"]), enums, flag_enum


def normalise(write: bool):
    """Rewrite the invalid flag. Returns (files_touched, occurrences)."""
    files, occ = 0, 0
    for p in sorted(RESP.glob("*.jsonl")):
        raw = p.read_text(encoding="utf-8")
        if BAD_FLAG not in raw:
            continue
        lines, n = [], 0
        for line in raw.splitlines():
            if not line.strip():
                lines.append(line)
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                lines.append(line)          # leave malformed lines alone
                continue
            fl = d.get("flags")
            if isinstance(fl, list) and BAD_FLAG in fl:
                d["flags"] = [GOOD_FLAG if f == BAD_FLAG else f for f in fl]
                # de-duplicate if both spellings were present
                seen, out = set(), []
                for f in d["flags"]:
                    if f not in seen:
                        seen.add(f)
                        out.append(f)
                d["flags"] = out
                n += 1
            lines.append(json.dumps(d, ensure_ascii=False))
        if n:
            files += 1
            occ += n
            if write:
                p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return files, occ


def main(write: bool = True):
    allowed, required, enums, flag_enum = load_schema()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = {b["batch"]: b for b in manifest["batches"]}
    fam_of = {b["batch"]: b["family"] for b in manifest["batches"]}

    norm_files, norm_occ = normalise(write)

    files = sorted(RESP.glob("*.jsonl"))
    problems = []                    # (severity, file, detail)
    per_file = {}
    parsed = collections.defaultdict(dict)   # reviewer -> batch -> [records]
    counts = collections.Counter()
    lowconf_keep = collections.Counter()
    flag_counts = collections.Counter()

    for p in files:
        name = p.name
        stem = name[:-len(".jsonl")]
        if "__" not in stem:
            problems.append(("ERROR", name, "filename is not "
                                            "<reviewer>__<batch>.jsonl"))
            continue
        who, batch = stem.split("__", 1)
        rec = {"reviewer": who, "batch": batch, "lines": 0, "objects": 0,
               "bad_json": 0, "not_object": 0, "missing_fields": 0,
               "extra_fields": 0, "bad_enum": 0, "bad_flag": 0,
               "family_inconsistent": 0, "exclusion_reason_missing": 0,
               "exclusion_reason_unexpected": 0, "dupe_ids": 0,
               "name_mismatch": 0}
        per_file[name] = rec

        if who not in REVIEWERS:
            problems.append(("ERROR", name,
                             f"unknown reviewer prefix {who!r}"))
        if batch not in expected:
            problems.append(("ERROR", name,
                             f"batch {batch!r} is not in batch_manifest.json"))

        fam = fam_of.get(batch)
        ids, records = [], []
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            rec["lines"] += 1
            s = line.strip()
            if not s:
                continue
            try:
                d = json.loads(s)
            except json.JSONDecodeError as e:
                rec["bad_json"] += 1
                problems.append(("ERROR", name,
                                 f"line {n}: not valid JSON ({e.msg})"))
                continue
            if not isinstance(d, dict):
                rec["not_object"] += 1
                problems.append(("ERROR", name,
                                 f"line {n}: JSON is not an object"))
                continue
            rec["objects"] += 1
            records.append(d)

            miss = required - set(d)
            if miss:
                rec["missing_fields"] += 1
                problems.append(("ERROR", name,
                                 f"line {n}: missing {sorted(miss)}"))
            extra = set(d) - allowed
            if extra:
                rec["extra_fields"] += 1
                problems.append(("ERROR", name,
                                 f"line {n}: unexpected field(s) "
                                 f"{sorted(extra)}"))
            for k, allowedvals in enums.items():
                if k in d and d[k] not in allowedvals:
                    rec["bad_enum"] += 1
                    problems.append(("ERROR", name,
                                     f"line {n}: field {k!r} has a value "
                                     f"outside its enum"))
            if d.get("reviewer_name") and d["reviewer_name"] != who:
                rec["name_mismatch"] += 1
                problems.append(("ERROR", name, f"line {n}: reviewer_name "
                                                f"disagrees with filename"))
            fl = d.get("flags", [])
            if not isinstance(fl, list):
                rec["bad_flag"] += 1
                problems.append(("ERROR", name, f"line {n}: flags is not a "
                                                f"list"))
            else:
                for f in fl:
                    flag_counts[f] += 1
                    if f not in flag_enum:
                        rec["bad_flag"] += 1
                        problems.append(("ERROR", name,
                                         f"line {n}: flag {f!r} is not in the "
                                         f"schema enum"))

            # family-specific consistency (structure, not verdicts)
            tv, mv = d.get("transformation_valid"), d.get("masked_variant_valid")
            if fam == MASKED:
                if mv == "not_applicable":
                    rec["family_inconsistent"] += 1
                    problems.append(("ERROR", name, f"line {n}: masked item "
                                     f"has masked_variant_valid="
                                     f"'not_applicable'"))
            else:
                if mv != "not_applicable":
                    rec["family_inconsistent"] += 1
                    problems.append(("ERROR", name, f"line {n}: non-masked "
                                     f"item does not have "
                                     f"masked_variant_valid='not_applicable'"))
            if fam == DIRECTIONAL:
                if tv == "not_applicable":
                    rec["family_inconsistent"] += 1
                    problems.append(("WARN", name, f"line {n}: directional "
                                     f"item has transformation_valid="
                                     f"'not_applicable'"))
            elif fam == "none":
                if tv not in (None, "not_applicable"):
                    rec["family_inconsistent"] += 1
                    problems.append(("WARN", name, f"line {n}: untransformed "
                                     f"item has a transformation_valid "
                                     f"verdict"))

            # exclusion_reason consistency -- violation counts only
            ke = str(d.get("keep_or_exclude", "")).strip().lower()
            er = str(d.get("exclusion_reason", "") or "").strip()
            if ke == "exclude" and not er:
                rec["exclusion_reason_missing"] += 1
                problems.append(("ERROR", name, f"line {n}: excluded row has "
                                                f"an empty exclusion_reason"))
            if ke == "keep" and er:
                rec["exclusion_reason_unexpected"] += 1
                problems.append(("WARN", name, f"line {n}: kept row has a "
                                               f"non-empty exclusion_reason"))
            if ke == "keep" and str(d.get("confidence", "")).lower() == "low":
                lowconf_keep[who] += 1

            hid = d.get("hedgeqa_id")
            if hid:
                ids.append(hid)

        dupes = [k for k, v in collections.Counter(ids).items() if v > 1]
        if dupes:
            rec["dupe_ids"] = len(dupes)
            problems.append(("ERROR", name,
                             f"{len(dupes)} duplicate hedgeqa_id(s)"))

        exp = expected.get(batch, {}).get("ids", [])
        if exp:
            if len(ids) != len(exp):
                problems.append(("ERROR", name,
                                 f"has {len(ids)} records, batch expects "
                                 f"{len(exp)}"))
            missing = set(exp) - set(ids)
            unknown = set(ids) - set(exp)
            if missing:
                problems.append(("ERROR", name,
                                 f"{len(missing)} expected id(s) absent"))
            if unknown:
                problems.append(("ERROR", name,
                                 f"{len(unknown)} id(s) not in this batch"))
            if ids and ids != exp and not missing and not unknown:
                problems.append(("WARN", name,
                                 "ids present but not in batch order"))
        parsed[who][batch] = ids
        counts[who] += len(ids)

    # pairing + cross-reviewer order
    pairing = []
    for batch in sorted(expected):
        g = parsed.get(REVIEWERS[0], {}).get(batch)
        c = parsed.get(REVIEWERS[1], {}).get(batch)
        state = "both"
        if g is None and c is None:
            state = "neither"
        elif g is None:
            state = f"missing {REVIEWERS[0]}"
        elif c is None:
            state = f"missing {REVIEWERS[1]}"
        same_order = None
        if g is not None and c is not None:
            same_order = (g == c)
            if not same_order:
                if set(g) == set(c):
                    problems.append(("WARN", batch,
                                     "both reviewers cover the same ids but "
                                     "in a different order"))
                else:
                    problems.append(("ERROR", batch,
                                     "reviewers cover different id sets"))
        pairing.append((batch, fam_of.get(batch, "?"),
                        len(expected[batch]["ids"]),
                        len(g) if g else 0, len(c) if c else 0,
                        state, same_order))

    # cross-file duplicate ids per reviewer
    for who in REVIEWERS:
        allids = [i for b in parsed.get(who, {}).values() for i in b]
        d = [k for k, v in collections.Counter(allids).items() if v > 1]
        if d:
            problems.append(("ERROR", who,
                             f"{len(d)} hedgeqa_id(s) appear in more than one "
                             f"file"))

    errors = [p for p in problems if p[0] == "ERROR"]
    warns = [p for p in problems if p[0] == "WARN"]

    # ------------------------------------------------------------------ report
    L, A = [], None
    A = L.append
    A("# AI review responses — structural QA")
    A("")
    A("**Blind-safe report.** Structure only. No gold labels, no rationales, "
      "no per-item reviewer decisions, and no counts that would reveal a "
      "reviewer's overall stance. Rule violations are reported as counts so "
      "that a defect is visible without disclosing the content behind it.")
    A("")
    A("**No agreement analysis is included.** The human review is not "
      "complete, and computing agreement now would put AI verdicts in front "
      "of the human reviewer, destroying their independence as a third "
      "rater. Run `analyze_ai_review_agreement.py` only after the human "
      "sheet is filled in.")
    A("")

    A("## Summary")
    A("")
    A(f"- response files: **{len(files)}**")
    A(f"- expected batches: **{len(expected)}** x {len(REVIEWERS)} reviewers "
      f"= **{len(expected) * len(REVIEWERS)}** files")
    A(f"- records parsed: **{sum(counts.values())}** "
      f"({' / '.join(f'{w}: {counts[w]}' for w in REVIEWERS)})")
    A(f"- expected records: **{manifest['total_items'] * len(REVIEWERS)}** "
      f"({manifest['total_items']} per reviewer)")
    A(f"- structural ERRORS: **{len(errors)}**")
    A(f"- structural WARNINGS: **{len(warns)}**")
    A("")

    A("## Checks")
    A("")
    A("| # | check | result |")
    A("|---|---|---|")

    def verdict(n, label="violations"):
        return "PASS" if n == 0 else f"**{n} {label}**"

    agg = collections.Counter()
    for r in per_file.values():
        for k, v in r.items():
            if isinstance(v, int):
                agg[k] += v
    order_warn = sum(1 for s, _, d in problems if "not in batch order" in d)
    setdiff = sum(1 for s, _, d in problems if "different id sets" in d)
    A(f"| 1 | valid JSONL | {verdict(agg['bad_json'], 'unparseable lines')} |")
    A(f"| 2 | exactly one JSON object per line | "
      f"{verdict(agg['not_object'], 'non-object lines')} |")
    A(f"| 3 | filename prefix matches `reviewer_name` | "
      f"{verdict(agg['name_mismatch'], 'mismatched rows')} |")
    A(f"| 4 | required fields present | "
      f"{verdict(agg['missing_fields'], 'rows missing a field')} |")
    A(f"| 5 | no extra fields | "
      f"{verdict(agg['extra_fields'], 'rows with extra fields')} |")
    A(f"| 6 | enum values legal | "
      f"{verdict(agg['bad_enum'], 'illegal enum values')} |")
    A(f"| 7 | flags from schema enum | "
      f"{verdict(agg['bad_flag'], 'illegal flags')} |")
    missing_pair = sum(1 for row in pairing if row[5] != "both")
    A(f"| 8 | every batch has both reviewer files | "
      f"{verdict(missing_pair, 'unpaired batches')} |")
    A(f"| 9 | paired files share ids in the same order | "
      f"{verdict(order_warn + setdiff, 'mismatched batches')} |")
    A(f"| 10 | no duplicate `hedgeqa_id` per reviewer | "
      f"{verdict(agg['dupe_ids'], 'duplicated ids')} |")
    A(f"| 11 | family-specific fields consistent | "
      f"{verdict(agg['family_inconsistent'], 'inconsistent rows')} |")
    A(f"| 12 | excluded rows carry a reason | "
      f"{verdict(agg['exclusion_reason_missing'], 'rows missing a reason')} |")
    A(f"| 13 | kept rows have no reason | "
      f"{verdict(agg['exclusion_reason_unexpected'], 'rows with a stray reason')} |")
    A(f"| 14 | low-confidence keeps (counted, not an error) | "
      f"{sum(lowconf_keep.values())} row(s) |")
    A("")

    A("## Normalisation applied")
    A("")
    if norm_occ:
        A(f"`{BAD_FLAG}` -> `{GOOD_FLAG}`: **{norm_occ} occurrence(s)** across "
          f"**{norm_files} file(s)**"
          + ("." if write else " (dry run — not written)."))
    else:
        A(f"`{BAD_FLAG}` did not occur. No normalisation was needed.")
    A("")
    A("No other value was rewritten. Repairing a reviewer's output beyond "
      "this one documented alias would destroy the signal being collected.")
    A("")

    A("## Batch pairing")
    A("")
    A("| batch | family | expected | gemini | codex | pairing | same order |")
    A("|---|---|---|---|---|---|---|")
    for b, fam, exp_n, gn, cn, state, same in pairing:
        so = "-" if same is None else ("yes" if same else "**no**")
        A(f"| `{b}` | {fam} | {exp_n} | {gn} | {cn} | {state} | {so} |")
    A("")

    A("## Per-file record counts")
    A("")
    A("| file | records | parse errors | schema errors |")
    A("|---|---|---|---|")
    for name in sorted(per_file):
        r = per_file[name]
        sch_err = (r["missing_fields"] + r["extra_fields"] + r["bad_enum"]
                   + r["bad_flag"] + r["family_inconsistent"]
                   + r["exclusion_reason_missing"] + r["name_mismatch"])
        A(f"| `{name}` | {r['objects']} | "
          f"{r['bad_json'] + r['not_object']} | {sch_err} |")
    A("")

    A("## Flag vocabulary")
    A("")
    A("Only whether the flag vocabulary is legal. **Per-flag frequencies are "
      "deliberately withheld**: a count like "
      "`answer_reconstructible: N` would tell the human reviewer how many "
      "masked items an AI judged answerable, which is precisely the "
      "substantive finding their own masked-item pass is supposed to reach "
      "independently. Those counts belong in the agreement report, after the "
      "human review is recorded.")
    A("")
    out_of_schema = sorted({f for f in flag_counts if f not in flag_enum})
    A(f"- distinct flag names used: **{len(flag_counts)}** of "
      f"{len(flag_enum)} available in the schema")
    A(f"- flag occurrences in total: **{sum(flag_counts.values())}** "
      f"(across {sum(counts.values())} records, both reviewers pooled)")
    if out_of_schema:
        A(f"- **names outside the schema enum: {out_of_schema}**")
    else:
        A("- names outside the schema enum: none")
    A("")

    A("## File-level problems")
    A("")
    if not problems:
        A("None.")
    else:
        A("| severity | file / batch | detail |")
        A("|---|---|---|")
        for sev, where, detail in problems[:200]:
            A(f"| {sev} | `{where}` | {detail} |")
        if len(problems) > 200:
            A("")
            A(f"…and {len(problems) - 200} more.")
    A("")

    A("## What this report does not tell you")
    A("")
    A("- whether the reviewers agreed with each other or with the pipeline;")
    A("- what any reviewer decided about any item;")
    A("- how many items either reviewer would exclude.")
    A("")
    A("All of that waits until the human review is recorded. Reading it "
      "first would make the human a second reader of the AI output rather "
      "than an independent rater, and the agreement numbers would no longer "
      "mean what they appear to mean.")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")

    # terminal output is also blind-safe
    print(f"wrote {OUT.relative_to(REPO)}")
    print(f"  files={len(files)} records={sum(counts.values())} "
          f"errors={len(errors)} warnings={len(warns)}")
    print(f"  normalisation: {norm_occ} occurrence(s) in {norm_files} file(s)")
    return len(errors)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-write", action="store_true",
                    help="report without applying the flag normalisation")
    sys.exit(0 if main(write=not ap.parse_args().no_write) == 0 else 1)
