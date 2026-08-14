# Configuration Management Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SUP8-001 |
| **Version** | v1.07 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SUP.8 — Configuration Management |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added CI-010 (MISRA C:2012 rule-texts asset) under configuration control. |
| v1.02 | 2026-08-13 | Dermot Murphy | Added CI-011 (release records: SVD instances and QT records) under configuration control, aligned with CCD-SPL2-001 §7. |
| v1.03 | 2026-08-13 | Dermot Murphy | §5.3 Release job now Active; §5.4 DockerHub secrets added; document DockerHub publishing alongside GHCR (issue #4). |
| v1.04 | 2026-08-13 | Dermot Murphy | §5.3 Release row: note skip condition when merged diff touches no image-affecting files (issue #24). |
| v1.05 | 2026-08-13 | Dermot Murphy | Added CI-012 (deviation records: CCD-DEV-001, CCD-DEV-002) under configuration control; promote Draft -> Released (issue #23). |
| v1.06 | 2026-08-13 | Dermot Murphy | §7 Configuration Audit: two audits (registry digest round-trip and version smoke on published image) now executed automatically by the `Release` job (issue #32, closes audit finding FIND-D). |
| v1.07 | 2026-08-13 | Dermot Murphy | Added CI-013 (Claude Code memory mirror at `documents/aspice/claude_memory/`, maintained by `scripts/sync_claude_memory.py` via `claude-memory-sync` local pre-commit hook) under configuration control (issue #44). |

---

## 1. Introduction

This document defines the Configuration Management (CM) plan for the CppCheckDocker project. It covers identification, control, status accounting, and auditing of all configuration items in accordance with ASPICE v4 process SUP.8.

---

## 2. Configuration Items

The following items are under configuration control:

| CI ID | Item | Location | Control Method |
|:--------------|:------------|:------------|:---------------|
| CI-001 | Dockerfile | `Dockerfile` | Git |
| CI-002 | Docker build-context exclusions | `.dockerignore` | Git |
| CI-003 | Test scripts and sample inputs | `test/` | Git |
| CI-004 | GitHub Actions workflows | `.github/workflows/` | Git |
| CI-005 | ASPICE documents (this set) | `documents/aspice/` | Git |
| CI-006 | Published container image | Container registry (`ghcr.io/<owner>/cppcheckdocker:<tag>`) | Registry tag |
| CI-007 | Upstream cppcheck source | External — `github.com/danmar/cppcheck` at tag `${CPPCHECK_VERSION}` | Build ARG pin |
| CI-008 | Base image | `ubuntu:${UBUNTU_VERSION}` on Docker Hub | Build ARG pin |
| CI-009 | Repository README and top-level docs | `README.md` | Git |
| CI-010 | MISRA C:2012 rule-texts asset | `documents/assets/misra_c_2012_for_cppcheck.txt` — MISRA Consortium file, CC BY-NC-ND 4.0. Bundled into runtime image at `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt`. Not modified from upstream release. | Git |
| CI-011 | Release records | `documents/aspice/records/CCD-SVD-<tag>.md` (Software Version Description per release, per CCD-SVD-001 template) and `documents/aspice/records/CCD-QTR-<tag>.md` (Qualification Test records per release) | Git |
| CI-012 | Process deviation records | `documents/aspice/CppCheckDocker_DEV001_Single_Engineer_Role_Collapse_Deviation.md` (CCD-DEV-001) and `documents/aspice/CppCheckDocker_DEV002_Independent_QA_Audit_Deviation.md` (CCD-DEV-002). Formal deviations issued under issue #23; retirement clauses recorded in each document. | Git |
| CI-013 | Claude Code memory mirror | `documents/aspice/claude_memory/` — per-project memory (`MEMORY.md` index plus individual feedback/project/reference/user records) mirrored from the developer's user-scope Claude Code memory directory by `scripts/sync_claude_memory.py`. Kept current by the `claude-memory-sync` local pre-commit hook. Preserves accumulated project lessons across machines and teammates. | Git |

---

## 3. Branching Strategy

The repository uses the following branch model:

| Branch Pattern | Purpose | Protection |
|:---------------|:------------|:------------|
| `main` | Production image releases | Protected; requires PR + CI pass |
| `develop` | Integration branch | Protected; requires PR + CI pass |
| `feature/**` | Feature development | Open; CI runs on push |
| `hotfix/**` | Urgent production fixes | Open; CI runs on push |

### 3.1 Merge Rules

- All changes must be submitted as Pull Requests
- CI pipeline (`AllChecksPassed` job) must pass before merge is permitted
- At least one review approval required before merge to `develop` or `main`
- Direct commits to `main` or `develop` are prohibited

---

## 4. Versioning

### 4.1 Image Version

The published image tag follows the upstream cppcheck version plus a project-local revision suffix:

```
<cppcheck-version>-r<revision>
```

Example: `2.21.1-r1`, `2.21.1-r2` (for a rebuild against a new base image with the same cppcheck version).

The `revision` starts at `1` for each new cppcheck version and increments on any change to the Dockerfile, base image, or build options that alters the resulting image.

The upstream cppcheck version is defined in the `Dockerfile` via `ARG CPPCHECK_VERSION=...`. The revision is defined in the `.github/workflows/` release job.

Additional floating tags may be published:
- `latest` — most recent release
- `<cppcheck-major>.<minor>` — latest revision for that cppcheck minor version

Floating tags are best-effort and are not covered by strict immutability guarantees. Consumers that require reproducibility should pin to `<cppcheck-version>-r<revision>` or to the image digest.

### 4.2 Release Tagging

Releases are created by a GitHub Actions job when a build succeeds on `main`. The release tag matches the image tag `<cppcheck-version>-r<revision>`.

Release artefacts (published to the container registry):
- `ghcr.io/<owner>/cppcheckdocker:<cppcheck-version>-r<revision>`
- `ghcr.io/<owner>/cppcheckdocker:latest` (updated to the same image)

GitHub Release notes include the resolved image digest and a link to the upstream cppcheck release notes.

---

## 5. Build Environment

### 5.1 Runners

CI builds run on GitHub-hosted `ubuntu-latest` runners using Docker with BuildKit enabled.

### 5.2 Build Command

```bash
docker build \
  --build-arg CPPCHECK_VERSION=2.21.1 \
  --build-arg UBUNTU_VERSION=24.04 \
  -t cppcheck:2.21.1 .
```

### 5.3 CI Build Jobs

| Job | Trigger | Purpose |
|:--------------|:------------|:------------|
| `Build-Image` | Every push | Build the Docker image; fail on any error |
| `Verify-Version` | Every push | Run `cppcheck --version` inside the image; check the string |
| `Run-Integration-Tests` | Every push | Execute test scripts against known-defective sample sources |
| `Lint-Dockerfile` (planned) | Every push | Run hadolint against the Dockerfile |
| `Scan-Image` (planned) | Every push | Trivy / Docker Scout vulnerability scan |
| `Release` | Push to `main` when the merged diff touches an image-affecting file | Build image, push to GHCR and DockerHub with `<version>-r<rev>` and `latest` tags, create annotated git tag and GitHub Release, record image digest in the Release body. **Skip condition:** the job runs on every push to `main` but early-exits (emitting a `::notice::` line and returning success without publishing) when the diff `github.event.before..github.sha` touches none of `Dockerfile`, `.dockerignore`, `documents/assets/misra_c_2012_for_cppcheck.txt`, or `.github/workflows/build.yml`. Skip is implemented via `dorny/paths-filter@v3.0.4` — see build.yml. Rationale: doc-only, workflow-only-non-image, or test-only merges to `main` should not consume a revision number. |

### 5.4 GitHub Actions Secrets

| Secret | Purpose | Scope |
|:--------------|:------------|:------------|
| `GITHUB_TOKEN` | Built-in token used by the `Release` job to push to GitHub Container Registry (`ghcr.io`) and create the GitHub Release. No manual configuration required. | Automatic per workflow run |
| `DOCKERHUB_USERNAME` | DockerHub user account that owns the target repository `docker.io/<user>/cppcheckdocker`. | Repository secret (Settings → Secrets and variables → Actions) |
| `DOCKERHUB_TOKEN` | DockerHub personal access token with `Read, Write, Delete` scope on the target repository. Not the account password. | Repository secret |
| `WIKI_TOKEN` | Classic PAT with `repo` scope used by the `Publish-Wiki` job. `GITHUB_TOKEN` cannot push to `.wiki.git` and is not a substitute. | Repository secret |

> **One-time setup for `ghcr.io` publishing:**
> 1. Under repository Settings → Actions → General → Workflow permissions, grant "Read and write permissions" so `GITHUB_TOKEN` can push packages.
> 2. On first push, the package appears under the owner's Packages tab; set visibility (public / internal / private) as needed.

> **One-time setup for DockerHub publishing:**
> 1. Create a DockerHub repository `<user>/cppcheckdocker`.
> 2. Create a DockerHub PAT under Account Settings → Security → New Access Token with `Read, Write, Delete` scope, expiry set per your org's policy.
> 3. Store the username as repository secret `DOCKERHUB_USERNAME` and the token as `DOCKERHUB_TOKEN`.
> 4. The `Release` job on the next push to `main` will publish both `<version>-r<rev>` and `latest` tags to both registries.

---

## 6. Document Version Control

All ASPICE documents are stored in Git under `documents/aspice/`. Document versions are tracked via the Document Control table in each document. When a document is updated:
1. Increment the version number in the document header
2. Add a row to the Document Control table with date, author, and change description
3. Commit the updated document with a descriptive commit message

---

## 7. Configuration Audit

A configuration audit is performed **automatically on every release** by the `Release` job in `.github/workflows/build.yml`, and additionally on demand:
- Automatically after every image publish to GHCR and DockerHub (see §7.1)
- After any change to the build environment (base image update, cppcheck version bump) - covered by the automated audit on the resulting release
- As part of the internal ASPICE audit process (e.g., `documents/aspice/CppCheckDocker_AUD_YYYY-MM-DD_ASPICE_L2_Audit.md`)

### 7.1 Automated audit steps

Two audit steps run inside the `Release` job immediately after the GitHub Release is created:

1. **Registry digest round-trip** - `Configuration audit - registry digest round-trip (SUP.8 §7)` step. For each of GHCR and DockerHub, runs `docker buildx imagetools inspect <tag> --format '{{.Manifest.Digest}}'` and compares against the digest reported by the earlier `docker/build-push-action` step. Fails the release on any mismatch with a `::error::` line. On success, emits a `::notice::` line recording the confirmed digest.
2. **Version smoke on the published image** - `Configuration audit - version smoke on published image (SUP.8 §7)` step. Pulls the just-published GHCR image, runs `cppcheck --version`, and compares the string against `Cppcheck ${CPPCHECK_VERSION}` from the workflow env. Fails on mismatch.

Both steps carry the `if: steps.filter.outputs.image == 'true'` guard from CR-24 so they only run when the merged diff actually triggered a publish.

### 7.2 Additional CI-based evidence available at audit time

Beyond the two automated audits, the following observable facts are recorded per release and available for retrospective audit:

- All CI jobs (Lint, Build-Image, Verify-Version, Run-Integration-Tests, Scan-Image, AllChecksPassed) passed for the release commit - captured in the GitHub Actions run for that commit.
- Published image digest is captured in the GitHub Release notes body (see the `Create GitHub Release` step in `build.yml`) and in the per-release SVD instance under `documents/aspice/records/CCD-SVD-<tag>.md` §5.1.
- The revision counter is self-authoritative: the `Compute revision suffix` step derives `-r<n>` from existing `v<version>-r*` git tags, so skipping a release (per CR-24 paths-filter guard) leaves the counter intact.

---

*End of CCD-SUP8-001 v1.06*
