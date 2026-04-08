from __future__ import annotations

import re
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
REPO_ROOT = SRC_DIR.parent
DATA_DIR = REPO_ROOT / "data"
DERIVED_DIR = DATA_DIR / "derived"
REFERENCE_DIR = DATA_DIR / "reference"
RAW_DIR = DATA_DIR / "raw"
RAW_ONET_DIR = RAW_DIR / "onet"
RAW_PSA_DIR = RAW_DIR / "psa"
SITE_DIR = REPO_ROOT / "site"
SITE_DATA_JSON = SITE_DIR / "data.json"
CANONICAL_OCCUPATIONS_JSON = REFERENCE_DIR / "occupations_seed.json"
DERIVED_ONET_OCCUPATIONS_JSON = DERIVED_DIR / "onet_occupations.json"
DERIVED_PH_OCCUPATIONS_JSON = DERIVED_DIR / "ph_occupations_v2.json"
DERIVED_PH_OCCUPATIONS_WITH_STATS_JSON = DERIVED_DIR / "ph_occupations_v2_with_stats.json"
DERIVED_OCCUPATIONS_CSV = DERIVED_DIR / "occupations_ph.csv"
DERIVED_SCORES_JSON = DERIVED_DIR / "scores_ai_only.json"
ONET_TEXT_ZIP_URL = "https://www.onetcenter.org/dl_files/database/db_30_2_text.zip"
ONET_RELEASE = "30.2"

PSOC_LABELS = {
    1: "Managers",
    2: "Professionals",
    3: "Technicians and Associate Professionals",
    4: "Clerical Support Workers",
    5: "Service and Sales Workers",
    6: "Skilled Agricultural, Forestry and Fishery Workers",
    7: "Craft and Related Trades Workers",
    8: "Plant and Machine Operators and Assemblers",
    9: "Elementary Occupations",
}

SOC_TO_PSOC_MAJOR = {
    "11": 1,
    "13": 2,
    "15": 2,
    "17": 2,
    "19": 2,
    "21": 2,
    "23": 2,
    "25": 2,
    "27": 2,
    "29": 2,
    "31": 3,
    "33": 3,
    "39": 3,
    "41": 3,
    "43": 4,
    "35": 5,
    "37": 5,
    "45": 6,
    "47": 7,
    "49": 7,
    "51": 8,
    "53": 8,
}

PSOC_OFW_SHARE = {
    1: 0.01,
    2: 0.06,
    3: 0.04,
    4: 0.02,
    5: 0.13,
    6: 0.02,
    7: 0.15,
    8: 0.15,
    9: 0.44,
}

PSOC_LABEL_BY_MAJOR = {major: label for major, label in PSOC_LABELS.items()}

EXCLUDED_TITLE_SUBSTRINGS = (
    "postal service",
    "usps",
    "nuclear",
    "gaming",
    "subway",
    "logging equipment",
)

TITLE_SIZE_MULTIPLIERS = (
    (r"\bregistered nurses?\b", 3.0),
    (r"\bteachers?\b", 2.2),
    (r"\bsoftware developers?\b", 2.0),
    (r"\bdevelopers?\b", 1.6),
    (r"\bdrivers?\b", 1.8),
    (r"\baccountants?\b", 1.6),
    (r"\bcaregivers?\b", 1.8),
    (r"\bdomestic workers?\b", 1.7),
    (r"\bfood service\b|\bcooks?\b|\bchefs?\b|\bservers?\b|\bwaiters?\b", 1.4),
    (r"\bcashiers?\b|\bsalespersons?\b|\bsales representatives?\b", 1.4),
    (r"\bconstruction laborers?\b|\bcarpenters?\b|\bplumbers?\b|\belectricians?\b", 1.5),
    (r"\bfarmers?\b|\bfishers?\b|\bfisherfolk\b", 1.5),
    (r"\bcleaners?\b|\bjanitors?\b", 1.3),
    (r"\bsecurity guards?\b", 1.3),
    (r"\bmachine operators?\b|\bassemblers?\b", 1.3),
)

WAGE_BY_CATEGORY = {
    "Management": 55000,
    "Finance and Business": 32000,
    "IT and Computer": 43676,
    "Engineering and Scientific": 36096,
    "Healthcare Professionals": 28000,
    "Healthcare Support": 22000,
    "Education": 28000,
    "Legal": 45000,
    "Engineering Technicians": 27000,
    "Construction Trades": 19000,
    "Installation and Maintenance": 14000,
    "Production and Manufacturing": 18000,
    "Transportation": 20000,
    "Food Service": 16000,
    "Personal Care": 15000,
    "Protective Service": 19000,
    "Sales": 17000,
    "Office/Admin": 20000,
    "Agricultural": 12000,
    "Community Service": 22000,
    "Arts and Media": 22000,
    "Service": 14000,
}

