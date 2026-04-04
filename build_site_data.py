"""
Build a compact JSON for the website by merging CSV stats with AI exposure scores.

Reads occupations_ph.csv (for stats) and scores.json (for AI exposure).
Writes site/data.json.

Usage:
    uv run python build_site_data.py
"""

import csv
import json


def to_bool(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def derive_outlook(informal_share, ofw_channel):
    # Synthetic PH proxy in [-10, 10]: higher informal share buffers automation,
    # while OFW-dependent channels face external demand risk.
    base = (0.5 - informal_share) * 14
    ofw_adjust = -2.0 if ofw_channel else 1.0
    return int(max(-10, min(10, round(base + ofw_adjust))))


def main():
    # Load AI exposure scores
    with open("scores.json") as f:
        scores_list = json.load(f)
    scores = {s["slug"]: s for s in scores_list}

    # Load CSV stats
    with open("occupations_ph.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Merge
    data = []
    for row in rows:
        slug = row["slug"]
        score = scores.get(slug, {})
        informal_share = float(row["informal_share"])
        ofw_channel = to_bool(row["ofw_channel"])
        outlook = derive_outlook(informal_share, ofw_channel)
        data.append({
            "title": row["title"],
            "slug": slug,
            "category": row["category"],
            "pay": int(float(row["avg_monthly_wage_php"])) if row["avg_monthly_wage_php"] else None,
            "jobs": int(float(row["employment"])) if row["employment"] else None,
            "outlook": outlook,
            "outlook_desc": "OFW-linked demand pressure" if ofw_channel else "Domestic-focused employment",
            "education": int(row["education_code"]) if row["education_code"] else None,
            "exposure": score.get("exposure"),
            "exposure_rationale": score.get("rationale"),
            "ofw_channel": ofw_channel,
            "informal_share": informal_share,
            "remote_share": row["remote_share"],
            "psoc_major": int(row["psoc_major"]),
            "psoc_label": row["psoc_label"],
            "url": row.get("url", ""),
        })

    import os
    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w") as f:
        json.dump(data, f)

    print(f"Wrote {len(data)} occupations to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    print(f"Total jobs represented: {total_jobs:,}")


if __name__ == "__main__":
    main()
