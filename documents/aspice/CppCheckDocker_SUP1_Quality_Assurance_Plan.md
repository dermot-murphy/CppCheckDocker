# Software Quality Assurance Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SUP1-001 |
| **Version** | v1.05 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SUP.1 — Quality Assurance |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Move hadolint (§5.1) from Planned to Active; add pre-commit local + CI enforcement (issue #5) |
| v1.02 | 2026-08-13 | Dermot Murphy | Move vulnerability scan (§5.2) from Planned to Active; document `.trivyignore` process (issue #6) |
| v1.03 | 2026-08-13 | Dermot Murphy | Add §11 referencing CCD-DEV-001 (single-engineer role collapse) and CCD-DEV-002 (independent QA audit gap); promote Draft -> Released (issue #23). |
| v1.04 | 2026-08-13 | Dermot Murphy | §3 image-size-regression gate moved from Planned to Active; implemented as a fail-gated step inside the `Build-Image` job (issue #29, closes audit finding FIND-A). |
| v1.05 | 2026-08-13 | Dermot Murphy | §3 image-size-regression gate row extended to cite the per-merge trend chart (`gh-pages/image_size_trend.svg`) produced by the new `Track-Image-Size` job (issue #42). |

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
| Dockerfile lint | `Lint` (pre-commit) | `hadolint` | **Active** | Fix lint warning |
| YAML lint | `Lint` (pre-commit) | `yamllint` | **Active** | Fix lint warning |
| Image vulnerability scan | `Scan-Image` | `trivy` | **Active** | Fix or accept CVE with justification in `.trivyignore` |
| Image size regression (SR-060, <= 200 MB) | `Build-Image` (step `Fail on image size regression (SR-060)`) for the hard gate; `Track-Image-Size` for the trend | `docker image inspect --format '{{.Size}}'` + numeric threshold in bytes; per-merge history in `image_size_history.csv` on the `gh-pages` branch; chart in `image_size_trend.svg` embedded in `README.md` | **Active** | Investigate size increase; suppress with justification only via a temporary threshold bump in the workflow, reviewed at next release. Trend chart shows drift toward the ceiling long before the gate fires. |
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
| **hadolint** | Dockerfile best-practice linting | `Dockerfile` | `.hadolint.yaml` | pre-commit (local + CI `Lint` job) | **Active** |
| **yamllint** | YAML syntax/style linting | `*.yml`, `*.yaml` | `.yamllint.yaml` | pre-commit (local + CI `Lint` job) | **Active** |
| **trivy** | Container vulnerability scan | Final runtime image | `.trivyignore` (suppression file) | CI: `Scan-Image` | **Active** |

### 5.1 hadolint (Active)

hadolint runs against the `Dockerfile` via pre-commit on every commit and in the CI `Lint` job on every push and PR. It checks for:
- Deprecated instructions
- Missing `--no-install-recommends` on apt-get calls
- Unpinned base images or packages where pinning is required
- Layer bloat (multiple `RUN` calls that should be merged)

The rule `DL3008` (pin apt-get versions) is intentionally suppressed in `.hadolint.yaml` because this project relies on the Ubuntu base image for CVE-driven package updates. Pinning at Dockerfile level would defeat that mechanism; see §5.2 for the compensating vulnerability-scan gate.

### 5.2 trivy (Active)

The final runtime image is scanned for known CVEs by the CI `Scan-Image` job using [`aquasecurity/trivy-action`](https://github.com/aquasecurity/trivy-action). The job runs two passes against the built image:

1. **Informational** — all severities (`LOW,MEDIUM,HIGH,CRITICAL`) reported as a table and uploaded as the `Image_Scan_Report` artefact (90-day retention).
2. **Gating** — `HIGH,CRITICAL` only, `exit-code=1`. A finding at these severities fails the job and blocks merge.

**MEDIUM** and below are advisory and do not block.

CVE-level suppressions live in `.trivyignore` at repo root. Each entry must carry an inline comment stating the rationale, an expiry date (or upstream-fix reference), and the reviewer. Suppressions are reviewed at each release per CCD-SPL2-001 §4.

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
| hadolint / yamllint report | CI `Lint` job log | GitHub Actions |
| Vulnerability scan report | `Image_Scan_Report` artefact (90-day retention) | CI |
| Peer review approvals | GitHub PR history | GitHub |
| Qualification test records | `documents/aspice/records/` | Manual |
| Problem reports | `documents/reviews/` | Manual |

---

## 9. ASPICE Process Compliance

This plan addresses the following ASPICE v4 Level 2 PA attributes for SUP.1:

| PA | Attribute | Evidence |
|:--------------|:------------|:------------|
| PA 1.1 | Process performance | QA activities performed and recorded in CI |
| PA 2.1 | Performance management | QA plan defines activities; CI enforces gates. **Deviation:** no independent internal QA audit has yet been conducted against the baseline - see [CCD-DEV-002](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md), first audit scheduled by 2026-11-11. |
| PA 2.2 | Work product management | QA records under version control in Git. **Deviation:** Author, Reviewer, and Approver are the same person (Dermot Murphy) - see [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md); compensating controls (PR review, CI gate stack, AI-assisted drafting review) apply. |

---

## 10. Referenced Documents

| Document ID | Title | Version |
|:------------|:------|:--------|
| CCD-DEV-001 | Process Deviation - Author, Reviewer, and Approver Are the Same Person | v1.00 |
| CCD-DEV-002 | Process Deviation - No Independent Internal QA Audit Yet Conducted | v1.00 |
| CCD-SUP8-001 | Configuration Management Plan | v1.05 |
| CCD-SUP9-001 | Problem Resolution and Change Request Management Plan | v1.01 |
| CCD-SPL2-001 | Software Release Plan | v1.02 |
| CCD-RTM-001 | Master Traceability Matrix | v1.05 |

---

## 11. Process Deviations

The following formal deviations apply to this QA plan and are attached as controlled work products:

- **[CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md) - Author, Reviewer, and Approver Are the Same Person.** Applies to every QA record in §8 and every ASPICE work product referenced by this plan. Disposition: Accepted with justification, permanent for the lifetime of the project as single-engineer. Retirement: when a second qualified reviewer joins.
- **[CCD-DEV-002](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md) - No Independent Internal QA Audit Yet Conducted Against the Baseline.** Applies to the audit obligation implicit in this plan. Disposition: Accepted with time-boxed corrective action - first audit target 2026-11-11. Retirement: on filing of the first audit report under `documents/aspice/audits/` with all findings dispositioned.

Both deviations were opened as part of GitHub issue #23 (ASPICE audit-readiness sweep).

---

*End of CCD-SUP1-001 v1.04*