INFORMAL_SHARE_BY_CATEGORY = {
    "Management": 0.05,
    "Finance and Business": 0.10,
    "IT and Computer": 0.10,
    "Engineering and Scientific": 0.10,
    "Healthcare Professionals": 0.05,
    "Healthcare Support": 0.15,
    "Education": 0.10,
    "Legal": 0.08,
    "Engineering Technicians": 0.15,
    "Construction Trades": 0.55,
    "Installation and Maintenance": 0.55,
    "Production and Manufacturing": 0.25,
    "Transportation": 0.45,
    "Food Service": 0.50,
    "Personal Care": 0.55,
    "Protective Service": 0.20,
    "Sales": 0.50,
    "Office/Admin": 0.10,
    "Agricultural": 0.85,
    "Community Service": 0.20,
    "Arts and Media": 0.20,
    "Service": 0.35,
}

PH_SPECIFIC_OCCUPATIONS = [
    {
        "id": "PH-0001",
        "soc_code": "PH-0001",
        "title": "Kasambahay (domestic workers)",
        "source_title": "Kasambahay (domestic workers)",
        "psoc_major": 5,
        "category": "Service",
    },
    {
        "id": "PH-0002",
        "soc_code": "PH-0002",
        "title": "Tricycle / jeepney drivers",
        "source_title": "Tricycle drivers",
        "psoc_major": 5,
        "category": "Transportation",
    },
    {
        "id": "PH-0003",
        "soc_code": "PH-0003",
        "title": "Delivery riders",
        "source_title": "Delivery riders",
        "psoc_major": 8,
        "category": "Transportation",
    },
    {
        "id": "PH-0004",
        "soc_code": "PH-0004",
        "title": "Barangay health workers",
        "source_title": "Barangay health workers",
        "psoc_major": 5,
        "category": "Healthcare Professionals",
    },
    {
        "id": "PH-0005",
        "soc_code": "PH-0005",
        "title": "Seafarers / merchant marine",
        "source_title": "Seafarers and merchant marine ratings",
        "psoc_major": 8,
        "category": "Transportation",
    },
    {
        "id": "PH-0006",
        "soc_code": "PH-0006",
        "title": "OFW caregivers",
        "source_title": "Kasambahay (domestic workers)",
        "psoc_major": 9,
        "category": "Personal Care",
    },
    {
        "id": "PH-0007",
        "soc_code": "PH-0007",
        "title": "Street vendors / market sellers",
        "source_title": "Street vendors and market sellers",
        "psoc_major": 9,
        "category": "Sales",
    },
    {
        "id": "PH-0008",
        "soc_code": "PH-0008",
        "title": "Hairdressers and beauty workers",
        "source_title": "Hairdressers and beauty service workers",
        "psoc_major": 5,
        "category": "Personal Care",
    },
    {
        "id": "PH-0009",
        "soc_code": "PH-0009",
        "title": "Agricultural farm laborers",
        "source_title": "Rice and corn farmers",
        "psoc_major": 9,
        "category": "Agricultural",
    },
    {
        "id": "PH-0010",
        "soc_code": "PH-0010",
        "title": "Fisherfolk",
        "source_title": "Fishers and aquaculture workers",
        "psoc_major": 6,
        "category": "Agricultural",
    },
]


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def soc_major_from_soc_code(soc_code: str):
    match = re.match(r"^(\d{2})-", soc_code or "")
    if not match:
        return None
    return int(match.group(1))


def psoc_major_from_soc_code(soc_code: str):
    major = soc_major_from_soc_code(soc_code)
    if major is None:
        return None
    return SOC_TO_PSOC_MAJOR.get(f"{major:02d}")


def psoc_label(psoc_major: int | None) -> str:
    if psoc_major is None:
        return "Unknown"
    return PSOC_LABEL_BY_MAJOR.get(psoc_major, "Unknown")


def is_us_specific_title(title: str) -> bool:
    lower_title = title.lower()
    return any(term in lower_title for term in EXCLUDED_TITLE_SUBSTRINGS)


