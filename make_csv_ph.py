"""
Build a CSV summary from the curated Philippine occupation list.

Reads occupations_ph.json and writes occupations_ph.csv.

Usage:
    uv run python make_csv_ph.py
"""

import csv
import json


FIELDNAMES = [
    "id",
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


def main():
    with open("occupations_ph.json") as f:
        occupations = json.load(f)

    rows = []
    for occ in occupations:
        rows.append({field: occ[field] for field in FIELDNAMES})

    with open("occupations_ph.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to occupations_ph.csv")
    if rows:
        print(f"Sample: {rows[0]['id']} | {rows[0]['title']} | {rows[0]['avg_monthly_wage_php']}")


if __name__ == "__main__":
    main()
