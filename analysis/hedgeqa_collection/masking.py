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


# ---------------------------------------------------------------------------
# Masking for the directional benchmarks (TAT-QA / FinQA / ConvFinQA)
#
# These are a BETTER masking target than FinanceBench's yes/no items, because
# the corpora state the arithmetic explicitly: TAT-QA ships a `derivation`
# ("(16,284 - 6,509) / 6,509") and FinQA/ConvFinQA a `program`
# ("subtract(959.2, 991.1), divide(#0, 991.1)"). We therefore know exactly
# which figures the answer depends on, instead of inferring them from prose.
#
# Their answer space already contains `insufficient_data` as a non-committal
# label, so a masked variant needs no new label -- only a different gold.
# ---------------------------------------------------------------------------

CONST_RE = re.compile(r"const_[a-z0-9_]+", re.I)
REF_RE = re.compile(r"#\d+")

# A mask that deletes most of the evidence yields a mutilated document rather
# than a fair question, and cues the model that something was done to it.
MAX_REMOVED_FRACTION = 0.5


def operands_from_program(program: str) -> list:
    """Numeric operands an answer actually depends on.

    Strips `const_1000` style literals and `#0` back-references, which are
    program plumbing rather than values read out of the evidence.
    """
    if not program:
        return []
    cleaned = REF_RE.sub(" ", CONST_RE.sub(" ", str(program)))
    return salient_numbers(cleaned)


def mask_directional(evidence: str, program: str, question: str = "") -> dict:
    """Remove the evidence rows carrying the operands of `program`.

    Adds a proportion guard to the shared checks: if more than half the
    evidence lines go, the item is rejected rather than shipped mutilated.
    """
    ops = operands_from_program(program)
    if not ops:
        return {"masked": evidence, "removed": [], "found": [], "ok": False,
                "reason": "no numeric operands in the derivation/program",
                "residual_concepts": [], "operands": []}

    res = mask_evidence(evidence, ops, question=question)
    res["operands"] = ops
    if not res["ok"]:
        return res

    total_lines = len([x for x in evidence.splitlines() if x.strip()])
    removed = len([x for x in res["removed"] if x.strip()])
    if total_lines and removed / total_lines > MAX_REMOVED_FRACTION:
        res["ok"] = False
        res["reason"] = (f"mask removes {removed}/{total_lines} lines "
                         f"(>{MAX_REMOVED_FRACTION:.0%}); the remaining "
                         f"document would be visibly mutilated")
        return res

    # roll-forward leakage: the literal figure is gone but the column still
    # sums to it (found by hand-inspecting a TAT-QA intangible-assets table)
    leaks = reconstructible_by_column_sum(res["masked"], ops)
    if leaks:
        res["ok"] = False
        res["reconstructible"] = leaks
        res["reason"] = ("masked figure is reconstructible: " + leaks[0])
    return res


def _cell_value(cell: str):
    """Parse a table cell to a float, honouring accounting negatives."""
    c = (cell or "").strip()
    if not c or c in {"-", "—", "–"}:
        return None
    neg = c.startswith("(") and c.endswith(")")
    c = c.strip("()").replace("$", "").replace(",", "").replace("%", "")
    try:
        v = float(c)
    except ValueError:
        return None
    return -v if neg else v


def _numbers_in(line: str) -> list:
    """Every parseable numeric cell on one line, in order."""
    out = []
    for tok in re.split(r"[ 	|]+", line.strip()):
        v = _cell_value(tok)
        if v is not None:
            out.append(v)
    return out


def _is_numeric_only(line: str) -> bool:
    t = line.strip()
    if not t:
        return False
    return bool(_numbers_in(t)) and not re.search(r"[A-Za-z]{2,}", t)


