# Process Deviation - No Independent Internal QA Audit Yet Conducted Against the Baseline

*Automotive SPICE(R) PAM v4.0 | PA 2.1 on SUP.1 - Quality Assurance / Deviation Record*

---

## 1. Document Identification & Control

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-DEV-002 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Approver** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **Related Process** | PA 2.1 on SUP.1 - Quality Assurance |
| **Project** | CppCheckDocker |

---

## 2. Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue - closes part 2 of issue #23 (independent QA audit gap deviation record). |

---

## 3. Deviation Summary

| Field | Value |
|:--------------|:------------|
| **Deviation ID** | CCD-DEV-002 |
| **Problem Record** | GitHub issue #23 (ASPICE audit-readiness sweep) |
| **Severity** | SEV-2 Moderate |
| **Standard Clause** | ASPICE PAM v4.0, PA 2.1 on SUP.1 - Quality Assurance |
| **Affected Process** | SUP.1 (as defined in CCD-SUP1-001) |
| **Disposition** | **Accepted with time-boxed corrective action - first independent audit to be conducted within 90 days of first release** |

The single-engineer constraint that shapes the "independent" wording in the corrective action is separately documented in [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md). This deviation records the audit-execution gap independently.

---

## 4. Non-Conformance Description

### 4.1 What the Standard Requires

ASPICE PAM v4.0, Process Attribute **PA 2.1 - Performance Management** on process **SUP.1 - Quality Assurance**, together with the SUP.1 base practices, requires that:

> "Quality assurance is planned and performed."
> "Compliance of work products and processes with applicable requirements is objectively evaluated."
> "Quality assurance activities and results are communicated to those affected, and issues are tracked to closure."

Assessment practice under PA 2.1 on SUP.1 expects that the QA function periodically **executes** the audit obligations defined in the QA plan and produces auditable records of those executions - not merely that the plan exists. A well-written plan with no evidence of execution is scored as "Not Achieved" or "Partially Achieved" on PA 2.1.

ASPICE assessors typically look for:

- A QA plan naming the audit obligation (present: CCD-SUP1-001)
- Dated, signed audit records showing that the obligation was actually met
- Non-conformance findings, corrective actions, and closure evidence linked back to the plan
- A schedule for future audits and evidence that previous scheduled audits were held

### 4.2 Actual State

- CCD-SUP1-001 (Quality Assurance Plan) is released and defines the QA audit obligation.
- **No independent internal QA audit has yet been conducted against the baseline.**
- No records exist under `documents/aspice/audits/`.
- The first two releases (`v2.21.1-r1`, `v2.21.1-r2`) were made without a prior QA audit.

### 4.3 Root Cause

