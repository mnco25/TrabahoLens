# TrabahoLens AI Agent Guidelines

This document outlines the roles and methodologies for AI agents (Claude, Antigravity, etc.) interacting with the TrabahoLens codebase and data pipeline.

## Agent Roles

### 1. The Scorer (scripts/score_ai_only.py)
- **Role**: Evaluates Philippine occupations for Generative AI (LLM) exposure.
- **Rubric**: Focuses exclusively on task reshaping risk from Large Language Models. Excludes machinery automation and platform-based algorithmic dispatch.
- **Model Selection**: Default is `claude-3-5-haiku`. Compatible with OpenRouter providers (Gemini, GPT, etc.).
- **Context**: Uses O*NET task descriptions and PH-specific occupational context (e.g., OFW share, informal sector prevalence).

### 2. The Developer Assistant (Antigravity/Claude)
- **Role**: Refines the frontend, updates the pipeline, and ensures documentation sync.
- **Priority**: Maintain the "Karpathy-style" minimalism while elevating the UX with "world-class" aesthetics (glassmorphism, micro-animations).
- **Guidelines**: Ensure all UI changes are responsive and performant (e.g., using `requestAnimationFrame` for canvas draws).

## Methodology: LLM Scoring Rubric

When scoring or generating rationale for occupations, agents should consider the following "Risk Vectors":

- **Code Generation**: Automated drafting, testing, and refactoring of software.
- **Writing Automation**: Generation of reports, emails, scripts, and content.
- **Knowledge Work Routinization**: Standardizing routine information tasks via LLMs.
- **Analysis Automation**: Synthesizing data and producing structured insights.
- **Generative AI (Broad)**: General cross-functional use cases for LLMs.
- **Minimal Exposure**: Physical, field-based, or high-touch service roles.

## Design Philosophy
- **Wow Factor**: First impressions matter. Use vibrant but harmonious color scales (Green-Yellow-Red for risk).
- **Data Density**: Provide deep insights (percentiles, wage comparisons, OFW share) without cluttering the viewport.
- **Transparency**: Every score should have a clear `exposure_rationale` explaining *why* the AI assigned that value.
