"""Build the reviewed research edition without relabeling historical DB data."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from build_reports import ROOT, chart, pdf
from PIL import Image, ImageDraw
from pypdf import PdfReader
from reviewed_evidence import safe_file, validate


def observed_tables(rows: list[dict]) -> str:
    lines = ["# Refreshed labor indicators", "", "SA = seasonally adjusted; NSA = not seasonally adjusted. Percentages have different denominators as named. Source IDs resolve in the appendix.", "", "| Indicator | Value | Geography / period | Basis / source |", "| --- | ---: | --- | --- |"]
    for row in rows:
        if row["id"].startswith("LAU"):
            continue
        value = "Unavailable" if row["value"] is None else f"{row['value']:,.1f}"
        lines.append(f"| {row['metric']} | {value} {row['unit']} | {row['geography']} / {row['period']} | {row['adjustment']}; {row['status']}; {row['source_id']} |")
    lines += ["", "# County and interstate unemployment", "", "These comparisons use the same month and NSA definition. County August values were not returned by the retrieved BLS endpoint. Rates do not adjust for population composition.", "", "| Geography | July 2025 | July 2026 | Change (pp) | August 2026 |", "| --- | ---: | ---: | ---: | ---: |"]
    for geography in ["Macomb County", "Oakland County", "Wayne County", "Michigan", "Ohio", "California", "Texas", "Florida"]:
        selected = {r["period"]: r["value"] for r in rows if r["id"].startswith("LAU") and r["geography"] == geography}
        old, new, august = selected.get("2025-07"), selected.get("2026-07"), selected.get("2026-08")
        fmt = lambda v: "Not verified" if v is None else f"{v:.1f}%"  # noqa: E731
        delta = "Unavailable" if old is None or new is None else f"{new-old:+.1f}"
        lines.append(f"| {geography} | {fmt(old)} | {fmt(new)} | {delta} | {fmt(august)} |")
    lines += ["", "Sources S21-S28: BLS LAUS. The U.S. August NSA rate is 4.3% in S03 table A-15; do not compare the 4.1% SA headline with this NSA table. Derived changes are July 2026 minus July 2025, using matching series."]
    return "\n".join(lines)


def projection_table(rows: list[dict]) -> str:
    region = {r["soc"]: r for r in rows if r["source_id"] == "S13"}
    lines = ["# Michigan occupation planning evidence", "", "Official projections, not current vacancies. State: 2024-34 (S12). Detroit Metro Prosperity Region: 2022-32 (S13). Different vintages must not be pooled. Annual openings include replacement/transfer demand and are not the number of new graduate jobs.", "", "| Occupation / SOC | Michigan change | Michigan annual openings | Region change / annual openings |", "| --- | ---: | ---: | ---: |"]
    for row in rows:
        if row["source_id"] != "S12":
            continue
        other = region[row["soc"]]
        lines.append(f"| {row['occupation']} / {row['soc']} | {row['change_percent']:+.1f}% | {row['annual_openings']:,} | {other['change_percent']:+.1f}% / {other['annual_openings']:,} |")
    lines += ["", "MCDA rounds employment and openings. Do not derive precise capacity requirements from small rounded cells. SOC identifiers and source worksheet rows are retained in projections.json."]
    return "\n".join(lines)


def source_appendix(sources: list[dict]) -> str:
    lines = ["# Source register", "", "Source IDs in report text resolve below. Retrieval times, response hashes and parser versions are in source-registry.json. Dates labeled unknown were not established; observation periods were inspected. Original source material retains provider terms."]
    for source in sources:
        lines += ["", f"**{source['id']} - {source['publisher']}.** [Source]({source['url']}). Publication: {source.get('published_at') or 'not established'}. Retrieval: {source['retrieved_at'][:10]} UTC. Review status: {source['extraction_status']}."]
        if source.get("note"):
            lines.append(source["note"])
    return "\n".join(lines)


def build(stamp: str, config: dict) -> None:
    source = safe_file(ROOT, config["directory"])
    audit = validate(source, config["evidence_review_date"])
    out = ROOT / "output/pdf" / stamp
    out.mkdir(parents=True, exist_ok=False)
    rows = json.loads((source / "observations.json").read_text())["observations"]
    projections = json.loads((source / "projections.json").read_text())["rows"]
    sources = json.loads((source / "source-registry.json").read_text())["sources"]
    source_urls = {s["id"]: s["url"] for s in sources}

    def read(name: str) -> str:
        content = (source / (name + ".md")).read_text()
        def links(match: re.Match) -> str:
            return ", ".join(f"[{sid}]({source_urls[sid]})" for sid in re.findall(r"S\d+", match.group()))
        return re.sub(r"\[S\d+(?:, S\d+)*\]", links, content)
    appendix = source_appendix(sources)
    tables = observed_tables(rows)
    occupation_table = projection_table(projections)
    by_id = {r["id"]: r for r in rows}
    charts = [chart(out, "august-unemployment", "August 2026 unemployment", "Percent, seasonally adjusted", [("Unemployment", ["Michigan", "United States"], [by_id["mi-u3"]["value"], by_id["us-u3"]["value"]])], "Sources: Michigan MCDA and BLS, S01/S03. Same month and seasonal adjustment; survey estimation differs.", bars=True)]
    mi = [r for r in projections if r["source_id"] == "S12"]
    select = [r for r in mi if r["soc"] in {"15-1252", "15-2051", "49-9041", "43-9021", "43-3031", "29-1224"}]
    labels = {"15-1252": "Software\ndevelopers", "15-2051": "Data\nscientists", "29-1224": "Physician\nradiologists", "43-3031": "Bookkeeping /\naccounting clerks", "43-9021": "Data entry\nkeyers", "49-9041": "Industrial\nmechanics"}
    charts.append(chart(out, "occupation-change", "Michigan occupation change: selected examples", "Projected percent change, 2024-2034", [("Change", [labels[r["soc"]] for r in select], [r["change_percent"] for r in select])], "Source: Michigan MCDA, S12. Projection, not current vacancies or an AI causal effect.", bars=True))
    documents = {
        "executive-brief": ("Michigan workforce: decisions for education and industry", [read("executive-brief")], []),
        "jobs-economic-report": ("Michigan jobs and economic trends", [read("economic-analysis"), tables, read("evidence-review"), appendix], charts),
        "job-continuity-solutions": ("Skills, education and job continuity in the AI transition", [read("university-programs"), occupation_table, read("ai-task-impact"), read("skills-bridges"), read("evidence-review"), appendix], []),
    }
    for name, (title, texts, figures) in documents.items():
        pdf(out / (name + ".pdf"), title, texts, figures, stamp, config["evidence_review_date"], section_breaks=False)
        (out / (name + ".md")).write_text("\n\n".join(texts))
    shutil.copytree(source, out / "evidence-edition")
    for name in ["LICENSE", "LICENSING.md", "THIRD_PARTY_NOTICES.md"]:
        shutil.copy2(ROOT / name, out / name)
    shutil.copytree(ROOT / "LICENSES", out / "LICENSES")
    qa = ROOT / "tmp/pdfs" / stamp
    qa.mkdir(parents=True)
    pages = {}
    for path in sorted(out.glob("*.pdf")):
        pages[path.name] = len(PdfReader(path).pages)
        renderer = "/usr/bin/pdftoppm" if Path("/usr/bin/pdftoppm").exists() else "pdftoppm"
        subprocess.run([renderer, "-scale-to", "1200", "-png", str(path), str(qa / path.stem)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    renders = sorted(qa.glob("*.png"))
    for batch in range(0, len(renders), 9):
        sheet = Image.new("RGB", (1800, 1440), "#e3e8eb")
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(renders[batch:batch+9]):
            with Image.open(path) as opened:
                im = opened.convert("RGB")
            im.thumbnail((590, 440))
            x, y = j % 3 * 600, j // 3 * 480
            sheet.paste(im, (x, y + 25))
            draw.text((x+5, y+5), path.name, fill="black")
        sheet.save(qa / f"contact-{batch//9+1}.png")
    files = {p.relative_to(out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob("*")) if p.is_file()}
    manifest = {"version": stamp, "source_commit": os.getenv("REPORT_SOURCE_COMMIT", "working-tree-local"), "evidence_review_date": config["evidence_review_date"], "timezone": config["timezone"], "edition": config["directory"], "description": config["description"], "research_audit": audit, "application_database_refreshed": False, "licenses": {"software": "MIT", "original_report_content": "CC-BY-4.0", "source_data": "Provider-specific"}, "pdf_pages": pages, "sha256": files, "visual_review": "Every page rendered; review recorded in spec 009 validation."}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    archive = out / f"reports-{stamp}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(out.rglob("*")):
            if path.is_file() and path != archive:
                bundle.write(path, path.relative_to(out).as_posix())
    # Publisher consumes only top-level allowlisted assets; full hashes live in manifest.
    (out / "SHA256SUMS.txt").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n" for p in sorted(out.iterdir()) if p.is_file() and p.name != "SHA256SUMS.txt"))
    print(json.dumps({"version": stamp, "pdf_pages": pages, "output": str(out), "qa": str(qa)}))
