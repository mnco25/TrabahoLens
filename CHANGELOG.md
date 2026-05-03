# Changelog

All notable changes to the TrabahoLens project will be documented in this file.

## [1.2.0] - 2026-05-03
### Added
- **PWA Integration**: Full manifest and theme support for home-screen installation.
- **Enhanced SEO**: Metadata for social sharing (OpenGraph, Twitter cards) and search indexing.
- **Bento UI Overhaul**: Modernized dashboard layout with "morphic" aesthetics and glassmorphic details.
- **Detailed Risk Panel**: An interactive drawer that explains AI risk vectors and economic footprints per occupation.
- **DataReceipt & ChartFrame**: New internal architectural patterns for data presentation.

### Changed
- **Documentation Sync**: Comprehensive audit and refinement of `README.md`, `CLAUDE.md`, `AGENTS.md`, and `CHANGELOG.md`.
- **UI Responsiveness**: Improved mobile layout for the treemap and stats grid.

## [1.1.0] - 2026-04-27
### Added
- **AI Exposure Refinement**: Narrowed focus to Generative AI and LLM-driven task displacement, removing conflation with machinery automation.
- **New Scorer**: Implementation of `score_ai_only.py` using OpenRouter (Claude-3.5-Haiku).
- **Philippine-Specific Occupations**: Added coverage for "Kasambahay", "Tricycle Drivers", and "OFW Caregivers".
- **i18n Infrastructure**: Initial support for English/Tagalog routing and translations.

## [1.0.0] - 2026-04-04
### Initial Release
- **Core Visualizer**: Treemap implementation based on Karpathy's jobs site.
- **Data Integration**: Integration of PSA (Philippine Statistics Authority) and O*NET datasets.
- **Static Pipeline**: Automated builds from CSV/JSON sources to `site/data.json`.
- **Theme System**: Minimalist dark-mode theme with interactive tooltips.
