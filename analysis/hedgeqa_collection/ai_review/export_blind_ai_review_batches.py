"""Export blind review batches for AI-assisted adjudication.

Blinding removes `gold_label`, `gold_commitment` and `validation_status`, so
a reviewer forms its own answer instead of grading ours.

## The leak this had to work around

`derivation` is required for `numeric_to_directional` items -- checking the
operand order IS the review task there. But on a masked item the derivation
reads:

    "...the evidence rows carrying its operands (['16284', '6509']) were
     removed..."

which names exactly what is missing. Handing that to a reviewer asked
"can this evidence still answer the question?" pre-answers it: they would
say no because we told them what we deleted, not because they looked.

So for masked items the derivation is replaced with a neutral statement that
the item is a controlled-insufficient variant, and the operand list plus
`masked_content` go to a separate `*_reveal.jsonl`. The reveal file is for
auditing a decision AFTER it is recorded -- never before. `transformation_type`
is still shown, because the reviewer needs to know which question is being
asked of them; what is withheld is the answer key.

## Batching

25 items per file, and the three families never mix:

    none                          natural, untransformed
    numeric_to_directional        natural, transformed
    evidence_masked_insufficient  constructed gold

Mixing them would let a reviewer calibrate on the easy family and carry that
prior into the hard one, and it would make per-family agreement impossible to
read off cleanly.

Both JSONL (for programmatic runs) and Markdown (for pasting into a chat UI)
are written for every batch.

Usage: python analysis/hedgeqa_collection/ai_review/export_blind_ai_review_batches.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE.parent))

from hedgeqa_schema import read_jsonl  # noqa: E402

CORE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_candidates.jsonl"
OUT = HERE / "batches"
REVEAL = HERE / "reveal"

BATCH_SIZE = 25
MASKED = "evidence_masked_insufficient"

FAMILY_ORDER = ["none", "numeric_to_directional", MASKED]

# Fields a reviewer never sees in a blind pass.
BLINDED = ("gold_label", "gold_commitment", "validation_status",
           "schema_confidence", "exclusion_reason", "masked_content")

def redact_directional_derivation(text: str) -> str:
    """Keep the source arithmetic; drop OUR computed answer and label.

    The stored derivation reads:

        "numeric_to_directional: the source answer -7.6 is a change, mapped
         to 'decreased'. Source derivation: turn_program='subtract(...)'"

    Both the signed answer and the mapped label give the gold away. The
    reviewer's task is to derive the direction from the program themselves
    and check the operand order, so only the trailing source expression is
    exposed.
    """
    if not text:
        return ""
    marker = "Source derivation:"
    tail = text.split(marker, 1)[1].strip() if marker in text else ""
    if not tail or tail.lower().startswith("no source derivation"):
        return ("The source supplies no explicit derivation for this item. "
                "Judge the direction from the evidence alone.")
    return ("Source arithmetic as stated by the originating benchmark: "
            + tail + " Derive the direction yourself; check the operand "
            "order before trusting it.")


NEUTRAL_DERIVATION = (
    "This item is a controlled-insufficient variant: some evidence rows were "
    "removed from the source document. You are NOT told which rows or which "
    "figures. Decide from the evidence below whether the question can still "
    "be answered."
)


def blind_item(it) -> dict:
    """The blind view of one item."""
    d = {
        "hedgeqa_id": it.hedgeqa_id,
        "source_benchmark": it.source_benchmark,
        "source_id": it.source_id,
        "transformation_type": it.transformation_type,
        "answer_type": it.answer_type,
        "question": it.question,
        "answer_space": list(it.answer_space),
        "noncommit_labels": list(it.noncommit_labels),
        "oracle_evidence": it.oracle_evidence,
    }
    if it.original_question and it.original_question != it.question:
        d["original_question"] = it.original_question

    if it.transformation_type == MASKED:
        # withhold the operand list -- it names what was removed
        d["derivation"] = NEUTRAL_DERIVATION
    elif it.transformation_type == "numeric_to_directional":
        d["derivation"] = redact_directional_derivation(it.derivation)
    elif it.derivation:
        d["derivation"] = it.derivation
    return d


def reveal_item(it) -> dict:
    """Post-decision audit material. Do not open before recording a label."""
    return {
        "hedgeqa_id": it.hedgeqa_id,
        "transformation_type": it.transformation_type,
        "derivation_full": it.derivation,
        "masked_content": it.masked_content,
    }


def to_markdown(batch, name) -> str:
    L = [f"# Blind review batch `{name}`", "",
         f"{len(batch)} items. Family: `{batch[0]['transformation_type']}`.",
         "",
         "Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, "
         "JSONL only, no prose outside the JSON.", "", "---", ""]
    for n, d in enumerate(batch, 1):
        L.append(f"## Item {n}/{len(batch)} — `{d['hedgeqa_id']}`")
        L.append("")
        L.append(f"- **source**: {d['source_benchmark']} / {d['source_id']}")
        L.append(f"- **transformation_type**: `{d['transformation_type']}`")
        L.append(f"- **answer_type**: `{d['answer_type']}`")
        L.append(f"- **answer_space**: {d['answer_space']}")
        L.append(f"- **noncommit_labels**: {d['noncommit_labels']}")
        L.append("")
        L.append(f"**Question**: {d['question']}")
        L.append("")
        if "original_question" in d:
            L.append(f"**Original source question**: {d['original_question']}")
            L.append("")
        if "derivation" in d:
            L.append(f"**Derivation / note**: {d['derivation']}")
            L.append("")
        L.append("**Oracle evidence**:")
        L.append("")
        L.append("```")
        L.append(d["oracle_evidence"])
        L.append("```")
        L.append("")
        L.append("---")
        L.append("")
    return "\n".join(L)


def main():
    items = read_jsonl(CORE)
    OUT.mkdir(parents=True, exist_ok=True)
    REVEAL.mkdir(parents=True, exist_ok=True)
    for old in list(OUT.glob("*")) + list(REVEAL.glob("*")):
        old.unlink()

    manifest, total = [], 0
    for fam in FAMILY_ORDER:
        fam_items = sorted((i for i in items if i.transformation_type == fam),
                           key=lambda x: x.hedgeqa_id)
        if not fam_items:
            continue
        short = {"none": "natural", "numeric_to_directional": "directional",
                 MASKED: "masked"}[fam]
        for b in range((len(fam_items) + BATCH_SIZE - 1) // BATCH_SIZE):
            chunk = fam_items[b * BATCH_SIZE:(b + 1) * BATCH_SIZE]
            name = f"{short}_batch{b + 1:02d}"
            blind = [blind_item(i) for i in chunk]

            with (OUT / f"{name}.jsonl").open("w", encoding="utf-8") as f:
                for d in blind:
                    f.write(json.dumps(d, ensure_ascii=False) + "\n")
            (OUT / f"{name}.md").write_text(to_markdown(blind, name),
                                            encoding="utf-8")

            if fam == MASKED:
                with (REVEAL / f"{name}_reveal.jsonl").open(
                        "w", encoding="utf-8") as f:
                    for i in chunk:
                        f.write(json.dumps(reveal_item(i),
                                           ensure_ascii=False) + "\n")
            manifest.append({"batch": name, "family": fam,
                             "n": len(chunk),
                             "ids": [i.hedgeqa_id for i in chunk]})
            total += len(chunk)

    (HERE / "batch_manifest.json").write_text(
        json.dumps({"batch_size": BATCH_SIZE, "total_items": total,
                    "batches": manifest}, indent=1), encoding="utf-8")

    # leak check: no blinded field may appear in any exported batch
    leaked = []
    for p in OUT.glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            d = json.loads(line)
            for k in BLINDED:
                if k in d:
                    leaked.append((p.name, d["hedgeqa_id"], k))
    print(f"exported {total} items in {len(manifest)} batches -> "
          f"{OUT.relative_to(REPO)}")
    for m in manifest:
        print(f"    {m['batch']:22s} {m['family']:30s} n={m['n']}")
    print(f"\nreveal files (masked only, post-decision) -> "
          f"{REVEAL.relative_to(REPO)}")
    print(f"blinded-field leak check: "
          f"{'CLEAN' if not leaked else f'LEAKED {leaked[:5]}'}")
    assert not leaked, "blinded field present in an exported batch"
    return manifest


if __name__ == "__main__":
    main()
