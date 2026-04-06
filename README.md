# TrabahoLens — AI Exposure of the Philippine Job Market

A research tool for visually exploring Philippine labor market structure and AI exposure risk. This is not a report, a paper, or a serious economic publication — it is a development tool for exploring Philippine occupation data visually.

## What's here

TrabahoLens adapts the architecture and visualization style of [karpathy.ai/jobs](https://karpathy.ai/jobs/) to a Philippine context. The treemap now uses an O*NET-based occupation list mapped to PSOC major groups, with employment, wage, informality, OFW-share, and hiring-intensity estimates aligned to Philippine data sources. Each rectangle's **area** is proportional to total employment and **color** shows the selected metric.

## Layers

TrabahoLens currently supports six layers:

1. **AI Exposure** — Generative-AI/LLM score from `score_ai_only.py`, calibrated for Philippine labor dynamics.
2. **Avg. Wage (₱)** — Monthly wage estimates aligned to PSA OWS concepts.
3. **Education** — Education code and label derived from the curated occupation master.
4. **Hiring Intensity** — Placeholder 0–100 demand proxy for later PhilJobNet replacement.
5. **OFW Share** — Estimated PSOC-group share working abroad from PSA Survey on Overseas Filipinos 2024.
6. **Informal %** — Curated informal-sector share aligned to PSA labor concepts.

## LLM-powered coloring

The repo includes a pipeline for writing custom LLM prompts to score and color occupations by any criteria. You write a prompt, the LLM scores each occupation, and the treemap colors accordingly.

**AI Exposure measures generative AI and LLM-driven task displacement risk only.**

What "AI Exposure" is NOT:
- It does **not** measure machinery automation (autonomous vehicles, robotics, autonomous farming equipment).
- It does **not** measure platform algorithms and optimization (dispatch routing, dynamic pricing, algorithmic management).
- It does **not** predict job disappearance, only significant work transformation.
- The scores are LLM estimates from Claude, not rigorous econometric predictions.

The layer focuses on generative AI (ChatGPT, Claude, code generation, writing synthesis, design feedback) and how LLMs will reshape occupations in the Philippines. Machine learning models without generative capabilities and non-AI platform algorithms are excluded this cycle.

## Philippine scoring rubric

The scoring prompt in `score_ai_only.py` is calibrated for Philippine labor dynamics:

- **OFW Channel Risk**: High `ofw_share` means LLM adoption at destination markets may reshape tasks sooner (for example, foreign firms automating drafting and analysis workflows).
- **Informal Economy Buffer**: High `informal_share` slows LLM adoption because informal workplaces use less software.
- **Infrastructure and Adoption Delay**: Enterprise AI adoption in the Philippines generally follows global trends with delay.
- **Task Value and Standardization**: Standardized, text-heavy, and routine digital tasks are more exposed than physical or relationship-centric tasks.

Score anchors (Generative AI Only):

- 0–1: Minimal. Physical work with no LLM exposure pathway (carpenter, nurse, delivery rider, electrician).
- 2–3: Low. Some documentation but LLM is not core to value creation (supervisor, machine operator).
- 4–5: Moderate. Mixed routine and judgment work; LLM assists but does not replace core tasks (accountant, junior analyst).
- 6–7: High. Standardized knowledge work; LLM capable of most tasks (copywriter, junior engineer, data analyst, translator).
- 8–9: Very high. Routine digital processing; LLM already capable of most output (content writer, junior researcher).
- 10: Maximum. Pure text-in, text-out with no domain judgment (transcriptionist, form automation).

Expected average: ~3.5–4.5 across Philippine occupations (lower than previous conflated baseline).

### Explicit Exclusions (This Cycle)

This layer does **not** include:
- **Machinery/Robotics Automation**: Autonomous vehicles, robotic systems, precision agriculture robots, manufacturing automation.
- **Non-Generative Platform Algorithms**: Dispatch optimization, route planning, dynamic pricing, algorithmic management systems.

These are real disruption risks but are distinct from generative AI exposure and will be measured separately in future iterations.

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
6. **Score** (`score_ai_only.py`) — Sends each occupation profile to Anthropic Claude Haiku using the strict generative-AI rubric and writes `scores_ai_only.json`.
7. **Build site data** (`build_site_data.py`) — Merges `occupations_ph.csv` and `scores_ai_only.json` into `site/data.json` for the visualization.
6. **Website** (`site/index.html`) — Interactive treemap visualization with Philippine-calibrated layers and tooltips.

## Key files

| File | Description |
|------|-------------|
| `occupations_ph.json` | Master list of Philippine occupations in the canonical schema |
| `data/onet_occupations.json` | Parsed O*NET occupation data and Job Zone education codes |
| `data/ph_occupations_v2.json` | Philippines-relevant occupation list filtered from O*NET plus PH-specific records |
| `data/ph_occupations_v2_with_stats.json` | Filtered occupations with wage, employment, informal, and OFW stats |
| `occupations_ph.csv` | Tabulated CSV used by scoring and site build |
| `scores.json` | Historical AI exposure scores from the old conflated rubric |
| `scores_ai_only.json` | AI exposure scores (0-10) with strict generative-AI-only rationales |
| `fetch_onet.py` | O*NET text database downloader and parser |
| `filter_ph_occupations.py` | O*NET-to-Philippines occupation filter |
| `assign_ph_stats.py` | Philippine wage/employment/statistics assignment stage |
| `fetch_psa.py` | PSA OpenSTAT PXWeb fetcher for LFS and OWS tables |
| `score.py` | Historical scorer for the old conflated AI/automation rubric |
| `score_ai_only.py` | Anthropic scorer for strict generative-AI/LLM exposure |
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

# Score AI exposure (strict generative-AI rubric)
python3 score_ai_only.py

# Build website data
python3 build_site_data.py

# Serve locally
cd site && python3 -m http.server 8000
```

## Credits

This project is directly inspired by [karpathy.ai/jobs](https://karpathy.ai/jobs/), adapted for Philippine labor-market structure and data sources from PSA, OWS, POEA, IBPAP, PhilJobNet, and TESDA.
