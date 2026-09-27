# Data model

Source: id, publisher, URL, publication date (nullable if not established), retrieved_at, media type, parser version, content SHA-256, artifact path, access status and terms. Original bytes are immutable.

Observation: id, source_id, metric, value (nullable), unit, geography, population, period, adjustment, status, source locator, limitations. Comparisons require matching semantic keys; rolling windows are not monthly observations.

Claim: stable id, type (observation/derived/inference/proposal), statement, source/observation IDs, dependencies, falsifier, confidence rationale, conflicts and status. Revisions supersede earlier claims.

Research event: sequence, UTC timestamp, kind, record, previous hash, SHA-256 of canonical JSON excluding own hash. Validity establishes retained-record integrity only, not truth or completeness of the application ledger.

Program/pathway: curriculum family, target roles, current transferable skills, bridge, assessment, completion horizon, decision category, evidence, constraints and review trigger. No program closure decision without local placement/demand and teach-out analysis.

Release config/manifest: edition path, review cutoff, version, source commit, files/hashes, evidence inventory, tests/QA status. Historical source snapshots are not refreshed by changing a build date.
