# Software Unit Verification Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SWE4-001 |
| **Version** | v1.03 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.4 — Software Unit Verification |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added §4.6 (MISRA C:2012 provisioning) with UVT-060 and UVT-061 covering SR-028 and SR-029. |
| v1.02 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |
| v1.03 | 2026-08-13 | Dermot Murphy | §1 CI execution line no longer cites the non-existent `Run-Unit-Tests` job; explains that UVT execution is folded into the single-tier CI model per CCD-SUP1-001 §6.1 (issue #33, closes audit finding FIND-E). |

---

## 1. Introduction

This document is the Software Unit Verification Plan (UVP) for the CppCheckDocker project. It defines the strategy, environment, and test cases for verifying each unit of the deliverable (Dockerfile instructions, image layers, image metadata) in accordance with ASPICE v4 process SWE.4.

Unit tests for this project inspect **image structure**: they exercise the built image without applying it to a source tree. Analysis-behaviour tests (image + source) are integration tests and belong to CCD-SWE5-001.

**Parent document:** CCD-SWE3-001 SDDD
**Test framework:** bash + `docker` CLI
**Test location:** `test/unit/`
**CI execution:** UVT cases are executed under the single-tier CI model defined in CCD-SUP1-001 §6.1. There is no dedicated `Run-Unit-Tests` job. Image-sanity UVTs (SR-023 version smoke, presence of required files, image-metadata invariants) are covered by the `Verify-Version` job on every push; the remaining UVTs are exercised as pre-conditions of the `Run-Integration-Tests` job (see the UVT->CI-step mapping in §5). A separate `Run-Unit-Tests` job may be added later if the suite outgrows this arrangement.

---

## 2. Unit Verification Strategy

### 2.1 Scope

Unit verification covers the structural properties of the built image:
- Version and identity of the payload (cppcheck binary)
- Presence of required files (cfg XMLs, platforms XMLs, addons)
- Presence of runtime dependencies (`libpcre3`, `python3`)
- Absence of build tools and source trees
- User, working directory, entrypoint metadata
- OCI labels
- Reproducibility of build outputs

Third-party COTS (Ubuntu base image, cppcheck itself) is not unit-tested — its correctness is assumed from supplier qualification.

### 2.2 Pass/Fail Criteria

A unit test passes when:
- The observed image property matches the expected value
- No unexpected `docker` command errors occur

A test run passes when all unit tests pass. CI enforces zero failures before merge.

### 2.3 Coverage Target

| Category | Minimum Coverage Target |
|:--------------|:-------------------------------|
| Image structure SRs (SR-001..SR-010) | 100% — every SR mapped to at least one UVT |
| Runtime metadata SRs (SR-020..SR-036) | 100% |
| Security SRs (SR-040..SR-044) | 100% |
| Reproducibility SRs (SR-050..SR-054) | Best-effort — SR-054 (bit-identical rebuild) is Desirable and may be waived |
| Performance/size SRs (SR-060..SR-063) | SR-060 always; SR-061..SR-063 measured in CI logs |

There is no branch-coverage concept for a Dockerfile; coverage is measured by SR-to-test mapping.

### 2.4 Tier

All unit tests run on every push. There is no smoke/component split — the total suite is small enough that the entire suite fits within the 15-minute overall CI budget.

### 2.5 Static Analysis Integration

Static analysis complements dynamic unit testing:

| Tool | When Applied | Output |
|:--------------|:-------------|:------------|
| **hadolint** (planned) | CI on every push once active; checks `Dockerfile` | Lint report uploaded as `Hadolint_Report` |
| **trivy / Docker Scout** (planned) | CI on every push once active; scans built image | CVE report uploaded as `Image_Scan_Report` |

Hadolint findings at severity **Error** will block merge once the CI gate is active. Trivy findings at CVE severity **CRITICAL** or **HIGH** will block merge unless a documented risk acceptance is attached.

---

## 3. Test Environment

| Item | Detail |
|:--------------|:------------|
| Host OS | Ubuntu 24.04 (GitHub Actions `ubuntu-latest` runner) |
| Container runtime | Docker Engine with BuildKit |
| Test framework | bash 5+ with standard POSIX tools (`grep`, `awk`, `sha256sum`) |
| Image under test | `cppcheck:ci` (built by the `Build-Image` job) |
| CI trigger | Every push |
| Test artefact | `Unit_Test_Output` — stdout/stderr of `test/unit/run.sh` |

Developers can execute unit tests locally with:
```bash
docker build -t cppcheck:local .
test/unit/run.sh cppcheck:local
```

---

## 4. Unit Test Cases

### 4.1 Image Build Structure

| Test ID | Function Under Test | Input | Expected Output | SR Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| UVT-001 | Base image tag | `docker image inspect cppcheck:ci --format '{{.Config.Image}}'` (via history) | Chain contains `ubuntu:24.04` or the pinned `UBUNTU_VERSION` | SR-001 |
| UVT-002 | Multi-stage layer count | `docker image inspect cppcheck:ci --format '{{len .RootFS.Layers}}'` | Layer count ≤ 8 (indicative of multi-stage discipline) | SR-002 |
| UVT-003 | Builder apt packages present in builder | Grep `docker history cppcheck:ci --no-trunc` for `build-essential cmake ninja-build git ca-certificates libpcre3-dev python3` in a *builder* layer, then confirm those layers are not part of runtime | Packages listed in an early layer that is *not* the top layer | SR-003 |
| UVT-004 | Cppcheck source tag pinned | `grep "ARG CPPCHECK_VERSION" Dockerfile` | Line matches `ARG CPPCHECK_VERSION=<version>` with a specific version | SR-004, SR-050, SR-051 |
| UVT-005 | CMake options in Dockerfile | `grep -E "HAVE_RULES=ON\|USE_MATCHCOMPILER=ON\|CMAKE_BUILD_TYPE=Release" Dockerfile` | All three options present | SR-005 |
| UVT-006 | Install prefix content | `docker run --rm --entrypoint sh cppcheck:ci -c 'ls /opt/cppcheck/bin /opt/cppcheck/share/cppcheck'` | `bin/cppcheck` and `share/cppcheck/cfg` both listed | SR-006 |
| UVT-007 | Runtime apt packages | `docker run --rm --entrypoint sh cppcheck:ci -c 'dpkg -l libpcre3 python3'` | Both packages report installed | SR-007 |
| UVT-008 | Payload copied from builder | `docker run --rm --entrypoint sh cppcheck:ci -c 'test -x /opt/cppcheck/bin/cppcheck && echo OK'` | Prints `OK` | SR-008 |
| UVT-009 | No build tools in runtime | `docker run --rm --entrypoint sh cppcheck:ci -c 'command -v gcc g++ cmake ninja git ; echo done'` | Only `done` printed (no compiler paths) | SR-009 |
| UVT-010 | .dockerignore correctness | `grep -E "^\.git\$\|^documents\$\|^test\$" .dockerignore` | All three lines present | SR-010 |

### 4.2 Runtime Metadata

| Test ID | Function Under Test | Input | Expected Output | SR Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| UVT-020 | Non-root user defined | `docker image inspect cppcheck:ci --format '{{.Config.User}}'` | `cppcheck` | SR-030, SR-042 |
| UVT-021 | Working directory | `docker image inspect cppcheck:ci --format '{{.Config.WorkingDir}}'` | `/work` | SR-031 |
| UVT-022 | Entrypoint value | `docker image inspect cppcheck:ci --format '{{json .Config.Entrypoint}}'` | `["cppcheck"]` | SR-021 |
| UVT-023 | Default CMD | `docker image inspect cppcheck:ci --format '{{json .Config.Cmd}}'` | `["--help"]` | SR-022 |
| UVT-024 | PATH includes install prefix | `docker run --rm --entrypoint sh cppcheck:ci -c 'echo $PATH'` | Contains `/opt/cppcheck/bin` | SR-020 |
| UVT-025 | Cppcheck version string | `docker run --rm cppcheck:ci --version` | `Cppcheck <CPPCHECK_VERSION>` (exact) | SR-023 |
| UVT-026 | cfg files present | `docker run --rm --entrypoint sh cppcheck:ci -c 'ls /opt/cppcheck/share/cppcheck/cfg/std.cfg /opt/cppcheck/share/cppcheck/cfg/posix.cfg'` | Both files listed | SR-024 |
| UVT-027 | Platforms XML present | `docker run --rm --entrypoint sh cppcheck:ci -c 'ls /opt/cppcheck/share/cppcheck/platforms/arm32-wchar_t4.xml'` | File listed | SR-025 |
| UVT-028 | python3 available in runtime | `docker run --rm --entrypoint python3 cppcheck:ci --version` | `Python 3.x` | SR-026 |

### 4.3 Security

| Test ID | Function Under Test | Input | Expected Output | SR Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| UVT-030 | No secret-like files | `docker run --rm --entrypoint sh cppcheck:ci -c 'find / -name .env -o -name id_rsa -o -name credentials.json 2>/dev/null'` | Empty output | SR-040 |
| UVT-031 | No .git directories | `docker run --rm --entrypoint sh cppcheck:ci -c 'find / -type d -name .git 2>/dev/null'` | Empty output | SR-041 |
| UVT-032 | Default user is not root | `docker run --rm --entrypoint id cppcheck:ci -u` | Non-zero UID (typically 1000) | SR-042 |
| UVT-033 | No exposed ports | `docker image inspect cppcheck:ci --format '{{json .Config.ExposedPorts}}'` | `null` or `{}` | SR-043 |
| UVT-034 | OCI labels present | `docker image inspect cppcheck:ci --format '{{index .Config.Labels "org.opencontainers.image.title"}}'` | Non-empty; equal to `cppcheck` | SR-044 |

### 4.4 Reproducibility

| Test ID | Function Under Test | Input | Expected Output | SR Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| UVT-040 | Build ARGs honoured | `docker build --build-arg CPPCHECK_VERSION=2.20.0 -t cppcheck:test-alt .`; `docker run --rm cppcheck:test-alt --version` | `Cppcheck 2.20.0` | SR-050 |
| UVT-041 | Cppcheck binary reproducible across two builds | Build twice from same commit; `sha256sum` the `cppcheck` binary extracted from each image | Both hashes identical | SR-054 (Desirable) |

### 4.5 Size and Performance

| Test ID | Function Under Test | Input | Expected Output | SR Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| UVT-050 | Runtime image size within budget | `docker image inspect cppcheck:ci --format '{{.Size}}'` | ≤ 210 000 000 (~200 MB) | SR-060 |

Performance SRs (SR-061 cold-build time, SR-062 `--version` latency, SR-063 integration suite time) are observed from CI job durations rather than asserted by dedicated unit tests. They are reported in job logs and reviewed at each release.

### 4.6 MISRA C:2012 Provisioning

| Test ID | Function Under Test | Input | Expected Output | SR Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| UVT-060 | MISRA rule-texts file bundled | `docker run --rm --entrypoint sh cppcheck:ci -c 'head -3 /opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt'` | Output includes `MISRA C:2012 Guideline Headlines for CPPcheck` | SR-028 |
| UVT-061 | Shim addon present and executable | `docker run --rm --entrypoint sh cppcheck:ci -c 'test -x /opt/cppcheck/share/cppcheck/addons/misra-c2012.py && head -1 /opt/cppcheck/share/cppcheck/addons/misra-c2012.py'` | Output = `#!/usr/bin/env python3` | SR-029 |

---

## 5. Regression Policy

All unit tests run on every push. A failing unit test blocks merge to `develop` and `main`. Results are uploaded as `Unit_Test_Output`.

New Mandatory requirements added to the SRS must be accompanied by at least one unit or integration test case before the implementing PR is merged.

**Static analysis:** hadolint (once active) runs on every push against the Dockerfile. Trivy / Docker Scout (once active) runs on every push against the built image.

---

## 6. Traceability Summary

| Test ID Range | Category | SR IDs Covered |
|:---------------|:------------|:---------------|
| UVT-001–010 | Image build structure | SR-001, SR-002, SR-003, SR-004, SR-005, SR-006, SR-007, SR-008, SR-009, SR-010, SR-050, SR-051 |
| UVT-020–028 | Runtime metadata | SR-020, SR-021, SR-022, SR-023, SR-024, SR-025, SR-026, SR-030, SR-031, SR-042 |
| UVT-030–034 | Security | SR-040, SR-041, SR-042, SR-043, SR-044 |
| UVT-040–041 | Reproducibility | SR-050, SR-054 |
| UVT-050 | Size | SR-060 |
| UVT-060–061 | MISRA provisioning | SR-028, SR-029 |

*Full traceability in CCD-RTM-001.*

---

*End of CCD-SWE4-001 v1.03*
