# Supplier Monitoring Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-ACQ4-001 |
| **Version** | v1.01 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Draft |
| **Classification** | Internal |
| **ASPICE Process** | ACQ.4 — Supplier Monitoring |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | SUP-001 change-detection method now automated via `.github/workflows/poll-cppcheck.yml` (issue #7). |

---

## 1. Introduction

This document defines the Supplier Monitoring process for the CppCheckDocker project in accordance with ASPICE v4 process ACQ.4 (Supplier Monitoring).

The CppCheckDocker deliverable is a container image that integrates and redistributes third-party components. There is no procurement contract or supplier-managed engineering deliverable; instead, the project consumes freely-available upstream releases and open-source assets. This plan therefore addresses ACQ.4 in a **COTS-consumption profile**: how we track upstream changes, what triggers a re-release, and where the evidence lives.

**Parent documents:** CCD-SUP8-001 (Configuration Management Plan), CCD-SUP9-001 (Problem Resolution and Change Request Management Plan)
**Related documents:** CCD-SPL2-001 (Software Release Plan), CCD-SVD-001 (Software Version Description)

---

## 2. Scope

The following suppliers deliver components that end up inside the published image and therefore fall under this plan:

| Supplier ID | Supplier | Deliverable | Delivery Channel | Licence |
|:--------------|:------------|:-------------|:------------------|:---------|
| SUP-001 | The cppcheck project (`danmar/cppcheck`) | cppcheck source at a named git tag | GitHub `git clone --branch <tag>` from `https://github.com/danmar/cppcheck.git` | GPL-3.0-or-later |
| SUP-002 | Canonical Ltd. | Ubuntu LTS base image | Docker Hub `library/ubuntu` @ tag `<UBUNTU_VERSION>` | Ubuntu FSA + component licences |
| SUP-003 | MISRA Consortium Limited | MISRA C:2012 rule-texts file (`misra_c_2012_for_cppcheck.txt`) | Currently: manual download; committed to `documents/assets/` | CC BY-NC-ND 4.0 |

Ubuntu package updates that reach the runtime image transitively (via `apt-get install libpcre3 python3`) are treated as part of SUP-002 (Canonical) — not as separate suppliers.

Cppcheck bundled addons (`misra.py`, `naming.py`, etc.) are part of the cppcheck deliverable (SUP-001) — not separate suppliers.

---

## 3. Supplier Register

### 3.1 SUP-001 — cppcheck

| Attribute | Value |
|:--------------|:------------|
| **Consumed via** | `ARG CPPCHECK_VERSION` in `Dockerfile`; `git clone --depth 1 --branch "${CPPCHECK_VERSION}"` |
| **Current pinned version** | `2.21.1` |
| **Change-detection method** | Automated: [`.github/workflows/poll-cppcheck.yml`](../../.github/workflows/poll-cppcheck.yml) runs on the 1st of each month (and on `workflow_dispatch`), polls `git ls-remote --tags https://github.com/danmar/cppcheck.git`, and files a bump PR against `develop` when a newer release-shaped tag (`X.Y[.Z]`) is available. The PR is pre-populated with the evaluation checklist from this row. |
| **Recommended cadence** | Check monthly; the upstream typically releases every 1–3 months. |
| **Evaluation criteria before bump** | 1) Read upstream release notes for breaking changes. 2) Verify the tag exists via `git ls-remote`. 3) Confirm no reported regressions on the upstream issue tracker for the release. |
| **Bump procedure** | Raise a CR per CCD-SUP9-001 §3.6; update `ARG CPPCHECK_VERSION`; run full CI; publish a new image tag `-r1`. |
| **Withdraw / rollback trigger** | Critical defect discovered in the bumped version — revert the ARG and publish a hotfix reverting to the prior pinned version. |
| **Contact / escalation** | GitHub issue at `danmar/cppcheck` (public tracker); no commercial support relationship. |

### 3.2 SUP-002 — Canonical (Ubuntu)

| Attribute | Value |
|:--------------|:------------|
| **Consumed via** | `ARG UBUNTU_VERSION` in `Dockerfile`; `FROM ubuntu:${UBUNTU_VERSION}` |
| **Current pinned version** | `24.04` (LTS) |
| **Change-detection method** | The `ubuntu:24.04` tag is a rolling tag re-published by Canonical whenever the LTS receives updates. Digest-level changes are detected on each rebuild automatically. Major-version bumps (e.g., `24.04` → `26.04`) are announced by Canonical on the [Ubuntu Releases page](https://wiki.ubuntu.com/Releases) and consumed only via explicit ARG bump. |
| **Recommended cadence** | Watch major LTS release cadence (every 2 years, April of even years). Rebuild + retest quarterly against the current pinned tag to catch cumulative transitive-package changes. |
| **Evaluation criteria before major bump** | 1) LTS declared stable by Canonical. 2) `libpcre3` and `python3` still available in the new release's default archive. 3) Full CI passes against the new tag on a feature branch. |
| **Bump procedure** | Raise a CR per CCD-SUP9-001 §3.1; update `ARG UBUNTU_VERSION`; run full CI; publish a new image tag `-r<n+1>`. |
| **Withdraw / rollback trigger** | Critical CVE with no upstream patch — pin to a specific point release, or roll back the ARG. |
| **Contact / escalation** | [Ubuntu Security Notices](https://ubuntu.com/security/notices) mailing list for CVE notifications; no commercial support relationship. |

### 3.3 SUP-003 — MISRA Consortium

| Attribute | Value |
|:--------------|:------------|
| **Consumed via** | `COPY documents/assets/misra_c_2012_for_cppcheck.txt …` in the runtime stage |
| **Current bundled version** | v1.00 (2024-04-17 release) |
| **Change-detection method** | Manual poll — MISRA does not publish this file on a discoverable feed. Author checks the [MISRA Forum](https://forum.misra.org.uk/) and cppcheck's [MISRA Rule Texts announcement](https://sourceforge.net/p/cppcheck/news/2025/02/misra-rule-texts/) periodically. |
| **Recommended cadence** | Check every 6 months, or when a new MISRA C amendment is announced. |
| **Evaluation criteria before update** | 1) File header revision line increments (§ Revision history in the file). 2) Licence statement is still CC BY-NC-ND 4.0 or compatible. 3) File is not derivative work (per licence terms). |
| **Bump procedure** | Replace `documents/assets/misra_c_2012_for_cppcheck.txt` in a feature branch; run full CI (in particular INT-040 and QT-015 must still pass since rule IDs are unchanged); publish a new image tag `-r<n+1>`. |
| **Withdraw / rollback trigger** | MISRA revokes the CC BY-NC-ND 4.0 redistribution permission — remove the file, republish image without the bundled asset, note the change loudly in the SVD Consumer Notes section. |
| **Contact / escalation** | `enquiries@misra.org.uk` for licensing queries; MISRA Forum for guideline discussion. |

