# Software Quality Assurance Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SUP1-001 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Draft |
| **Classification** | Internal |
| **ASPICE Process** | SUP.1 — Quality Assurance |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |

---

## 1. Introduction

This document defines the Software Quality Assurance (QA) plan for the CppCheckDocker project in accordance with ASPICE v4 process SUP.1. It identifies the quality activities, gates, tools, and responsibilities that ensure the delivered Docker image meets its stated requirements and process standards.

---

## 2. Quality Objectives

| Objective | Measure |
|:--------------|:------------|
| All SRS requirements are verified | 100% of Mandatory SR IDs traced to at least one test case in QTS |
| Image builds cleanly | Zero build failures in CI `Build-Image` job |
| Image runs cppcheck | `cppcheck --version` returns the pinned version string in CI |
| Image is minimal | Runtime image size ≤ 200 MB (soft target); regression flagged in review |
| Analysis functionality preserved | Sample-file integration tests detect all seeded defects |
| No secrets in image | Image content review; no `.git`, credentials, or build history in runtime layer |
| Peer review on all changes | Every PR has at least one review approval before merge |
| Traceability maintained | All SR IDs appear in traceability matrix (CCD-RTM-001) |
| Build completes in time | End-to-end image build (cold cache) completes within 10 minutes |
| Integration tests complete in time | Full integration test suite completes within 3 minutes |

---

## 3. Quality Gates

Quality is enforced via CI pipeline gates. A gate failure blocks merge.

| Gate | CI Job | Tool | Status | Failure Action |
|:--------------|:------------|:------------|:------------|:---------------|
| Build | `Build-Image` | `docker build` | **Active** | Fix Dockerfile error |
| Version smoke test | `Verify-Version` | `docker run … --version` | **Active** | Fix build or version pin |
| Integration tests | `Run-Integration-Tests` | shell test harness against sample inputs | **Active** | Fix regression |
| Dockerfile lint | `Lint-Dockerfile` | `hadolint` | **Planned** | Fix lint warning |
| Image vulnerability scan | `Scan-Image` | `trivy` or `docker scout` | **Planned** | Fix or accept CVE with justification |
| Image size regression | `Check-Image-Size` | `docker image inspect` + threshold check | **Planned** | Investigate size increase |
| All checks | `AllChecksPassed` | Aggregator | **Active** | All above active gates must pass |

Gates marked **Planned** are defined in this document but not yet wired into the workflow. They are included to define the target state and will be activated as the CI infrastructure matures.

---

## 4. Code Review Process

All changes are reviewed before merge:

1. Developer opens a Pull Request on GitHub against `develop`
2. CI pipeline runs all gates automatically
3. At least one reviewer approves the PR (reviewing Dockerfile correctness, security, and design conformance)
4. Reviewer checks that:
   - New functionality is covered by at least one integration test
   - SRS requirements affected by the change are identified in the PR description
   - No new secrets, credentials, or personal data added to the image
5. PR is merged only when all CI gates pass and approval is recorded

Peer review records are retained as part of the GitHub PR history, which is version-controlled.

---

## 5. Static Analysis

Two static-analysis tools apply to this project. The deliverable itself is a Dockerfile (not C/C++), so MISRA-style code analysis does not apply.

| Tool | Purpose | Scope | Configuration | Execution | Status |
|:--------------|:------------|:------------|:-------------|:------------|:------------|
| **hadolint** | Dockerfile best-practice linting | `Dockerfile` | `.hadolint.yaml` (default rules) | CI: `Lint-Dockerfile` | **Planned** |
| **trivy** (or Docker Scout) | Container vulnerability scan | Final runtime image | Default vulnerability database | CI: `Scan-Image` | **Planned** |

### 5.1 hadolint (Planned)

hadolint will run against the `Dockerfile` on every push. It will check for:
- Deprecated instructions
- Missing `--no-install-recommends` on apt-get calls
- Unpinned base images or packages where pinning is required
- Layer bloat (multiple `RUN` calls that should be merged)

### 5.2 trivy / Docker Scout (Planned)

The final runtime image will be scanned for known CVEs. Findings at severity **CRITICAL** or **HIGH** will block merge unless a documented risk acceptance is attached to the PR. **MEDIUM** and below are advisory.

### 5.3 Note on cppcheck itself

The cppcheck binary shipped in the image *is* a static analysis tool, but is treated as a third-party COTS component of the deliverable — not as a QA tool applied to this project's own source. Its correctness is assumed from upstream qualification; the CppCheckDocker tests verify only that the image invokes it correctly and returns the expected outputs.

---

## 6. Test Adequacy

### 6.1 Test Classification

The CI pipeline implements a single-tier test model — the deliverable is small enough that a smoke/component split adds no value.

| Tier | Environment | CI Job | Time Budget | Status |
|:--------------|:------------|:------------|:-------------|:------------|
| All tests | GitHub Actions ubuntu-latest | `Build-Image` + `Verify-Version` + `Run-Integration-Tests` | < 15 minutes total | **Active** |

All tests run on every push and every pull request. A failure on `develop` or `main` blocks merge.

### 6.2 Adequacy Criteria

| Level | Criterion |
|:--------------|:------------|
| Unit (image sanity) | All Mandatory SR IDs classified as "image structure" have a UVT case |
| Integration (image + sample input) | All Mandatory SR IDs classified as "analysis behaviour" have an INT case |
| Qualification | All Mandatory SR IDs have at least one QT case |

The Master Traceability Matrix (CCD-RTM-001) is reviewed at each release to confirm all Mandatory requirements are covered.

---

## 7. Non-Conformance Handling

Non-conformances (test failures, process deviations, requirement violations) are tracked using the process defined in CCD-SUP9-001 (Problem Resolution and Change Request Management Plan).

Each non-conformance is assigned:
- A unique Problem Report (PR) identifier
- A severity classification (Critical / Major / Minor)
- An owner and target resolution date
- A verification step to confirm fix

---

## 8. QA Records

The following records are retained as objective evidence of QA activities:

| Record | Location | Retained By |
|:--------------|:------------|:------------|
| CI build logs | GitHub Actions artefacts | Automatic (30-day retention) |
| Integration test output | `Integration_Test_Output` artefact | CI |
| Image manifest and digest | `docker inspect` output logged in CI | CI |
| hadolint report (planned) | `Hadolint_Report` artefact | CI |
| Vulnerability scan report (planned) | `Image_Scan_Report` artefact | CI |
| Peer review approvals | GitHub PR history | GitHub |
| Qualification test records | `documents/aspice/records/` | Manual |
| Problem reports | `documents/reviews/` | Manual |

---

## 9. ASPICE Process Compliance

This plan addresses the following ASPICE v4 Level 2 PA attributes for SUP.1:

| PA | Attribute | Evidence |
|:--------------|:------------|:------------|
| PA 1.1 | Process performance | QA activities performed and recorded in CI |
| PA 2.1 | Performance management | QA plan defines activities; CI enforces gates |
| PA 2.2 | Work product management | QA records under version control in Git |

---

*End of CCD-SUP1-001 v1.00*
