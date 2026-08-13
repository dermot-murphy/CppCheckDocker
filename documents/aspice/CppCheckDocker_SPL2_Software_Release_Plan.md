# Software Release Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SPL2-001 |
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
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |

---

## 1. Introduction

This document defines the Software Release process for the CppCheckDocker project in accordance with ASPICE v4 process SPL.2 (Software Release).

A **release** is a published Docker image identified by an immutable tag and digest, together with the release-supporting artefacts (Software Version Description, release notes, CI evidence) required to reconstruct or audit that release.

**Parent documents:** CCD-SUP8-001 (Configuration Management Plan), CCD-SWE6-001 (Qualification Test Specification)  
**Child document:** CCD-SVD-001 (Software Version Description — one instance per release)

---

## 2. Release Scope

Each release comprises:

| Artefact | Location | Immutability |
|:--------------|:------------|:--------------|
| Container image | `ghcr.io/<owner>/cppcheckdocker:<cppcheck-version>-r<revision>` | Immutable (tagged) + immutable (digest) |
| Floating tag | `ghcr.io/<owner>/cppcheckdocker:latest` (updated to same digest) | Mutable — best-effort convenience tag |
| Floating tag | `ghcr.io/<owner>/cppcheckdocker:<cppcheck-major>.<minor>` | Mutable — tracks latest revision for that upstream minor |
| Git tag | `v<cppcheck-version>-r<revision>` on `main` branch | Immutable |
| GitHub Release | Attached to the git tag | Immutable body; can be edited but is version-controlled |
| Software Version Description | `documents/aspice/records/CCD-SVD-<tag>.md` (populated instance of CCD-SVD-001) | Committed to Git; immutable once released |

---

## 3. Release Cadence and Triggers

The project follows a continuous-delivery model driven by upstream cppcheck releases. There is no fixed cadence.

| Trigger | Release Type | Version Increment |
|:--------------|:-------------|:-------------------|
| Upstream cppcheck patch release (e.g., 2.21.1 → 2.21.2) | Minor | New `<cppcheck-version>-r1` tag |
| Upstream cppcheck minor release (e.g., 2.21.x → 2.22.0) | Minor | New `<cppcheck-version>-r1` tag |
| Upstream cppcheck major release (e.g., 2.x → 3.0) | Major review | New `<cppcheck-version>-r1` tag; requires CR review |
| Base image bump (Ubuntu LTS or minor tag) | Patch | Same cppcheck version, `-r<n+1>` |
| CppCheckDocker Dockerfile change (options, addons) | Patch | Same cppcheck version, `-r<n+1>` |
| MISRA rule-texts update from MISRA Consortium | Patch | Same cppcheck version, `-r<n+1>` |
| Critical CVE fix in base image | Hotfix | Follows hotfix branch model per CMP §3 |

---

## 4. Release Entry Criteria

Before a release is created, the following criteria must be met:

| # | Criterion | Evidence |
|:--|:------------|:------------|
| 1 | All Mandatory unit tests pass (CCD-SWE4-001) | GitHub Actions `Verify-Version` and unit-test jobs green on release commit |
| 2 | All integration tests pass (CCD-SWE5-001) | `Run-Integration-Tests` green on release commit |
| 3 | All Mandatory qualification tests pass (CCD-SWE6-001) | Signed QT record filed at `documents/aspice/records/CCD-QTR-<tag>.md` |
| 4 | CI aggregator gate passed | `AllChecksPassed` green on release commit |
| 5 | Wiki successfully published | `Publish-Wiki` green on release commit; wiki reflects tagged doc versions |
| 6 | Traceability matrix reviewed | CCD-RTM-001 updated for any new SRs; reviewer sign-off recorded in PR |
| 7 | SVD populated and reviewed | `documents/aspice/records/CCD-SVD-<tag>.md` present and signed off |
| 8 | Release notes drafted | GitHub Release body drafted, including MISRA-file version if changed |
| 9 | No open Critical or Major problem reports (CCD-SUP9-001) | Review of `documents/reviews/` — none in `Open` or `In Progress` |

Failure of any entry criterion blocks the release. Deferred failures (waived, downgraded, or scheduled for a follow-up release) require documented reviewer approval.

---

## 5. Release Procedure

### 5.1 Automated (normal case)