---

## 4. Monitoring Cadence Summary

| Check | Frequency | Owner | Evidence |
|:--------------|:-----------|:------|:---------|
| cppcheck upstream tags | Monthly | `poll-cppcheck.yml` (author reviews auto-raised PR) | Bump PR opened by workflow, or "no bump required" log line in the workflow run |
| Ubuntu base tag digest | Per CI build (automatic) | CI | Build log records the resolved digest |
| Ubuntu LTS major release | Per Canonical announcement | Author | CR record filed when a bump is proposed |
| Ubuntu Security Notices affecting `libpcre3` or `python3` | Continuous (mailing list) | Author | Any hit triggers a PR per CCD-SUP9-001 |
| MISRA rule-texts revisions | Every 6 months | Author | Note recorded in this file's §7 Change Log |
| Overall supplier register review | At each release | Author | This document referenced from CCD-SVD-<tag>.md §7 Third-Party Components |

---

## 5. Change Response

When a supplier change is detected and passes the evaluation criteria (§3), the response is:

1. **Raise a Change Request** per CCD-SUP9-001 §3 (SUP.10 process — folded into that document).
2. **Update the affected `ARG` or file** in a `feature/` branch.
3. **Run full CI**. All Mandatory tests in CCD-SWE4-001, CCD-SWE5-001, CCD-SWE6-001 must pass. INT-040 and QT-015 explicitly cover MISRA integrity.
4. **Publish a new image tag** per CCD-SPL2-001 §5. Increment the `-r<n>` revision suffix if the cppcheck version is unchanged, or start a new `-r1` if the cppcheck version changed.
5. **Populate the SVD** (CCD-SVD-001 template) — the Third-Party Components section in the SVD is the per-release snapshot of this Supplier Register.

If evaluation criteria fail — e.g., upstream release notes flag a breaking change we cannot absorb — the bump is deferred and the decision recorded on the CR record. No release is published.

---

## 6. Records

| Record | Location | Retention |
|:--------------|:------------|:-----------|
| Supplier register (this document) | `documents/aspice/CppCheckDocker_ACQ4_Supplier_Monitoring_Plan.md` | Version-controlled in Git |
| Per-release supplier snapshot | `documents/aspice/records/CCD-SVD-<tag>.md` §7 Third-Party Components | Version-controlled in Git |
| Change Requests triggered by supplier changes | `documents/reviews/YYYY-MM-DD_CR-NNN_<title>.md` | Version-controlled in Git |
| Ubuntu digest per build | GitHub Actions `Build-Image` job log | 30-day CI retention; reproducible from tagged image |

---

## 7. Supplier-Change Log

A running log of significant supplier changes acted on by this project. New entries are added at the top.

| Date | Supplier | Change | Response | CR / Release |
|:-----|:---------|:-------|:---------|:-------------|
| 2026-08-13 | SUP-001 | Initial pinning to cppcheck 2.21.1 | Baseline | Initial commit |
| 2026-08-13 | SUP-002 | Initial pinning to Ubuntu 24.04 | Baseline | Initial commit |
| 2026-08-13 | SUP-003 | Initial bundling of MISRA rule-texts v1.00 (2024-04-17) | Baseline | Initial commit |

---

## 8. ASPICE Process Compliance

This plan addresses the following ASPICE v4 Level 2 PA attributes for ACQ.4:

| PA | Attribute | Evidence |
|:--------------|:------------|:------------|
| PA 1.1 | Process performance | Supplier register (§3) maintained; monitoring cadence (§4) defined and executed; supplier-change log (§7) records each acted-on change |
| PA 2.1 | Performance management | Change-detection method and evaluation criteria defined per supplier; CR process (CCD-SUP9-001) enforces evaluation before bump; SVD snapshot enforces at-release capture |
| PA 2.2 | Work product management | This document and all CRs/SVDs under version control; per-release supplier snapshot committed alongside the release |

---

*End of CCD-ACQ4-001 v1.01*
