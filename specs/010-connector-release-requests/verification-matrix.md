# Verification matrix

| Requirement | Check | Status |
|---|---|---|
| FR-001 | Remote request push starts workflow | pending |
| FR-002 | Six admission tests plus six existing launcher tests | pass, evidence/portable-linux.log |
| FR-003 | Remote portable matrix, Docker report build and publish | pending |
| FR-004 | Procedure and remote asset hash verification | procedure complete; remote verification pending |

Docker and RTK remain unavailable locally. Native full CI is recorded separately; the initial run encountered missing SOCKS transport support in the fresh execution environment, then socksio was installed and the gate rerun. No code test was removed or weakened.
