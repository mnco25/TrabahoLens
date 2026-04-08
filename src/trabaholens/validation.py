from __future__ import annotations

import csv
import json
from pathlib import Path

from .pipeline_utils import (
    DERIVED_OCCUPATIONS_CSV,
    DERIVED_SCORES_JSON,
    SITE_DATA_JSON,
)


def require_file(path: Path, label: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"{label} was not found at {path}. Rebuild the pipeline step that produces it."
        )
    return path


def load_json(path: Path, label: str):
    require_file(path, label)
    with open(path, encoding="utf-8") as file_handle:
        return json.load(file_handle)


def load_csv_rows(path: Path, label: str) -> list[dict[str, str]]:
    require_file(path, label)
    with open(path, encoding="utf-8", newline="") as file_handle:
        return list(csv.DictReader(file_handle))


def validate_scores_cover_titles(
    csv_path: Path = DERIVED_OCCUPATIONS_CSV,
    scores_path: Path = DERIVED_SCORES_JSON,
) -> tuple[list[dict[str, str]], list[dict], list[str]]:
    rows = load_csv_rows(csv_path, "Occupation CSV")
    scores = load_json(scores_path, "AI exposure scores")
    titles = [row["title"] for row in rows]
    score_map = {entry["title"]: entry for entry in scores}
    missing = [title for title in titles if title not in score_map]
    return rows, scores, missing


def validate_site_data(
    csv_path: Path = DERIVED_OCCUPATIONS_CSV,
    scores_path: Path = DERIVED_SCORES_JSON,
    site_data_path: Path = SITE_DATA_JSON,
) -> None:
    rows, scores, missing = validate_scores_cover_titles(csv_path, scores_path)
    if missing:
        raise RuntimeError(
            f"Site data cannot be built because {len(missing)} occupations are missing scores."
        )

    site_rows = load_json(site_data_path, "Site data JSON")
    if len(site_rows) != len(rows):
        raise RuntimeError(
            f"site/data.json contains {len(site_rows)} rows but the CSV contains {len(rows)} rows."
        )

    score_titles = {entry["title"] for entry in scores}
    site_titles = {entry["title"] for entry in site_rows}
    csv_titles = {row["title"] for row in rows}
    if site_titles != csv_titles or not csv_titles.issubset(score_titles):
        raise RuntimeError("CSV, score cache, and site JSON titles are out of sync.")

