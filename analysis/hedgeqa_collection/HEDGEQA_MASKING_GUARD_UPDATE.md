# Masking guard update — the `total_minus_components` gap

The human review flagged **11 `total_minus_components` leaks on masked items
the automated guard had passed**. This documents what was wrong, what was
fixed, and — importantly — what could not be fixed.

---

## 1. The gap

`reconstructible_by_column_sum` began with:

```python
rows = [r.split("|") for r in masked.splitlines() if "|" in r]
if not rows:
    return []
```

Every line without a pipe was discarded. All 11 flagged items are
FinanceBench filings, and **every one of them contains zero pipe
characters** — 0 of 99 lines, 0 of 34, 0 of 70. The guard returned an empty
list on line 3 without examining anything.

Their actual layout is vertical: a label on its own line, then one numeric
line per period.

```
Sales of products
$55,893
$51,386
$47,142
Sales of services
10,715
10,900
11,016
Total revenues
58,158            <- two of the three period totals were masked
```

`47,142 + 11,016 = 58,158` exactly. The information was never removed, only
the literal string.

## 2. What was fixed

**`parse_value_rows()`** replaces the pipe-only reader and recovers
`(label, values)` rows from three layouts:

| layout | example |
|---|---|
| pipe-delimited | `Total \| 23,678 \| 12,907` |
| whitespace table | `Total revenues   58,158   62,286` |
| vertical run | `Total revenues` / `58,158` / `62,286` |

Rows pool across the whole document, so a total in one block reconciles
against components in another. The existing column checks — whole-column sum,
and one cell minus the others — now run over this richer row set, and a third
was added: **partial sums** (pairs and triples drawn from a column), because
a whole-column sum misses the Boeing case whenever the column also carries
unrelated rows.

### A regression caught on the way

Parsing pipe cells by whitespace-splitting made a header cell `30 June 2019`
yield `30` and `2019`, injecting them into the value columns and destroying
the positional alignment every check depends on. The existing
`test_catches_total_minus_components_reconstruction` failed immediately.
Layout-1 parsing is back to whole-cell, and
`test_pipe_header_cells_do_not_leak_numbers` pins it.

## 3. What could NOT be fixed, and why that matters

A prose reconstruction — "total revenues of X comprised A and B" — has no
table structure at all. The natural approach is a small subset-sum search
over nearby numbers. It was implemented as `reconstructible_by_window` and
then **deliberately not wired into the rejecting guard**, because measuring
it on the 93 human-reviewed masked items showed it does not work:

| check | fires on human-REJECTED | fires on human-KEPT | discrimination |
|---|---|---|---|
| `colsum` | 0% | 0% | none |
| `total_minus` | 0% | 0% | none |
| `partial` (new) | 14% | 8% | +5 pts |
| `window` (new) | 27% | **22%** | +5 pts |

A 5-point lift on a 22% base rate is coincidence, not signal. Wiring the
window search in would have **rejected 13 of the 49 human-verified-good
items (27%) while catching only 1 of the 11 it was built for.**

The reason is structural: a filing contains hundreds of figures, and their
pairwise and three-way sums land within tolerance of almost any target. The
human reviewer succeeded because they reasoned about which figures are
*semantically relevant to the question*. The guard has no semantics, and no
threshold separates the two populations.

**So the honest position is that arithmetic reconstruction cannot be
detected reliably by search on this corpus.** The window function is kept as
an ADVISORY — it can produce a shortlist for a human — and is asserted by
test to stay out of `mask_directional`.

## 4. Tests added

All **22 pass**, including every pre-existing one.

| test | what it pins |
|---|---|
| `test_parses_vertical_label_then_numbers_layout` | layout 3 parsing |
| `test_parses_whitespace_table_layout` | layout 2 parsing |
| `test_pipe_header_cells_do_not_leak_numbers` | **regression** — date headers contribute no values |
| `test_catches_total_minus_components_in_prose_layout` | **required** — the real Boeing case, no pipes |
| `test_catches_reconstruction_spanning_two_blocks` | **required** — total and components in separate blocks |
| `test_catches_one_step_deeper_total_minus_several_components` | **required** — total minus three siblings |
| `test_negative_control_ordinary_totals_do_not_fire` | **required negative control** — an innocent consistent statement is not rejected, by either the guard or the advisory |
| `test_window_search_stays_advisory` | the window search must never gate `mask_directional` |

## 5. Did the 319-item collection change?

**No. `hedgeqa_core_v0_1_validated_candidates.jsonl` is byte-identical
(md5 verified), and no human-failed variant was re-admitted** — the guard
only ever rejects, and the validated file is derived from the human verdict
rather than from the guard.

**But a rebuild would churn the core, so the reviewed artifacts are pinned.**
Re-running the builders with the tightened guard produced **12 added and 12
removed** core ids: the stricter guard rejects some masked candidates at
construction time and the quota refills with different ones. Seven of the 12
removed are in the validated 319, and all 12 added have never been reviewed
by anyone.

The candidate pools, full collection and core were therefore **restored to
the reviewed state**. The tightened guard applies to *future* mask
construction; the reviewed core is frozen, because the human review is keyed
to those 368 ids and silently swapping 12 of them would break that linkage
without any visible error.

## 6. Are the smoke manifests affected?

**No.** Both are built from the validated 319, which did not change.
`hedgeqa_core_v0_1_smoke_15.jsonl` and
`hedgeqa_core_v0_1_edge_smoke_15.jsonl` are deterministic across consecutive
builds and disjoint from each other.

## 7. Limitations of the improved guard

1. **It cannot detect prose reconstruction.** The only mechanism that could
   has no discrimination on this corpus and is advisory-only.
2. **Its two original checks fire on 0% of this corpus, in both
   directions.** They catch the synthetic cases in the tests and the one
   hand-found TAT-QA item; they found nothing in 93 real reviewed items. The
   layout fix makes them *able* to see FinanceBench at all, which they
   previously could not — but that is extended coverage, not demonstrated
   yield.
3. **The partial-sum check has a measured 8% false-positive rate** on
   human-verified-good items. It is kept because failing closed is the
   stated philosophy and it only ever reduces the number of masks built,
   but it is not free.
4. **Alignment is assumed, not verified.** Column *i* is treated as period
   *i* across rows. A filing that interleaves a differently-shaped block
   will misalign, producing either a missed leak or a spurious hit.
5. **Nothing here validates a mask.** Passing the guard means no *modelled*
   reconstruction route was found. The human review remains the only
   evidence that a mask holds, and it disagreed with the automated
   assessment on 47% of items.

## 8. Recommendation

Do not treat this as closing the gap. The measured discrimination says the
gap is **not closable by arithmetic search**, and the practical consequence
is that **every future batch of masked variants needs human reading** — the
guard narrows the candidate set and nothing more. If a larger masked stratum
is wanted, the cost is reviewer time, not a better regex.