CppCheckDocker is a single-engineer project (see [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md)). The QA-plan obligation was authored during initial process definition, but no audit run has yet been scheduled or executed. Compensating CI controls provide continuous quality checking, which masked the missing formal-audit record until the ASPICE audit-readiness sweep (issue #23) surfaced it.

---

## 5. Justification for Acceptance

### 5.1 Project Context

CppCheckDocker is a single-engineer open-source project packaging an existing static-analysis tool into a Docker image. It has no safety-critical claims, no customer contract requiring a scheduled QA audit, and no organisational QA function separate from the engineer.

### 5.2 Compensating Controls

Until the first formal QA audit is conducted (target 2026-11-11), the following compensating controls provide continuous quality assurance:

| Control | Description | Evidence |
|:--------|:------------|:---------|
| **CI gate stack acts as continuous QA** | `Lint` (pre-commit: hadolint, yamllint, whitespace/EOF/EOL), `Verify-Version`, `Run-Integration-Tests`, `Scan-Image` (Trivy HIGH+CRITICAL fail-gate), and `AllChecksPassed` umbrella job run on every push and every PR. Each is a QA evaluation of a defined check against a defined criterion, with a durable log. | GitHub Actions run history |
| **Pull Request review as per-change audit** | Every change to the baseline is submitted as a PR with a per-commit binary-impact and risk table per CLAUDE.md, then reviewed and merged. The PR body records the reasoning; the CI status records the objective evaluation; the merge commit records the approval. | GitHub PR history |
| **SPL.2 sign-off gate on every release** | CCD-SPL2-001 §4 entry criteria and §6 exit criteria explicitly enumerate the QA-relevant checks that must pass before a release is cut. The `Release` job in `.github/workflows/build.yml` will not fire unless the CI gate stack is green. | build.yml `Release` job `needs:` list; SPL2 §§4-6 |
| **Configuration audit obligations** | CCD-SUP8-001 §7 defines a configuration audit before each production release, checking that the published digest matches the CI-produced digest for the release commit. | SUP8-001 §7 |
| **Trivy scan report as continuous vulnerability QA** | The `Scan-Image` job produces an artefact `Image_Scan_Report` (retention 90 days) covering all severities, and a separate fail-gate on HIGH/CRITICAL. Both are QA activities executed on every push. | Trivy report artefacts on GitHub Actions runs |

### 5.3 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|:-----|:-----------|:-------|:-----------|
| Assessor rates PA 2.1 on SUP.1 as "Not Achieved" due to missing audit records | Medium | Medium | Time-boxed corrective action in §6 (first audit within 90 days); compensating controls in §5.2 provide continuous QA in the interim; this deviation is the formal audit trail entry until the first audit report exists |
| First audit is missed or slips past target date (2026-11-11) | Medium | Low | Follow-up issue booked; retirement clause requires an audit record to be filed before this deviation can be closed |
| Audit surfaces a systemic gap that requires re-work of released images | Low | Medium | Compensating CI controls have been executing continuously since first release, reducing the probability that a systemic gap has survived undetected; SPL.2 §8 provides a withdrawal procedure if needed |

**Residual risk: LOW-MEDIUM** - the compensating controls are strong, but the lack of a formal audit record is a visible audit-trail gap that must be closed on schedule.

---

## 6. Corrective Action

**Disposition: Accepted with time-boxed corrective action.**

**Actions:**

| Action | Owner | Target Date | Status |
|:-------|:------|:------------|:-------|
| Create this deviation document (CCD-DEV-002) | Dermot Murphy | 2026-08-13 | Complete |
| Reference CCD-DEV-002 from CCD-SUP1-001 (QA Plan) | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Reference CCD-DEV-002 from CCD-SUP8-001 (CM Plan) §2 CI table | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Reference CCD-DEV-002 from CCD-SUP9-001 (Problem Resolution Plan) - deviation record format | Dermot Murphy | 2026-08-13 | Complete (this PR) |
| Open a follow-up GitHub issue booking the first independent internal QA audit | Dermot Murphy | 2026-08-20 | Pending (see §6.1) |
| Conduct the first independent internal QA audit against the CCD-SUP1-001 baseline | Dermot Murphy | **2026-11-11** (90 days from first release) | Pending |
| File the audit report under `documents/aspice/audits/CCD-AUD-YYYY-MM-DD.md` | Dermot Murphy | Same commit as audit | Pending |
| Retire this deviation once the first audit record exists and any findings are dispositioned | Dermot Murphy | On audit closure | Pending |

### 6.1 Follow-up issue

A follow-up GitHub issue shall be opened titled "Conduct first independent internal QA audit against CCD-SUP1-001 baseline (target 2026-11-11)". The issue shall reference this deviation and shall be labelled `change-request` per CLAUDE.md workflow rules. The audit report shall land as `documents/aspice/audits/CCD-AUD-<date>.md` in a `feature/CR-<n>-*` branch.

### 6.2 Retirement clause

This deviation is retired when:

1. The first audit report exists under `documents/aspice/audits/`.
2. Any non-conformance findings have been dispositioned (fixed, waived, or scheduled).
3. The next-audit date is entered in CCD-SUP1-001 and in this deviation as a superseding record.

The single-engineer clause in [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md) applies to the audit itself - "independent" is interpreted per that deviation's compensating-control framework for as long as the project remains single-engineer.

---

## 7. Approval

This deviation is accepted on the basis that a time-boxed corrective action is in place, that compensating CI controls are executing continuously as documented in §5.2, and that the residual risk is LOW-MEDIUM until the first audit closes.

| Role | Name | Signature | Date |
|:-----|:-----|:----------|:-----|
| Author | Dermot Murphy | Approved | 2026-08-13 |
| Reviewer | Dermot Murphy | Approved (single-engineer clause per CCD-DEV-001) | 2026-08-13 |
| Approver | Dermot Murphy | Approved | 2026-08-13 |

---

## 8. Referenced Documents

| Document ID | Title | Version |
|:------------|:------|:--------|
| CCD-DEV-001 | Process Deviation - Author, Reviewer, and Approver Are the Same Person | v1.00 |
| CCD-SUP1-001 | Software Quality Assurance Plan | v1.03 |
| CCD-SUP8-001 | Configuration Management Plan | v1.05 |
| CCD-SUP9-001 | Problem Resolution and Change Request Management Plan | v1.01 |
| CCD-SPL2-001 | Software Release Plan | v1.02 |
| GitHub Issue #23 | ASPICE audit-readiness sweep | - |
| ASPICE PAM v4.0 | Automotive SPICE Process Assessment Model, PA 2.1 on SUP.1 | v4.0 |

---

*End of CCD-DEV-002 v1.00*
