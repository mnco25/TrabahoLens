"""
Build a CSV summary from the generated Philippine occupation list.

Reads data/ph_occupations_v2_with_stats.json and writes occupations_ph.csv.

Usage:
    uv run python make_csv_ph.py
"""

import csv
import json
from pathlib import Path


FIELDNAMES = [
    "id",
    "soc_code",
    "title",
    "psoc_major",
    "psoc_label",
    "category",
    "employment_estimate",
    "avg_monthly_wage_php",
    "education_code",
    "education_label",
    "informal_share",
    "ofw_share",
    "hiring_intensity",
    "description",
]

SOURCE_JSON = Path("data/ph_occupations_v2_with_stats.json")
OUTPUT_CSV = Path("occupations_ph.csv")


def main():
    with open(SOURCE_JSON, encoding="utf-8") as f:
        occupations = json.load(f)

    rows = []
    for occ in occupations:
        rows.append({field: occ[field] for field in FIELDNAMES})

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to occupations_ph.csv")
    if rows:
        print(f"Sample: {rows[0]['id']} | {rows[0]['title']} | {rows[0]['avg_monthly_wage_php']}")


if __name__ == "__main__":
    main()
