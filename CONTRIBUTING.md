# Contributing to TrabahoLens

Thank you for your interest in contributing to TrabahoLens! We welcome contributions that improve the accuracy of our labor-market data or enhance the visualization experience.

## Development Workflow

1.  **Environment**: Use `uv` for package management. Run `uv sync` to install dependencies.
2.  **Checks**: Always run `uv run python scripts/check.py` before submitting a pull request to ensure data integrity and code quality.
3.  **Data Changes**: If you modify the scoring rubric or underlying reference data, please rebuild the site data using `uv run python scripts/build_site_data.py` and include the updated `site/data.json` in your PR.

## Scope & Philosophy

- **Simplicity**: Keep the static site lightweight. Avoid adding heavy client-side frameworks unless necessary.
- **Data Integrity**: Curated source input lives in `data/reference/`. Derived artifacts that are committed (`occupations_ph.csv`, `scores_ai_only.json`) should only be updated via the official scripts.
- **Transparency**: Any changes to the AI scoring methodology must be documented in `AGENTS.md`.

## Pull Requests

- **Rationale**: Clearly explain *what* changed and *why* it matters for the Philippine labor market context.
- **Visuals**: If you change the UI (especially the treemap or dashboard), please include "before and after" screenshots.
- **Testing**: Ensure the site still runs locally using `uv run python scripts/serve.py`.
