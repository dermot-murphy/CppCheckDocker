# Process Deviation - Author, Reviewer, and Approver Are the Same Person

*Automotive SPICE(R) PAM v4.0 | PA 2.2 - Work Product Management / Deviation Record*

---

## 1. Document Identification & Control

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-DEV-001 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Approver** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **Related Process** | PA 2.2, GP 2.2.3 (Review and Adjust Work Products) |
| **Project** | CppCheckDocker |

---

## 2. Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue - closes part 1 of issue #23 (single-engineer role-collapse deviation record). |

---

## 3. Deviation Summary

| Field | Value |
|:--------------|:------------|
| **Deviation ID** | CCD-DEV-001 |
| **Problem Record** | GitHub issue #23 (ASPICE audit-readiness sweep) |
| **Severity** | SEV-3 Minor |
| **Standard Clause** | ASPICE PAM v4.0, GP 2.2.3 - Review and Adjust Work Products |
| **Affected Documents** | All ASPICE work products in `documents/aspice/` and every record file in `documents/aspice/records/` |
| **Disposition** | **Accepted with justification - permanent for the lifetime of the project as single-engineer** |

---

## 4. Non-Conformance Description

### 4.1 What the Standard Requires

ASPICE PAM v4.0, Generic Practice **GP 2.2.3 - Review and Adjust Work Products** requires that:

> "Work products are reviewed in accordance with planned arrangements to ensure that they are suitable for use."

Assessment practice under PA 2.2 - Work Product Management expects the reviewer of a work product to be **independent of the author**. The intent is that an independent perspective is applied to catch errors, omissions, and inconsistencies before a work product is approved for use. Independence means, at minimum, that the reviewer is not the same individual who authored the document.

ASPICE assessors typically look for:

- A named reviewer who is not the document author
- Evidence that the reviewer actively examined the content (e.g., review comments, a signed review record, or a separate review checklist)
- A named approver who accepts responsibility for the content after review

### 4.2 Actual State

Every ASPICE work product in `documents/aspice/` and every release record in `documents/aspice/records/` carries the following in its Document Identification header:

| Field | Value |
|:--------------|:------------|
| Author | Dermot Murphy (drafted with AI assistance from Claude) |
| Reviewer | Dermot Murphy |
| Approver (where present) | Dermot Murphy |

In every document, the **Author, Reviewer, and Approver are the same person: Dermot Murphy**.

### 4.3 Root Cause

CppCheckDocker is a single-engineer open-source project. **Dermot Murphy is the sole human team member.** There is no second employee, contractor, or independent colleague available to act as reviewer. The requirement for independent review cannot be met in a single-person organisation without engaging an external third party, which is disproportionate to the project's scope and risk profile.

---

## 5. Justification for Acceptance

### 5.1 Project Context

CppCheckDocker is a **single-engineer open-source project with one human participant: Dermot Murphy**. The project has:

- No employees, contractors, or other team members
- No organisational hierarchy (no QA department, no separate reviewer pool)
- A benign risk profile: it packages an existing static-analysis tool (`cppcheck`) into a Docker image; it does not ship safety-critical firmware, medical device software, or automotive control software
- An MIT licence: users are responsible for assessing fitness for their own use

In this context, requiring independent human review - as would be appropriate in an organisation with multiple engineers - would be structurally impossible without artificially importing a third party solely to satisfy a process checkbox.

### 5.2 Compensating Controls

Although the Author, Reviewer, and Approver are the same person, the following compensating controls provide equivalent assurance:

| Control | Description | Evidence |
|:--------|:------------|:---------|
| **Pull Request review mechanism** | Every change to a controlled work product is submitted as a GitHub Pull Request. The PR mechanism creates a structured, immutable review record: unified diff, CI status per check, timestamped approval, merge commit linked to the source branch. | GitHub PR history on `dermot-murphy/CppCheckDocker` |
| **CI gate stack** | Every PR must clear the `Lint` (pre-commit: hadolint, yamllint, whitespace, EOF, mixed-line-ending), `Verify-Version`, `Run-Integration-Tests`, and `Scan-Image` (Trivy HIGH+CRITICAL) jobs before merge is permitted. `AllChecksPassed` acts as the umbrella gate. | GitHub Actions run for each PR; branch-protection ruleset on `develop`/`main` |
| **Version-controlled audit trail** | All work product changes are committed to Git with a Conventional Commit message. The commit history is immutable and publicly auditable. Each PR body includes a per-commit binary-impact and risk table per CLAUDE.md. | GitHub repository log; PR bodies |
| **AI-assisted drafting review** | Every document is drafted or reviewed with an AI assistant (Claude), providing an independent analytical perspective before Dermot Murphy's human review. AI-generated content is critically read and edited before commit. | Commit history; PR conversations |
| **Systematic self-review against clause intent** | Before approval, Dermot Murphy explicitly reads the document in the context of the ASPICE clause it satisfies, comparing content against the corresponding GP requirements. | Issue-close evidence in each PR |

