# Verification matrix

| Requirement | Check | Status / evidence |
|---|---|---|
| FR-001 | Request-only main push starts workflow | pass; evidence/github-run.json |
| FR-002 | Six admission tests plus six launcher tests | pass; evidence/portable-linux.log and three remote OS jobs |
| FR-003 | Three-OS matrix, Docker report build and publication | pass; evidence/github-jobs.json |
| FR-004 | Procedure, downloadable hashes and manifest identity | pass; docs/report-operations.md and evidence/published-release-verification.json |

Run: https://github.com/AXIOVEX/michigan-workforce-intelligence/actions/runs/36321581479
Release: https://github.com/AXIOVEX/michigan-workforce-intelligence/releases/tag/reports-2026.09.27.131143Z

Canonical application Docker CI could not run locally (Docker absent); native full CI passed. Remote Docker report build and portable gates passed. These are distinct checks. The missing local RTK and initial runtime dependency recovery remain documented in convergence.md.
