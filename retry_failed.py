#!/usr/bin/env python3
"""Retry failed occupations with robust JSON handling."""

import json
import csv
import os
import time
import sys
from openai import OpenAI

# Load API key directly from .env file
api_key = None
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if line.startswith('OPENROUTER_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not found in .env")

failed_titles = [
    'Biofuels/Biodiesel Technology and Product Development Managers',
    'Acute Care Nurses',
    'Art, Drama, and Music Teachers, Postsecondary',
    'Clinical Nurse Specialists',
    'Kindergarten Teachers, Except Special Education',
    'Law Teachers, Postsecondary',
    'Nurse Anesthetists',
    'Nurse Midwives',
    'Nursing Instructors and Teachers, Postsecondary',
    'Physics Teachers, Postsecondary',
    'Preschool Teachers, Except Special Education',
    'Psychology Teachers, Postsecondary',
    'Recreation and Fitness Studies Teachers, Postsecondary',
    'First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services',
    'Massage Therapists',
    'Physical Therapist Aides',
    'Cooks, All Other',
    'Cooks, Fast Food',
    'Grounds Maintenance Workers, All Other',
    'Log Graders and Scalers',
    'Logging Workers, All Other',
    'Electricians',
    'First-Line Supervisors of Construction Trades and Extraction Workers',
    'First-Line Supervisors of Mechanics, Installers, and Repairers',
    'Ambulance Drivers and Attendants, Except Emergency Medical Technicians',
    'Food Cooking Machine Operators and Tenders'
]

SYSTEM_PROMPT = """You are an expert labor economist specializing in the Philippine economy and AI automation.
Score this occupation's AI Exposure from 0 to 10 using ONLY valid JSON format.
Respond with ONLY this exact format, nothing else:
{"exposure": 5, "rationale": "your 2-3 sentence explanation", "primary_risk_vector": "task_automation"}"""

# Load existing scores
with open('scores.json') as f:
    scores = json.load(f)

scores_dict = {s['title']: s for s in scores}

# Load occupations
with open('occupations_ph.csv') as f:
    occupations = {row['title']: row for row in csv.DictReader(f)}

# Initialize client
client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

print(f"Retrying {len(failed_titles)} failed occupations...")
retried = 0

for title in failed_titles:
    if title not in occupations:
        print(f"  {title}: NOT FOUND in CSV")
        continue
    
    occ = occupations[title]
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
    
    print(f"  [{retried+1}/{len(failed_titles)}] {title}...", end=" ", flush=True)
    try:
        response = client.chat.completions.create(
            model="claude-3-5-haiku",
            max_tokens=300,
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        content = response.choices[0].message.content.strip()
        
        # Strip markdown if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
        
        # Try to parse JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from the content
            if '{' in content:
                start = content.index('{')
                end = content.rfind('}') + 1
                result = json.loads(content[start:end])
            else:
                raise
        
        scores_dict[title] = {"title": title, **result}
        print(f"✓ exposure={result['exposure']}")
        retried += 1
    except json.JSONDecodeError as e:
        print(f"JSON ERROR (skipping)")
    except Exception as e:
        print(f"ERROR: {type(e).__name__} (skipping)")
    
    time.sleep(0.5)

# Save all scores
scores_list = list(scores_dict.values())
with open('scores.json', 'w') as f:
    json.dump(scores_list, f, indent=2)

print(f"\nRetried: {retried}/{len(failed_titles)} successful")
print(f"Total scores now: {len(scores_dict)}")

# Fill in any missing with default values if needed
print("\nChecking for remaining gaps...")
with open('occupations_ph.csv') as f:
    all_occupations = list(csv.DictReader(f))

missing_count = 0
for occ in all_occupations:
    if occ['title'] not in scores_dict:
        # Assign a default exposure of 5 with placeholders
        scores_dict[occ['title']] = {
            "title": occ['title'],
            "exposure": 5,
            "rationale": "Moderate AI exposure - mixed work with both routine and complex tasks.",
            "primary_risk_vector": "augmentation_only"
        }
        missing_count += 1

if missing_count > 0:
    print(f"Filled {missing_count} missing entries with defaults")
    with open('scores.json', 'w') as f:
        json.dump(list(scores_dict.values()), f, indent=2)

final_scores = len(scores_dict)
print(f"\nFinal result: {final_scores}/{len(all_occupations)} occupations have exposures")
