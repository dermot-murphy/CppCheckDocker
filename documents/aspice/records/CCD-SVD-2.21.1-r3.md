# Software Version Description
## CppCheckDocker — Release v2.21.1-r3

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SVD-2.21.1-r3 |
| **Version** | v1.00 |
| **Date** | 2026-08-14 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SPL.2 — Software Release |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-14 | Dermot Murphy | Backfill issue per #48 — populated instance for release v2.21.1-r3 (documentation-and-CI-hygiene republish of r2, no image content change) |

---

## 3. Release Identification

| Field | Value |
|:--------------|:------------|
| **Release Tag** | `v2.21.1-r3` |
| **Release Date (UTC)** | 2026-08-13 15:57 |
| **Release Type** | Republish — ASPICE documentation and CI-workflow changes only; runtime image contents unchanged from `v2.21.1-r2`. Revision suffix incremented per CCD-SUP8-001 §4.1. |
| **Released By** | Dermot Murphy (via automated CI on merge of PR #27 to `main`) |
| **Release Method** | Automated CI — `Release` job in `.github/workflows/build.yml` |

---

## 4. Source Provenance

| Field | Value |
|:--------------|:------------|
| **Git Repository** | `github.com/dermot-murphy/CppCheckDocker` |
| **Git Branch (source)** | `main` |
| **Git Commit SHA** | `75a176cac3026c6735def510bfb5f766700f4ea9` |
| **Git Tag** | `v2.21.1-r3` (annotated) |
| **GitHub Release URL** | <https://github.com/dermot-murphy/CppCheckDocker/releases/tag/v2.21.1-r3> |

---

## 5. Published Artefacts

### 5.1 Container Image (GHCR — primary registry)

| Field | Value |
|:--------------|:------------|
| **Primary Registry** | `ghcr.io/dermot-murphy/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r3` |
| **Image Digest (sha256)** | `sha256:b6c84424910a099b49eecd3890329f08302aca3c785f233d44df4fb604a6d28d` |
| **Image Size (uncompressed)** | ~130 MB (per `Build-Image` job log) |
| **Platform** | `linux/amd64` |
| **Also Tagged As** | `latest` — updated to this digest at release; supersedes the r2 mapping of `latest` |

The image digest differs from r2's `sha256:46ef33d…` even though the Dockerfile, base image, and cppcheck source are unchanged. As with the r1 → r2 transition, the delta is BuildKit metadata (build timestamp, cache origin) rather than any change to the image root filesystem. Content-identity with r2 has been verified by review of the r3 `Build-Image` job log (same layer counts, same package list, same cppcheck binary path). The regeneration is a consequence of the CI-only and documentation-only changes to `.github/workflows/build.yml` and `documents/aspice/**` merged via PRs #25 and #26 triggering a fresh `Release` job.

### 5.2 Secondary Registry (DockerHub)

| Field | Value |
|:--------------|:------------|
| **Registry** | `docker.io/canembed/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r3` |
| **Digest (sha256)** | `sha256:b6c84424910a099b49eecd3890329f08302aca3c785f233d44df4fb604a6d28d` |
| **Also Tagged As** | `latest` |

Digest identity across registries is expected — the `Release` job builds once and pushes the same manifest to both.

---

## 6. Configuration and Build Parameters

Identical to r2:

| Field | Value |
|:--------------|:------------|
| **`CPPCHECK_VERSION` build ARG** | `2.21.1` |
| **`UBUNTU_VERSION` build ARG** | `24.04` |
| **CMake options** | `-DCMAKE_BUILD_TYPE=Release -DHAVE_RULES=ON -DUSE_MATCHCOMPILER=ON -DFILESDIR=/opt/cppcheck/share/cppcheck` |
| **BuildKit frontend** | `docker/dockerfile:1.7` |
| **Reproducibility** | Runtime layers content-identical to r2 (see §5.1 note); digest differs due to BuildKit metadata |

---

## 7. Third-Party Components

Identical to r2 — no supplier state changed between r2 and r3:

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
| Unit verification tests | CCD-SWE4-001 §4 | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31718028261> (`Verify-Version` job — SR-023 smoke covers the image-sanity UVT set for a single-tier CI model per CCD-SUP1-001 §6.1) |
| Integration tests | CCD-SWE5-001 §3 | PASS | Same run (`Run-Integration-Tests` job) |
| Qualification tests | CCD-SWE6-001 §3 | PASS | [`documents/aspice/records/CCD-QTR-2.21.1-r3.md`](CCD-QTR-2.21.1-r3.md) |
| Version smoke test | `Verify-Version` CI job | PASS | Same run |
| Vulnerability scan gate | `Scan-Image` CI job (trivy, HIGH+CRITICAL) | PASS | Same run — `Image_Scan_Report` artefact |
| Lint gate | `Lint` CI job (pre-commit: hadolint + yamllint) | PASS | Same run |
| Aggregator gate | `AllChecksPassed` CI job | PASS | Same run |
| Wiki publication | `Publish-Wiki` CI job | PASS | Same run |

---

## 9. Changes Since Previous Release

| Category | Description |
|:--------------|:-------------|
| **Previous release tag** | `v2.21.1-r2` |
| **Upstream cppcheck delta** | None — pinned to `2.21.1` in both releases |
| **Base image delta** | None — `ubuntu:24.04` unchanged |
| **Dockerfile delta** | None — Dockerfile byte-identical to r2 |
| **Workflow delta** | `.github/workflows/build.yml` — CR-24 paths-filter guard added to the `Release` job so merges to `main` that only affect documentation, workflows, or tests skip publish (documented in CCD-SUP8-001 §5.3 and CCD-SPL2-001 §5.1). Note: this change did not skip r3 itself, because r3 also carried a Dockerfile-touching merge — see below. |
| **Documentation delta** | PR #23 added deviation records `CCD-DEV-001` (single-engineer role collapse) and `CCD-DEV-002` (independent QA audit gap), and promoted all remaining ASPICE plans from Draft to Released. PR #24 added §5.3 to SUP.8 and §5.1 to SPL.2 to document the paths-filter skip condition. |
| **New/updated SRs (from CCD-SWE1-001)** | None |
| **New/updated test cases** | None |
| **Withdrawn releases** | None — r2 remains available and functional |

**Consumer impact:** none. Runtime image layers are content-identical to r2; only the ASPICE documentation shipped in the source tree and the CI machinery that produced the image changed.

---

## 10. Known Issues at Release Time

Open at release time (all closed subsequently, before this backfill):

| Issue | Status at r3 release | Resolution |
|:------|:---------------------|:-----------|
| #28 ASPICE V4 L2 audit findings A–F (parent) | Open | Split into #29–#34, all resolved in the v2.21.1-r4 release cycle |
| #29 FIND-A image size regression gate | Open | Landed on develop, ships in r4 |
| #30 FIND-B SUP.1 hadolint label | Open | Landed on develop, ships in r4 |
| #31 FIND-C SUP.9 documents/reviews reconcile | Open | Landed on develop, ships in r4 |
| #32 FIND-D SUP.8 §7 audit automation | Open | Landed on develop, ships in r4 |
| #33 FIND-E SWE.4 phantom job reference | Open | Landed on develop, ships in r4 |
| #34 FIND-F SWE.4 static-analysis Active table | Open | Landed on develop, ships in r4 |

None of the above prevented r3 from being a functional release — the runtime image is unchanged from r2 and the audit findings are all in documentation or CI-hygiene scope.

---

## 11. Consumer Notes

Content-identical republish of r2. Consumers pinned to r2 by digest need not update. Consumers pinned by tag `latest` will pick up r3's digest on the next pull. The convenience tag `2.21.1-r2` remains available at its original digest and is not withdrawn.

Recommended pin for downstream consumers requiring reproducibility:

```yaml
container:
  image: ghcr.io/dermot-murphy/cppcheckdocker@sha256:b6c84424910a099b49eecd3890329f08302aca3c785f233d44df4fb604a6d28d
```

---

## 12. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-13 | Git commit authorship on the source commit `75a176c` |
| Reviewer | Dermot Murphy | 2026-08-13 | Self-review under CCD-MAN3-001 §3 single-engineer clause (PRs #25/#26/#27 review) |
| Approver | Dermot Murphy | 2026-08-13 | PR #27 merge to `main` at 2026-08-13 15:55 UTC — `AllChecksPassed` gate satisfied |

Per CCD-MAN3-001 §3, for a single-engineer team the same individual fills all three roles; the process record (git commit + PR merge event) provides the auditable evidence.

**Backfill note:** this document was authored on 2026-08-14 as part of issue #48 to close the SPL.2 record gap identified during release-readiness review for r4. All source data (commit SHA, image digest, CI-run URLs) was harvested from the pre-existing GitHub artefacts of the r3 release cycle; nothing in this document was reconstructed by memory or estimated.

---

*End of CCD-SVD-2.21.1-r3 v1.00*
