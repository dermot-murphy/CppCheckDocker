# Project Management Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-MAN3-001 |
| **Version** | v1.03 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | MAN.3 — Project Management |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added WBS-15 (Software Release process) and WBS-16 (Software Version Description) for the SPL.2 process area. |
| v1.02 | 2026-08-13 | Dermot Murphy | Added WBS-17 (Supplier Monitoring) for the ACQ.4 process area covering cppcheck upstream, Ubuntu base image, and MISRA rule-texts as COTS suppliers. |
| v1.03 | 2026-08-13 | Dermot Murphy | §3 single-engineer note now cites CCD-DEV-001 as the formal deviation record; promote Draft -> Released (issue #23). |

---

## 1. Introduction

This document is the Project Management Plan (PMP) for the CppCheckDocker project in accordance with ASPICE v4 process MAN.3. It defines the scope, work breakdown, roles, resource plan, schedule framework, and monitoring approach for the delivery of an Ubuntu-based Docker image that packages the latest release of the cppcheck static analysis tool for use by other projects in GitHub Actions CI pipelines.

---

## 2. Project Scope

**In scope:**
- Dockerfile that builds the latest tagged release of cppcheck from source on Ubuntu LTS
- Multi-stage build producing a runtime image with the compiled `cppcheck` binary, addons directory, and cfg files
- Version pinning mechanism via build argument for reproducibility
- Test harness that exercises the built image against sample C/C++ inputs
- GitHub Actions workflow that builds and (optionally) publishes the image to a container registry
- All ASPICE SWE process work products (SRS, SADD, SDDD, UVP, ITP, QTS)
- All ASPICE supporting process work products (CMP, QAPLAN, PMP, PRCMP)

**Out of scope:**
- Modifications to the upstream cppcheck source code
- GUI (cppcheck-gui) — not required for CI use cases
- Windows or macOS container variants
- Wrapping other static analysis tools (Helix QAC, Coverity, clang-tidy)
- Providing prebuilt binaries outside a container

---

## 3. Roles and Responsibilities

| Role | Name | Responsibility |
|:--------------|:------------|:---------------|
| Lead Engineer / PM | Dermot Murphy | Dockerfile authorship, ASPICE documentation, QA oversight |
| Reviewer | Dermot Murphy | Code review, document review |
| Approver (release) | Dermot Murphy | Image publication sign-off |

*Note: For a single-engineer team, the Lead Engineer fulfils all roles. For ASPICE Level 2 capability, evidence of self-review and process execution is required. Independent review is recommended as the team grows.*

The role-collapse condition (Author = Reviewer = Approver = Dermot Murphy) is formally captured as [CCD-DEV-001 - Author, Reviewer, and Approver Are the Same Person](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md). That deviation documents the compensating controls (PR review, CI gate stack, AI-assisted drafting review, systematic self-review against clause intent) and sets a retirement clause: retire when a second qualified reviewer joins the project. RSK-005 in §8 is the corresponding risk-register entry.

---

## 4. Work Breakdown Structure

| WBS ID | Work Package | ASPICE Process | Deliverable |
|:--------------|:-------------|:----------------|:-------------|
| WBS-01 | Requirements Analysis | SWE.1 | CCD-SWE1-001 SRS |
| WBS-02 | Architectural Design | SWE.2 | CCD-SWE2-001 SADD |
| WBS-03 | Detailed Design | SWE.3 | CCD-SWE3-001 SDDD |
| WBS-04 | Unit Verification | SWE.4 | CCD-SWE4-001 UVP + test results |
| WBS-05 | Integration Testing | SWE.5 | CCD-SWE5-001 ITP + test results |
| WBS-06 | Qualification Testing | SWE.6 | CCD-SWE6-001 QTS + test records |
| WBS-07 | Configuration Management | SUP.8 | CCD-SUP8-001 CMP |
| WBS-08 | Quality Assurance | SUP.1 | CCD-SUP1-001 QAPLAN |
| WBS-09 | Project Management | MAN.3 | CCD-MAN3-001 PMP (this document) |
| WBS-10 | Problem/Change Management | SUP.9/10 | CCD-SUP9-001 PRCMP |
| WBS-11 | Traceability Matrix | All | CCD-RTM-001 Traceability Matrix |
| WBS-12 | Dockerfile Implementation | SWE.3 | `Dockerfile`, `.dockerignore` |
| WBS-13 | CI/CD Pipeline | SUP.8 | `.github/workflows/` |
| WBS-14 | Test Assets | SWE.4/5 | `test/` sample inputs and expected outputs |
| WBS-15 | Software Release | SPL.2 | CCD-SPL2-001 Software Release Plan |
| WBS-16 | Software Version Description | SPL.2 | CCD-SVD-001 SVD template; populated `CCD-SVD-<tag>.md` per release under `documents/aspice/records/` |
| WBS-17 | Supplier Monitoring | ACQ.4 | CCD-ACQ4-001 Supplier Monitoring Plan |

---

## 5. Lifecycle Model

The CppCheckDocker project uses an iterative development lifecycle aligned with the git branching strategy:

```
Requirement Analysis → Architectural Design → Detailed Design
        ↓
Feature Development (feature/** branches)
        ↓
Integration (develop branch) → CI gates
        ↓
Release (main branch) → GitHub Release + published container image
```

Each significant change (upstream cppcheck version bump, base-image update, new build option) begins with an SRS review and ends with the corresponding test cases passing in CI.

---

## 6. Schedule Framework

The project operates on a continuous delivery model driven by upstream cppcheck releases. There is no fixed sprint cadence. Milestones are defined as follows:

| Milestone | Description | Completion Criterion |
|:--------------|:-------------|:---------------------|
| M1 | ASPICE documentation baseline v1.00 | All 11 documents issued at v1.00 |
| M2 | Dockerfile builds and image runs `cppcheck --version` | UVT-001..UVT-005 pass in CI |
| M3 | Integration test suite complete | All INT test cases executed on sample inputs |
| M4 | Qualification test complete | All QT test cases executed; QT records filed |
| M5 | First tagged image release | All M1–M4 complete; image published with semantic version tag |

Subsequent releases follow the same pattern with a shorter cycle, triggered by upstream cppcheck releases.

---

## 7. Estimation

Project complexity is estimated at:
- **Source items:** 1 Dockerfile, 1 `.dockerignore`, 1 GitHub Actions workflow, ~5 test scripts
- **Lines of Dockerfile:** ~50 SLOC excluding comments
- **Unit test cases:** ~10 defined in this baseline
- **Integration test cases:** ~8 defined in this baseline
- **Qualification test cases:** ~6 defined in this baseline

---

## 8. Risk Register

| Risk ID | Description | Likelihood | Impact | Mitigation |
|:--------------|:-------------|:------------|:------------|:------------|
| RSK-001 | Upstream cppcheck build system change breaks the Dockerfile | Medium | Medium | Pin `CPPCHECK_VERSION` via build ARG; smoke-test on each bump before publishing |
| RSK-002 | Ubuntu base image removes a required build package | Low | Medium | Pin `UBUNTU_VERSION` via build ARG; retest before major-version bump |
| RSK-003 | Image size grows past a reasonable size (currently ~130 MB) | Low | Low | Multi-stage build keeps runtime layer minimal; monitor size in UVT |
| RSK-004 | Published image consumed by third-party workflows breaks after a change | Medium | High | Immutable semantic-version tags; `latest` tag is best-effort |
| RSK-005 | Single-engineer team — knowledge bus factor | High | High | Documentation-first approach; ASPICE documents encode design rationale |
| RSK-006 | Docker Hub rate limits during CI pulls of base image | Low | Low | Consider mirroring base image if it becomes an issue |

---

## 9. Monitoring and Control

Progress is monitored through:
- **CI dashboard:** GitHub Actions status on every push provides real-time build and test health
- **GitHub Issues:** Used to track open defects and feature work
- **PR review history:** Provides audit trail of changes and decisions
- **ASPICE document versions:** Updated when significant requirements or design changes occur
- **Traceability matrix reviews:** Performed before each release to confirm coverage
- **Image size and layer count:** Reported in each build log; regression against previous release triggers review

---

## 10. Interfaces

| Interface | Party | Communication Method |
|:--------------|:------------|:---------------------|
| Upstream cppcheck project | `danmar/cppcheck` GitHub repository | Release tag polling; GitHub tag reference in build ARG |
| Consumer projects | Any repository that pulls the published image | Container registry (GitHub Container Registry `ghcr.io` recommended) |
| Ubuntu base image | Canonical | `ubuntu:<version>` Docker Hub tag |

---

*End of CCD-MAN3-001 v1.03*
