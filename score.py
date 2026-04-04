"""
Score each occupation's AI exposure using Anthropic.

Reads occupations_ph.csv, sends each occupation profile to an LLM with a
Philippine-calibrated rubric, and collects structured scores. Results are
cached incrementally to scores.json so the script can be resumed if
interrupted.

Usage:
    uv run python score.py
    uv run python score.py --model claude-haiku-4-5-20251001
    uv run python score.py --start 0 --end 10   # test on first 10
"""

import argparse
import csv
import json
import os
import time
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
OUTPUT_FILE = "scores.json"

SYSTEM_PROMPT = """\
You are an expert labor economist specializing in the Philippine economy and AI automation.

Score this occupation's AI Exposure from 0 to 10.

AI Exposure measures how much AI and automation will reshape this occupation in the
Philippines over the next 5–10 years. Consider direct automation and indirect demand
reduction.

PHILIPPINE-SPECIFIC FACTORS:

1. OFW Channel Risk: If this occupation has high ofw_share, AI may automate the
destination job abroad — displacing Filipino workers before domestic effects arrive.

2. Informal Economy Buffer: High informal_share delays automation — informal
workplaces do not adopt technology at the same rate as formal establishments.

3. Platform/Gig Disruption: Delivery and transport workers face algorithmic
management and route optimization — this is real automation even without LLMs.

4. Philippine Infrastructure Reality: Autonomous vehicles, precision agriculture
robots, and humanoid robots face higher deployment barriers in PH than in the US.

SCORE ANCHORS:
0–1: Minimal. Physical, highly informal, no realistic automation pathway in 10 years.
2–3: Low. Physical + strong informal buffer or regulatory protection.
4–5: Moderate. Mixed work; AI assists but does not replace core tasks.
6–7: High. Knowledge work or significant OFW channel risk.
8–9: Very high. Digital or routine work; AI already capable of most tasks.
10: Maximum. Pure routine digital processing; AI can do this today.

Expected average: ~4.5–5.0 across PH occupations.

Respond ONLY with valid JSON, no other text:
{"exposure": <0–10 number>, "rationale": "<2–3 PH-specific sentences>",
"primary_risk_vector": "<task_automation|ofw_channel|platform_disruption|demand_reduction|augmentation_only|minimal>"}
"""


def score_occupation(client, text, model):
    """Send one occupation to the LLM and parse the structured response."""
    response = client.messages.create(
        model=model,
        max_tokens=350,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": text},
        ],
    )
    content = "".join(
        block.text for block in response.content if getattr(block, "type", "") == "text"
    )

    # Strip markdown code fences if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[1]  # remove first line
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    return json.loads(content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=None)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--force", action="store_true",
                        help="Re-score even if already cached")
    args = parser.parse_args()

    with open("occupations_ph.csv") as f:
        occupations = list(csv.DictReader(f))

    subset = occupations[args.start:args.end]

    # Load existing scores
    scores = {}
    if os.path.exists(OUTPUT_FILE) and not args.force:
        with open(OUTPUT_FILE) as f:
            for entry in json.load(f):
                scores[entry["title"]] = entry

    print(f"Scoring {len(subset)} occupations with {args.model}")
    print(f"Already cached: {len(scores)}")

    errors = []
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in environment or .env")
    client = Anthropic(api_key=api_key)

    for i, occ in enumerate(subset):
        title = occ["title"]

        if title in scores:
            continue

        text = (
            f"title: {occ['title']}\n"
            f"psoc_label: {occ['psoc_label']}\n"
            f"category: {occ['category']}\n"
            f"employment_estimate: {int(float(occ['employment_estimate']))}\n"
            f"avg_monthly_wage_php: {int(float(occ['avg_monthly_wage_php']))}\n"
            f"education_label: {occ['education_label']}\n"
            f"ofw_share: {float(occ['ofw_share']):.2f}\n"
            f"informal_share: {float(occ['informal_share']):.2f}\n"
            f"description: {occ['description']}"
        )

        print(f"  [{i+1}/{len(subset)}] {occ['title']}...", end=" ", flush=True)

        try:
            result = score_occupation(client, text, args.model)
            scores[title] = {
                "title": title,
                **result,
            }
            print(f"exposure={result['exposure']}")
        except Exception as e:
            print(f"ERROR: {e}")
            errors.append(slug)

        # Save after each one (incremental checkpoint)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(list(scores.values()), f, indent=2)

        if i < len(subset) - 1:
            time.sleep(args.delay)

    print(f"\nDone. Scored {len(scores)} occupations, {len(errors)} errors.")
    if errors:
        print(f"Errors: {errors}")

    # Summary stats
    vals = [s for s in scores.values() if "exposure" in s]
    if vals:
        avg = sum(s["exposure"] for s in vals) / len(vals)
        by_score = {}
        for s in vals:
            bucket = s["exposure"]
            by_score[bucket] = by_score.get(bucket, 0) + 1
        print(f"\nAverage exposure across {len(vals)} occupations: {avg:.1f}")
        print("Distribution:")
        for k in sorted(by_score):
            print(f"  {k}: {'█' * by_score[k]} ({by_score[k]})")


if __name__ == "__main__":
    main()
