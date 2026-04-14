# OpenRouter Scoring

TrabahoLens can re-score the derived occupation dataset through OpenRouter, but scoring is optional. The committed repo already includes a score cache so anyone can run the site locally without an API key.

## Setup

```bash
cp .env.example .env
# add your OPENROUTER_API_KEY
```

## Commands

```bash
# score all occupations
uv run python scripts/score_ai_only.py

# score with the default model
uv run python scripts/score_ai_only.py --model claude-3-5-haiku

# example alternatives through OpenRouter
uv run python scripts/score_ai_only.py --model anthropic/claude-3.5-haiku
uv run python scripts/score_ai_only.py --model google/gemini-2.5-flash
uv run python scripts/score_ai_only.py --model openai/gpt-4o-mini

# score a subset
uv run python scripts/score_ai_only.py --start 0 --end 10

# force a full rerun
uv run python scripts/score_ai_only.py --force

# rebuild the frontend dataset after scoring
uv run python scripts/build_site_data.py
```

## Notes

- The supported scorer is `scripts/score_ai_only.py`.
- The current default model in code is `claude-3-5-haiku`.
- You can override the model at runtime with `--model <openrouter-model-id>`.
- Typical choices include Claude, Gemini, GPT, and other models exposed by your OpenRouter account.
- Exact provider-qualified model IDs can change over time, so check the current OpenRouter catalog if a slug stops resolving.
- Output is written to `data/derived/scores_ai_only.json`.
- Missing `OPENROUTER_API_KEY` now fails with a direct setup message.
- Historical experimental scorers have been removed from the supported open-source repo surface.
