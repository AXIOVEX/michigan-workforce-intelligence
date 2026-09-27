# Connector-compatible release requests

User authorization: 2026-09-27, recover and script publication and enable required repository configuration. This extends spec 006's scoped report automation. It does not enable unrelated application CI or alter branch protection.

FR-001: A dedicated request-only commit on main must trigger the existing report workflow through authenticated GitHub content writes, without browser or local credentials.
FR-002: Validate calendar version, exact reviewed parent SHA, request-only diff and main ref before building. Preserve workflow_dispatch.
FR-003: Keep three-OS portable tests, Docker report build and checksum verification before additive release creation. Only publish job has contents:write.
FR-004: Document connector and CLI procedures, source identity, limitations and actual remote verification in SDD/AEE records.

Acceptance: request commit yields successful workflow and new release whose six assets download and match checksums. A local build or commit alone does not satisfy acceptance.
