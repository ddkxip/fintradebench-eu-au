"""Smoke test for the AI-review merge and agreement machinery.

The merger and the agreement report are only exercised once real reviewer
output exists, which is exactly when a bug in them is most expensive. This
builds synthetic reviewer files with KNOWN agreement structure, runs both
scripts, and asserts the numbers come back right.

Synthetic files are written into a temporary responses directory and removed
afterwards; a real `responses/` is saved and restored, so running this never
destroys collected reviews.

Run: python analysis/hedgeqa_collection/ai_review/test_ai_review_pipeline.py
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))

from hedgeqa_schema import read_jsonl  # noqa: E402

CORE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_candidates.jsonl"
RESP = HERE / "responses"
BACKUP = HERE / "_responses_backup_during_test"
HUMAN = HERE.parent / "hedgeqa_core_v0_1_manual_review.csv"
HUMAN_BAK = HERE / "_human_backup_during_test.csv"
MERGED = HERE / "hedgeqa_core_review_merged.csv"
GEM, GPT = "gemini_antigravity", "chatgpt_codex"
MASKED = "evidence_masked_insufficient"


def rec(it, who, label=None, commit=None, keep="keep", conf="high",
        mvv=None, tv=None, flags=()):
    is_mask = it.transformation_type == MASKED
    return {
        "hedgeqa_id": it.hedgeqa_id, "reviewer_name": who,
        "reviewer_gold_label": label if label is not None else it.gold_label,
        "reviewer_gold_commitment": commit or it.gold_commitment,
        "evidence_sufficient_for_gold": "no" if is_mask else "yes",
        "transformation_valid": tv or (
            "not_applicable" if it.transformation_type != "numeric_to_directional"
            else "yes"),
        "masked_variant_valid": mvv or ("yes" if is_mask else "not_applicable"),
        "keep_or_exclude": keep, "exclusion_reason": "" if keep == "keep" else "synthetic",
        "confidence": conf, "rationale_short": "synthetic test record",
        "flags": list(flags),
    }


def main():
    items = sorted(read_jsonl(CORE), key=lambda x: x.hedgeqa_id)
    assert len(items) >= 40, "core too small to smoke-test"

    # preserve anything real
    restored = False
    if RESP.exists() and any(RESP.glob("*.jsonl")):
        if BACKUP.exists():
            shutil.rmtree(BACKUP)
        shutil.move(str(RESP), str(BACKUP))
        restored = True
    RESP.mkdir(parents=True, exist_ok=True)
    shutil.copy(HUMAN, HUMAN_BAK)

    try:
        masked = [i for i in items if i.transformation_type == MASKED][:6]
        direc = [i for i in items
                 if i.transformation_type == "numeric_to_directional"][:6]
        plain = [i for i in items if i.transformation_type == "none"][:8]
        sample = masked + direc + plain

        # --- construct KNOWN structure -------------------------------------
        # plain[0]: everyone agrees                       -> strong_keep
        # plain[1]: gemini disagrees on label             -> review_needed
        # plain[2]: gemini keeps with low confidence      -> review_needed
        # plain[3]: both AI exclude                       -> exclude
        # plain[4]: human excludes                        -> exclude
        # plain[5]: commitment split                      -> review_needed
        # masked[0]: gemini says answerable               -> review_needed + high risk
        # direc[0]: chatgpt challenges transformation     -> review_needed + high risk
        gem, gpt = [], []
        for it in sample:
            g = rec(it, GEM)
            c = rec(it, GPT)
            if it is plain[1]:
                g["reviewer_gold_label"] = "__SYNTHETIC_DIFFERENT__"
            if it is plain[2]:
                g["confidence"] = "low"
            if it is plain[3]:
                g["keep_or_exclude"] = c["keep_or_exclude"] = "exclude"
                g["exclusion_reason"] = c["exclusion_reason"] = "synthetic"
            if it is plain[5]:
                g["reviewer_gold_commitment"] = (
                    "noncommitted" if it.gold_commitment == "committed"
                    else "committed")
            if it is masked[0]:
                g["masked_variant_valid"] = "no"
                g["keep_or_exclude"] = "exclude"
                g["exclusion_reason"] = "synthetic reconstruction route"
                g["flags"] = ["rollforward_reconstruction"]
            if it is direc[0]:
                c["transformation_valid"] = "no"
                c["keep_or_exclude"] = "exclude"
                c["exclusion_reason"] = "synthetic operand order"
                c["flags"] = ["operand_order_suspect"]
            gem.append(g)
            gpt.append(c)

        for who, recs in ((GEM, gem), (GPT, gpt)):
            with (RESP / f"{who}__smoketest_batch01.jsonl").open(
                    "w", encoding="utf-8") as f:
                for d in recs:
                    f.write(json.dumps(d) + "\n")

        # --- synthetic human sheet ----------------------------------------
        with HUMAN.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
            cols = rows[0].keys()
        ids = {i.hedgeqa_id: i for i in sample}
        for r in rows:
            it = ids.get(r["hedgeqa_id"])
            if not it:
                continue
            r["reviewer_gold_label"] = it.gold_label
            r["reviewer_gold_commitment"] = it.gold_commitment
            r["keep_or_exclude"] = "exclude" if it is plain[4] else "keep"
            r["masked_variant_valid"] = (
                "yes" if it.transformation_type == MASKED else "not_applicable")
            r["transformation_valid"] = (
                "yes" if it.transformation_type == "numeric_to_directional"
                else "not_applicable")
            r["evidence_sufficient_for_gold"] = (
                "no" if it.transformation_type == MASKED else "yes")
        with HUMAN.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(cols))
            w.writeheader()
            w.writerows(rows)

        # --- run both scripts ---------------------------------------------
        for script in ("merge_ai_reviews.py", "analyze_ai_review_agreement.py"):
            p = subprocess.run([sys.executable, str(HERE / script)],
                               capture_output=True, text=True)
            assert p.returncode == 0, f"{script} failed:\n{p.stdout}\n{p.stderr}"

        with MERGED.open(encoding="utf-8", newline="") as f:
            merged = {r["hedgeqa_id"]: r for r in csv.DictReader(f)}

        checks = [
            ("plain[0] unanimous -> strong_keep",
             merged[plain[0].hedgeqa_id]["promotion_class"], "strong_keep"),
            ("plain[1] label split -> review_needed",
             merged[plain[1].hedgeqa_id]["promotion_class"], "review_needed"),
            ("plain[2] low confidence -> review_needed",
             merged[plain[2].hedgeqa_id]["promotion_class"], "review_needed"),
            ("plain[3] both AI exclude -> exclude",
             merged[plain[3].hedgeqa_id]["promotion_class"], "exclude"),
            ("plain[4] human excludes -> exclude",
             merged[plain[4].hedgeqa_id]["promotion_class"], "exclude"),
            ("plain[5] commitment split -> review_needed",
             merged[plain[5].hedgeqa_id]["promotion_class"], "review_needed"),
            ("masked[0] answerable -> review_needed",
             merged[masked[0].hedgeqa_id]["promotion_class"], "review_needed"),
            ("direc[0] transform challenged -> review_needed",
             merged[direc[0].hedgeqa_id]["promotion_class"], "review_needed"),
            ("unreviewed item -> review_needed",
             merged[[i for i in items if i.hedgeqa_id not in ids][0]
                    .hedgeqa_id]["promotion_class"], "review_needed"),
        ]
        fails = 0
        for name, got, want in checks:
            ok = got == want
            fails += (not ok)
            print(f"{'PASS' if ok else 'FAIL'} {name}: {got}")

        report = (HERE / "AI_REVIEW_AGREEMENT_REPORT.md").read_text(
            encoding="utf-8")
        for must in ("Cohen kappa", "High-risk disagreements",
                     "masked item reported answerable",
                     "not human ground truth"):
            ok = must in report
            fails += (not ok)
            print(f"{'PASS' if ok else 'FAIL'} report contains {must!r}")

        # the two seeded high-risk items must be listed
        for it, what in ((masked[0], "masked"), (direc[0], "directional")):
            ok = it.hedgeqa_id in report
            fails += (not ok)
            print(f"{'PASS' if ok else 'FAIL'} report lists seeded {what} "
                  f"risk item")

        print("\nai-review pipeline smoke test:",
              "all passed" if not fails else f"{fails} FAILED")
        return 1 if fails else 0

    finally:
        shutil.copy(HUMAN_BAK, HUMAN)
        HUMAN_BAK.unlink()
        shutil.rmtree(RESP, ignore_errors=True)
        if restored:
            shutil.move(str(BACKUP), str(RESP))
        else:
            RESP.mkdir(parents=True, exist_ok=True)
        # leave merged/report regenerated from the restored inputs
        subprocess.run([sys.executable, str(HERE / "merge_ai_reviews.py")],
                       capture_output=True, text=True)
        subprocess.run([sys.executable,
                        str(HERE / "analyze_ai_review_agreement.py")],
                       capture_output=True, text=True)


if __name__ == "__main__":
    sys.exit(main())
