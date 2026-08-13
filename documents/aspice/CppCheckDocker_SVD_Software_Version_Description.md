# Software Version Description
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SVD-001 (template) |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Draft |
| **Classification** | Internal |
| **ASPICE Process** | SPL.2 — Software Release |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial template issue |

---

## 1. Purpose

This document is the Software Version Description (SVD) **template** for the CppCheckDocker project. It is produced in accordance with ASPICE v4 process SPL.2 (Software Release).

For every release, a **populated instance** of this template is committed to `documents/aspice/records/CCD-SVD-<tag>.md`. The populated instance is the definitive record of what was released, from what source, containing which third-party components, verified against which test evidence.

**Parent document:** CCD-SPL2-001 (Software Release Plan)

---

## 2. How to Use This Template

For each release:

1. Copy this file to `documents/aspice/records/CCD-SVD-<cppcheck-version>-r<revision>.md`
2. Populate every `{{placeholder}}` in §3–§9
3. Delete this §2 (How to Use) and §1 (Purpose) from the populated instance
4. Change the header **Document ID** to `CCD-SVD-<tag>`, **Version** to `v1.00`, and **Status** to `Released`
5. Commit as part of the release PR
6. Link the committed file from the GitHub Release body

---

## 3. Release Identification

| Field | Value |
|:--------------|:------------|
| **Release Tag** | `{{v2.21.1-r1}}` |
| **Release Date (UTC)** | `{{YYYY-MM-DD HH:MM}}` |
| **Release Type** | `{{Minor / Patch / Hotfix / Major}}` |
| **Released By** | `{{Author name}}` |
| **Release Method** | `{{Automated CI / Manual fallback}}` |

---

## 4. Source Provenance

| Field | Value |
|:--------------|:------------|
| **Git Repository** | `github.com/{{owner}}/CppCheckDocker` |
| **Git Branch (source)** | `main` |
| **Git Commit SHA** | `{{full 40-char SHA}}` |
| **Git Tag** | `v{{tag}}` |
| **GitHub Release URL** | `{{https://github.com/.../releases/tag/v...}}` |

---

## 5. Published Artefacts

### 5.1 Container Image

| Field | Value |
|:--------------|:------------|
| **Primary Registry** | `ghcr.io/{{owner}}/cppcheckdocker` |
| **Immutable Tag** | `{{cppcheck-version}}-r{{revision}}` |
| **Image Digest (sha256)** | `{{sha256:0123...}}` |
| **Image Size (uncompressed)** | `{{130 MB}}` |
| **Platform** | `linux/amd64` |
| **Also Tagged As** | `{{latest, 2.21}}` (mutable convenience tags — same digest at time of release) |

### 5.2 Secondary Registry (if applicable)

| Field | Value |
|:--------------|:------------|
| **Registry** | `{{docker.io/<owner>/cppcheckdocker or "N/A"}}` |
| **Digest (sha256)** | `{{sha256:... or "N/A"}}` |

---

## 6. Configuration and Build Parameters

| Field | Value |
|:--------------|:------------|
| **`CPPCHECK_VERSION` build ARG** | `{{2.21.1}}` |
| **`UBUNTU_VERSION` build ARG** | `{{24.04}}` |
| **CMake options** | `-DCMAKE_BUILD_TYPE=Release -DHAVE_RULES=ON -DUSE_MATCHCOMPILER=ON` |
| **BuildKit frontend** | `docker/dockerfile:1.7` |
| **Reproducibility** | Bit-identical builds expected across CI runs from the same commit (SR-054 Desirable) |

---

## 7. Third-Party Components

| Component | Version | Licence | Source | Modified? |
|:--------------|:--------|:--------|:-------|:----------|
| cppcheck | `{{2.21.1}}` | GPL-3.0-or-later | `github.com/danmar/cppcheck` @ tag `{{2.21.1}}` | No |
| Ubuntu (base image) | `{{24.04}}` | Ubuntu FSA + component licences | Docker Hub `library/ubuntu` @ tag `{{24.04}}` | No |
| libpcre3 (runtime) | Ubuntu-provided | BSD-3-Clause | apt `libpcre3` from Ubuntu {{24.04}} archive | No |
| python3 (runtime) | Ubuntu-provided | PSF-2.0 | apt `python3` from Ubuntu {{24.04}} archive | No |
| MISRA C:2012 rule-texts | v1.00 (2024-04-17 release) | CC BY-NC-ND 4.0 | © MISRA Consortium Limited, redistributed at `documents/assets/misra_c_2012_for_cppcheck.txt` | No |

---

## 8. Verification Evidence

| Test Set | Reference | Result | Location |
|:--------------|:------------|:-------|:---------|
| Unit verification tests | CCD-SWE4-001 §4 | `{{PASS / FAIL}}` | GitHub Actions run: `{{URL}}` |
| Integration tests | CCD-SWE5-001 §3 | `{{PASS / FAIL}}` | GitHub Actions run: `{{URL}}` |
| Qualification tests | CCD-SWE6-001 §3 | `{{PASS / FAIL}}` | `documents/aspice/records/CCD-QTR-{{tag}}.md` |
| Version smoke test | `Verify-Version` CI job | `{{PASS / FAIL}}` | GitHub Actions run: `{{URL}}` |
| Aggregator gate | `AllChecksPassed` CI job | `{{PASS / FAIL}}` | GitHub Actions run: `{{URL}}` |
| Wiki publication | `Publish-Wiki` CI job | `{{PASS / FAIL}}` | GitHub Actions run: `{{URL}}` |

---

## 9. Changes Since Previous Release

| Category | Description |
|:--------------|:-------------|
| **Previous release tag** | `{{v2.21.0-r3 or "N/A - first release"}}` |
| **Upstream cppcheck delta** | `{{2.21.0 → 2.21.1: bug fixes only — link to upstream release notes}}` |
| **Base image delta** | `{{None / Ubuntu 24.04.1 → 24.04.2}}` |
| **Dockerfile delta** | `{{Summary of any changes; N/A if none}}` |
| **New/updated SRs (from CCD-SWE1-001)** | `{{list SR IDs or "N/A"}}` |
| **New/updated test cases** | `{{list UVT/INT/QT IDs or "N/A"}}` |
| **Withdrawn releases** | `{{None or list of withdrawn tags with reason}}` |

---

## 10. Known Issues at Release Time

| Issue ID | Severity | Summary | Mitigation |
|:--------------|:---------|:-------------|:------------|
| `{{PR-YYYYMMDD-NNN or "None"}}` | `{{Critical / Major / Minor}}` | `{{summary}}` | `{{workaround or planned fix release}}` |

If none: state `"No open issues at release time."` and delete the placeholder row.

---

## 11. Consumer Notes

`{{Free-text notes for downstream consumers of this release. Examples:
 - "This release changes the default value of X — consumers relying on the old default must add flag Y."
 - "The MISRA rule-texts file was updated to v1.01; downstream reports will now include additional guideline text for Rule Z."
 - "Delete this section if there are no consumer-visible changes worth calling out."}}`

---

## 12. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | `{{name}}` | `{{YYYY-MM-DD}}` | Git commit authorship |
| Reviewer | `{{name}}` | `{{YYYY-MM-DD}}` | PR review approval on release commit |
| Approver | `{{name}}` | `{{YYYY-MM-DD}}` | PR merge to `main` |

Per CCD-MAN3-001 §3, for a single-engineer team the same individual fills all three roles; the process record (git commit + PR merge event) provides the auditable evidence.

---

*End of CCD-SVD-001 v1.00 template*
