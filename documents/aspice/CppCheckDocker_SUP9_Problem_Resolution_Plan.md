# Problem Resolution and Change Request Management Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SUP9-001 |
| **Version** | v1.02 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SUP.9 — Problem Resolution Management / SUP.10 — Change Request Management |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added §5 Process Deviation Records format; referenced CCD-DEV-001 and CCD-DEV-002; promote Draft -> Released (issue #23). |
| v1.02 | 2026-08-13 | Dermot Murphy | §2.4 and §3.5 reconciled with actual practice: GitHub Issues + PRs are the authoritative record; markdown-under-`documents/reviews/` retained only for cases where prose is required (issue #31, closes audit finding FIND-C). |

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

The authoritative store for problem reports is **GitHub Issues** on this repository. Each problem is opened as an Issue with:

- The `bug` label for defects observed in the deliverable or its CI
- The `hotfix` label if the fix must land on `main` outside the normal `develop`-first flow (see the Workflow section of CLAUDE.md)
- A branch name of `feature/BUGFIX-<issue-number>-<abstract>` (or `hotfix/HOTFIX-<n>-<abstract>`)
- An implementing PR that references the issue and carries the fix

The GitHub Issue thread captures the description, discussion, severity classification, resolution, and closure timestamp. The implementing PR captures the diff, CI verification, and reviewer sign-off. Issue and PR together form the immutable, version-controlled record.

**Markdown records under `documents/reviews/YYYY-MM-DD_PR-NNN_<short-title>.md` are retained only when prose analysis outgrows an Issue thread** — for example, a root-cause investigation with diagrams, cross-project impact write-ups, or precursor material to a deviation record. Small routine problems are not required to have a markdown record; the GitHub Issue is sufficient.

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

The authoritative store for change requests is **GitHub Issues** on this repository. Each CR is opened as an Issue with:

- The `change-request` label (or `feature` for new features)
- A branch name of `feature/CR-<issue-number>-<abstract>` (or `feature/FEATURE-<n>-<abstract>`) per the Workflow section of CLAUDE.md
- An implementing PR that references the issue, carries the diff, and includes the per-commit binary-impact and risk table
- The `pending-merge` label added once the implementing PR merges to `develop`; the Issue closes automatically when the change reaches `main` (see [[project-issues-close-on-main-merge]] and CLAUDE.md convention)

The GitHub Issue thread captures the proposal, impact assessment, decision, and closure. The implementing PR captures the diff and CI verification. Issue and PR together form the immutable, version-controlled record.

**Markdown records under `documents/reviews/YYYY-MM-DD_CR-NNN_<short-title>.md` are retained only when prose expression is required** — for example, a multi-page impact analysis, an architecture-decision record, or a precursor to a deviation record. Small routine CRs are not required to have a markdown record; the GitHub Issue plus the PR body is sufficient.

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

## 5. Process Deviation Records

A **process deviation record** documents a formally accepted departure from the ASPICE PAM v4.0 process model. Deviations are used when a required practice cannot be executed as written but the intent is met through compensating controls, or when a required practice is scheduled for time-boxed corrective action rather than immediate implementation.

Process deviations are treated as controlled work products (see [CCD-SUP8-001](CppCheckDocker_SUP8_CM_Plan.md) §2, CI-012) and follow the file naming pattern:

```
CppCheckDocker_DEV<NNN>_<Short_Title>_Deviation.md
```

### 5.1 Required Content

Every deviation record shall include:

- **Document Identification & Control** (Deviation ID, version, author, reviewer, approver, status, related ASPICE PA/GP clause)
- **Document Control** (revision history)
- **Deviation Summary** (severity, standard clause, affected documents/process, disposition)
- **Non-Conformance Description** (what the standard requires, actual state, root cause)
- **Justification for Acceptance** (project context, compensating controls, risk assessment, ASPICE interpretation)
- **Corrective Action and Retirement Clause** (actions with owner and target date; explicit conditions under which the deviation is retired)
- **Approval** (author, reviewer, approver sign-off - subject to CCD-DEV-001 while single-engineer)
- **Referenced Documents** (with correct current version numbers)

### 5.2 Dispositions

| Disposition | Meaning |
|:------------|:--------|
| Accepted with justification | Compensating controls satisfy clause intent; deviation is permanent unless a retirement condition is met |
| Accepted with time-boxed corrective action | Compensating controls apply until a deadline by which the required practice must be executed; retire when the corrective action closes |
| Rejected | Deviation is not accepted; the required practice must be executed as written |

### 5.3 Current Deviations

| Deviation ID | Title | Disposition | Retirement Condition |
|:-------------|:------|:------------|:---------------------|
| [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md) | Author, Reviewer, and Approver Are the Same Person | Accepted with justification | A second qualified reviewer joins the project |
| [CCD-DEV-002](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md) | No Independent Internal QA Audit Yet Conducted Against the Baseline | Accepted with time-boxed corrective action (target 2026-11-11) | First audit report filed under `documents/aspice/audits/` with all findings dispositioned |

Both deviations were opened as part of GitHub issue #23 (ASPICE audit-readiness sweep).

---

*End of CCD-SUP9-001 v1.02*
