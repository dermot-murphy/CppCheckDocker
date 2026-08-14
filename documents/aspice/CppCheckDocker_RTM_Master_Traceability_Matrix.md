# Master Traceability Matrix
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-RTM-001 |
| **Version** | v1.07 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | All SWE — Full Traceability |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added FEAT-011 (MISRA C:2012 support) with SR-028/SR-029; UVT-060/UVT-061; INT-040; QT-015. Updated coverage summary. |
| v1.02 | 2026-08-13 | Dermot Murphy | Extended traceability key to include CCD-SPL2-001 (Release Plan) and CCD-SVD-001 (SVD template). |
| v1.03 | 2026-08-13 | Dermot Murphy | Extended traceability key to include CCD-ACQ4-001 (Supplier Monitoring Plan) with the three suppliers SUP-001..SUP-003. |
| v1.04 | 2026-08-13 | Dermot Murphy | Updated NFR-002 traceability: `Scan-Image` gate now Active via trivy (issue #6). |
| v1.05 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |
| v1.06 | 2026-08-13 | Dermot Murphy | §3a NFR-001 row: CI Gate corrected from stale `Lint-Dockerfile (planned)` to `Lint (pre-commit)` (Active) - hadolint has been Active since CCD-SUP1-001 v1.01 / issue #5. Issue #30, closes audit finding FIND-B. |
| v1.07 | 2026-08-13 | Dermot Murphy | SR-060 verification: cite the per-merge image-size trend chart (`gh-pages/image_size_trend.svg`, produced by `Track-Image-Size`) as ancillary evidence alongside UVT-050 / QT-008 (issue #42). |

---

## 1. Introduction

This document is the Master Traceability Matrix for the CppCheckDocker project. It provides full vertical traceability from product features through software requirements, architectural elements, detailed design sections, and test cases at every level (unit, integration, qualification).

This matrix is the primary evidence for ASPICE v4 SWE process traceability requirements and must be kept current with every change to the document set.

---

## 2. Traceability Key

| Identifier Prefix | Document | Description |
|:-------------------|:------------|:-------------|
| `FEAT-NNN` | CCD-SWE1-001 §5 | Product feature requirement |
| `SR-NNN` | CCD-SWE1-001 §6–11 | Software requirement |
| `NFR-NNN` | CCD-SWE1-001 §12 | Non-functional requirement |
| `ARC-XXX-NNN` | CCD-SWE2-001 | Architectural element |
| `§X.Y` | CCD-SWE3-001 | Detailed design section |
| `UVT-NNN` | CCD-SWE4-001 | Unit verification test |
| `INT-NNN` | CCD-SWE5-001 | Integration test |
| `QT-NNN` | CCD-SWE6-001 | Qualification test |
| `CCD-SPL2-001` | Standalone | Software Release Plan (SPL.2) |
| `CCD-SVD-001` | Template | Software Version Description template; instances at `documents/aspice/records/CCD-SVD-<tag>.md` |
| `CCD-ACQ4-001` | Standalone | Supplier Monitoring Plan (ACQ.4) |
| `SUP-NNN` | CCD-ACQ4-001 §3 | Supplier register entry (SUP-001 cppcheck, SUP-002 Ubuntu, SUP-003 MISRA) |

---

## 3. Feature to Software Requirement Traceability

| Feature ID | Feature Description | Derived SR IDs |
|:--------------|:---------------------|:---------------|
| FEAT-001 | Working `cppcheck` executable inside Ubuntu container | SR-001, SR-003, SR-005, SR-007, SR-020, SR-022, SR-062 |
| FEAT-002 | Latest cppcheck version available at build time | SR-004, SR-023, SR-051 |
| FEAT-003 | Runnable on GHA hosted Linux runners | (Environmental — verified by CI job success) |
| FEAT-004 | Analysis of C/C++ mounted via bind mount | SR-027, SR-032, SR-033, SR-034, SR-035, SR-063 |
| FEAT-005 | Reproducible image build | SR-001, SR-004, SR-010, SR-050, SR-053, SR-054 |
| FEAT-006 | Publishable to `ghcr.io` with immutable tags | SR-044, SR-052, SR-053, SR-061 |
| FEAT-007 | Usable as GHA step container | SR-021, SR-036 |
| FEAT-008 | Non-root by default | SR-030, SR-042, SR-043 |
| FEAT-009 | No build tools, source, credentials in runtime image | SR-002, SR-009, SR-040, SR-041, SR-060 |
| FEAT-010 | Standard cppcheck addons and cfg files present | SR-005, SR-006, SR-007, SR-024, SR-025, SR-026 |
| FEAT-011 | MISRA C:2012 support with bundled rule-texts | SR-028, SR-029 |

---

## 3a. Non-Functional Requirements Traceability

Non-functional requirements (SRS §12) are cross-cutting obligations that apply to the entire deliverable. They do not trace to individual features but are verified through static analysis, CI gates, and design review.

| NFR ID | Non-Functional Requirement Summary | Verification Method | CI Gate / Evidence |
|:--------------|:-----------------------------------|:--------------------|:--------------------|
| NFR-001 | Dockerfile conforms to hadolint default rule set | Static analysis | `Lint (pre-commit)` (Active; see CCD-SUP1-001 §3 and §5.1) |
| NFR-002 | No CRITICAL/HIGH CVEs in published image | Vulnerability scan | `Scan-Image` (trivy, active) |
| NFR-003 | Base image tag pinned via ARG (not `:latest`) | Review | PR review checklist; verified by inspecting `Dockerfile` |
| NFR-004 | `--no-install-recommends` used on all apt installs | Review | PR review checklist; hadolint DL3015 |
| NFR-005 | apt lists removed in same `RUN` layer | Review | PR review checklist; hadolint DL3009 |
| NFR-006 | Layer count kept low via combined `RUN` where sensible | Review | PR review checklist |
| NFR-007 | Review checklist executed at each PR | Process | PR reviewer confirmation |
| NFR-008 | OCI `LABEL` metadata present | Test | UVT-034; QT-009 |
| NFR-009 | All components under permissive/copyleft OSS licences compatible with redistribution | Review | Manual review; SPDX identifiers in labels |

**Ancillary evidence for SR-060 (Runtime image size ≤ 200 MB):** the `Track-Image-Size` CI job (see `.github/workflows/build.yml`) appends a row to `image_size_history.csv` on the `gh-pages` branch on every merge to `develop` or `main` and re-renders `image_size_trend.svg`. The chart is embedded in `README.md` and draws the 200 MiB SR-060 ceiling. This is a monitoring artefact; the hard verification remains UVT-050 (per-build gate) and QT-008 (release check).

---

## 4. Full Requirement Traceability

For each Software Requirement (SR), the following table lists its source feature, architectural elements, detailed design section, and every test case that verifies it.

| SR ID | Requirement Summary | FEAT | Architecture | Detailed Design | UVT | INT | QT |
|:---------|:---------------------|:-----|:--------------|:-----------------|:----|:----|:---|
| SR-001 | Ubuntu LTS base | FEAT-001, FEAT-005 | ARC-IMG-001, ARC-BLD-002, ARC-RUN-002 | §3.1, §3.2, §3.3 | UVT-001 | — | — |
| SR-002 | Multi-stage build | FEAT-009 | ARC-IMG-001, ARC-IMG-002 | §3.2, §3.3 | UVT-002 | — | — |
| SR-003 | Builder apt packages | FEAT-001 | ARC-BLD-001 | §3.2 | UVT-003 | — | — |
| SR-004 | Cppcheck source at pinned tag | FEAT-002, FEAT-005 | ARC-BLD-002 | §3.2 | UVT-004 | — | — |
| SR-005 | CMake build options | FEAT-001, FEAT-010 | ARC-BLD-003 | §3.2 | UVT-005 | — | — |
| SR-006 | Install prefix /opt/cppcheck | FEAT-010 | ARC-BLD-004 | §3.2 | UVT-006 | — | — |
| SR-007 | Runtime apt packages (libpcre3, python3) | FEAT-001, FEAT-010 | ARC-RUN-001 | §3.3 | UVT-007 | — | — |
| SR-008 | COPY --from=builder | FEAT-009 | ARC-RUN-002 | §3.3 | UVT-008 | — | — |
| SR-009 | No build tools in runtime | FEAT-009 | ARC-RUN-003 | §3.3, §3.4 | UVT-009 | — | QT-011 |
| SR-010 | .dockerignore correct | FEAT-005, FEAT-009 | ARC-IMG-003 | §4 | UVT-010 | — | — |
| SR-020 | cppcheck on PATH | FEAT-001 | ARC-RUN-004 | §3.3 | UVT-024 | INT-001 | — |
| SR-021 | ENTRYPOINT = cppcheck | FEAT-007 | ARC-RUN-005 | §3.3 | UVT-022 | INT-002 | — |
| SR-022 | CMD = --help | FEAT-001 | ARC-RUN-006 | §3.3 | UVT-023 | INT-003 | — |
| SR-023 | --version returns pinned string | FEAT-002 | ARC-BLD-002, ARC-RUN-004 | §3.2 (smoke) | UVT-025 | — | QT-001 |
| SR-024 | cfg files present | FEAT-010 | ARC-BLD-004 | §3.2 | UVT-026 | INT-004 | — |
| SR-025 | platforms XML present | FEAT-010 | ARC-BLD-004 | §3.2 | UVT-027 | INT-005 | — |
| SR-026 | python3 at runtime | FEAT-010 | ARC-RUN-001 | §3.3 | UVT-028 | INT-006 | QT-012 |
| SR-027 | --enable=all works | FEAT-004, FEAT-010 | ARC-RUN-007 | §6.1 (test harness) | — | INT-007, INT-023 | QT-004, QT-005 |
| SR-028 | MISRA rule-texts file bundled | FEAT-011 | ARC-RUN-010 | §3.5 | UVT-060 | — | QT-015 |
| SR-029 | misra-c2012 shim addon | FEAT-011 | ARC-RUN-010 | §3.5 | UVT-061 | INT-040 | QT-015 |
| SR-030 | Non-root user `cppcheck` | FEAT-008 | ARC-RUN-008 | §3.3 | UVT-020 | — | QT-007 |
| SR-031 | WORKDIR = /work | FEAT-004, FEAT-008 | ARC-RUN-008 | §3.3 | UVT-021 | — | — |
| SR-032 | Analyse mounted /work | FEAT-004 | ARC-RUN-009 | §6.1 | — | INT-010, INT-014, INT-015 | QT-003 |
| SR-033 | Non-zero exit with --error-exitcode | FEAT-004 | ARC-RUN-007 | §7.2 | — | INT-011, INT-032 | QT-004 |
| SR-034 | Zero exit without --error-exitcode | FEAT-004 | ARC-RUN-007 | §7.2 | — | INT-012 | QT-005 |
| SR-035 | XML / SARIF output | FEAT-004 | ARC-RUN-007 | §7.2 | — | INT-013 | QT-006 |
| SR-036 | Usable as GHA step container | FEAT-007 | ARC-INT-001 | §5 | — | INT-030, INT-031, INT-032 | QT-002 |
| SR-040 | No secrets | FEAT-009 | ARC-IMG-003, ARC-RUN-003 | §4, §7.1 | UVT-030 | — | — |
| SR-041 | No .git in image | FEAT-009 | ARC-RUN-003 | §3.3, §4 | UVT-031 | — | QT-010 |
| SR-042 | Non-root default (with override support) | FEAT-008 | ARC-RUN-005, ARC-RUN-008 | §3.3 | UVT-020, UVT-032 | INT-025 | QT-007, QT-014 |
| SR-043 | No exposed network ports | FEAT-008 | ARC-RUN-005 | §3.3 | UVT-033 | — | — |
| SR-044 | OCI labels | FEAT-006 | ARC-IMG-004 | §3.3 (LABEL) | UVT-034 | — | QT-009 |
| SR-050 | CPPCHECK_VERSION / UBUNTU_VERSION ARGs | FEAT-005 | ARC-BLD-002 | §3.1 | UVT-004, UVT-040 | — | — |
| SR-051 | Default CPPCHECK_VERSION current at release | FEAT-002, FEAT-005 | ARC-BLD-002 | §3.1 | UVT-004 | — | — |
| SR-052 | Image tag format `<version>-r<rev>` | FEAT-006 | ARC-INT-001 | §5.5 | — | — | QT-001 |
| SR-053 | Digest recorded in GitHub Release notes | FEAT-005, FEAT-006 | ARC-INT-001 | §5.5 | — | — | (Release process; verified by CM audit) |
| SR-054 | Reproducible builds (bit-identical) | FEAT-005 | ARC-BLD-002 | §3.1, §3.2 | UVT-041 (Desirable) | — | — |
| SR-060 | Runtime image size ≤ 200 MB | FEAT-009 | ARC-RUN-002 | §3.4 | UVT-050 | — | QT-008 |
| SR-061 | Cold build ≤ 10 min | FEAT-006 | ARC-BLD-003 | §5.2 (CI infrastructure) | — | INT-020 | — |
| SR-062 | `--version` ≤ 3 seconds | FEAT-001, FEAT-007 | ARC-RUN-004 | §3.2 (smoke) | — | INT-021 | QT-013 |
| SR-063 | Integration suite ≤ 3 min | FEAT-004 | ARC-INT-002 | §6.1 | — | INT-022 | — |

---

## 5. Test Case Reverse Traceability

For each test case, the requirements it verifies.

### 5.1 Unit Verification Tests

| UVT ID | SR IDs Covered |
|:--------------|:---------------|
| UVT-001 | SR-001 |
| UVT-002 | SR-002 |
| UVT-003 | SR-003 |
| UVT-004 | SR-004, SR-050, SR-051 |
| UVT-005 | SR-005 |
| UVT-006 | SR-006 |
| UVT-007 | SR-007 |
| UVT-008 | SR-008 |
| UVT-009 | SR-009 |
| UVT-010 | SR-010 |
| UVT-020 | SR-030, SR-042 |
| UVT-021 | SR-031 |
| UVT-022 | SR-021 |
| UVT-023 | SR-022 |
| UVT-024 | SR-020 |
| UVT-025 | SR-023 |
| UVT-026 | SR-024 |
| UVT-027 | SR-025 |
| UVT-028 | SR-026 |
| UVT-030 | SR-040 |
| UVT-031 | SR-041 |
| UVT-032 | SR-042 |
| UVT-033 | SR-043 |
| UVT-034 | SR-044, NFR-008 |
| UVT-040 | SR-050 |
| UVT-041 | SR-054 |
| UVT-050 | SR-060 |
| UVT-060 | SR-028 |
| UVT-061 | SR-029 |

### 5.2 Integration Tests

| INT ID | SR IDs Covered |
|:--------------|:---------------|
| INT-001 | SR-020 |
| INT-002 | SR-021 |
| INT-003 | SR-022 |
| INT-004 | SR-024 |
| INT-005 | SR-025 |
| INT-006 | SR-026 |
| INT-007 | SR-027 |
| INT-010 | SR-032 |
| INT-011 | SR-033 |
| INT-012 | SR-034 |
| INT-013 | SR-035 |
| INT-014 | SR-032 |
| INT-015 | SR-027, SR-032 |
| INT-020 | SR-061 |
| INT-021 | SR-062 |
| INT-022 | SR-063 |
| INT-023 | SR-027 |
| INT-024 | SR-026 |
| INT-025 | SR-042 |
| INT-030 | SR-036 |
| INT-031 | SR-036 |
| INT-032 | SR-033, SR-036 |
| INT-040 | SR-028, SR-029 |

### 5.3 Qualification Tests

| QT ID | SR IDs Covered |
|:--------------|:---------------|
| QT-001 | SR-023, SR-052 |
| QT-002 | SR-036 |
| QT-003 | SR-032 |
| QT-004 | SR-027, SR-033 |
| QT-005 | SR-027, SR-034 |
| QT-006 | SR-035 |
| QT-007 | SR-030, SR-042 |
| QT-008 | SR-060 |
| QT-009 | SR-044, NFR-008 |
| QT-010 | SR-041 |
| QT-011 | SR-009 |
| QT-012 | SR-026 |
| QT-013 | SR-062 |
| QT-014 | SR-042 |
| QT-015 | SR-028, SR-029 |

---

## 6. Coverage Summary

| Category | Total SRs | Verified by ≥ 1 Test | Coverage % |
|:--------------|:---------|:-------|:--------|
| Image build (SR-001..SR-010) | 10 | 10 | 100% |
| Runtime metadata (SR-020..SR-029) | 10 | 10 | 100% |
| Runtime behaviour (SR-030..SR-036) | 7 | 7 | 100% |
| Security (SR-040..SR-044) | 5 | 5 | 100% |
| Reproducibility / versioning (SR-050..SR-054) | 5 | 4 (SR-053 verified by process, not test) | 80% test / 100% process |
| Performance and size (SR-060..SR-063) | 4 | 4 | 100% |
| **Total Mandatory Functional SRs** | **40** | **39** | **97.5% test / 100% including process verification** |

Mandatory NFRs (NFR-001..NFR-009) are verified by analysis and review as documented in §3a; they are not counted in the test-coverage percentage.

---

## 7. Change Log Cross-Reference

When any SR is added, modified, or retired, this matrix must be updated in the same PR that changes the SRS. Failure to update the matrix is a merge blocker per SUP.1 §2 and SUP.9 §3.4.

---

*End of CCD-RTM-001 v1.07*
