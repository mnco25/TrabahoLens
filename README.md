# TrabahoLens — AI Exposure of the Philippine Job Market

A research tool for visually exploring Philippine labor market structure and AI exposure risk. This is not a report, a paper, or a serious economic publication — it is a development tool for exploring Philippine occupation data visually.

## What's here

TrabahoLens adapts the architecture and visualization style of karpathy/jobs to a Philippine context. The treemap currently uses a hand-curated occupation list mapped to PSOC major groups, with employment and wage estimates aligned to PSA concepts. Each rectangle's **area** is proportional to total employment and **color** shows the selected metric — OFW risk, median pay, education, informal share, or AI exposure.

## LLM-powered coloring

The repo includes a pipeline for writing custom LLM prompts to score and color occupations by any criteria. You write a prompt, the LLM scores each occupation, and the treemap colors accordingly. The default "Digital AI Exposure" layer is calibrated for the Philippines and accounts for OFW channel risk, informal economy buffering, platform/gig disruption, and local infrastructure constraints.

**What "AI Exposure" is NOT:**
- It does **not** predict that a job will disappear.
- It does **not** account for demand elasticity, latent demand, regulatory barriers, or social preferences for human workers.
- The scores are rough LLM estimates (Claude Haiku via Anthropic), not rigorous predictions. Many high-exposure jobs will be reshaped, not replaced.

## Data pipeline

1. **Fetch PSA metadata/data** (`fetch_psa.py`) — Queries PSA OpenSTAT PXWeb API for LFS occupation employment and OWS wage tables, saving raw JSON to `data/psa_raw/` and printing variable codes.
2. **Curate occupation master** (`occupations_ph.json`) — Hand-curated Philippine occupation list with PSOC major group, employment/wage estimates, informality, OFW channel, and narrative context.
3. **Tabulate** (`make_csv_ph.py`) — Converts curated JSON into `occupations_ph.csv` for downstream processing.
4. **Score** (`score.py`) — Sends each occupation profile to Anthropic with a Philippine AI-exposure rubric. Outputs `scores.json`.
5. **Build site data** (`build_site_data.py`) — Merges `occupations_ph.csv` and `scores.json` into `site/data.json`.
6. **Website** (`site/index.html`) — Interactive treemap visualization with Philippine-calibrated layers and tooltips.

## Key files

| File | Description |
|------|-------------|
| `occupations_ph.json` | Master list of Philippine occupations with PSOC and labor-structure fields |
| `occupations_ph.csv` | Tabulated CSV used by scoring + site build |
| `scores.json` | AI exposure scores (0-10) with rationales |
| `fetch_psa.py` | PSA OpenSTAT PXWeb fetcher for LFS and OWS tables |
| `build_site_data.py` | Merges CSV + scores into `site/data.json` |
| `site/` | Static website (treemap visualization) |

## LLM prompt

The scoring prompt in `score.py` is calibrated for Philippine labor dynamics:
- OFW channel risk
- Informal economy buffer
- Platform/gig disruption
- Philippine infrastructure deployment constraints

Output schema is strict JSON:
`{"exposure": <0-10>, "rationale": "...", "primary_risk_vector": "..."}`

## Setup

```bash
uv sync
# or
pip install -r requirements.txt
```

Requires an Anthropic API key in `.env`:

```bash
ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
# Create tabulated CSV from curated occupation list
uv run python make_csv_ph.py

# (Optional) Fetch PSA raw JSON tables + metadata
uv run python fetch_psa.py

# Score AI exposure (Anthropic)
uv run python score.py

# Build website data
uv run python build_site_data.py

# Serve locally
cd site && python -m http.server 8000
```

## Credits

This project is directly inspired by [karpathy/jobs](https://github.com/karpathy/jobs), adapted for Philippine labor-market structure and data sources (PSA, OWS, POEA, IBPAP).
