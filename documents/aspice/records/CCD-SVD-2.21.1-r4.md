# Software Version Description
## CppCheckDocker — Release v2.21.1-r4

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SVD-2.21.1-r4 |
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
| v1.00 | 2026-08-14 | Dermot Murphy | Initial issue per #54 — populated instance for release v2.21.1-r4 (substantive release: image-size tracking, wiki layout refresh, Claude memory mirror, six ASPICE L2 audit findings closed) |

---

## 3. Release Identification

| Field | Value |
|:--------------|:------------|
| **Release Tag** | `v2.21.1-r4` |
| **Release Date (UTC)** | 2026-08-14 09:04 |
| **Release Type** | Feature — new CI jobs (Track-Image-Size, SUP.8 §7 automated digest audit), new ASPICE documentation (User Guide wiki layout, deviations, PA2 records, DEV001/DEV002), Claude memory mirror. Runtime image contents changed only through the new SR-060 image-size gate (which enforces existing behaviour rather than altering it); underlying Dockerfile and pinned dependencies are unchanged. Revision suffix incremented per CCD-SUP8-001 §4.1. |
| **Released By** | Dermot Murphy (via automated CI on merge of PR #50 to `main`) |
| **Release Method** | Automated CI — `Release` job in `.github/workflows/build.yml` |

---

## 4. Source Provenance

| Field | Value |
|:--------------|:------------|
| **Git Repository** | `github.com/dermot-murphy/CppCheckDocker` |
| **Git Branch (source)** | `main` |
| **Git Commit SHA** | `6a4f8be0480483ae0e012e263a251eddd39dd537` |
| **Git Tag** | `v2.21.1-r4` (annotated) |
| **GitHub Release URL** | <https://github.com/dermot-murphy/CppCheckDocker/releases/tag/v2.21.1-r4> |

---

## 5. Published Artefacts

### 5.1 Container Image (GHCR — primary registry)

| Field | Value |
|:--------------|:------------|
| **Primary Registry** | `ghcr.io/dermot-murphy/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r4` |
| **Image Digest (sha256)** | `sha256:e83c25f55c4a8a39e421e3f13c3fb1c26c3d2898daf0958f875dd38d56ec9e25` |
| **Image Size (uncompressed)** | 129,101,911 bytes (~130 MB) — within SR-060 200 MB threshold |
| **Platform** | `linux/amd64` |
| **Also Tagged As** | `latest` — updated to this digest at release; supersedes the r3 mapping of `latest` |

The image digest differs from r3's `sha256:b6c8442…` even though the Dockerfile and pinned third-party components are unchanged. As with earlier revision bumps, the delta is BuildKit metadata (build timestamp, cache origin) rather than any change to the image root filesystem. **This release is the first to have that identity confirmed by an automated audit** — the new `Configuration audit (digest round-trip)` step introduced by CR-32 (issue #32) verified at release time that both GHCR and DockerHub resolve to the same digest for tag `2.21.1-r4`, and the version-smoke sub-step verified that `docker run … --version` returns `Cppcheck 2.21.1` from the published image. See §8 Verification Evidence.

### 5.2 Secondary Registry (DockerHub)

| Field | Value |
|:--------------|:------------|
| **Registry** | `docker.io/canembed/cppcheckdocker` |
| **Immutable Tag** | `2.21.1-r4` |
| **Digest (sha256)** | `sha256:e83c25f55c4a8a39e421e3f13c3fb1c26c3d2898daf0958f875dd38d56ec9e25` |
| **Also Tagged As** | `latest` |

Digest identity across registries verified at release time by the SUP.8 §7 audit step (see §8).

---

## 6. Configuration and Build Parameters

Identical to r3:

| Field | Value |
|:--------------|:------------|
| **`CPPCHECK_VERSION` build ARG** | `2.21.1` |
| **`UBUNTU_VERSION` build ARG** | `24.04` |
| **CMake options** | `-DCMAKE_BUILD_TYPE=Release -DHAVE_RULES=ON -DUSE_MATCHCOMPILER=ON -DFILESDIR=/opt/cppcheck/share/cppcheck` |
| **BuildKit frontend** | `docker/dockerfile:1.7` |
| **Reproducibility** | Runtime layers content-identical to r3 (Dockerfile and dependencies unchanged); digest differs due to BuildKit metadata |

---

## 7. Third-Party Components

Identical to r3 — no supplier state changed between r3 and r4:

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
| Unit verification tests | CCD-SWE4-001 §4 | PASS | GitHub Actions run: <https://github.com/dermot-murphy/CppCheckDocker/actions/runs/31786463201> (`Verify-Version` job — SR-023 smoke covers the image-sanity UVT set for a single-tier CI model per CCD-SUP1-001 §6.1) |
| Integration tests | CCD-SWE5-001 §3 | PASS | Same run (`Run-Integration-Tests` job) |
| Qualification tests | CCD-SWE6-001 §3 | PASS | [`documents/aspice/records/CCD-QTR-2.21.1-r4.md`](CCD-QTR-2.21.1-r4.md) |
| Version smoke test | `Verify-Version` CI job | PASS | Same run |
| Vulnerability scan gate | `Scan-Image` CI job (trivy, HIGH+CRITICAL) | PASS | Same run — `Image_Scan_Report` artefact |
| Image-size regression gate (SR-060, CR-29) | `Build-Image` CI job | PASS | Same run — annotation: `Image size (129101911 bytes) is within the SR-060 200 MB threshold.` |
| **Configuration audit — digest round-trip (SUP.8 §7, CR-32)** | `Release` CI job | **PASS — first automated audit execution** | Same run — annotation: `Configuration audit (digest round-trip) passed: both registries resolve sha256:e83c25f55c4a8a39e421e3f13c3fb1c26c3d2898daf0958f875dd38d56ec9e25 for tag 2.21.1-r4.` |
| Configuration audit — version smoke on published image (SUP.8 §7) | `Release` CI job | PASS | Same run — annotation: `Configuration audit (version smoke on published image) passed.` |
| Image-size trend record (CR-42) | `Track-Image-Size` CI job | PASS | Same run — row appended to `image_size_history.csv` on `gh-pages` branch |
| Lint gate | `Lint` CI job (pre-commit: hadolint + yamllint) | PASS | Same run |
| Aggregator gate | `AllChecksPassed` CI job | PASS | Same run |
| Wiki publication (CStyleCheck layout, CR-43) | `Publish-Wiki` CI job | PASS | Same run |

---

## 9. Changes Since Previous Release

| Category | Description |
|:--------------|:-------------|
| **Previous release tag** | `v2.21.1-r3` |
| **Upstream cppcheck delta** | None — pinned to `2.21.1` |
| **Base image delta** | None — `ubuntu:24.04` unchanged |
| **Dockerfile delta** | None — Dockerfile byte-identical to r3 |
| **New CI jobs** | `Track-Image-Size` (CR-42): appends image size to `gh-pages/image_size_history.csv` on every merge to develop/main and renders `image_size_trend.svg` (embedded in README). `Release` job gains a `Configuration audit` step (CR-32) that verifies GHCR ⇔ DockerHub digest round-trip and version smoke on the published image. `Build-Image` gains an SR-060 size-regression gate (CR-29). |
| **Workflow delta** | Six ASPICE L2 audit findings closed (CR-29, CR-30, CR-31, CR-32, CR-33, CR-34). CR-51 fixed a bootstrap-race in the new Track-Image-Size job (first-ever gh-pages fetch was unguarded). |
| **Documentation delta** | CR-43: `Publish-Wiki` rewritten to emit a CStyleCheck-style layout with a User Guide section plus ASPICE CL2 with process groups; User Guide pages authored; PA2 capability records consolidated; N/A stubs added for MAN.5 and SYS. RTM and SUP.1 and MAN.3 refreshed. CR-44: Claude memory and lessons-learned mirrored into the repo under `documents/aspice/claude_memory/`, maintained by a pre-commit hook. CR-48: backfilled the previously missing CCD-SVD-2.21.1-r3 and CCD-QTR-2.21.1-r3 records. |
| **New/updated SRs (from CCD-SWE1-001)** | None — SR-060 (image size ≤ 200 MB) existed as a Desirable requirement; the new CI gate promotes it to an automated release blocker without changing the target. |
| **New/updated test cases** | None |
| **Withdrawn releases** | None — r3 remains available and functional |
| **Deprecation warnings** | New: Node.js 20 deprecation on `dorny/paths-filter@v3.0.4` (currently runs on Node 24 with warning). Tracked as issue #53 for the next release cycle. |

**Consumer impact:** none for existing consumers pinned to r3 by digest. Consumers pinned by tag `latest` will pick up r4's digest on the next pull. New downstream benefit: the image-size trend chart at <https://raw.githubusercontent.com/dermot-murphy/CppCheckDocker/gh-pages/image_size_trend.svg> is now published and updated on every release.

---

## 10. Known Issues at Release Time

No open blocking issues at release time. Open issues carried over that do not block release:

| Issue | Class | Status |
|:------|:------|:-------|
| #53 | Deferred upgrade | Bump `dorny/paths-filter` from v3.0.4 to a Node-24 tag before the deprecation warning becomes a hard error. Filed at release time; scheduled for the next release cycle. |
| #55 | Gitflow hygiene | Sync main back to develop after this release (standard post-release step). Filed at release time. |

The following issues were closed by the PR #50 merge that produced this release:

- #28 (parent ASPICE L2 audit), #29 (FIND-A image-size gate), #30 (FIND-B hadolint label), #31 (FIND-C SUP.9 reconcile), #32 (FIND-D digest audit automation), #33 (FIND-E phantom job), #34 (FIND-F static-analysis Active table), #42 (image-size tracking), #43 (wiki tidy-up), #44 (Claude memory mirror), #48 (r3 record backfill), #51 (Track-Image-Size bootstrap fix).

---

## 11. Consumer Notes

Substantive release. The runtime image itself is content-identical to r3, but the surrounding CI and documentation posture change materially:

- **Image-size trend chart** is now published to `gh-pages` and embedded in the README. Downstream consumers can watch the trend and pre-empt regressions.
- **Automated SUP.8 §7 digest audit** runs on every release, providing per-release evidence that the two published registries hold the same manifest.
- **Wiki** now includes a User Guide section and an ASPICE CL2 process-groups layout, matching the CStyleCheck reference style.
- **ASPICE L2** is now Fully Implemented across all previously-Largely-implemented audit findings (see the CCD-AUD-2026-08-13 audit report and the six FIND-A..F issues it spawned, all closed by this release).

Recommended pin for downstream consumers requiring reproducibility:

```yaml
container:
  image: ghcr.io/dermot-murphy/cppcheckdocker@sha256:e83c25f55c4a8a39e421e3f13c3fb1c26c3d2898daf0958f875dd38d56ec9e25
```

---

## 12. Sign-Off

| Role | Name | Date | Signature/Approval |
|:-----|:-----|:-----|:-------------------|
| Author | Dermot Murphy | 2026-08-14 | Git commit authorship on the source-branch commits merged via PR #50 |
| Reviewer | Dermot Murphy | 2026-08-14 | Self-review under CCD-MAN3-001 §3 single-engineer clause (per-PR reviews across the release window; CCD-DEV-001/DEV-002 apply) |
| Approver | Dermot Murphy | 2026-08-14 | PR #50 merge to `main` at 2026-08-14 09:03 UTC — `AllChecksPassed` gate satisfied |

Per CCD-MAN3-001 §3, for a single-engineer team the same individual fills all three roles; the process record (git commit + PR merge event) provides the auditable evidence.

---

*End of CCD-SVD-2.21.1-r4 v1.00*
