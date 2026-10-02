# Gemma experiment

Model: `google/gemma-4-E4B-it`, about 8B parameters including embeddings.
[Model card](https://huggingface.co/google/gemma-4-E4B-it).

`config.gemma.json` changes only the model and output folder from `config.json`.
The prompts, role data, seed, sampling, thinking-off setting, and JSON schema stay
unchanged. Sampling is matched to the Qwen experiment, not tuned for Gemma.
`sweep.json` still controls rounds, identity modes, and generations.

Stop the existing server on port 8000. In the vLLM environment:

```bash
python3 -m pip install -U 'vllm>=0.19.1'

CUDA_VISIBLE_DEVICES=2 vllm serve google/gemma-4-E4B-it \
  --host 127.0.0.1 --port 8000 \
  --max-model-len 16384 \
  --limit-mm-per-prompt '{"image": 0, "audio": 0}' \
  --reasoning-parser gemma4
```

The [vLLM recipe](https://recipes.vllm.ai/Google/gemma-4-E4B-it)
specifies vLLM 0.19.1+ and a single 24GB+ GPU. Actual fit depends on available memory.
The client sends `enable_thinking: false`; the parser is Gemma-specific.

From the repository root, in another terminal:

```bash
python3 -m src.fin_debate_failure.sweep \
  --config src/fin_debate_failure/config.gemma.json \
  --rows 5 --rounds 1 2 3 \
  --identity-modes fake_ticker real_name --generations 1
```

Expected: **810 calls; 270 CSV rows**. No evaluation runs.
Output: `src/fin_debate_failure/runs/gemma4/sweep_<timestamp>/decisions.csv`.
Prompts, responses, and settings are saved alongside it.
Add `--dry-run` to check configuration without contacting vLLM.

For a short compatibility check before the full grid:

```bash
python3 -m src.fin_debate_failure.sweep \
  --config src/fin_debate_failure/config.gemma.json \
  --rows 1 --rounds 1 --identity-modes fake_ticker --generations 1
```

This makes 18 calls. Live serving and GPU memory fit must be verified locally.
