from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("reviewed_evidence", ROOT / "scripts/reviewed_evidence.py")
assert SPEC and SPEC.loader
EVIDENCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVIDENCE)
EDITION = ROOT / "reports/2026-09-26-graduation-horizons"


@pytest.fixture
def edition(tmp_path: Path) -> Path:
    target = tmp_path / "edition"
    shutil.copytree(EDITION, target)
    return target


def test_reviewed_edition_integrity() -> None:
    result = EVIDENCE.validate(EDITION, "2026-09-26")
    assert result["sources"] >= 20
    assert result["ledger"]["valid"]


def test_tampered_source_rejected(edition: Path) -> None:
    artifact = next((edition / "evidence").glob("*.json"))
    artifact.write_text("{}")
    with pytest.raises(ValueError, match="Raw source hash"):
        EVIDENCE.validate(edition, "2026-09-26")


def test_future_publication_rejected(edition: Path) -> None:
    path = edition / "source-registry.json"
    value = json.loads(path.read_text())
    value["sources"][0]["published_at"] = "2026-09-28"
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="after cutoff"):
        EVIDENCE.validate(edition, "2026-09-26")


def test_null_is_not_an_observed_zero(edition: Path) -> None:
    path = edition / "observations.json"
    value = json.loads(path.read_text())
    value["observations"][0]["value"] = None
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="Null"):
        EVIDENCE.validate(edition, "2026-09-26")


def test_ledger_rejects_reordered_events(edition: Path) -> None:
    path = edition / "research-ledger.jsonl"
    lines = path.read_text().splitlines()
    lines[0], lines[1] = lines[1], lines[0]
    path.write_text("\n".join(lines) + "\n")
    with pytest.raises(ValueError, match="sequence/chain"):
        EVIDENCE.verify_ledger(edition)


def test_append_preserves_history_and_requires_new_event(edition: Path) -> None:
    ledger = edition / "research-ledger.jsonl"
    original = ledger.read_bytes()
    (edition / "README.md").write_text("Reviewed update\n")
    with pytest.raises(ValueError, match="without ledger event"):
        EVIDENCE.verify_ledger(edition)
    EVIDENCE.record_changes(edition)
    assert ledger.read_bytes().startswith(original)
    assert EVIDENCE.verify_ledger(edition)["valid"]


def test_raw_api_observations_match_public_records() -> None:
    sources = json.loads((EDITION / "source-registry.json").read_text())["sources"]
    observations = json.loads((EDITION / "observations.json").read_text())["observations"]
    for source in sources:
        if "artifact_path" not in source:
            continue
        raw = json.loads((EDITION / source["artifact_path"]).read_text())
        series = raw["Results"]["series"][0]
        for row in series["data"]:
            if row["period"] == "M13":
                continue
            identifier = series["seriesID"] + "-" + row["year"] + "-" + row["period"][1:]
            normalized = next(o for o in observations if o["id"] == identifier)
            assert normalized["value"] == (None if row["value"] == "-" else float(row["value"]))
            assert normalized["source_id"] == source["id"]


def test_artifact_traversal_rejected(edition: Path) -> None:
    with pytest.raises(ValueError, match="escapes"):
        EVIDENCE.safe_file(edition, "../outside.json")
