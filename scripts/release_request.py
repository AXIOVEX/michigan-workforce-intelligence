"""Prepare or resolve a reviewed report release request using only the standard library."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

from reports import ROOT, version

REQUEST = "release/request.json"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def resolve(request: dict, *, parent: str, changed: list[str], ref: str) -> str:
    if ref != "refs/heads/main":
        raise ValueError("Release requests require main")
    if set(request) != {"version", "reviewed_source_commit"}:
        raise ValueError("Unexpected release request fields")
    if request["reviewed_source_commit"] != parent:
        raise ValueError("Request must reference its immediate reviewed parent")
    if changed != [REQUEST]:
        raise ValueError("Release request must be the only changed file in its commit")
    if not isinstance(request["version"], str) or not request["version"]:
        raise ValueError("Explicit version is required")
    return version(request["version"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "resolve"])
    parser.add_argument("--version")
    args = parser.parse_args()
    if args.command == "prepare":
        if git("status", "--porcelain"):
            raise SystemExit("Commit reviewed changes before preparing a request")
        if git("branch", "--show-current") != "main":
            raise SystemExit("Prepare release requests on main")
        data = {"version": version(args.version), "reviewed_source_commit": git("rev-parse", "HEAD")}
        target = ROOT / REQUEST
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"Commit only {REQUEST} and push main to request reports-{data['version']}")
        return
    event = os.environ["GITHUB_EVENT_NAME"]
    if os.environ["GITHUB_REF"] != "refs/heads/main":
        raise SystemExit("Report publication requires main")
    if event == "push":
        stamp = resolve(
            json.loads((ROOT / REQUEST).read_text()),
            parent=git("rev-parse", "HEAD^"),
            changed=git("diff", "--name-only", "HEAD^", "HEAD").splitlines(),
            ref=os.environ["GITHUB_REF"],
        )
    elif event == "workflow_dispatch":
        requested = os.environ.get("REQUESTED_VERSION", "")
        if not requested:
            raise SystemExit("Explicit version required")
        stamp = version(requested)
    else:
        raise SystemExit("Unsupported release event")
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as stream:
        stream.write(f"version={stamp}\n")
    print(f"Validated release request: reports-{stamp}")


if __name__ == "__main__":
    main()
