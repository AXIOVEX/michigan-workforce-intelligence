"""Validate public research lineage independently of the application database."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def event_hash(event: dict) -> str:
    return hashlib.sha256(canonical({k: v for k, v in event.items() if k != "hash"})).hexdigest()


def safe_file(root: Path, relative: str) -> Path:
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Artifact path escapes evidence directory")
    return path


def verify_ledger(directory: Path) -> dict:
    events = [json.loads(line) for line in (directory / "research-ledger.jsonl").read_text().splitlines()]
    previous = "0" * 64
    latest = {}
    for sequence, event in enumerate(events, 1):
        if event["sequence"] != sequence or event["previous_hash"] != previous:
            raise ValueError("Research ledger sequence/chain mismatch")
        if event_hash(event) != event["hash"]:
            raise ValueError("Research ledger event hash mismatch")
        previous = event["hash"]
        latest[event["path"]] = event["sha256"]
    for path, expected in latest.items():
        if digest(safe_file(directory, path)) != expected:
            raise ValueError(f"Research artifact changed without ledger event: {path}")
    required = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file() and p.name != "research-ledger.jsonl"}
    if required != set(latest):
        raise ValueError("Research ledger file coverage mismatch")
    return {"valid": True, "events": len(events), "head_hash": previous, "files": len(latest), "scope": "public research edition only; not application database"}


def record_changes(directory: Path) -> None:
    ledger = directory / "research-ledger.jsonl"
    existing = [json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
    previous = "0" * 64
    latest = {}
    for index, event in enumerate(existing, 1):
        if event["sequence"] != index or event["previous_hash"] != previous or event_hash(event) != event["hash"]:
            raise ValueError("Refusing to append to invalid ledger")
        previous = event["hash"]
        latest[event["path"]] = event["sha256"]
    sequence = len(existing)
    with ledger.open("a") as stream:
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path == ledger:
                continue
            relative = path.relative_to(directory).as_posix()
            sha = digest(path)
            if latest.get(relative) == sha:
                continue
            sequence += 1
            event = {"sequence": sequence, "at": datetime.now(UTC).isoformat(), "kind": "superseding_artifact" if relative in latest else "artifact_recorded", "path": relative, "sha256": sha, "previous_hash": previous}
            event["hash"] = event_hash(event)
            stream.write(json.dumps(event, sort_keys=True) + "\n")
            previous = event["hash"]


def validate(directory: Path, cutoff: str) -> dict:
    cutoff_date = date.fromisoformat(cutoff)
    registry = json.loads((directory / "source-registry.json").read_text())
    sources = {s["id"]: s for s in registry["sources"]}
    if len(sources) != len(registry["sources"]):
        raise ValueError("Duplicate source identifier")
    for source in sources.values():
        if source.get("published_at") and date.fromisoformat(source["published_at"]) > cutoff_date:
            raise ValueError("Source published after cutoff")
        for required in ["url", "publisher", "retrieved_at", "parser_version", "media_type", "raw_sha256"]:
            if not source.get(required):
                raise ValueError(f"Missing source provenance: {required}")
        if source.get("artifact_path") and digest(safe_file(directory, source["artifact_path"])) != source["raw_sha256"]:
            raise ValueError("Raw source hash mismatch")
    observations = json.loads((directory / "observations.json").read_text())["observations"]
    identifiers = set()
    for row in observations:
        if row["id"] in identifiers or row["source_id"] not in sources:
            raise ValueError("Duplicate observation or unknown source")
        identifiers.add(row["id"])
        for required in ["metric", "unit", "geography", "period", "adjustment", "locator", "status"]:
            if not row.get(required):
                raise ValueError(f"Missing observation definition: {required}")
        if row["value"] is None and row["status"] != "unavailable":
            raise ValueError("Null must remain explicitly unavailable")
        period = row["period"]
        if len(period) == 7 and period[4] == "-" and period[5:].isdigit() and period > cutoff[:7]:
            raise ValueError("Observed month after cutoff")
    projections = json.loads((directory / "projections.json").read_text())["rows"]
    for row in projections:
        if row["source_id"] not in sources or row["status"] != "official_projection":
            raise ValueError("Untraced projection")
        if row["period"] not in {"2024-2034", "2022-2032"}:
            raise ValueError("Unreviewed projection vintage")
    return {"sources": len(sources), "observations": len(observations), "projection_rows": len(projections), "ledger": verify_ledger(directory)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true", help="Append changed reviewed artifacts; never rewrite prior events")
    args = parser.parse_args()
    config = json.loads((ROOT / "reports/current-edition.json").read_text())
    directory = safe_file(ROOT, config["directory"])
    if args.record:
        record_changes(directory)
    print(json.dumps(validate(directory, config["evidence_review_date"]), indent=2))


if __name__ == "__main__":
    main()
