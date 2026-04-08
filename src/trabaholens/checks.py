from __future__ import annotations

import compileall

from .pipeline_utils import REPO_ROOT
from .validation import validate_site_data


def main() -> None:
    targets = [REPO_ROOT / "src", REPO_ROOT / "scripts", REPO_ROOT / "tests"]
    failed = [str(path) for path in targets if not compileall.compile_dir(path, quiet=1)]
    if failed:
        raise RuntimeError(f"Compilation failed for: {', '.join(failed)}")

    validate_site_data()
    print("Checks passed.")
