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

# score a subset
uv run python scripts/score_ai_only.py --start 0 --end 10

# force a full rerun
uv run python scripts/score_ai_only.py --force

# rebuild the frontend dataset after scoring
uv run python scripts/build_site_data.py
```

## Notes

- The supported scorer is `scripts/score_ai_only.py`.
- Output is written to `data/derived/scores_ai_only.json`.
- Missing `OPENROUTER_API_KEY` now fails with a direct setup message.
- Historical experimental scorers have been removed from the supported open-source repo surface.