1. PR merged to `main` on a commit that satisfies all entry criteria (§4)
2. `Build-Image`, `Verify-Version`, `Run-Integration-Tests`, `AllChecksPassed` jobs run automatically
3. `Release` job (see CCD-SUP8-001 §5.3) runs on `main`:
   - Tags the image `<cppcheck-version>-r<revision>` and `latest`
   - Pushes to `ghcr.io` (and to DockerHub if the DockerHub secret is configured)
   - Creates a git tag `v<cppcheck-version>-r<revision>`
   - Creates a GitHub Release attached to the git tag
   - Records the pushed image digest in the Release notes body
4. `Publish-Wiki` job (see build.yml) publishes the tagged versions of the ASPICE documents to the repository wiki
5. Author populates and commits `documents/aspice/records/CCD-SVD-<tag>.md` (template CCD-SVD-001), including the digest recorded in the Release notes
6. Author reviews and self-approves the SVD, then updates the Release notes to link to the committed SVD

### 5.2 Manual (fallback)

If automation is unavailable (e.g., GitHub Actions outage), a release may be created manually:

1. Build image locally with pinned ARGs matching the release commit:  
   `docker build --build-arg CPPCHECK_VERSION=<v> --build-arg UBUNTU_VERSION=<u> -t <tag> .`
2. Run full test suite locally (`build-and-test.bat` or `test/integration/run.sh`)
3. Push manually: `docker push ghcr.io/<owner>/cppcheckdocker:<tag>`
4. Record the resulting digest in the SVD
5. Create the git tag and GitHub Release by hand via `gh release create`

Manual releases must be flagged in the SVD (§ Release Method) and reviewed at the next audit.

---

## 6. Release Exit Criteria

A release is considered complete when:

| # | Criterion | Evidence |
|:--|:------------|:------------|
| 1 | Image digest confirmed present at `ghcr.io/<owner>/cppcheckdocker:<tag>` | `docker manifest inspect` returns the same digest as the CI job log |
| 2 | Git tag pushed to `origin/main` | `git ls-remote --tags origin` shows the tag |
| 3 | GitHub Release attached to the git tag | `gh release view <tag>` succeeds |
| 4 | SVD committed and linked from Release notes | File exists at `documents/aspice/records/CCD-SVD-<tag>.md` |
| 5 | Wiki reflects the tagged doc versions | Wiki `Home.md` shows the release commit hash |
| 6 | Consumer smoke test passes | `docker pull ghcr.io/<owner>/cppcheckdocker:<tag> && docker run --rm <img> --version` returns the expected string |

---

## 7. Release Records

The following records are retained for each release under `documents/aspice/records/`:

| Record | Filename Pattern | Owner |
|:--------------|:------------------|:------|
| Software Version Description | `CCD-SVD-<tag>.md` | Release author |
| Qualification Test Record | `CCD-QTR-<tag>.md` | Release author |
| CI evidence bundle | Reference to GitHub Actions run URLs (kept in SVD) | Automatic |

Records are committed to Git and are therefore version-controlled and reproducible.

---

## 8. Deprecation and Withdrawal

Published images are **not deleted** from the registry — even when superseded — so that downstream projects pinning a specific tag continue to build.

An image may be **withdrawn** (marked "do not use") if a critical defect is discovered after release. The withdrawal procedure:
1. Raise a Critical PR in CCD-SUP9-001 process
2. Publish a hotfix release with the fix
3. Update the withdrawn release's GitHub Release notes with a "⚠️ WITHDRAWN — use `<replacement-tag>` instead" prefix and a link to the fix release
4. Do **not** delete the registry tag — leave it in place with the withdrawal notice for auditability
5. Announce via GitHub Discussions if the repository has any known downstream users

---

## 9. ASPICE Process Compliance

This plan addresses the following ASPICE v4 Level 2 PA attributes for SPL.2:

| PA | Attribute | Evidence |
|:--------------|:------------|:------------|
| PA 1.1 | Process performance | Release procedure defined (§5); exit criteria validated per release (§6) |
| PA 2.1 | Performance management | Entry criteria (§4) and release triggers (§3) defined; automated CI enforces the criteria |
| PA 2.2 | Work product management | SVD (CCD-SVD-001) and QT records retained per release under version control |

---

*End of CCD-SPL2-001 v1.00*