### 5.3 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| Assessor rates GP 2.2.3 as "Not Achieved" due to lack of independent reviewer | Medium | Medium | This deviation document is the formal rebuttal; compensating controls in §5.2 provide equivalent assurance |
| Document quality is lower than it would be with a second human reviewer | Low | Low | AI-assisted drafting review and CI quality gates provide independent challenge of content and correctness |
| Future team growth makes deviation obsolete | Low | None | Deviation can be retired when a second qualified reviewer joins the project; no ongoing maintenance cost |

**Residual risk: LOW** - the single-person context is transparent and documented; compensating controls are demonstrable to an assessor.

### 5.4 ASPICE Assessment Interpretation

ASPICE PAM v4.0 is written for organisational contexts with multiple team members. Automotive SPICE user groups (intacs, VDA QMC) acknowledge that process tailoring is permissible for small projects and personal-scale software, provided the intent of each GP is addressed. The intent of GP 2.2.3 is:

> "Work products are checked against their requirements before use, so that errors are found and corrected before they propagate."

The compensating controls in §5.2 collectively satisfy this intent. An assessor may award this practice **"Largely Achieved" (L)** rather than "Fully Achieved (F)" on the independence criterion, but the project accepts this outcome as proportionate.

---

## 6. Corrective Action and Retirement Clause

No change is made to the Author/Reviewer/Approver fields in any work product. **Dermot Murphy remains Author, Reviewer, and Approver on all ASPICE documents and records for the lifetime of the project as single-engineer.**

**Retirement clause:** this deviation shall be retired, and the affected documents updated to name separate Reviewer and Approver individuals, when a second qualified reviewer joins the project.

**Actions:**

| Action | Owner | Target Date | Status |
|:-------|:------|:------------|:-------|
| Create this deviation document (CCD-DEV-001) | Dermot Murphy | 2026-08-13 | Complete |
| Reference CCD-DEV-001 from CCD-SUP1-001 (QA Plan) | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Reference CCD-DEV-001 from CCD-SUP8-001 (CM Plan) §2 CI table | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Reference CCD-DEV-001 from CCD-SUP9-001 (Problem Resolution Plan) | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Reference CCD-DEV-001 from CCD-MAN3-001 §3 (single-engineer role note) | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Review deviation at 12-month anniversary or on any change to team composition | Dermot Murphy | 2027-08-13 | Pending |

---

## 7. Approval

This deviation is accepted on the basis that CppCheckDocker is a single-engineer project with no available independent reviewer, that the intent of GP 2.2.3 is satisfied by the compensating controls documented in §5.2, and that the residual risk is low.

| Role | Name | Signature | Date |
|:-----|:-----|:----------|:-----|
| Author | Dermot Murphy | Approved | 2026-08-13 |
| Reviewer | Dermot Murphy | Approved (single-engineer clause) | 2026-08-13 |
| Approver | Dermot Murphy | Approved | 2026-08-13 |

The single-engineer sign-off is itself governed by this deviation - see §5.

---

## 8. Referenced Documents

| Document ID | Title | Version |
|:------------|:------|:--------|
| CCD-DEV-002 | Process Deviation - Independent Internal QA Audit Gap | v1.00 |
| CCD-SUP1-001 | Software Quality Assurance Plan | v1.03 |
| CCD-SUP8-001 | Configuration Management Plan | v1.05 |
| CCD-SUP9-001 | Problem Resolution and Change Request Management Plan | v1.01 |
| CCD-MAN3-001 | Project Management Plan | v1.03 |
| GitHub Issue #23 | ASPICE audit-readiness sweep: add deviations for single-engineer roles and independent-audit gap, promote all documents Draft -> Released | - |
| ASPICE PAM v4.0 | Automotive SPICE Process Assessment Model, GP 2.2.3 | v4.0 |

---

*End of CCD-DEV-001 v1.00*
