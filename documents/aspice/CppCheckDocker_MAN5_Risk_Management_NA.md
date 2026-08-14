# MAN.5 Risk Management — Not Applicable (folded into MAN.3)

## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-MAN5-NA-001 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | MAN.5 — Risk Management (declared folded into MAN.3) |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue as part of the wiki tidy-up (issue #43). |

---

## 1. Declaration

A dedicated ASPICE **MAN.5 Risk Management** plan is **not issued** for the CppCheckDocker project. The MAN.5 base-practice outcomes are met by the risk-register content in [CCD-MAN3-001 §8 Risk Register](CppCheckDocker_MAN3_Project_Management_Plan) — a single, small, actively-maintained table of six risks with likelihood, impact, and mitigation columns.

## 2. Rationale

- The project scope is narrow (a single Dockerfile plus its build, test, and publish workflow).
- The team size (single engineer, formally recorded in [CCD-DEV-001](CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation)) means a separate risk-management authority cannot be distinguished from project management.
- A separate MAN.5 plan for six risks would duplicate every row from the MAN.3 §8 register without adding new content or a distinct governance loop.

## 3. Where MAN.5 obligations are satisfied

| MAN.5 Base Practice (ISO/IEC 33020) | Where satisfied |
|:------------------------------------|:----------------|
| Establish risk management scope | [CCD-MAN3-001 §8](CppCheckDocker_MAN3_Project_Management_Plan) — the risk register frames scope by listing what risks are tracked. |
| Define risk management strategies | Implicit: each register row carries its mitigation strategy inline. |
| Identify risks | [CCD-MAN3-001 §8](CppCheckDocker_MAN3_Project_Management_Plan) — six risks currently tracked (RSK-001 .. RSK-006). |
| Analyse risks | Same table — Likelihood and Impact columns. |
| Define risk treatment actions | Mitigation column. |
| Monitor risks | Register is reviewed at each ASPICE audit (see [CCD-AUD-2026-08-13](CppCheckDocker_AUD_2026-08-13_ASPICE_L2_Audit)) and refreshed whenever a new class of risk emerges. |
| Take corrective action | Handled via the project's normal issue → PR → merge flow (see [CCD-SUP9-001](CppCheckDocker_SUP9_Problem_Resolution_Plan)). |

## 4. Retirement

Retire this stub — and issue a standalone MAN.5 plan — when either of the following holds:

- The risk register grows past ~15 active items, at which point governance value from a separate plan starts to exceed the maintenance overhead;
- The team grows so that a distinct Risk Manager role is meaningful.

Neither trigger has fired in this baseline.

---

*End of CCD-MAN5-NA-001 v1.00*