def parse_value_rows(masked: str) -> list:
    """Recover (label, values) rows from the three layouts that occur here.

    The original guard read only pipe-delimited lines. Every FinanceBench
    item is a filing rendered VERTICALLY -- a label on its own line followed
    by one numeric line per period -- and contains no pipe at all, so the
    guard was blind to 100% of that source. That is the gap the human review
    surfaced as 11 `total_minus_components` flags on items the automated
    check had passed.

    Handled:
      1. pipe-delimited   `Total | 23,678 | 12,907`
      2. whitespace table `Total revenues   58,158   62,286`
      3. vertical runs    `Total revenues` / `58,158` / `62,286`
         (a label line followed by a maximal run of numeric-only lines)

    Rows are returned with their values positionally aligned, so column *i*
    is period *i* for every row that has one. Rows from different blocks of
    the document pool together, which is what lets a total in one block
    reconcile against components in another.
    """
    rows, lines = [], masked.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if "|" in line:                              # layout 1
            # Whole-cell parsing, NOT token splitting. A header cell like
            # "30 June 2019" must yield nothing; splitting it on whitespace
            # injects 30 and 2019 into the value columns and destroys the
            # positional alignment every downstream check depends on.
            parts = line.split("|")
            label = parts[0].strip()
            vals = [_cell_value(c) for c in parts[1:]]
            vals = [v for v in vals if v is not None]
            if vals:
                rows.append((label, vals))
            i += 1
            continue
        nums = _numbers_in(line)
        has_text = bool(re.search(r"[A-Za-z]{2,}", line))
        if nums and has_text:                        # layout 2
            label = re.split(r"\s{2,}|	", line.strip())[0]
            rows.append((label[:60], nums))
            i += 1
            continue
        if has_text and not nums:                    # layout 3: label, then
            run, j = [], i + 1                       # a run of numeric lines
            while j < len(lines) and _is_numeric_only(lines[j]):
                run.extend(_numbers_in(lines[j]))
                j += 1
            if run:
                rows.append((line.strip()[:60], run))
                i = j
                continue
        i += 1
    return rows


def _match(value, targets, tol):
    for t in targets:
        if t and abs(abs(value) - t) <= max(tol, abs(t) * 0.001):
            return t
    return None


def reconstructible_by_window(masked: str, operands: list, tol: float = 0.01,
                              window: int = 6, max_pool: int = 12) -> list:
    """Small-subset arithmetic inside a sliding window of lines.

    Catches a reconstruction stated in running prose -- "total revenues of X
    comprised A and B" -- which no row parser will see as a table.

    ADVISORY ONLY -- this does NOT gate `mask_directional`.

    Measured on the 93 human-reviewed masked items it fires on 27% of those
    a human rejected and 22% of those a human kept. A 5-point lift on a 22%
    base rate is coincidence, not discrimination: a filing contains hundreds
    of figures whose pairwise and three-way sums land within tolerance of
    almost any target. Locality (a few adjacent lines, a capped pool, only
    2- and 3-term combinations) reduces that but does not remove it.

    Use it to produce a shortlist for a human to read, never to auto-reject.
    """
    targets = [abs(float(o)) for o in operands
               if _cell_value(str(o)) is not None]
    targets = [t for t in targets if t >= 100]      # tiny targets match noise
    if not targets:
        return []
    lines = [ln for ln in masked.splitlines() if ln.strip()]
    hits = []
    for start in range(max(1, len(lines) - window + 1)):
        pool = []
        for ln in lines[start:start + window]:
            pool.extend(_numbers_in(ln))
        pool = [v for v in dict.fromkeys(pool) if abs(v) >= 1][:max_pool]
        if len(pool) < 2:
            continue
        for a in range(len(pool)):
            for b in range(a + 1, len(pool)):
                x, y = pool[a], pool[b]
                t = _match(x + y, targets, tol)
                if t:
                    hits.append(f"{x:g} + {y:g} = {x + y:g} reproduces "
                                f"masked operand {t:g} within {window} lines")
                t = _match(x - y, targets, tol)
                if t:
                    hits.append(f"{x:g} - {y:g} = {x - y:g} reproduces "
                                f"masked operand {t:g} within {window} lines")
                for c in range(b + 1, len(pool)):
                    z = pool[c]
                    t = _match(x + y + z, targets, tol)
                    if t:
                        hits.append(f"{x:g} + {y:g} + {z:g} = {x + y + z:g} "
                                    f"reproduces masked operand {t:g}")
                    t = _match(x - y - z, targets, tol)
                    if t:
                        hits.append(f"{x:g} - ({y:g} + {z:g}) = "
                                    f"{x - y - z:g} reproduces masked "
                                    f"operand {t:g}")
    return sorted(set(hits))[:8]


