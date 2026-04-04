# TrabahoLens Prompt Notes

This file replaces the old US/BLS prompt artifact.

Use this as a scratchpad for custom scoring prompts for Philippine occupations.

## Current default scoring target
- Dataset: occupations_ph.csv
- Output: scores.json
- Layer in site: AI Exposure

## Suggested prompt fields
- title
- psoc_label
- category
- employment_estimate
- avg_monthly_wage_php
- education_label
- ofw_share
- informal_share
- description

## Output contract
Return strict JSON:
{"exposure": 0, "rationale": "...", "primary_risk_vector": "..."}

## Notes
- Keep calibration aligned with Philippine labor dynamics.
- Rebuild site data after scoring:
  1) python3 build_site_data.py
  2) Serve site/ and refresh browser
