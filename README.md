# TrabahoLens — AI Exposure of the Philippine Job Market

A research tool for visually exploring Philippine labor market structure and AI exposure risk. This is not a report, a paper, or a serious economic publication — it is a development tool for exploring Philippine occupation data visually.

## What's here

TrabahoLens adapts the architecture and visualization style of [karpathy/jobs](https://github.com/karpathy/jobs) to a Philippine context. The treemap now uses an O*NET-based occupation list mapped to PSOC major groups, with employment, wage, informality, OFW-share, and hiring-intensity estimates aligned to Philippine data sources. Each rectangle's **area** is proportional to total employment and **color** shows the selected metric.

## Layers

TrabahoLens currently supports six layers:

1. **AI Exposure** — LLM score from `score.py`, calibrated for Philippine labor dynamics.
2. **Avg. Wage (₱)** — Monthly wage estimates aligned to PSA OWS concepts.
3. **Education** — Education code and label derived from the curated occupation master.
4. **Hiring Intensity** — Placeholder 0–100 demand proxy for later PhilJobNet replacement.
5. **OFW Share** — Estimated PSOC-group share working abroad from PSA Survey on Overseas Filipinos 2024.
6. **Informal %** — Curated informal-sector share aligned to PSA labor concepts.

## LLM-powered coloring

The repo includes a pipeline for writing custom LLM prompts to score and color occupations by any criteria. You write a prompt, the LLM scores each occupation, and the treemap colors accordingly. The default AI Exposure layer is calibrated for the Philippines and accounts for OFW channel risk, informal economy buffering, platform/gig disruption, and local infrastructure constraints.

**What "AI Exposure" is NOT:**
- It does **not** predict that a job will disappear.
- It does **not** account for demand elasticity, latent demand, regulatory barriers, or social preferences for human workers.
- The scores are rough LLM estimates from Anthropic Claude Haiku 4.5, not rigorous predictions. Many high-exposure jobs will be reshaped, not replaced.

## Philippine scoring rubric

The scoring prompt in `score.py` is calibrated for Philippine labor dynamics:

- **OFW Channel Risk**: High `ofw_share` means AI may automate the destination job abroad before domestic effects arrive.
- **Informal Economy Buffer**: High `informal_share` slows adoption because informal workplaces upgrade technology less quickly.
- **Platform/Gig Disruption**: Delivery and transport workers face algorithmic management and route optimization even without LLM-style automation.
- **Philippine Infrastructure Reality**: Autonomous vehicles, precision agriculture robots, and humanoid robots face higher deployment barriers in the Philippines than in the US.

Score anchors:

- 0–1: Minimal. Physical, highly informal, no realistic automation pathway in 10 years.
- 2–3: Low. Physical plus strong informal buffer or regulatory protection.
- 4–5: Moderate. Mixed work; AI assists but does not replace core tasks.
- 6–7: High. Knowledge work or significant OFW channel risk.
- 8–9: Very high. Digital or routine work; AI already capable of most tasks.
- 10: Maximum. Pure routine digital processing; AI can do this today.

Expected average: roughly 4.5–5.0 across Philippine occupations.

Output schema is strict JSON:

```json
{"exposure": 0, "rationale": "...", "primary_risk_vector": "..."}
```

## Data pipeline

1. **Fetch PSA metadata/data** (`fetch_psa.py`) — Queries the PSA OpenSTAT PXWeb API for LFS occupation employment and OWS wage tables, saving raw JSON to `data/psa_raw/` and printing variable codes for inspection. This script is local-only and is not part of the build.
2. **Fetch O*NET data** (`fetch_onet.py`) — Downloads the O*NET 30.2 text database, extracts occupation and Job Zone files, and writes `data/onet_occupations.json`.
3. **Filter Philippines-relevant occupations** (`filter_ph_occupations.py`) — Selects the O*NET occupations that map cleanly to Philippine labor-market categories, then appends PH-specific records.
4. **Assign stats** (`assign_ph_stats.py`) — Adds wage, employment, informal-share, and OFW-share estimates to the filtered occupation list.
5. **Tabulate** (`make_csv_ph.py`) — Converts `data/ph_occupations_v2_with_stats.json` into `occupations_ph.csv` with the downstream column set.
6. **Score** (`score.py`) — Sends each occupation profile to Anthropic Claude Haiku 4.5 using the Philippine AI-exposure rubric and writes `scores.json`.
7. **Build site data** (`build_site_data.py`) — Merges `occupations_ph.csv` and `scores.json` into `site/data.json` for the visualization.
6. **Website** (`site/index.html`) — Interactive treemap visualization with Philippine-calibrated layers and tooltips.

## Key files

| File | Description |
|------|-------------|
| `occupations_ph.json` | Master list of Philippine occupations in the canonical schema |
| `data/onet_occupations.json` | Parsed O*NET occupation data and Job Zone education codes |
| `data/ph_occupations_v2.json` | Philippines-relevant occupation list filtered from O*NET plus PH-specific records |
| `data/ph_occupations_v2_with_stats.json` | Filtered occupations with wage, employment, informal, and OFW stats |
| `occupations_ph.csv` | Tabulated CSV used by scoring and site build |
| `scores.json` | AI exposure scores (0-10) with rationales |
| `fetch_onet.py` | O*NET text database downloader and parser |
| `filter_ph_occupations.py` | O*NET-to-Philippines occupation filter |
| `assign_ph_stats.py` | Philippine wage/employment/statistics assignment stage |
| `fetch_psa.py` | PSA OpenSTAT PXWeb fetcher for LFS and OWS tables |
| `score.py` | Anthropic scorer for Philippine AI exposure |
| `build_site_data.py` | Merges CSV + scores into `site/data.json` |
| `site/` | Static treemap website |

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

## Data Sources

**O*NET 30.2 Database** (US Department of Labor)  
Used for occupation descriptions and education (Job Zone) data for non-PH-specific occupations. O*NET covers 923 occupations under Creative Commons Attribution 4.0. Philippine wage and employment data are applied separately from PSA sources.  
URL: https://www.onetcenter.org/database.html

## Usage

```bash
# Create tabulated CSV from curated occupation list
python3 make_csv_ph.py

# (Optional) Fetch PSA raw JSON tables + metadata
python3 fetch_psa.py

# Score AI exposure (Anthropic)
python3 score.py

# Build website data
python3 build_site_data.py

# Serve locally
cd site && python3 -m http.server 8000
```

## Credits

This project is directly inspired by [karpathy/jobs](https://github.com/karpathy/jobs), adapted for Philippine labor-market structure and data sources from PSA, OWS, POEA, IBPAP, PhilJobNet, and TESDA.
