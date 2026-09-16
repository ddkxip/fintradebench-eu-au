# Fin Debate Failure: Experiment Plan

**Baseline:** Use real financial data for 20 companies. Replace real tickers with fake tickers. Keep the numbers unchanged.

**Location:** `src/fin_debate_failure/`

**Research Question:** To be filled in.

**Motivation:** To be filled in.

## Hypothesis

1. If we replace the real ticker with a fake one, the model will not respond from memory.
   1. If it does not hold, do a perturbation and add a new hypothesis.
2. To be filled in.

## Questions

Use each template unchanged across all 20 tickers.

**1. Valuation-forcing (numerical reasoning)**

> Based on the data available to you, does [Ticker] look attractively priced, fairly priced, or expensive right now — and specifically why?

**2. Core-holding synthesis (qualitative interpretation)**

> Is [Ticker] a good core holding for a 3–5 year investment thesis, based on the information available to you?

**3. Confidence/falsifiability (uncertainty-heavy inference)**

> How confident are you in your BUY/SELL/HOLD call on [Ticker] right now, on a rough scale from low to high, and what specific piece of missing information would most change your mind?

## Setup

Use three agents with [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B), thinking off.

- **Fundamental:** Fundamental data only.
- **Trading:** Trading signals only.
- **Challenger:** Both sets. Check claims and calculations; give an independent recommendation.

- **Baseline:** Each answers alone.
- **Debate:** Three rounds. Each reads the previous round's JSON recommendations and reasons. Peer text can reveal other data.
- **Control (optional):** Each reviews only its own previous answer.

Require a recommendation and short reason in JSON. No abstention; core holding uses YES/NO. Compare agent changes and group votes after each round.

Try different LLMs for the roles later.

**Size:** Five-company smoke test: 180 responses. All 20: 720. These include baseline and three debate rounds, without control. Each identity mode is a separate pass.

## Output

```text
FakeTicker, QuestionType, Question, AgentRole, Config, Verdict, Reasoning, RawResponse
```

Keep the three agents together for each `(FakeTicker, QuestionType, Config)`. Add run, round, and control fields to separate repeat answers.

## Tasks

1. **Model Selection:** Confirm model quality and hardware fit.
2. **Data Collection:** Get and check the 20-company CSV.
3. **Debate Architecture:** Build homogeneous first; heterogeneous later.
4. **Replace Tickers:** Save the mapping. Remove real names. Preserve numbers.
5. **Collect responses:** Trial first, then run all questions.
6. **Human evaluation:** Two reviewers check evidence, calculations, uncertainty, agreement, and reasoning differences.
7. **Update claims and findings:** Report results. Keep the original hypothesis. Add a new one after perturbation if needed.

**Limit:** Fake tickers alone cannot prove that memory was not used.

**Next:** Run the five-row smoke test with vLLM. See [README.md](README.md) for commands.
