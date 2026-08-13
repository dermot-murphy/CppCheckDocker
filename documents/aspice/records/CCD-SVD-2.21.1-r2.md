# Software Version Description
## CppCheckDocker — Release v2.21.1-r2

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SVD-2.21.1-r2 |
| **Version** | v1.00 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SPL.2 — Software Release |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue — populated instance for release v2.21.1-r2 (CI-hygiene republish, no image content change) |

---

## 3. Release Identification

| Field | Value |
|:--------------|:------------|
| **Release Tag** | `v2.21.1-r2` |
| **Release Date (UTC)** | 2026-08-13 14:05 |
| **Release Type** | Republish — CI-workflow change only; image contents unchanged from `v2.21.1-r1`. Revision suffix incremented per CCD-SUP8-001 §4.1. |
| **Released By** | Dermot Murphy (via automated CI on merge of hotfix PR #19 to `main`) |
| **Release Method** | Automated CI — `Release` job in `.github/workflows/build.yml` |

---

## 4. Source Provenance

| Field | Value |
|:--------------|:------------|
| **Git Repository** | `github.com/dermot-murphy/CppCheckDocker` |
| **Git Branch (source)** | `main` |
| **Git Commit SHA** | `d3b6eb977127bcd6ea399af2aa8056974de455bd` |
| **Git Tag** | `v2.21.1-r2` (annotated) |
| **GitHub Release URL** | <https://github.com/dermot-murphy/CppCheckDocker/releases/tag/v2.21.1-r2> |

---

## 5. Published Artefacts

### 5.1 Container Image (GHCR — primary registry)

| Field | Value |
|:--------------|:------------|
| **Primary Registry** | `ghcr.io/dermot-murphy/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r2` |
| **Image Digest (sha256)** | `sha256:46ef33dae5b2a0c1d426c472e6961f74d6f0595eaec8b6bba4cb970318f278fd` |
| **Image Size (uncompressed)** | ~130 MB (per `Build-Image` job log) |
| **Platform** | `linux/amd64` |
| **Also Tagged As** | `latest` — updated to this digest at release; supersedes the r1 mapping of `latest` |

The image digest differs from r1's `sha256:632aeb9…` even though the Dockerfile, base image, and cppcheck source are unchanged. The delta is explained by BuildKit metadata (build timestamp, cache origin) rather than any change to the image root filesystem. Content-identity has been verified: the runtime layers, cppcheck binary, MISRA rule-texts file, and OCI labels are byte-identical between r1 and r2. The regeneration is a consequence of the CI-only change to `.github/workflows/build.yml` triggering a fresh `Release` job.

### 5.2 Secondary Registry (DockerHub)

| Field | Value |
|:--------------|:------------|
| **Registry** | `docker.io/canembed/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r2` |
| **Digest (sha256)** | `sha256:46ef33dae5b2a0c1d426c472e6961f74d6f0595eaec8b6bba4cb970318f278fd` |
| **Also Tagged As** | `latest` |

---

## 6. Configuration and Build Parameters

Identical to r1:

| Field | Value |
|:--------------|:------------|
| **`CPPCHECK_VERSION` build ARG** | `2.21.1` |
| **`UBUNTU_VERSION` build ARG** | `24.04` |
| **CMake options** | `-DCMAKE_BUILD_TYPE=Release -DHAVE_RULES=ON -DUSE_MATCHCOMPILER=ON -DFILESDIR=/opt/cppcheck/share/cppcheck` |
| **BuildKit frontend** | `docker/dockerfile:1.7` |
| **Reproducibility** | Runtime layers content-identical to r1 (see §5.1 note); digest differs due to BuildKit metadata |

---

## 7. Third-Party Components

Identical to r1 — no supplier state changed between r1 and r2:

| Component | Version | Licence | Source | Modified? |
|:--------------|:--------|:--------|:-------|:----------|
| cppcheck | `2.21.1` | GPL-3.0-or-later | `github.com/danmar/cppcheck` @ tag `2.21.1` | No |
| Ubuntu (base image) | `24.04` | Ubuntu FSA + component licences | Docker Hub `library/ubuntu` @ tag `24.04` | No |
| libpcre3 (runtime) | Ubuntu-provided | BSD-3-Clause | apt `libpcre3` from Ubuntu 24.04 archive | No |
| python3 (runtime) | Ubuntu-provided | PSF-2.0 | apt `python3` from Ubuntu 24.04 archive | No |
| MISRA C:2012 rule-texts | v1.00 (2024-04-17 release) | CC BY-NC-ND 4.0 | © MISRA Consortium Limited, redistributed at `documents/assets/misra_c_2012_for_cppcheck.txt` | No |

---

## 8. Verification Evidence

| Test Set | Reference | Result | Location |
|:--------------|:------------|:-------|:---------|
| Unit verification tests | CCD-SWE4-001 §4 | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31708219764> (`Verify-Version` job) |
| Integration tests | CCD-SWE5-001 §3 | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31708219764> (`Run-Integration-Tests` job) |
| Qualification tests | CCD-SWE6-001 §3 | PASS | [`documents/aspice/records/CCD-QTR-2.21.1-r2.md`](CCD-QTR-2.21.1-r2.md) |
| Version smoke test | `Verify-Version` CI job | PASS | Same run as above |
| Vulnerability scan gate | `Scan-Image` CI job (trivy, HIGH+CRITICAL) | PASS | Same run — `Image_Scan_Report` artefact |
| Lint gate | `Lint` CI job (pre-commit: hadolint + yamllint) | PASS | Same run |
| Aggregator gate | `AllChecksPassed` CI job | PASS | Same run |
| Wiki publication | `Publish-Wiki` CI job | PASS | Same run |

---

## 9. Changes Since Previous Release

| Category | Description |
|:--------------|:-------------|
| **Previous release tag** | `v2.21.1-r1` |
| **Upstream cppcheck delta** | None — pinned to `2.21.1` in both releases |
| **Base image delta** | None — `ubuntu:24.04` unchanged |
| **Dockerfile delta** | None — Dockerfile byte-identical to r1 |
| **Workflow delta** | `.github/workflows/build.yml` only. `docker/login-action@v3` → `@v4`; `pre-commit/action@v3.0.1` replaced with `pip install pre-commit && pre-commit run`. Purpose: clear Node.js 20 deprecation warnings that surfaced on r1's CI run. See hotfix issue #18 and PR #19. |
| **New/updated SRs (from CCD-SWE1-001)** | None |
| **New/updated test cases** | None |
| **Withdrawn releases** | None — r1 remains available and functional |

**Consumer impact:** none. The image layers are content-identical to r1; only the CI machinery that produced them changed.

---

## 10. Known Issues at Release Time

No open issues at release time. Hotfix #18 was closed by the PR #19 merge that produced this release.

---

## 11. Consumer Notes

Content-identical republish of r1. Consumers pinned to r1 by digest need not update. Consumers pinned by tag `latest` will pick up r2's digest on the next pull. The convenience tag `2.21.1-r1` remains available at its original digest and is not withdrawn.

Recommended pin for downstream consumers requiring reproducibility:

```yaml
container:
  image: ghcr.io/dermot-murphy/cppcheckdocker@sha256:46ef33dae5b2a0c1d426c472e6961f74d6f0595eaec8b6bba4cb970318f278fd
```

---

## 12. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-13 | Git commit authorship on the source commit `d3b6eb9` |
| Reviewer | Dermot Murphy | 2026-08-13 | Self-review under CCD-MAN3-001 §3 single-engineer clause (PR #19 review) |
| Approver | Dermot Murphy | 2026-08-13 | PR #19 merge to `main` at 2026-08-13 14:05 UTC |

---

*End of CCD-SVD-2.21.1-r2 v1.00*
