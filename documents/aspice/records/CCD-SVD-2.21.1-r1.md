# Software Version Description
## CppCheckDocker — Release v2.21.1-r1

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SVD-2.21.1-r1 |
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
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue — populated instance for release v2.21.1-r1 |

---

## 3. Release Identification

| Field | Value |
|:--------------|:------------|
| **Release Tag** | `v2.21.1-r1` |
| **Release Date (UTC)** | 2026-08-13 13:55 |
| **Release Type** | Initial (first tagged release from the project baseline) |
| **Released By** | Dermot Murphy (via automated CI on merge of PR #17) |
| **Release Method** | Automated CI — `Release` job in `.github/workflows/build.yml` |

---

## 4. Source Provenance

| Field | Value |
|:--------------|:------------|
| **Git Repository** | `github.com/dermot-murphy/CppCheckDocker` |
| **Git Branch (source)** | `main` |
| **Git Commit SHA** | `f077468d7eb3f98cc14037467243aadc3e33c9e8` |
| **Git Tag** | `v2.21.1-r1` (annotated) |
| **GitHub Release URL** | <https://github.com/dermot-murphy/CppCheckDocker/releases/tag/v2.21.1-r1> |

---

## 5. Published Artefacts

### 5.1 Container Image (GHCR — primary registry)

| Field | Value |
|:--------------|:------------|
| **Primary Registry** | `ghcr.io/dermot-murphy/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r1` |
| **Image Digest (sha256)** | `sha256:632aeb9918397fcc15f8bc2f6d384188eb2d13a9c4460412629214b93dcad46f` |
| **Image Size (uncompressed)** | ~130 MB (per `Build-Image` job log) |
| **Platform** | `linux/amd64` |
| **Also Tagged As** | `latest` — same digest at time of release; subject to change as later releases update the floating tag |

### 5.2 Secondary Registry (DockerHub)

| Field | Value |
|:--------------|:------------|
| **Registry** | `docker.io/canembed/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r1` |
| **Digest (sha256)** | `sha256:632aeb9918397fcc15f8bc2f6d384188eb2d13a9c4460412629214b93dcad46f` |
| **Also Tagged As** | `latest` |

Digest identity across registries is expected — the `Release` job builds once and pushes the same manifest to both.

---

## 6. Configuration and Build Parameters

| Field | Value |
|:--------------|:------------|
| **`CPPCHECK_VERSION` build ARG** | `2.21.1` |
| **`UBUNTU_VERSION` build ARG** | `24.04` |
| **CMake options** | `-DCMAKE_BUILD_TYPE=Release -DHAVE_RULES=ON -DUSE_MATCHCOMPILER=ON -DFILESDIR=/opt/cppcheck/share/cppcheck` |
| **BuildKit frontend** | `docker/dockerfile:1.7` |
| **Reproducibility** | Bit-identical builds expected across CI runs from the same commit (SR-054 Desirable) |

---

## 7. Third-Party Components

Per-release snapshot of CCD-ACQ4-001 §3, frozen at commit `f077468`:

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
| Unit verification tests | CCD-SWE4-001 §4 | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> (`Verify-Version` job — SR-023 smoke covers the image-sanity UVT set for a single-tier CI model per CCD-SUP1-001 §6.1) |
| Integration tests | CCD-SWE5-001 §3 | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> (`Run-Integration-Tests` job) |
| Qualification tests | CCD-SWE6-001 §3 | PASS | [`documents/aspice/records/CCD-QTR-2.21.1-r1.md`](CCD-QTR-2.21.1-r1.md) |
| Version smoke test | `Verify-Version` CI job | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> |
| Vulnerability scan gate | `Scan-Image` CI job (trivy, HIGH+CRITICAL) | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> (`Image_Scan_Report` artefact — 90-day retention) |
| Lint gate | `Lint` CI job (pre-commit: hadolint + yamllint) | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> |
| Aggregator gate | `AllChecksPassed` CI job | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> |
| Wiki publication | `Publish-Wiki` CI job | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31707301287> |

---

## 9. Changes Since Previous Release

| Category | Description |
|:--------------|:-------------|
| **Previous release tag** | N/A — first release |
| **Upstream cppcheck delta** | Initial pin to `2.21.1` |
| **Base image delta** | Initial pin to `ubuntu:24.04` |
| **Dockerfile delta** | N/A — first release |
| **New/updated SRs (from CCD-SWE1-001)** | Full baseline — all Mandatory SRs delivered in this release |
| **New/updated test cases** | Full baseline — UVT-001..034 + UVT-060..061 (MISRA), INT-001..040, QT-001..015 |
| **Withdrawn releases** | None |

---

## 10. Known Issues at Release Time

No open issues at release time. All CR issues raised against the baseline (#4, #5, #6, #7, #9, #15) were closed by the PR #17 merge that produced this release. Issue #8 (populate ASPICE records) was later reopened as #21 to write this document and the corresponding QTR — its absence at release time is noted here for audit transparency.

---

## 11. Consumer Notes

First public release of the image. No prior behaviour to break.

Recommended pin for downstream consumers requiring reproducibility:

```yaml
container:
  image: ghcr.io/dermot-murphy/cppcheckdocker@sha256:632aeb9918397fcc15f8bc2f6d384188eb2d13a9c4460412629214b93dcad46f
```

The `latest` floating tag pointed at this digest at release time but will move on the next release.

---

## 12. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-13 | Git commit authorship on the source commit `f077468` |
| Reviewer | Dermot Murphy | 2026-08-13 | Self-review under the single-engineer clause of CCD-MAN3-001 §3 (PR #17 review) |
| Approver | Dermot Murphy | 2026-08-13 | PR #17 merge to `main` at 2026-08-13 13:55 UTC |

Per CCD-MAN3-001 §3, for a single-engineer team the same individual fills all three roles; the process record (git commit + PR merge event) provides the auditable evidence.

---

*End of CCD-SVD-2.21.1-r1 v1.00*
