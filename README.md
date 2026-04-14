# TrabahoLens

TrabahoLens is a small research project for exploring Philippine occupations, employment size, wages, and generative-AI exposure in a static treemap view.

The repository is open-source-ready and runnable out of the box: the committed demo data is already built, so you can launch the site locally without any API key.

## Quickstart

```bash
uv sync
uv run python scripts/serve.py
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Common Commands

```bash
# Run code + data checks before opening a PR
uv run python scripts/check.py

# Rebuild site/data.json from the committed derived CSV + score cache
uv run python scripts/build_site_data.py

# Rebuild the derived CSV from the stats JSON
uv run python scripts/make_csv_ph.py

# Optional: rescore occupations with OpenRouter, then rebuild the site data
cp .env.example .env
# add OPENROUTER_API_KEY to .env
uv run python scripts/score_ai_only.py
uv run python scripts/build_site_data.py

# Optional: score with a specific OpenRouter model
uv run python scripts/score_ai_only.py --model claude-3-5-haiku
uv run python scripts/score_ai_only.py --model google/gemini-2.5-flash
uv run python scripts/score_ai_only.py --model openai/gpt-4o-mini
```

## Data Layout

- `data/reference/occupations_seed.json`
  Curated source/reference occupation records used to guide PH-specific shaping.
- `data/derived/occupations_ph.csv`
  Derived occupation table used by the supported scoring and site build steps.
- `data/derived/scores_ai_only.json`
  Derived AI exposure cache used by the site.
- `site/data.json`
  Built frontend dataset used by the static visualization.
- `data/raw/`
  Ignored local-only fetch output for O*NET and PSA downloads.

Only the files needed for local viewing and optional rescoring are committed. Pipeline intermediates are regenerated locally and ignored.

## Pipeline

The supported pipeline is:

```bash
uv run python scripts/fetch_onet.py
uv run python scripts/filter_ph_occupations.py
uv run python scripts/assign_ph_stats.py
uv run python scripts/make_csv_ph.py
uv run python scripts/score_ai_only.py   # optional, requires OPENROUTER_API_KEY
uv run python scripts/build_site_data.py
```

The repo keeps the derived demo artifacts committed so contributors can inspect the visualization without rerunning the whole pipeline.

## Data Sources

- [O*NET 30.2 Database](https://www.onetcenter.org/database.html) for occupation descriptions and job-zone inputs
- [Philippine Statistics Authority OpenSTAT](https://openstat.psa.gov.ph/) for employment and wage reference material used during dataset construction

## Notes

- `OPENROUTER_API_KEY` is only needed for rescoring.
- The default scorer model is `claude-3-5-haiku`.
- You can switch models through OpenRouter with `--model`, including Claude, Gemini, GPT, and other compatible providers.
- More detailed scoring notes live in `docs/openrouter-setup.md`.
