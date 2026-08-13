# System Engineering — Not Applicable

## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SYS-NA-001 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SYS.* — System Engineering (declared out of scope) |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue as part of the wiki tidy-up (issue #43). |

---

## 1. Declaration

The ASPICE v4 **System Engineering** process group (SYS.1 Requirements Elicitation, SYS.2 System Requirements Analysis, SYS.3 System Architectural Design, SYS.4 System Integration and Integration Test, SYS.5 System Qualification Test) is **not applicable** to the CppCheckDocker project.

## 2. Rationale

CppCheckDocker delivers a **software-only** artefact: a Docker image bundling the [cppcheck](https://github.com/danmar/cppcheck) static analyser plus the MISRA C:2012 rule-texts file. The deliverable has:

- No hardware component;
- No system-level integration with other software or hardware subsystems;
- No system-level stakeholder requirements distinct from the software requirements captured in [CCD-SWE1-001](CppCheckDocker_SWE1_SW_Requirements);
- No system architecture separate from the software architecture in [CCD-SWE2-001](CppCheckDocker_SWE2_SW_Architecture).

There is no separate "system" layer above the software: the software **is** the deliverable. All stakeholder-facing needs are captured directly as Software Requirements in SWE.1 and traced end-to-end via [CCD-RTM-001](CppCheckDocker_RTM_Master_Traceability_Matrix).

## 3. Deliberate exclusion

This document exists so an ASPICE assessor sees a **deliberate declaration** rather than a gap. Any future scope change that introduces a system-level component (for example, a Kubernetes operator, a plugin architecture with a discovery protocol, or hardware-in-the-loop testing) requires re-evaluating the SYS.* applicability and creating the corresponding SYS work products.

## 4. Retirement

Retire this stub when SYS.* is brought into scope. Until then, no revision or re-issue is required beyond the initial version.

---

*End of CCD-SYS-NA-001 v1.00*
