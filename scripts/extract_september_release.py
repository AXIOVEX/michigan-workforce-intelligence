"""Reproduce reviewed September source extracts from a local immutable raw cache.

Raw third-party pages are not republished. Their hashes/URLs and limited factual
extracts are distributed. Download source-registry URLs into --cache/<sha256>
to rerun; changed source bytes require a new vintage, never silent replacement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "reports/2026-09-26-graduation-horizons"
CODES = {
    "13-2011", "15-1212", "15-1251", "15-1252", "15-2051", "17-2112",
    "17-3013", "23-2011", "27-1024", "29-1171", "29-1224", "29-2034",
    "43-3031", "43-4051", "43-9021", "47-2111", "49-9041", "51-4071",
}


def extract(cache: Path) -> list[dict]:
    sources = json.loads((EDITION / "source-registry.json").read_text())["sources"]
    rows = []
    for sid, geography, period, marker in [
        ("S12", "Michigan", "2024-2034", "2024-2034"),
        ("S13", "Detroit Metro Prosperity Region", "2022-2032", "2022 to 2032"),
    ]:
        source = next(s for s in sources if s["id"] == sid)
        path = cache / source["raw_sha256"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["raw_sha256"]:
            raise ValueError(f"Source hash mismatch: {sid}")
        with path.open("rb") as stream:
            workbook = load_workbook(stream, data_only=True, read_only=True)
            values = list(workbook.active.values)
        if marker not in " ".join(str(r[0]) for r in values[:3]):
            raise ValueError(f"Unexpected projection vintage: {sid}")
        for number, row in enumerate(values, 1):
            if row[0] not in CODES:
                continue
            rows.append({
                "id": f"{sid}-{row[0]}", "source_id": sid, "soc": row[0],
                "occupation": row[1], "geography": geography, "period": period,
                "base_employment": row[2], "projected_employment": row[3],
                "change_percent": round(row[5] * 100, 1),
                "annual_openings": row[10], "unit": "people/jobs as defined by MCDA; annual openings",
                "status": "official_projection", "locator": f"worksheet row {number}",
                "note": "Rounded source values; annual openings include exits/transfers, not only growth. Regional/state vintages differ.",
            })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    args = parser.parse_args()
    target = EDITION / "projections.json"
    content = json.dumps({"parser_version": "mcda-xlsx-selected-v1", "rows": extract(args.cache)}, indent=2) + "\n"
    if target.exists() and target.read_text() != content:
        raise ValueError("Existing extract differs; create a new version instead")
    target.write_text(content)


if __name__ == "__main__":
    main()
