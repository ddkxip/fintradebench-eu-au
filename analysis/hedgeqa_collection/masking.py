"""Evidence masking for controlled-insufficient variants.

Separated from the FinanceBench builder because this is the single most
error-prone construction in HedgeQA: a bad mask produces an item whose gold
label ("insufficient_data") is simply WRONG, and nothing downstream catches
it.

## Two flaws found while building this, both fixed here

**1. Naive salience.** The first version treated every number in the gold
justification as decisive. Tokens like "3", "1", "23" match all over a
balance sheet and deleted unrelated rows, and the 4-digit year in a column
header ("June 30, 2023") was treated as a figure. `salient_numbers` now
excludes bare years, sub-100 integers, and short tokens.

**2. A vacuous post-condition.** The second version checked that no salient
figure survived masking. That check CANNOT FAIL: if you delete every line
containing a figure, the figure is gone by construction. It reported zero
rejections not because the masks were good but because the test was empty.

What replaces it is a check that can actually fail:

  * `grounded`   -- at least one salient figure must genuinely appear in the
                    evidence. If the gold's numbers are nowhere in the
                    annotated span, we never established that this evidence
                    settled the question, so removing lines proves nothing.
  * `coverage`   -- EVERY salient figure found in the evidence must be
                    removed. If some are removed and others survive in an
                    untouched line, the remaining subset may still support
                    the answer.
  * `residual_concept` -- the noun phrases the question turns on (e.g.
                    "current liabilities") must not still head a numeric row
                    in the remaining text.

## What automation still cannot do

None of this proves the masked question is genuinely unanswerable. A model
may reconstruct a ratio from components we left behind, or infer a direction
from surrounding prose. These checks narrow the candidate set; they do not
certify it. Every masked variant is therefore emitted with
`validation_status="candidate"` and flagged for MANDATORY human review, and
must never be promoted to `auto_validated`.
"""

from __future__ import annotations

import re

NUM_RE = re.compile(r"-?\$?\d[\d,]*\.?\d*%?")

# Concepts a yes/no financial question commonly turns on. If one of these
# still heads a numeric row after masking, the item is suspect.
CONCEPT_WORDS = (
    "total current liabilities", "total current assets", "total liabilities",
    "total assets", "total equity", "net income", "total revenue",
    "net sales", "operating income", "gross profit", "inventories",
    "cash and cash equivalents", "accounts receivable", "long-term debt",
    "capital expenditure", "free cash flow", "operating cash flow",
)


def salient_numbers(text: str) -> list:
    """Figures a gold answer actually turns on.

    Excludes bare years, single/double digit tokens and small integers --
    these match indiscriminately inside financial tables.
    """
    out = []
    for m in NUM_RE.finditer(text or ""):
        flat = m.group(0).replace("$", "").replace(",", "").rstrip("%")
        try:
            val = float(flat)
        except ValueError:
            continue
        digits = sum(ch.isdigit() for ch in flat)
        has_dp = "." in flat
        if not has_dp and float(val).is_integer() and 1900 <= abs(val) <= 2100:
            continue                      # bare year
        if digits < 3 and not has_dp:
            continue                      # too short to be distinctive
        if abs(val) < 10 and not has_dp:
            continue
        out.append(flat)
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def _flat(s: str) -> str:
    return s.replace("$", "").replace(",", "")


def mask_evidence(evidence: str, salient: list, question: str = "") -> dict:
    """Remove evidence lines carrying the decisive figures.

    Returns a dict describing the attempt. `ok` is True only when the mask is
    grounded, complete, and leaves no give-away concept row. `ok` False is
    the normal, safe outcome -- skipping an item is free.
    """
    result = {"masked": evidence, "removed": [], "found": [], "ok": False,
              "reason": "", "residual_concepts": []}
    if not salient:
        result["reason"] = "no salient figures identified in the gold answer"
        return result

    eflat = _flat(evidence)
    found = [s for s in salient if s in eflat]
    result["found"] = found
    if not found:
        result["reason"] = ("none of the gold's figures appear in the "
                            "annotated evidence, so we cannot show this "
                            "evidence settled the question")
        return result

    kept, removed = [], []
    for line in evidence.splitlines():
        f = _flat(line)
        if any(s in f for s in found):
            removed.append(line)
        else:
            kept.append(line)
    masked = "\n".join(kept)
    result["masked"], result["removed"] = masked, removed

    if not removed:
        result["reason"] = "nothing was removed"
        return result

    # coverage: every found figure must be gone (can fail if a figure occurs
    # only as a substring of a longer token on a line we kept)
    mflat = _flat(masked)
    survivors = [s for s in found if s in mflat]
    if survivors:
        result["reason"] = (f"{len(survivors)} decisive figure(s) survive "
                            f"masking ({survivors[:5]})")
        return result

    # residual concept rows: a labelled numeric row for a concept named in
    # the question is a strong hint the answer is still derivable
    q = (question or "").lower()
    hits = []
    for line in kept:
        low = line.lower().strip()
        if not any(ch.isdigit() for ch in low):
            continue
        for c in CONCEPT_WORDS:
            if c in low and (c in q or c.split()[-1] in q):
                hits.append(line.strip()[:80])
                break
    if hits:
        result["residual_concepts"] = hits[:5]
        result["reason"] = (f"remaining text still carries {len(hits)} numeric "
                            f"row(s) for a concept the question names")
        return result

    result["ok"] = True
    result["reason"] = ("grounded, complete, no residual concept rows -- "
                        "STILL REQUIRES HUMAN REVIEW")
    return result
