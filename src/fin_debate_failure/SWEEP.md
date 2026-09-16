# Parameter sweep

Use `config.json` for model, data, roles, seed, and inference settings.
Use `sweep.json` for the parameter grid:

```json
{
  "rounds": [1, 2, 3],
  "identity_modes": ["fake_ticker", "real_name"],
  "generations": [1]
}
```

Run every combination:

```bash
python3 -m src.fin_debate_failure.sweep
```

Override parameters:

```bash
python3 -m src.fin_debate_failure.sweep \
  --rows 5 --rounds 1 2 3 \
  --identity-modes fake_ticker real_name --generations 1 3
```

Preview the call count without inference:

```bash
python3 -m src.fin_debate_failure.sweep --dry-run
```

`--output PATH` chooses a new output folder. Existing folders are never overwritten.
Default output: `runs/sweep_<timestamp>/decisions.csv`.

## Sampling and rounds

- Round 0 is an independent baseline. `--rounds 3` adds rounds 1–3.
- `generations` is samples **per agent per round**, including baseline. Default: 1.
- Each sample uses a separate seed. All samples read the same frozen previous round.
- The next round receives every previous sample, including its decision and reason.
- Each sample gets one vote. A strict majority across all agent samples decides the round.
- No majority: `NO_MAJORITY`. Any failed or missing sample: `INCOMPLETE`.
- The sweep runs debate only. It ignores the optional self-revision control setting.
- Real mode uses **company names**, matching the earlier experiment.

Each grid entry runs separately. Seeds are paired across identity modes and round
limits. Thus, shorter runs share the intended prefix of longer runs; they are
not independent repetitions. More generations changes both voting and peer context.

Default grid: **810 calls**, **270 CSV rows**.
Adding `--generations 1 3`: **3,240 calls**, **1,080 CSV rows**.
Formula per configuration: companies × 3 questions × agents × (rounds + 1) × generations.

## CSV

One row = one company × question × round × generation within a configuration.

| Columns | Meaning |
| --- | --- |
| `RunID`, `Model`, `Seed` | Run identification |
| `DebateRounds`, `IdentityMode`, `GenerationsPerAgent` | Grid settings |
| `FakeTicker`, `DisplayName`, `QuestionType`, `Question` | Matched company and question |
| `Round`, `Stage`, `IsFinalRound`, `Generation` | Position in the debate |
| `fundamental_Decision`, `fundamental_Reasoning`, `fundamental_Status` | Fundamental sample |
| `trading_Decision`, `trading_Reasoning`, `trading_Status` | Trading sample |
| `challenger_Decision`, `challenger_Reasoning`, `challenger_Status` | Challenger sample |
| `DebateDecision`, `DebateStatus`, `VoteCounts` | Round result across every sample |

The round result repeats on its generation rows. It is not a separate vote for
each generation row. Filter `IsFinalRound=True` for each configuration's last result.
Reasoning stays in separate cells. Multiline text is CSV-quoted for Excel.

`calls.jsonl` preserves exact prompts, request seeds, JSON answers, and provider
responses. `manifest.json` preserves settings and hashes. No evaluation is run.
Connection errors stop the sweep and preserve partial results. There is no resume.

## Model and GPU 2

Default: `Qwen/Qwen3.5-9B`, thinking disabled. It is the largest model under 10B
in the latest small-model release verified in the [official release list](https://github.com/QwenLM/Qwen3.8#news).
See the [model card](https://huggingface.co/Qwen/Qwen3.5-9B) for serving details.
Stop the old server on port 8000, then run:

```bash
CUDA_VISIBLE_DEVICES=2 vllm serve Qwen/Qwen3.5-9B \
  --host 127.0.0.1 --port 8000 \
  --language-model-only --max-model-len 16384 --reasoning-parser qwen3
```

Start the sweep in another terminal. Large generation counts increase peer
context and can exceed the server's context limit. Errors are saved, not retried.
