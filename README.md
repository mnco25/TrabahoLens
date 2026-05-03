# TrabahoLens — Philippine Job Market Visualizer

TrabahoLens is a research tool for exploring the Philippine labor market through an interactive, data-dense treemap. It visualizes 173 occupations across dimensions like employment size, wages, education requirements, and **Generative AI (LLM) exposure**.

Inspired by [karpathy.ai/jobs](https://karpathy.ai/jobs/), this adaptation is tailored for the Philippine context using data from the Philippine Statistics Authority (PSA) and O*NET.

## 🚀 Key Features

- **Interactive Treemap**: Explore the labor market at scale, where tile area represents employment volume.
- **AI Exposure Scoring**: Specialized rubric for measuring task reshaping risk from Large Language Models (LLMs).
- **Economic Footprint**: Real-time stats on total jobs, monthly payrolls, and informal sector prevalence.
- **Bento Dashboard**: A world-class, "morphic" UI with smooth transitions and glassmorphic details.
- **PWA Ready**: Installable as a mobile app with offline-capable metadata and theme support.
- **Multi-Layer Analysis**: Toggle between AI exposure, wages, education, OFW share, and hiring intensity.

## 🛠️ Quickstart

```bash
uv sync
uv run python scripts/serve.py
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 📊 Common Commands

```bash
# Run code + data checks
uv run python scripts/check.py

# Rebuild site dataset (site/data.json)
uv run python scripts/build_site_data.py

# Optional: Rescore occupations with OpenRouter
# (Requires OPENROUTER_API_KEY in .env)
uv run python scripts/score_ai_only.py --model claude-3-5-haiku
```

Detailed scoring instructions can be found in [docs/openrouter-setup.md](docs/openrouter-setup.md).

## 🧪 Methodology

### Data Sources
- **PSA LFS & OWS 2024**: Employment totals and wage reference material.
- **PSA Survey on Overseas Filipinos**: For calculating OFW share per occupational group.
- **O*NET 30.2**: For occupation descriptions and Job Zone (education) data.
- **PhilJobNet & IBPAP**: For real-time hiring intensity signals.

### AI Exposure Scoring
We use an LLM-powered pipeline to score occupations on a 0–10 scale based on their potential for **Generative AI task reshaping**.
- **Included**: Task automation in coding, writing, analysis, and routine knowledge work.
- **Excluded**: Physical machinery automation, robotics, and platform-based dispatch algorithms.

## 📁 Data Layout

- `data/reference/occupations_seed.json`: Curated source occupation records.
- `data/derived/occupations_ph.csv`: Main derived occupation table.
- `data/derived/scores_ai_only.json`: AI exposure cache used by the site.
- `site/data.json`: Final built dataset for the frontend.

## 📜 Documentation

- [CLAUDE.md](CLAUDE.md): Development guide and code standards.
- [AGENTS.md](AGENTS.md): AI scoring rubric and agent role descriptions.
- [CHANGELOG.md](CHANGELOG.md): History of project updates.
- [CONTRIBUTING.md](CONTRIBUTING.md): Guidelines for project contributors.
- [SECURITY.md](SECURITY.md): Security reporting policy.