def category_from_soc_code(soc_code: str, title: str) -> str:
    major = psoc_major_from_soc_code(soc_code)
    lower_title = title.lower()

    if major == 1:
        return "Management"
    if major == 2:
        if any(word in lower_title for word in ("nurse", "dentist", "doctor", "pharmacist", "therapist", "medical", "health")):
            return "Healthcare Professionals"
        if any(word in lower_title for word in ("teacher", "instruction", "instructor", "educat")):
            return "Education"
        if any(word in lower_title for word in ("lawyer", "judge", "paralegal", "legal")):
            return "Legal"
        if any(word in lower_title for word in ("software", "computer", "web", "network", "data", "systems", "developer", "programmer", "it ")):
            return "IT and Computer"
        if any(word in lower_title for word in ("account", "finance", "budget", "tax", "insurance", "loan", "credit", "financial", "auditor", "business")):
            return "Finance and Business"
        if any(word in lower_title for word in ("engineer", "architect", "surveyor", "drafter", "science", "chemist", "biologist", "geologist", "physicist")):
            return "Engineering and Scientific"
        if any(word in lower_title for word in ("social worker", "counselor", "community", "clergy", "priest", "chaplain")):
            return "Community Service"
        if any(word in lower_title for word in ("artist", "design", "writer", "editor", "photograph", "media", "broadcast", "translator", "musician")):
            return "Arts and Media"
        return "Community Service"
    if major == 3:
        if any(word in lower_title for word in ("security guard", "police", "firefighter", "protective")):
            return "Protective Service"
        if any(word in lower_title for word in ("nurse aide", "health", "medical", "dental", "therapy", "home health", "care aide")):
            return "Healthcare Support"
        if any(word in lower_title for word in ("hairdresser", "barber", "beauty", "cosmet")):
            return "Personal Care"
        if any(word in lower_title for word in ("sales", "cashier", "retail", "customer service")):
            return "Sales"
        if any(word in lower_title for word in ("technician", "technologist", "dental assistant", "medical assistant", "engineering", "it", "computer", "data")):
            return "Engineering Technicians"
        return "Service"
    if major == 4:
        return "Office/Admin"
    if major == 5:
        if any(word in lower_title for word in ("food", "cook", "server", "waiter", "waitress", "barista", "dishwasher")):
            return "Food Service"
        if any(word in lower_title for word in ("cleaner", "janitor", "grounds", "building maintenance", "pest control", "housekeeping")):
            return "Service"
        return "Service"
    if major == 6:
        return "Agricultural"
    if major == 7:
        if any(word in lower_title for word in ("installer", "repair", "maintenance", "mechanic", "electrician", "plumber", "welder", "carpenter", "mason", "painter", "construction")):
            return "Construction Trades"
        return "Installation and Maintenance"
    if major == 8:
        if any(word in lower_title for word in ("driver", "pilot", "operator", "conductor", "captain", "dispatcher", "sailor", "seafarer", "aircraft")):
            return "Transportation"
        return "Production and Manufacturing"
    if major == 9:
        if any(word in lower_title for word in ("laborer", "helper", "hand packer", "packer", "cleaner", "street vendor", "market seller", "cashier")):
            return "Sales"
        return "Service"
    return "Service"


def wage_for_occupation(soc_code: str, title: str, category: str) -> int:
    lower_title = title.lower()
    major = psoc_major_from_soc_code(soc_code)

    if major == 1:
        return WAGE_BY_CATEGORY["Management"]
    if major == 2:
        if category == "Legal":
            return 45000
        if category == "Education":
            return 28000
        if category == "Healthcare Professionals":
            return 28000
        if category == "IT and Computer":
            return 43676
        if category == "Finance and Business":
            return 32000
        if category == "Engineering and Scientific":
            return 36096
        if any(word in lower_title for word in ("technician", "technologist", "drafter", "survey")):
            return 27000
        return 36096
    if major == 3:
        if category == "Healthcare Support":
            return 22000
        if category == "Protective Service":
            return 19000
        if category == "Personal Care":
            return 15000
        return 17000
    if major == 4:
        return 20000
    if major == 5:
        if category == "Food Service":
            return 16000
        if category == "Service":
            return 14000
        return 15000
    if major == 6:
        return 12000
    if major == 7:
        if category == "Construction Trades":
            return 19000
        return 14000
    if major == 8:
        if category == "Transportation":
            return 20000
        return 18000
    if major == 9:
        if category == "Sales":
            return 17000
        if category == "Service":
            return 14000
        return 13000
    return WAGE_BY_CATEGORY.get(category, 18000)


def informal_share_for_category(category: str) -> float:
    return INFORMAL_SHARE_BY_CATEGORY.get(category, 0.25)


def size_multiplier_for_title(title: str) -> float:
    lower_title = title.lower()
    for pattern, multiplier in TITLE_SIZE_MULTIPLIERS:
        if re.search(pattern, lower_title):
            return multiplier
    return 1.0


def ensure_parent_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def load_current_occupations_map(path: Path | None = None):
    import json

    if path is None:
        path = CANONICAL_OCCUPATIONS_JSON

    with open(path, encoding="utf-8") as file_handle:
        occupations = json.load(file_handle)

    return {normalize_text(occupation["title"]): occupation for occupation in occupations}


def make_onet_id(soc_code: str) -> str:
    return f"ONET-{soc_code.replace('-', '').replace('.', '')}"
