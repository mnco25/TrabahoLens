"""
Fetch Philippine labor datasets from PSA OpenSTAT PXWeb API.

Targets:
- LFS occupation employment: DB/DB__1B__LFS/0031B3AEPO0.px
- OWS wages by industry:   DB/DB__1B__OWS/0031B3E1030.px

This script fetches both metadata and data payloads, prints variable codes for
inspection, and stores raw JSON under data/psa_raw/.

Usage:
    uv run python fetch_psa.py
"""

import json
import os
from datetime import datetime, timezone

import requests

BASE_URL = "https://openstat.psa.gov.ph/PXWeb/api/v1/en"
TABLES = {
    "lfs_employment_by_occupation": "DB/DB__1B__LFS/0031B3AEPO0.px",
    "ows_wage_by_industry": "DB/DB__1B__OWS/0031B3E1030.px",
}
OUT_DIR = "data/psa_raw"


def endpoint(path):
    return f"{BASE_URL}/{path}"


def fetch_metadata(path):
    resp = requests.get(endpoint(path), timeout=60)
    resp.raise_for_status()
    return resp.json()


def build_all_query(metadata):
    query = []
    for var in metadata.get("variables", []):
        query.append(
            {
                "code": var["code"],
                "selection": {
                    "filter": "all",
                    "values": ["*"],
                },
            }
        )
    return {
        "query": query,
        "response": {"format": "json-stat2"},
    }


def fetch_data(path, payload):
    resp = requests.post(endpoint(path), json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


def save_json(path, payload):
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)


def print_variable_codes(label, metadata):
    print(f"\n[{label}] variable codes:")
    for var in metadata.get("variables", []):
        values = var.get("values", [])
        value_count = len(values)
        sample = ", ".join(values[:5])
        if value_count > 5:
            sample += ", ..."
        print(f"- {var.get('code')}: {var.get('text')} ({value_count} values)")
        if sample:
            print(f"  sample codes: {sample}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for label, table_path in TABLES.items():
        print(f"Fetching metadata for {label}...")
        metadata = fetch_metadata(table_path)
        print_variable_codes(label, metadata)

        metadata_path = os.path.join(OUT_DIR, f"{label}_metadata_{run_ts}.json")
        save_json(metadata_path, metadata)
        print(f"Saved metadata: {metadata_path}")

        payload = build_all_query(metadata)
        query_path = os.path.join(OUT_DIR, f"{label}_query_{run_ts}.json")
        save_json(query_path, payload)
        print(f"Saved query payload: {query_path}")

        print(f"Fetching data for {label}...")
        data = fetch_data(table_path, payload)
        data_path = os.path.join(OUT_DIR, f"{label}_data_{run_ts}.json")
        save_json(data_path, data)
        print(f"Saved data: {data_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
