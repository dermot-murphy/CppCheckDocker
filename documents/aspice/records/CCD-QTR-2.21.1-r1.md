# Qualification Test Record
## CppCheckDocker — Release v2.21.1-r1

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-QTR-2.21.1-r1 |
| **Version** | v1.00 |
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
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue — qualification test record for release v2.21.1-r1 |

---

## 1. Scope

Executes every qualification test case defined in [CCD-SWE6-001](../CppCheckDocker_SWE6_Qualification_Test.md) §3 against the released image and records the outcome. Passing this record is a merge gate for the release commit and evidence for ASPICE SWE.6.

Related SVD: [`CCD-SVD-2.21.1-r1`](CCD-SVD-2.21.1-r1.md).

---

## 2. Test Environment

| Field | Value |
|:--------------|:------------|
| **Image Tag** | `ghcr.io/dermot-murphy/cppcheckdocker:2.21.1-r1` |
| **Image Digest** | `sha256:632aeb9918397fcc15f8bc2f6d384188eb2d13a9c4460412629214b93dcad46f` |
| **Test Host** | GitHub Actions `ubuntu-latest` runner (per CCD-SWE6-001 §2) |
| **Test Date (UTC)** | 2026-08-13 |
| **Tester** | Dermot Murphy (via automated CI on merge of PR #17) |
| **Evidence Trail** | CI run <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> |

The `Run-Integration-Tests` job executes `test/integration/run.sh`, which drives the full INT case set. Because the CI pipeline uses a single-tier test model per CCD-SUP1-001 §6.1, every QT case is verified either directly by that harness or by the `Verify-Version` / `Scan-Image` / `Lint` / `Publish-Wiki` jobs on the same run. Result rows below cite the specific CI evidence for each case.

---

## 3. Test Results

| Test ID | Date | Tester | Image Tag | Image Digest | Result | Actual Value | Notes |
|:--------------|:------------|:------------|:------------|:-------------|:------------|:-------------|:------------|
| QT-001 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `Cppcheck 2.21.1` | `Verify-Version` job — matches pinned `CPPCHECK_VERSION` env |
| QT-002 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | ENTRYPOINT accepts args from GHA step container context | Verified by INT-002 (default `--help`) and INT-011 (`--enable=all` with args) |
| QT-003 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `docker run -v` mount analysis returns findings | Verified by INT-010/INT-011/INT-012 against `/work` bind mount |
| QT-004 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `arrayIndexOutOfBounds` on `buggy.c`; exit 1 with `--error-exitcode=1` | INT-011 |
| QT-005 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | No findings on `clean.c`; exit 0 | INT-010 |
| QT-006 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `<errors>` root element present in `--xml` output | INT-013 |
| QT-007 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `WORKDIR /work`, `USER cppcheck` verified by inspect | Dockerfile lines 81–83; UVT-020/UVT-021 |
| QT-008 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | ~130 MB (< 200 MB budget in CCD-SUP1-001 §2) | `Build-Image` job "Record image size" step |
| QT-009 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | OCI labels present (`org.opencontainers.image.title/description/source/licenses`) | Dockerfile lines 47–50; UVT-034 |
| QT-010 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | No `.git` directory in runtime layer | Multi-stage build with `COPY --from=builder /opt/cppcheck /opt/cppcheck` only; `.dockerignore` excludes `.git` |
| QT-011 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | No `gcc`/`g++`/`cmake`/`ninja` in runtime image | Runtime stage installs only `libpcre3` and `python3`; build tools live in the discarded builder stage |
| QT-012 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `python3 --version` returns Python 3.12.x | Verified by INT-040 MISRA addon (fails loudly if python3 missing) |
| QT-013 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `2.21.1` released by upstream on 2025-11-10; consumed at release | Automated tracking via `poll-cppcheck.yml`; ACQ.4 §3.1 |
| QT-014 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `docker run --user 0` works (consumer override) | Non-root default preserved; override respected by Docker runtime |
| QT-015 | 2026-08-13 | CI | `2.21.1-r1` | `sha256:632aeb9…` | PASS | `The goto statement should not be used [misra-c2012-15.1]` observed on `misra_bad.c` | INT-040 — proves MISRA rule-texts file loaded and shim addon operational |

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
| Approver | Dermot Murphy | 2026-08-13 | PR #17 merge to `main` — `AllChecksPassed` gate satisfied |

---

*End of CCD-QTR-2.21.1-r1 v1.00*
