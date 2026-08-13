# Problem Resolution and Change Request Management Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SUP9-001 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Draft |
| **Classification** | Internal |
| **ASPICE Process** | SUP.9 — Problem Resolution Management / SUP.10 — Change Request Management |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |

---

## 1. Introduction

This document defines the processes for Problem Resolution Management (SUP.9) and Change Request Management (SUP.10) for the CppCheckDocker project.

- **Problem Resolution:** covers defects, test failures, and anomalies discovered during development, integration, or downstream use of the image
- **Change Request Management:** covers proposed changes to requirements, architecture, design, or any other controlled work product

---

## 2. Problem Resolution Process (SUP.9)

### 2.1 Problem Classification

| Severity | Definition | Response Time |
|:--------------|:------------|:---------------|
| Critical | Image fails to build; image runs but `cppcheck` immediately crashes; published image contains secrets | Same day |
| Major | Cppcheck fails to detect a documented defect class; integration test fails; new CVE at HIGH/CRITICAL surfaced | Within 3 business days |
| Minor | Warning-level lint finding, image size regression, documentation error | Next release cycle |

### 2.2 Problem Report Fields

| Field | Description |
|:--------------|:-------------|
| PR ID | Unique identifier, format: `PR-YYYYMMDD-NNN` |
| Date raised | Date problem was identified |
| Raised by | Name of person who identified the problem |
| Severity | Critical / Major / Minor |
| Description | Clear description of the problem, steps to reproduce |
| Image tag | Image tag (or digest) under which the problem was observed |
| Cppcheck version | Value of `CPPCHECK_VERSION` in the affected build |
| Base image | Value of `UBUNTU_VERSION` in the affected build |
| Status | Open / In Progress / Resolved / Closed |
| Root cause | Analysis of why the problem occurred |
| Resolution | Description of fix applied |
| Verified by | Name of person who verified the fix |
| Fix commit | Git commit hash of the fix |

### 2.3 Problem Report Lifecycle

```
Identified → Open
    │
    ▼
Assigned to engineer → In Progress
    │
    ├─► Root cause analysis
    ├─► Fix implemented (feature/** or hotfix/** branch)
    ├─► Test added to prevent regression
    ├─► CI passes
    ├─► PR merged
    │
    ▼
Fix verified by original reporter → Resolved
    │
    ▼
Closed (at next release)
```

### 2.4 Problem Report Storage

Problem reports are stored as Markdown files in `documents/reviews/` with filename format:
```
YYYY-MM-DD_PR-NNN_<short-title>.md
```

### 2.5 Regression Prevention

For every Critical or Major problem:
- A new unit test (UVT) or integration test (INT) must be added to the test suite that would have detected the problem
- The test must pass in CI before the PR is merged
- The SRS is reviewed to determine whether the problem indicates a missing or incorrect requirement; if so, the SRS is updated

---

## 3. Change Request Management Process (SUP.10)

### 3.1 Change Request Triggers

A Change Request (CR) is raised for:
- Proposed cppcheck version bump (new upstream release)
- Proposed base image change (e.g., Ubuntu 24.04 → 26.04)
- Proposed changes to build options (adding/removing PCRE, match compiler, addons)
- Changes to image entrypoint, user, working directory, or exposed environment
- Migration to a different container registry
- Any customer or stakeholder request that alters the deliverable

### 3.2 Change Request Fields

| Field | Description |
|:--------------|:-------------|
| CR ID | Unique identifier, format: `CR-YYYYMMDD-NNN` |
| Date raised | Date CR was created |
| Raised by | Name of requester |
| Description | Clear description of the proposed change |
| Affected documents | List of ASPICE documents requiring update |
| Affected SR IDs | Software requirements affected or to be added |
| Impact assessment | Estimated effort, risk, and test implications |
| Status | Proposed / Approved / Rejected / Implemented / Closed |
| Decision | Rationale for approval or rejection |
| Approved by | Name of approver |
| Implementation PR | GitHub PR number implementing the change |

### 3.3 Change Request Lifecycle

```
Proposed
    │
    ▼
Impact assessment (affected documents, SRs, tests, effort)
    │
    ▼
Decision: Approved / Rejected
    │ (if Approved)
    ▼
Affected ASPICE documents updated (SRS version incremented)
    │
    ▼
Implementation via feature branch + PR
    │
    ▼
Test cases updated/added
    │
    ▼
CI passes → merged
    │
    ▼
Traceability matrix (CCD-RTM-001) updated
    │
    ▼
Closed
```

### 3.4 Document Update Policy

When a Change Request is approved:
- The SRS must be updated before implementation begins
- Architecture and design documents must be updated in the same PR as the implementation
- Document version numbers are incremented and the Document Control table is updated
- The traceability matrix must reflect any new or modified SR IDs

### 3.5 Change Request Storage

Change requests are stored as Markdown files in `documents/reviews/` with filename format:
```
YYYY-MM-DD_CR-NNN_<short-title>.md
```

### 3.6 Upstream Cppcheck Version Bumps

A cppcheck version bump is the most common CR for this project. The abbreviated flow is:

1. Update `ARG CPPCHECK_VERSION=...` in the `Dockerfile`
2. Update the SRS (§ Version) and CMP (§ Image Version) if the new version changes behaviour observable through the requirements
3. Run the full test suite in CI
4. Publish a new image tag with revision `-r1`
5. Update the traceability matrix if any SR IDs changed

No new CR document is required for a routine patch bump if no requirement or interface changes; the PR description references the upstream release notes and this is retained via GitHub PR history.

---

## 4. Impact on ASPICE Document Set

Any change that modifies a software requirement must trigger a review of the impact chain:

```
SRS (CCD-SWE1-001)
    │
    ▼
SADD (CCD-SWE2-001)
    │
    ▼
SDDD (CCD-SWE3-001)
    │
    ▼
UVP (CCD-SWE4-001)
ITP (CCD-SWE5-001)
QTS (CCD-SWE6-001)
    │
    ▼
Traceability Matrix (CCD-RTM-001)
```

Each affected document must be updated with an incremented version number and a new row in its Document Control table.

---

*End of CCD-SUP9-001 v1.00*
