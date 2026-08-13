# Software Qualification Test Specification
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SWE6-001 |
| **Version** | v1.02 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.6 — Software Qualification Test |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added QT-015 (MISRA C:2012 end-to-end) covering SR-028 and SR-029. |
| v1.02 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |

---

## 1. Introduction

This document is the Software Qualification Test Specification (QTS) for the CppCheckDocker image. It defines the qualification tests that demonstrate complete satisfaction of the software requirements (CCD-SWE1-001), in accordance with ASPICE v4 process SWE.6.

Qualification tests are black-box tests executed against the **published** container image (the image tagged for release and pushed to `ghcr.io`), not against the CI-built local image. They verify that the delivered image meets its stated requirements from the consumer's perspective, with no knowledge of internal Dockerfile structure.

**Parent document:** CCD-SWE1-001 SRS
**Image under test:** `ghcr.io/<owner>/cppcheckdocker:<cppcheck-version>-r<revision>`
**Test environment:** A GitHub-hosted `ubuntu-latest` runner in a separate consumer repository (or a fresh workstation with Docker installed)

---

## 2. Qualification Test Strategy

### 2.1 Entry Criteria

Before qualification testing begins:
- All unit tests (CCD-SWE4-001) pass with zero failures
- All integration tests (CCD-SWE5-001) pass on GitHub Actions
- The image under test is pulled from `ghcr.io` at a specific `<cppcheck-version>-r<revision>` tag (not `latest`)
- The image digest is recorded in the test record

### 2.2 Pass Criteria

Each test case specifies an expected result. The test passes when the actual result matches the expected result. All Mandatory test cases must pass. Desirable and Optional test failures are recorded but do not block qualification.

### 2.3 Test Record

Each test execution must be recorded with:
- Date of execution
- Tester name
- Image tag under test
- Image digest under test
- Host OS
- Docker Engine version
- Pass / Fail result
- Actual measured value (where applicable)
- Deviation notes (where applicable)

---

## 3. Qualification Test Cases

### QT-001 — Cppcheck Version Reporting

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-001 |
| **SR Reference** | SR-023, SR-052 |
| **Priority** | Mandatory |
| **Title** | Cppcheck reports the pinned version |
| **Procedure** | 1. `docker pull ghcr.io/<owner>/cppcheckdocker:<version>-r<rev>`. 2. `docker run --rm <image> --version`. |
| **Expected** | Output is exactly `Cppcheck <version>` where `<version>` matches the tag portion of the image reference |
| **Tolerance** | Exact match |

---

### QT-002 — Consumer Use as GitHub Actions Step Container

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-002 |
| **SR Reference** | SR-036, SR-007 (FEAT-007) |
| **Priority** | Mandatory |
| **Title** | Image runs as a GitHub Actions step container |
| **Procedure** | 1. In a separate repository, define a workflow with `container: ghcr.io/<owner>/cppcheckdocker:<version>-r<rev>`. 2. Add a step running `cppcheck --enable=all src/`. 3. Push and observe. |
| **Expected** | The job step runs; cppcheck output appears in the log; job exit reflects the presence or absence of findings per `--error-exitcode` |

---

### QT-003 — Consumer Use as `docker run` on Local Source Tree

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-003 |
| **SR Reference** | SR-032 |
| **Priority** | Mandatory |
| **Title** | Docker run against a bind-mounted source directory |
| **Procedure** | 1. `docker run --rm -v "$(pwd):/work:ro" <image> --enable=all --error-exitcode=1 src/`. |
| **Expected** | cppcheck runs against `src/`; any real defects reported; exit code = 1 if defects present, 0 otherwise |

---

### QT-004 — Analysis of a Known-Defective File

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-004 |
| **SR Reference** | SR-027, SR-033 |
| **Priority** | Mandatory |
| **Title** | Cppcheck detects deliberately seeded defects |
| **Procedure** | 1. Create a file `bad.c` containing: `int main(void){int *p=malloc(sizeof(int)*10); p[10]=0; return 0;}`. 2. `docker run --rm -v $(pwd):/work:ro <image> --enable=all --error-exitcode=1 bad.c`. |
| **Expected** | Output contains `arrayIndexOutOfBounds` and `memleak`; exit code 1 |

---

### QT-005 — Analysis of a Known-Clean File

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-005 |
| **SR Reference** | SR-027, SR-034 |
| **Priority** | Mandatory |
| **Title** | Cppcheck produces no findings for clean code |
| **Procedure** | 1. Create a trivial `hello.c` containing `int main(void){return 0;}`. 2. `docker run --rm -v $(pwd):/work:ro <image> --enable=all --error-exitcode=1 hello.c`. |
| **Expected** | Zero findings emitted; exit code 0 |

---

### QT-006 — XML Output Format

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-006 |
| **SR Reference** | SR-035 |
| **Priority** | Desirable |
| **Title** | XML output is well-formed |
| **Procedure** | 1. `docker run --rm -v $(pwd):/work:ro <image> --xml --enable=all bad.c 2> out.xml`. 2. Pipe `out.xml` through `xmllint --noout`. |
| **Expected** | `xmllint` returns zero; document contains `<errors>` and at least one `<error>` element |

