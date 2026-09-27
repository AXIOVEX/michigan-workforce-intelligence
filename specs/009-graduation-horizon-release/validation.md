# Validation and convergence

Native `scripts/local_ci.sh` passed: governance, compile, 263 unit tests, 91.55% source coverage (90% gate), source catalog, all-feature traceability, Ruff and mypy. Linux portable launcher tests passed (6). `make ci` could not execute because Docker is not installed; RTK is also absent. These are recorded environment deficiencies, not silently waived gates. Windows/macOS and Docker gates await the existing manual GitHub workflow.

Eight added boundary tests cover original BLS correspondence, null semantics, future dates, content tampering, reordered ledger, append-only preservation and unsafe paths. The offline evidence validator passed for 28 sources, 187 observations and 36 projection rows.

PDF QA build 2026.09.27.030300Z: executive 3 pages, economic 13 pages, education/continuity 15 pages. Every one of the 31 pages was rendered and inspected in four contact sheets. Initial layout defects (sparse section pagination, chart labels) were corrected and all pages rechecked. A bundled pdftoppm failure was resolved by selecting the installed system binary; a missing Path import was corrected. No clipping or overlaps remained. This prepublication QA version label was selected before 03:03 UTC; the final release will use its actual build timestamp.

AEE initial prose plan/tasks parses produced zero-claim passes and are not substantive acceptance evidence. They were retained and rerun with structured claims; gather-evidence results were expected before implementation. Final claims distinguish executable test evidence from model-authored interpretations. AEE scoring is advisory and cannot establish statistical truth, employer demand or publication completion.

Remote release publication and downloadable asset verification remain pending until authenticated dispatch succeeds. No release is represented as published merely because local PDFs exist.

Final rebuild exposed one truncated renderer output despite exit zero. The builder now decodes every PNG and retries only a damaged page once, failing if the retry is invalid. The eight edition boundary tests and Ruff passed after this change.
