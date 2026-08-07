"""Ingest FinanceBench open-source into a flat oracle-evidence JSONL.

ORACLE-EVIDENCE ONLY. This uses FinanceBench's own human-annotated evidence
strings (evidence_text) and full-page evidence (evidence_text_full_page).
It performs NO PDF retrieval, builds NO RAG index, and makes NO model calls.
The point of the extension is to test reasoning/debate uncertainty
*conditional on gold evidence*, mirroring FinTradeBench's oracle mode.

Data resolution order:
  1. $FINANCEBENCH_DATA_DIR/financebench_open_source.jsonl
  2. <repo>/data/financebench_open_source.jsonl
Document metadata (optional): financebench_document_information.jsonl

Output: analysis/financebench/financebench_oracle_examples.jsonl
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = HERE / "financebench_oracle_examples.jsonl"

SRC_NAME = "financebench_open_source.jsonl"
DOC_NAME = "financebench_document_information.jsonl"


def resolve_dir() -> Path:
    env = os.environ.get("FINANCEBENCH_DATA_DIR")
    cands = ([Path(env)] if env else []) + [REPO / "data", HERE / "data"]
    for c in cands:
        if (c / SRC_NAME).exists():
            return c
    raise SystemExit(
        f"[error] {SRC_NAME} not found. Looked in: "
        f"{[str(c) for c in cands]}\n"
        "Set FINANCEBENCH_DATA_DIR to the directory containing the "
        "FinanceBench open-source JSONL, or place it in <repo>/data/.")


def read_jsonl(p: Path) -> list[dict]:
    out = []
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main() -> None:
    d = resolve_dir()
    rows = read_jsonl(d / SRC_NAME)
    docs = {}
    if (d / DOC_NAME).exists():
        for r in read_jsonl(d / DOC_NAME):
            key = r.get("doc_name") or r.get("document_name")
            if key:
                docs[key] = r

    out_rows, no_ev = [], 0
    for r in rows:
        ev = r.get("evidence") or []
        texts, pages, names, fulls = [], [], [], []
        for e in ev:
            if not isinstance(e, dict):
                continue
            t = (e.get("evidence_text") or "").strip()
            fp = (e.get("evidence_text_full_page") or "").strip()
            # the open-source file names this key `doc_name` inside evidence
            dn = (e.get("evidence_doc_name") or e.get("doc_name") or "").strip()
            pn = e.get("evidence_page_num")
            if t:
                texts.append(t)
            if fp:
                fulls.append(fp)
            if dn:
                names.append(dn)
            if pn is not None:
                pages.append(pn)
        if not texts and not fulls:
            no_ev += 1
        doc_meta = docs.get(r.get("doc_name"), {})
        out_rows.append({
            "financebench_id": r.get("financebench_id"),
            "question": r.get("question"),
            "gold_answer": r.get("answer"),
            "justification": r.get("justification"),
            "company": r.get("company"),
            "doc_name": r.get("doc_name"),
            "question_type": r.get("question_type"),
            "question_reasoning": r.get("question_reasoning"),
            "evidence_text_joined": "\n\n---\n\n".join(texts),
            "evidence_full_page_joined": "\n\n---\n\n".join(fulls),
            "evidence_doc_names": "|".join(dict.fromkeys(names)),
            "evidence_page_nums": "|".join(str(p) for p in pages),
            "n_evidence": len(ev),
            "doc_period": doc_meta.get("doc_period"),
            "doc_type": doc_meta.get("doc_type"),
            "dataset_subset_label": r.get("dataset_subset_label"),
        })

    with OUT.open("w", encoding="utf-8") as f:
        for o in out_rows:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")

    n_txt = sum(1 for o in out_rows if o["evidence_text_joined"])
    n_full = sum(1 for o in out_rows if o["evidence_full_page_joined"])
    print(f"source dir: {d}")
    print(f"wrote {OUT} ({len(out_rows)} rows)")
    print(f"  with evidence_text: {n_txt}/{len(out_rows)}; "
          f"with full-page evidence: {n_full}/{len(out_rows)}; "
          f"with neither: {no_ev}")
    print(f"  doc metadata joined for "
          f"{sum(1 for o in out_rows if o['doc_period'])}/{len(out_rows)} rows")


if __name__ == "__main__":
    main()
