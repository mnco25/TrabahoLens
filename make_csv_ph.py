"""
Build a CSV summary from the curated Philippine occupation list.

Reads occupations_ph.json and writes occupations_ph.csv.

Usage:
    uv run python make_csv_ph.py
"""

import csv
import json
import re


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[']", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text


def main():
    with open("occupations_ph.json") as f:
        occupations = json.load(f)

    fieldnames = [
        "slug",
        "title",
        "psoc_major",
        "psoc_label",
        "category",
        "employment",
        "avg_monthly_wage_php",
        "education_code",
        "education_min",
        "remote_share",
        "ofw_channel",
        "informal_share",
        "description",
    ]

    rows = []
    for occ in occupations:
        rows.append(
            {
                "slug": slugify(occ["title"]),
                "title": occ["title"],
                "psoc_major": occ["psoc_major"],
                "psoc_label": occ["psoc_label"],
                "category": occ["category"],
                "employment": occ["employment_estimate"],
                "avg_monthly_wage_php": occ["avg_monthly_wage_php"],
                "education_code": occ["education_code"],
                "education_min": occ["education_min"],
                "remote_share": occ["remote_share"],
                "ofw_channel": str(bool(occ["ofw_channel"])) .lower(),
                "informal_share": occ["informal_share"],
                "description": occ["description"],
            }
        )

    with open("occupations_ph.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to occupations_ph.csv")
    print(f"Sample: {rows[0]['slug']} | {rows[0]['title']} | {rows[0]['avg_monthly_wage_php']}")


if __name__ == "__main__":
    main()
