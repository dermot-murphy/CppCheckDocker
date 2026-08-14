# PA2 Capability Records

## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-PA2-001 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | All processes — Capability Level 2 record |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue as part of the wiki tidy-up (issue #43). Extracts the per-process PA 1.1 / PA 2.1 / PA 2.2 ratings from CCD-AUD-2026-08-13 into a dedicated capability-record page so an ASPICE assessor can see the CL2 posture on one screen without walking the full audit report. |

---

## 1. Scope

This page is the **authoritative source of the current per-process capability ratings** for the CppCheckDocker project. Ratings are drawn from the internal ASPICE audit executed on 2026-08-13 ([CCD-AUD-2026-08-13-L2](CppCheckDocker_AUD_2026-08-13_ASPICE_L2_Audit)). The audit report holds the full rationale; this page condenses the numbers.

Standing deviations that shape every rating:

- **[CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation)** — Author = Reviewer = Approver = Dermot Murphy. Applied to every PA 2.2 rating: **GP 2.2.3** (Review and Adjust Work Products) is met with compensating controls only, so every PA 2.2 caps at **L**.
- **[CCD-DEV-002](CppCheckDocker_DEV002_Independent_QA_Audit_Deviation)** — No independent internal QA audit executed against the baseline. Retired by CCD-AUD-2026-08-13 executing that audit.

Rating scale (per ISO/IEC 33020):

| Symbol | Meaning |
|:------:|:--------|
| **N** | Not achieved (0-15%) |
| **P** | Partially achieved (16-50%) |
| **L** | Largely achieved (51-85%) |
| **F** | Fully achieved (86-100%) |

Level 2 is **achieved** when both PA 1.1 and PA 2.x are rated **at least L** across every process in scope.

---

## 2. Per-process ratings (from CCD-AUD-2026-08-13-L2 §7)

Ratings are captured as of the audit date. Where a Blocker finding was open at audit time, the retirement path is noted in the last column.

| Process | Document | PA 1.1 Process performance | PA 2.1 Performance management | PA 2.2 Work product management | Open findings at audit |
|:--------|:---------|:-------------------------:|:-----------------------------:|:------------------------------:|:-----------------------|
| MAN.3 Project Management | [CCD-MAN3-001](CppCheckDocker_MAN3_Project_Management_Plan) | F | F | L | None |
| ACQ.4 Supplier Monitoring | [CCD-ACQ4-001](CppCheckDocker_ACQ4_Supplier_Monitoring_Plan) | F | F | L | None |
| SPL.2 Software Release | [CCD-SPL2-001](CppCheckDocker_SPL2_Software_Release_Plan) | F | F | L | None |
| SUP.1 Quality Assurance | [CCD-SUP1-001](CppCheckDocker_SUP1_Quality_Assurance_Plan) | L | L | L | FIND-A (SR-060 gate) — closed by #29 to develop; FIND-B (hadolint label) — closed by #30 to develop |
| SUP.8 Configuration Management | [CCD-SUP8-001](CppCheckDocker_SUP8_CM_Plan) | F | F | L | FIND-D (digest audit) — closed by #32 to develop |
| SUP.9 / SUP.10 Problem & Change Management | [CCD-SUP9-001](CppCheckDocker_SUP9_Problem_Resolution_Plan) | L | F | L | FIND-C (`documents/reviews/`) — closed by #31 to develop |
| SWE.1 Software Requirements | [CCD-SWE1-001](CppCheckDocker_SWE1_SW_Requirements) | F | F | L | None |
| SWE.2 Software Architecture | [CCD-SWE2-001](CppCheckDocker_SWE2_SW_Architecture) | F | F | L | None |
| SWE.3 Detailed Design | [CCD-SWE3-001](CppCheckDocker_SWE3_Detailed_Design) | F | F | L | None |
| SWE.4 Unit Verification | [CCD-SWE4-001](CppCheckDocker_SWE4_Unit_Verification) | L | L | L | FIND-E (phantom job) — closed by #33 to develop; FIND-F (SA table) — closed by #34 to develop |
| SWE.5 Integration Test | [CCD-SWE5-001](CppCheckDocker_SWE5_Integration_Test) | F | F | L | None |
| SWE.6 Qualification Test | [CCD-SWE6-001](CppCheckDocker_SWE6_Qualification_Test) | F | F | L | None |

Processes declared **not applicable** (see the linked stub for the deliberate exclusion):

- [SYS.* System Engineering](CppCheckDocker_SYS_System_Engineering_NA)
- [MAN.5 Risk Management](CppCheckDocker_MAN5_Risk_Management_NA) — obligations satisfied by CCD-MAN3-001 §8.

## 3. Level 2 overall

**Level 2 is achieved** on every in-scope process: PA 1.1 and PA 2.x are all at **L or better** across the twelve process areas above. Open Blocker findings do not lower the rating below L; they are corrective actions filed as follow-up issues #29-#34 and tracked to `develop` via the standard gitflow.

---

## 4. Refresh cadence

This page is regenerated whenever an audit closes. The next scheduled internal audit is at the release-candidate cut for the following annual baseline (see [CCD-SUP1-001 §7](CppCheckDocker_SUP1_Quality_Assurance_Plan)); ad-hoc audits may be triggered by any scope change that adds or removes a process area.

---

*End of CCD-PA2-001 v1.00*
