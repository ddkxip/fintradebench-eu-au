# Findings

Source: `runs/sweep_20260916T234554_810584Z/decisions.csv`.
Model: Qwen3.5-9B. Five companies. Three questions. One seed. One generation.
All 810 responses completed without recorded response errors.

## Row summaries

`row_summaries.csv` keeps all 270 original rows and reasoning fields.
Added columns describe the votes, changes from the prior round, and matched
identity differences. Each agent's short reasoning summary is an extract of
its first two sentences. These extracts are not a full factual audit.
`SourceRow` starts at 1 for the first data row, excluding the CSV header.

## Fake versus real names

Use the three-round runs to avoid counting repeated prefixes as new evidence.
The one-round and two-round runs repeat the same matching decisions AND reasons.
There are 120 distinct company/question/identity/round observations, not 270
independent observations. Repeated rounds within a trajectory are also dependent.

| Round | Different group outcomes | Different agent decisions |
| --- | --- | --- |
| Baseline (0) | 5/15 | 11/45 |
| 1 | 4/15 | 9/45 |
| 2 | 3/15 | 7/45 |
| 3 | 4/15 | 8/45 |

Round-3 differences:

| Company | Question | Fake | Real |
| --- | --- | --- | --- |
| McDonald's | Confidence | NO_MAJORITY | HOLD |
| NVIDIA | Core holding | NO | YES |
| NVIDIA | Confidence | SELL | HOLD |
| Johnson & Johnson | Valuation | ATTRACTIVELY_PRICED | NO_MAJORITY |

The remaining 11 group outcomes match. Matching verdicts do not imply matching reasons.

## Evidence about memory

Real-name answers add context absent from the data:

- Caterpillar: industrial/cyclical leader (source row 223, challenger).
- McDonald's: brand strength (source row 239, challenger).
- Johnson & Johnson: historical norms for a mature healthcare company (source row 259, fundamental).

These claims are consistent with background knowledge prompted by the name.
They are not proof of the internal mechanism producing the answer.
An exact-name/ticker scan found no actual workbook identities in the 180 fake-mode
agent reasoning texts from the three-round run. This only tests explicit mentions.

Fake answers also contain unsupported inferences. For example, UDAX's baseline
fundamental answer claims extreme future growth is not currently realized and
compares earnings power with peers, without growth or peer data (source row 151).
At round 1, its fundamental answer discusses RSI and price/SMA values received
through peers (row 152). Filtering raw fields does not enforce isolation in prose.

## Conclusion

The results support sensitivity to company identity. They do not establish:
“If we replace the real ticker with a fake one, the model will not respond from memory.”
Both modes cite supplied numbers. Neither citations nor written reasons prove
that memory was excluded. Learned knowledge and reasoning can operate together.

Unanimous groups increase from 8 to 9 of 15 in fake mode and from 6 to 7 in real
mode between baseline and round 3. This measures agreement, not correctness.
The identity difference does not decline consistently with more debate rounds.

Next: vary the numbers under fixed names, and vary names under fixed numbers.
Repeat across seeds. Annotate unsupported company-specific claims and numerical
correctness. The current forced-choice protocol cannot abstain, which must be
considered when interpreting decisive answers. The five companies are all from
the workbook's Overvalued bucket; this does not establish an objectively correct verdict.
