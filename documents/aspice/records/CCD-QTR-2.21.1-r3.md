# Qualification Test Record
## CppCheckDocker — Release v2.21.1-r3

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-QTR-2.21.1-r3 |
| **Version** | v1.00 |
| **Date** | 2026-08-14 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.6 — Software Qualification Test |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-14 | Dermot Murphy | Backfill issue per #48 — qualification test record for release v2.21.1-r3 (documentation-and-CI-hygiene republish of r2) |

---

## 1. Scope

Executes every qualification test case defined in [CCD-SWE6-001](../CppCheckDocker_SWE6_Qualification_Test.md) §3 against the released image and records the outcome. This QTR is independent evidence for r3 even though the runtime image is content-identical to r2 — SPL.2 requires per-release qualification, not per-content.

Related SVD: [`CCD-SVD-2.21.1-r3`](CCD-SVD-2.21.1-r3.md).

---

## 2. Test Environment

| Field | Value |
|:--------------|:------------|
| **Image Tag** | `ghcr.io/dermot-murphy/cppcheckdocker:2.21.1-r3` |
| **Image Digest** | `sha256:b6c84424910a099b49eecd3890329f08302aca3c785f233d44df4fb604a6d28d` |
| **Test Host** | GitHub Actions `ubuntu-latest` runner (per CCD-SWE6-001 §2) |
| **Test Date (UTC)** | 2026-08-13 |
| **Tester** | Dermot Murphy (via automated CI on merge of PR #27) |
| **Evidence Trail** | CI run <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31718028261> |

The `Run-Integration-Tests` job executes `test/integration/run.sh`, which drives the full INT case set on the built image. Because the CI pipeline uses a single-tier test model per CCD-SUP1-001 §6.1, every QT case is verified either directly by that harness or by the `Verify-Version` / `Scan-Image` / `Lint` / `Publish-Wiki` jobs on the same run.

---

## 3. Test Results

| Test ID | Date | Tester | Image Tag | Image Digest | Result | Actual Value | Notes |
|:--------------|:------------|:------------|:------------|:-------------|:------------|:-------------|:------------|
| QT-001 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `Cppcheck 2.21.1` | `Verify-Version` job |
| QT-002 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | ENTRYPOINT accepts args from GHA step container context | INT-002, INT-011 |
| QT-003 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `docker run -v` mount analysis returns findings | INT-010/INT-011/INT-012 |
| QT-004 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `arrayIndexOutOfBounds` on `buggy.c`; exit 1 with `--error-exitcode=1` | INT-011 |
| QT-005 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | No findings on `clean.c`; exit 0 | INT-010 |
| QT-006 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `<errors>` root element present in `--xml` output | INT-013 |
| QT-007 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `WORKDIR /work`, `USER cppcheck` verified | Dockerfile lines 81–83 |
| QT-008 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | ~130 MB (< 200 MB budget) | `Build-Image` job "Record image size" step |
| QT-009 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | OCI labels present | Dockerfile lines 47–50 |
| QT-010 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | No `.git` directory in runtime layer | Multi-stage build; `.dockerignore` |
| QT-011 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | No `gcc`/`g++`/`cmake`/`ninja` in runtime image | Runtime stage installs only `libpcre3`, `python3` |
| QT-012 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `python3 --version` returns Python 3.12.x | Verified by INT-040 MISRA addon |
| QT-013 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `2.21.1` still the current upstream stable at release | ACQ.4 §3.1; `poll-cppcheck.yml` |
| QT-014 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `docker run --user 0` works (consumer override) | Non-root default preserved |
| QT-015 | 2026-08-13 | CI | `2.21.1-r3` | `sha256:b6c8442…` | PASS | `The goto statement should not be used [misra-c2012-15.1]` on `misra_bad.c` | INT-040 |

---

## 4. Coverage Summary

| Metric | Value |
|:--------------|:------------|
| **Total QT cases** | 15 |
| **PASS** | 15 |
| **FAIL** | 0 |
| **Skipped / Blocked** | 0 |
| **Coverage of Mandatory SRs** | 100% — see CCD-RTM-001 |

---

## 5. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-13 | Git commit authorship |
| Reviewer | Dermot Murphy | 2026-08-13 | Self-review under CCD-MAN3-001 §3 single-engineer clause |
| Approver | Dermot Murphy | 2026-08-13 | PR #27 merge to `main` — `AllChecksPassed` gate satisfied |

**Backfill note:** this record was authored on 2026-08-14 as part of issue #48 to close the SWE.6 record gap identified during release-readiness review for r4. All results are copied from the pre-existing GitHub Actions run 31718028261 evidence; no tests were re-executed for the backfill.

---

*End of CCD-QTR-2.21.1-r3 v1.00*
