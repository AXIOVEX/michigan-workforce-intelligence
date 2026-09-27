# Traceable tasks

- [x] T001 FR-001 FR-008 Inspect baseline, specify scope and clarify cutoff/assumptions.
- [x] T002 FR-008 Install released AEE/evaluator and run specification/planning/tasks assessments.
- [x] T003 FR-001 FR-002 FR-006 FR-011 Collect primary sources, observation records, corroboration/independence assessment, conflicts and research ledger.
- [x] T004 FR-003 FR-004 FR-010 Write graduation-horizon and cross-sector AI task-impact recommendations, including clinical imaging as one case.
- [x] T005 FR-005 Write skills bridges, industry coordination and outcome framework.
- [x] T006 FR-007 Implement edition-aware build and manifest/publication metadata.
- [x] T007 FR-006 FR-007 Add evidence/edition validation and boundary tests.
- [x] T008 FR-007 FR-009 Run local and portable gates; generate/render/review all PDFs.
- [x] T009 FR-008 Run AEE challenge, graph, implementation assessment, ledger verification and gap register; retain unresolved findings.
- [x] T010 FR-009 Commit/push reviewed changes, publish additive release, verify remote assets and hashes.

Dependencies: T001 -> T002/T003; T003 -> T004/T005; T004/T005 -> T006 -> T007 -> T008 -> T009 -> T010. No checked item implies an unperformed verification.

T008: native CI, Linux portable tests and all-page PDF QA passed. Docker and Windows/macOS execution pending. T010: publication remains pending.

T008/T010 completed through native full CI, reviewed PDF build and successful remote three-OS/Docker report workflow; downloaded release hashes verified in spec 010. Full application Docker CI remains an environment gap, distinct from the successful Docker report build.
