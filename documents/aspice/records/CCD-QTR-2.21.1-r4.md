# Qualification Test Record
## CppCheckDocker — Release v2.21.1-r4

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-QTR-2.21.1-r4 |
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
| v1.00 | 2026-08-14 | Dermot Murphy | Initial issue per #54 — qualification test record for release v2.21.1-r4 |

---

## 1. Scope

Executes every qualification test case defined in [CCD-SWE6-001](../CppCheckDocker_SWE6_Qualification_Test.md) §3 against the released image and records the outcome. The runtime image is content-identical to r3, but per-release QT execution is still required by SPL.2, and r4 adds the first automated SUP.8 §7 configuration audit — captured here as additional pass evidence.

Related SVD: [`CCD-SVD-2.21.1-r4`](CCD-SVD-2.21.1-r4.md).

---

## 2. Test Environment

| Field | Value |
|:--------------|:------------|
| **Image Tag** | `ghcr.io/dermot-murphy/cppcheckdocker:2.21.1-r4` |
| **Image Digest** | `sha256:e83c25f55c4a8a39e421e3f13c3fb1c26c3d2898daf0958f875dd38d56ec9e25` |
| **Test Host** | GitHub Actions `ubuntu-latest` runner (per CCD-SWE6-001 §2) |
| **Test Date (UTC)** | 2026-08-14 |
| **Tester** | Dermot Murphy (via automated CI on merge of PR #50) |
| **Evidence Trail** | CI run <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31786463201> |

The `Run-Integration-Tests` job executes `test/integration/run.sh`, which drives the full INT case set on the built image. Because the CI pipeline uses a single-tier test model per CCD-SUP1-001 §6.1, every QT case is verified either directly by that harness or by the `Verify-Version` / `Scan-Image` / `Lint` / `Publish-Wiki` jobs on the same run.

**New for r4:** the `Release` job's `Configuration audit` step (SUP.8 §7, CR-32) provides additional automated evidence for QT-001 (version smoke on the published image) and cross-registry manifest identity.

---

## 3. Test Results

| Test ID | Date | Tester | Image Tag | Image Digest | Result | Actual Value | Notes |
|:--------------|:------------|:------------|:------------|:-------------|:------------|:-------------|:------------|
| QT-001 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `Cppcheck 2.21.1` | `Verify-Version` job; also confirmed by SUP.8 §7 version smoke on the published image |
| QT-002 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | ENTRYPOINT accepts args from GHA step container context | INT-002, INT-011 |
| QT-003 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `docker run -v` mount analysis returns findings | INT-010/INT-011/INT-012 |
| QT-004 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `arrayIndexOutOfBounds` on `buggy.c`; exit 1 with `--error-exitcode=1` | INT-011 |
| QT-005 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | No findings on `clean.c`; exit 0 | INT-010 |
| QT-006 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `<errors>` root element present in `--xml` output | INT-013 |
| QT-007 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `WORKDIR /work`, `USER cppcheck` verified | Dockerfile lines 81–83 |
| QT-008 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | 129,101,911 bytes (~130 MB) — within SR-060 200 MB threshold | `Build-Image` job SR-060 gate (new CR-29 automation) |
| QT-009 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | OCI labels present | Dockerfile lines 47–50 |
| QT-010 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | No `.git` directory in runtime layer | Multi-stage build; `.dockerignore` |
| QT-011 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | No `gcc`/`g++`/`cmake`/`ninja` in runtime image | Runtime stage installs only `libpcre3`, `python3` |
| QT-012 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `python3 --version` returns Python 3.12.x | Verified by INT-040 MISRA addon |
| QT-013 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `2.21.1` still the current upstream stable at release | ACQ.4 §3.1; `poll-cppcheck.yml` |
| QT-014 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `docker run --user 0` works (consumer override) | Non-root default preserved |
| QT-015 | 2026-08-14 | CI | `2.21.1-r4` | `sha256:e83c25f…` | PASS | `The goto statement should not be used [misra-c2012-15.1]` on `misra_bad.c` | INT-040 |

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

## 5. Additional Automated Audit Evidence (New for r4)

Introduced by CR-32 in the `Release` job:

| Audit | Result | Evidence |
|:------|:-------|:---------|
| Digest round-trip: GHCR digest = DockerHub digest for tag `2.21.1-r4` | PASS | `Configuration audit (digest round-trip) passed: both registries resolve sha256:e83c25f55c4a8a39e421e3f13c3fb1c26c3d2898daf0958f875dd38d56ec9e25 for tag 2.21.1-r4.` |
| Version smoke on published image (post-push, from GHCR) | PASS | `Configuration audit (version smoke on published image) passed.` |

This is the **first release** where these two audits have been executed automatically — CCD-SUP8-001 §7 previously described the obligation without a CI mechanism (FIND-D). CR-32 closed that gap.

---

## 6. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-14 | Git commit authorship |
| Reviewer | Dermot Murphy | 2026-08-14 | Self-review under CCD-MAN3-001 §3 single-engineer clause |
| Approver | Dermot Murphy | 2026-08-14 | PR #50 merge to `main` — `AllChecksPassed` gate satisfied |

---

*End of CCD-QTR-2.21.1-r4 v1.00*
