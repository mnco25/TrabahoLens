# TrabahoLens Development Guide

## Build & Run Commands

### Environment Setup
- Install dependencies: `uv sync`
- Activate virtual environment: `source .venv/bin/activate` (or use `uv run`)

### Site Serving
- Run local dev server: `uv run python scripts/serve.py`
- Default URL: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Data Pipeline
- Full rebuild: `uv run python scripts/build_site_data.py`
- Rescore occupations (OpenRouter): `uv run python scripts/score_ai_only.py` (requires `OPENROUTER_API_KEY`)
- Methodology checks: `uv run python scripts/check.py`

### Testing
- Run validation tests: `uv run pytest tests/` (if implemented) or use `scripts/check.py`

## Code Style & Standards

### Frontend (site/)
- **Structure**: Single-page application (SPA) in `site/index.html`.
- **Logic**: Vanilla JavaScript, functional approach for treemap rendering.
- **Styling**: Vanilla CSS with custom properties for theme and color scales.
- **Components**: Bento-style dashboard layout with interactive tiles and a details drawer (Risk Panel).
- **Aesthetics**: Minimalist, dark-mode focused, glassmorphic elements, smooth transitions.

### Backend (scripts/ & src/)
- **Language**: Python 3.10+ managed via `uv`.
- **Naming**: `snake_case` for variables and functions, `PascalCase` for classes.
- **Docs**: Preservation of existing docstrings and comments.
- **Data**: JSON and CSV intermediates are stored in `data/derived/`.

## Key Components
- `DataReceipt`: Logic for summarizing labor market footprints.
- `ChartFrame`: Reusable containers for treemap and histogram blocks.
- `RiskVector`: Explainer system for LLM-driven task reshaping.