def reconstructible_by_column_sum(masked: str, operands: list,
                                  tol: float = 0.01) -> list:
    """Operands still derivable by summing a remaining table column.

    Financial statements are full of movement / roll-forward tables:

        Opening balance      8,053
        Additions            5,253
        Additions            1,256
        Transfers           (7,563)
        Disposals             (490)
        Closing balance      6,509   <- removed by the mask

    Deleting the closing row hides the figure but not the information: the
    column still sums to it. A mask that leaves this intact produces an item
    whose "insufficient_data" gold is simply wrong, and no other guard here
    catches it -- the operand really is absent as a literal string.

    The mirror case is a summary table that keeps its TOTAL row:

        Rights and licences              13
        Internally generated software  7,381
        Software under development       ---   <- removed by the mask
        Total intangible assets       23,678

    Here the removed component is recoverable as total minus siblings.

    Checks both, per column of the pipe-delimited render: whether the signed
    sum of surviving cells reproduces an operand, and whether any single cell
    minus the others does.
    """
    rows = parse_value_rows(masked)
    if not rows:
        return []
    width = max(len(v) for _, v in rows) if rows else 0
    targets = []
    for o in operands:
        try:
            targets.append(abs(float(o)))
        except ValueError:
            continue
    if not targets:
        return []

    hits = []
    for col in range(width):
        vals = [v[col] for _, v in rows if col < len(v)]
        if len(vals) < 2:
            continue

        # (a) roll-forward: the column of components sums to the masked total
        total = abs(sum(vals))
        for t in targets:
            if t and abs(total - t) <= max(tol, abs(t) * 0.001):
                hits.append(f"column {col} of the remaining table sums to "
                            f"{total:g}, reproducing masked operand {t:g}")

        # (b) total-minus-components: a summary table keeps its TOTAL row and
        # the sibling components, so a removed component is recoverable as
        # total - sum(siblings). Found by hand on a TAT-QA intangible-assets
        # table where 23,678 - (13 + 7,381) = 16,284, the masked figure.
        for i, cand_total in enumerate(vals):
            others = sum(v for j, v in enumerate(vals) if j != i)
            residual = abs(cand_total - others)
            for t in targets:
                if t and abs(residual - t) <= max(tol, abs(t) * 0.001):
                    hits.append(
                        f"column {col}: {cand_total:g} minus the other "
                        f"entries ({others:g}) gives {residual:g}, "
                        f"reproducing masked operand {t:g}")

        # (c) partial sums within a column. The Boeing case: three period
        # columns, the total row masked for two of them, and the two
        # component rows still summing to it. A whole-column sum misses this
        # whenever the column also carries unrelated rows, so pairs and
        # triples drawn from the column are checked directly.
        if 2 <= len(vals) <= 14:
            for i in range(len(vals)):
                for j in range(i + 1, len(vals)):
                    t = _match(vals[i] + vals[j], targets, tol)
                    if t:
                        hits.append(
                            f"column {col}: {vals[i]:g} + {vals[j]:g} = "
                            f"{vals[i] + vals[j]:g}, reproducing masked "
                            f"operand {t:g}")
                    for k in range(j + 1, len(vals)):
                        t = _match(vals[i] + vals[j] + vals[k], targets, tol)
                        if t:
                            hits.append(
                                f"column {col}: {vals[i]:g} + {vals[j]:g} + "
                                f"{vals[k]:g} reproduces masked operand "
                                f"{t:g}")

    # reconstructible_by_window is deliberately NOT called here. Measured on
    # the 93 reviewed masked items it fires on 27% of the ones a human
    # rejected and 22% of the ones a human kept -- a 5-point lift on a 22%
    # base rate, which is coincidence, not signal. Wiring it in would discard
    # roughly one good item in five to catch roughly one bad one in four. It
    # is exposed for human triage instead; see ADVISORY note on that function.
    return sorted(set(hits))
