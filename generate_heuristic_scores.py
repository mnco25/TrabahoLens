"""
Generate heuristic AI exposure scores from occupations_ph.csv.
Rules (simple):
- Start base = 4.0
- +2 if remote_share == 'high'
- +1 if education_code >=4 (college)
- +1 if ofw_channel is true
- -2 * informal_share (as fraction)
- adjust by pay: lower pay -> -0.5, higher pay -> +0.5 (thresholds)
Clamp 0-10. Produce rationale and primary_risk_vector.
"""
import csv
import json

OUT = "scores.json"


def heuristic_for(row):
    base = 4.0
    remote = row.get("remote_share","").lower()
    if remote == "high":
        base += 2.0
    elif remote == "medium":
        base += 0.5
    edu = int(float(row.get("education_code",0))) if row.get("education_code") else 0
    if edu >= 4:
        base += 1.0
    ofw = str(row.get("ofw_channel","false")).strip().lower() in ("1","true","yes")
    if ofw:
        base += 1.0
    informal = float(row.get("informal_share",0.0))
    base -= 2.0 * informal
    pay = float(row.get("avg_monthly_wage_php") or 0)
    if pay >= 60000:
        base += 0.5
    elif pay <= 15000 and pay>0:
        base -= 0.5

    # round and clamp
    score = max(0, min(10, round(base)))

    # rationale
    parts = []
    if ofw:
        parts.append("OFW channel increases external demand risk")
    if informal > 0.5:
        parts.append("High informal share reduces automation risk")
    if remote == "high":
        parts.append("Work is highly digital/remote")
    if edu >= 4:
        parts.append("Higher education correlates with cognitive tasks")
    if pay>0 and pay>=60000:
        parts.append("Higher wages indicate formal, digital roles")
    if not parts:
        parts = ["Mixed signals; moderate exposure expected"]
    rationale = "; ".join(parts)[:240]

    # primary risk vector heuristic
    if ofw:
        primary = "ofw_channel"
    elif remote == "high":
        primary = "task_automation"
    elif row.get("category","").lower() in ("platform economy","transport services"):
        primary = "platform_disruption"
    elif informal > 0.6:
        primary = "minimal"
    else:
        primary = "demand_reduction"

    return {
        "slug": row.get("slug"),
        "title": row.get("title"),
        "exposure": score,
        "rationale": rationale,
        "primary_risk_vector": primary
    }


def main():
    with open("occupations_ph.csv") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append(heuristic_for(r))
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {len(out)} heuristic scores to {OUT}")

if __name__ == "__main__":
    main()
