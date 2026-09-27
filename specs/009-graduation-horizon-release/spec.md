# September workforce release and graduation-horizon planning

Date: 2026-09-26 (America/Detroit). Status: specified; verification pending.

## User scenarios and acceptance

1. A Michigan employer reads the new edition and can distinguish weakening hiring, falling participation, unemployment, insufficient hours, and graduate skill mismatch. Every number identifies period, geography, definition, source, and freshness.
2. A university dean plans credentials beginning in 2026 for completion in 2027, 2028, 2030, and 2032 or later. Each recommendation identifies retain/expand/redesign/conditional teach-out, relevant skills, evidence, review horizon, and uncertainty.
3. An incumbent worker/employer identifies an adjacent role, transferable competencies, missing competencies, a practical assessment, transition constraints, and receiving-employer validation before training expenditure.
4. A maintainer reproduces PDFs from committed evidence, inspects SDD/AEE results, and publishes an additive versioned release without changing prior evidence or releases.

## Functional requirements

- FR-001 / REQ-FRESHNESS-001: Research information published by the September 26 cutoff; label observation, publication, retrieval, and review dates independently. Preserve unavailable and conflicting values rather than infer them.
- FR-002 / REQ-LABOR-002: Cover Michigan, Macomb, Oakland, Wayne, national benchmarks, U-3/U-6, participation, employment-population ratio, involuntary part-time work, graduate underemployment, hires/quits, sentiment, and indirect demand/household indicators. Missing refreshed series must be explicit; geography and adjustment mismatches must not masquerade as comparisons.
- FR-003 / REQ-EDUCATION-003: Provide graduation-horizon program recommendations and evidence-based redesign/conditional teach-out candidates. Do not assign an occupational extinction date without defensible evidence; distinguish projected decline, replacement openings, task change, and local demand.
- FR-004 / REQ-IMAGING-004: Analyze radiology and AI medical imaging separately from radiologic technologists and adjacent professions; propose role-appropriate AI competencies without promising job preservation or expanded clinical privileges.
- FR-005 / REQ-TRANSITIONS-005: Provide at least eight skills-bridge pathways, employer validation criteria, paid transition design, and measurable retention/earnings outcomes.
- FR-006 / REQ-LINEAGE-006: Preserve source snapshots or retrieval records with hashes, parser versions, claim IDs, uncertainty, contradictions, and append-only evidence events. Clearly separate this edition's research ledger from the pre-existing application database audit.
- FR-007 / REQ-ARTIFACTS-007: Generate a new executive brief, economic report, and continuity/education report with human-readable citations, attribution, versioned manifest/checksums, machine-readable inputs, and visual QA. Historical snapshots remain historical and are never relabeled as refreshed.
- FR-008 / REQ-SDD-008: Use Spec Kit stages and actual AEE adapter assessment, challenge, trace, ledger verification, and gap generation. Retain failures and recovery evidence. AEE scores do not establish factual truth.
- FR-009 / REQ-RELEASE-009: Run required local gates, commit authorized changes, publish a new additive release and verify downloadable assets; leave publication pending if access or required gates cannot be satisfied.
- FR-010 / REQ-AI-SECTORS-010: Treat radiology as one example within a cross-sector AI task-impact matrix covering software, accounting, legal support, engineering design, administration, customer service, media, and manufacturing. For each distinguish task exposure, occupation demand, remaining human accountability, curriculum adaptation, and evidence confidence.
- FR-011 / REQ-CORROBORATION-011: Authoritative official government statistical releases may support a factual observation as a single source. Seek second-source corroboration when feasible, distinguish independent evidence from republication of the same underlying series, and preserve discrepancies. Do not label a source certified unless it explicitly has that status. Extra source count alone must not inflate confidence.

## Edge cases

Preliminary/final sentiment disagreement; official prose inconsistent with its own tables; missing monthly observations; shutdown-distorted averaging periods; source changes after cutoff; national growth alongside Michigan contraction; overlapping occupations and credential awards; no live employer requisitions; no local database volume; protected branches; absent Docker/RTK; unavailable publication endpoint.

## Success criteria

- SC-001: All published numeric observations are traceable to a preserved source record and carry their period and geography.
- SC-002: At least eight education/transition pathways include skills, assessment, horizon and constraints; radiology has a dedicated section.
- SC-003: No missing metric is silently filled, no proposal is labeled a confirmed placement, and no unsupported obsolescence date is published.
- SC-004: Every FR maps to a task and verification item; generated reports pass structural and visual review; release state is verified rather than assumed.

## Assumptions and clarifications

Use the existing geographic scope and three primary release filenames. User authorizes report generation and new release publication, not replacement/deletion of older releases, outreach, institutional commitments, or live deployment. Existing institutions remain candidates. Review windows are proposed governance dates, not forecasts of extinction. Constitution 1.1.0 remains applicable without amendment.

## Key entities

Source record; observation; claim; contradiction; program recommendation; transition pathway; verification evidence; release manifest. See data-model.md.
