"""
Build the website JSON by merging CSV stats with AI exposure scores.

Reads occupations_ph.csv (for stats) and scores.json (for AI exposure).
Writes site/data.json.

Usage:
    uv run python build_site_data.py
"""

import csv
import json
import os


def main():
    # Load AI exposure scores
    with open("scores.json") as f:
        scores_list = json.load(f)
    scores = {s["title"]: s for s in scores_list}

    # Load CSV stats
    with open("occupations_ph.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Merge
    data = []
    for row in rows:
        title = row["title"]
        score = scores.get(title, {})
        data.append({
            "title": title,
            "category": row["category"],
            "pay": int(float(row["avg_monthly_wage_php"])) if row["avg_monthly_wage_php"] else None,
            "jobs": int(float(row["employment_estimate"])) if row["employment_estimate"] else None,
            "outlook": int(float(row["hiring_intensity"])) if row["hiring_intensity"] else None,
            "outlook_desc": "Hiring intensity (0-100)",
            "education": int(row["education_code"]) if row["education_code"] else None,
            "exposure": score.get("exposure"),
            "exposure_rationale": score.get("rationale"),
            "ofw_share": float(row["ofw_share"]),
            "informal_share": float(row["informal_share"]),
            "psoc_major": int(row["psoc_major"]),
            "psoc_label": row["psoc_label"],
        })

    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)

    print(f"Wrote {len(data)} occupations to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    print(f"Total jobs represented: {total_jobs:,}")


if __name__ == "__main__":
    main()
