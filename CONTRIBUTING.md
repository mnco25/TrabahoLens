# Contributing

Thanks for taking an interest in TrabahoLens.

## Development

1. Install dependencies with `uv sync`.
2. Run `uv run python scripts/check.py` before submitting changes.
3. If you change derived data, rebuild the affected outputs and include them in the same change.

## Scope

- Keep the default local run path simple.
- Treat `data/reference/` as curated source input.
- Treat `data/derived/occupations_ph.csv` and `data/derived/scores_ai_only.json` as the only committed derived artifacts.
- Treat `data/raw/` as local-only fetch output and do not commit it.

## Pull Requests

- Explain what changed and why.
- Mention any dataset or methodology change clearly.
- Include screenshots if you change the site experience.