---

### QT-007 — Non-Root Default User

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-007 |
| **SR Reference** | SR-030, SR-042 |
| **Priority** | Mandatory |
| **Title** | Container runs as non-root by default |
| **Procedure** | `docker run --rm --entrypoint id <image>` |
| **Expected** | UID and GID are non-zero (typically 1000); user name is `cppcheck` |

---

### QT-008 — Image Size Within Budget

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-008 |
| **SR Reference** | SR-060 |
| **Priority** | Mandatory |
| **Title** | Runtime image size is within 200 MB target |
| **Procedure** | `docker image inspect <image> --format '{{.Size}}'` |
| **Expected** | Value ≤ 210 000 000 (leaves margin against a 200 MB soft target) |

---

### QT-009 — OCI Labels Set

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-009 |
| **SR Reference** | SR-044 |
| **Priority** | Mandatory |
| **Title** | OCI standard labels present |
| **Procedure** | `docker image inspect <image> --format '{{json .Config.Labels}}' \| jq` |
| **Expected** | Keys `org.opencontainers.image.title`, `.description`, `.source`, `.licenses` present with non-empty values |

---

### QT-010 — No .git Directory in Image

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-010 |
| **SR Reference** | SR-041 |
| **Priority** | Mandatory |
| **Title** | No .git directory shipped in the image |
| **Procedure** | `docker run --rm --entrypoint sh <image> -c 'find / -type d -name .git 2>/dev/null'` |
| **Expected** | Empty output |

---

### QT-011 — No Compilers in Runtime Image

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-011 |
| **SR Reference** | SR-009 |
| **Priority** | Mandatory |
| **Title** | Runtime image contains no C/C++ compiler |
| **Procedure** | `docker run --rm --entrypoint sh <image> -c 'command -v gcc g++ cc clang cmake ninja ; true'` |
| **Expected** | Empty output |

---

### QT-012 — python3 Available for Addons

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-012 |
| **SR Reference** | SR-026 |
| **Priority** | Mandatory |
| **Title** | python3 present at runtime |
| **Procedure** | `docker run --rm --entrypoint python3 <image> --version` |
| **Expected** | Output starts with `Python 3.` |

---

### QT-013 — Version Latency

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-013 |
| **SR Reference** | SR-062 |
| **Priority** | Mandatory |
| **Title** | `--version` returns within 3 seconds |
| **Procedure** | `time docker run --rm <image> --version` |
| **Expected** | Real time ≤ 3 seconds after the image is already loaded |

---

### QT-015 — MISRA C:2012 Addon End-to-End

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-015 |
| **SR Reference** | SR-028, SR-029 |
| **Priority** | Mandatory |
| **Title** | MISRA C:2012 analysis with bundled rule-texts |
| **Procedure** | 1. `docker pull ghcr.io/<owner>/cppcheckdocker:<version>-r<rev>`. 2. Create `misra_bad.c` with `int main(void) { goto e; e: return 0; }`. 3. Run: `docker run --rm -v $(pwd):/work:ro <image> --enable=style --addon=misra-c2012 --cppcheck-build-dir=/tmp misra_bad.c` |
| **Expected** | Exit 0. Stdout contains both `The goto statement should not be used` (readable rule text — proves the bundled rule-texts file was loaded) and `[misra-c2012-15.1]` (rule ID) |

---

### QT-014 — Consumer Override to Root

| Field | Detail |
|:--------------|:------------|
| **Test ID** | QT-014 |
| **SR Reference** | SR-042 (override) |
| **Priority** | Desirable |
| **Title** | Consumer may override user to root |
| **Procedure** | `docker run --rm -u 0:0 --entrypoint id <image>` |
| **Expected** | UID 0, GID 0 |

---

## 4. Qualification Test Record Template

| Test ID | Date | Tester | Image Tag | Image Digest | Result | Actual Value | Notes |
|:--------------|:------------|:------------|:------------|:-------------|:------------|:-------------|:------------|
| QT-001 | | | | | PASS/FAIL | | |
| QT-002 | | | | | PASS/FAIL | | |
| QT-003 | | | | | PASS/FAIL | | |
| ... | | | | | | | |

*Complete this table for each test execution. Retain completed records per the Configuration Management Plan (CCD-SUP8-001) at `documents/aspice/records/`.*

---

## 5. Traceability Summary

| Test ID | SR References |
|:--------------|:--------------|
| QT-001 | SR-023, SR-052 |
| QT-002 | SR-036 |
| QT-003 | SR-032 |
| QT-004 | SR-027, SR-033 |
| QT-005 | SR-027, SR-034 |
| QT-006 | SR-035 |
| QT-007 | SR-030, SR-042 |
| QT-008 | SR-060 |
| QT-009 | SR-044 |
| QT-010 | SR-041 |
| QT-011 | SR-009 |
| QT-012 | SR-026 |
| QT-013 | SR-062 |
| QT-014 | SR-042 |
| QT-015 | SR-028, SR-029 |

*Full traceability in CCD-RTM-001.*

---

*End of CCD-SWE6-001 v1.02*
