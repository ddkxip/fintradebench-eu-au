# Financial debate

For parameter sweeps and one side-by-side CSV, see [SWEEP.md](SWEEP.md).

Edit `config.json`. `agents` sets the roles and their count. `rounds: 3` runs
an independent baseline (round 0), then debate rounds 1, 2, and 3.
Default: **5 companies × 3 questions × 3 agents × 4 stages = 180 calls**.
All agents use `Qwen/Qwen3.5-9B`. Thinking is disabled.
The original questions and hypothesis stay unchanged.

## Roles and data

| Role | Raw data | Job |
| --- | --- | --- |
| Fundamental | P/E, P/B, P/S, EV/EBITDA, sector P/E, quarter date | Recommend using fundamentals only. |
| Trading | Price, RSI, 50-day MA, price/MA ratios, volume and volume ratio | Recommend using trading signals only. |
| Challenger | Both sets | Check calculations, unsupported claims, role boundaries, and time horizons. Give an independent recommendation. |

All receive the company identifier and snapshot date. Sector P/E is missing.
Missing numbers remain null; agents must not invent them.

Each debate round shares all agents' completed JSON answers from the previous
round. Agents keep or change their recommendation and explain why. Calls run
sequentially, but no agent sees another agent's answer from the current round.
The challenger flags a specific claim, or explains why no challenge is needed.
It is not the final judge and does not have to disagree.

Raw data is filtered in code. **Peer reasoning can still reveal other data.**
Specialists are instructed to use only their own data as evidence. Allowed
citation names are enforced; whether prose stays in scope needs manual review.

## JSON answers

`Verdict` is the recommendation. Every reply must pass a strict JSON schema.

| Question | Allowed Verdict |
| --- | --- |
| Valuation | ATTRACTIVELY_PRICED, FAIRLY_PRICED, EXPENSIVE |
| Core holding | YES, NO |
| Confidence | BUY, SELL, HOLD |

There is no abstention option. Uncertainty belongs in the justification.
For the confidence question, a response has this form:

```json
{
  "Verdict": "HOLD",
  "Reasoning": "Price is 2.82% above its 50-day MA, while volume is near average.",
  "Confidence": "LOW",
  "MissingInformation": "A longer price and volume history.",
  "CitedIndicators": ["PriceVsSMA50_Percent", "Volume_to_AvgVol20"],
  "ChallengeTarget": null
}
```

For the other two questions, `Confidence` and `MissingInformation` are null.
Reasoning is a short justification, limited by the prompt to 180 words.
Invalid or truncated JSON counts as an error and blocks dependent rounds.
There are no retries, resume, or extra judge calls.

## Run on GPU 2

Stop the old vLLM server on port 8000 before serving the new model.
From the repository root:

```bash
python3 -m pip install -r src/fin_debate_failure/requirements.txt
python3 -m pip install -U 'vllm>=0.19.0'

CUDA_VISIBLE_DEVICES=2 vllm serve Qwen/Qwen3.5-9B \
  --host 127.0.0.1 --port 8000 \
  --language-model-only --max-model-len 16384 --reasoning-parser qwen3
```

In another terminal:

```bash
python3 -m src.fin_debate_failure --identity-mode fake_ticker
python3 -m src.fin_debate_failure --identity-mode real_name
```

[Official model instructions](https://huggingface.co/Qwen/Qwen3.5-9B)
describe vLLM serving and disabling thinking.
GPU 2 memory fit must be checked on the machine running vLLM.

Other commands:

```bash
python3 -m src.fin_debate_failure --dry-run
python3 -m src.fin_debate_failure --rounds 1
python3 -m src.fin_debate_failure --config src/fin_debate_failure/config.json
python3 -m pytest src/fin_debate_failure/tests -q
```

CLI values override config. Config changes affect new runs only.
Config paths are relative to the config file. Set `VLLM_API_KEY` if needed.
Progress bars show company, question, and round/agent progress.

## Results

Each run creates a separate folder under `runs/`.

| File | What to inspect |
| --- | --- |
| `round_answers.csv` | Group votes, reasons, and outcome changes at rounds 0–3; 60 rows. |
| `agent_behavior.csv` | Verdict counts, changes, failures, and challenges by role/question/round; 36 rows. |
| `responses.csv` | Every agent answer at every round; 180 rows. |
| `final_answers.csv` | Last-round group result; 15 rows. |
| `final_agent_answers.csv` | Last-round agent answers; 45 rows. |
| `summary.json` | Agreement by round and identity flags. |
| `calls.jsonl` | Exact prompts and full server replies. |
| `manifest.json` | Config, evidence, data hash, and code hashes. |

These counts use the default setup. Round checkpoints share the same trajectory;
you do not need three separate runs. They are not independent trials.
`ReasoningChanges` counts text changes, not meaningful improvements.
Review correctness, unsupported claims, and role adherence manually.

A group verdict needs more than half the votes. A tie gives `no_majority` and
an empty group verdict. Failed or missing answers give `incomplete`.
These are group statuses, not agent abstention options.
`OutcomeChanged` is blank for baseline or incomplete comparisons.

Optional `self_revision: true` adds 135 calls where agents see only their own
previous answers. These controls are excluded from group voting.

Both identity modes use the same instructions, values, and paired seeds.
Real-name mode hides the fake ticker from prompts but retains it as a CSV key.
Both modes hide real tickers and valuation buckets. Company name mentions are
expected in real-name mode. No identity mentions does not prove no memory use.
The first five companies all come from the workbook's Overvalued bucket.

This protocol changes data access, answer choices, model, and sampling.
Rerun both identity modes; do not treat old versus new runs as a name-only test.

## Files

- `config.json`: experiment settings.
- `protocol.py`: prompts, role field lists, and JSON validation.
- `debate.py`: round order and peer exchange.
- `inference.py`: vLLM requests.
- `data.py`: workbook loading and identity masking.
- `review.py`: round outcomes and behavior counts.
