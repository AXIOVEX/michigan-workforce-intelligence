# Plan and clarification

The historical run 34793451385 used workflow_dispatch as tbitcs. scripts/reports.py delegates to gh workflow run. Current tools expose Git data writes and Actions reads/retries but no dispatch. No authenticated gh is present. Changing token permissions alone cannot add a missing tool operation.

Use GitHub's native push trigger filtered to main and release/request.json. An initial configuration commit must not trigger publication. A second request-only commit references its immediate reviewed parent. A resolver validates that invariant and emits the version as a job output. Build the request commit (source parent plus request only), preserving exact GITHUB_SHA in the manifest. Retain manual dispatch.

No new dependencies, secrets, arbitrary command inputs or administrative permission changes. Existing protected main write authorization controls requests. Request edits are explicit publication actions. Failure recovery uses normal failed-job retry or a fresh reviewed request/version; never delete a previous release.
