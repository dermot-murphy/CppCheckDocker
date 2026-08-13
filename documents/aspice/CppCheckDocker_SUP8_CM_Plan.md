# Configuration Management Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SUP8-001 |
| **Version** | v1.03 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Draft |
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
| `Release` | Push to `main` | Build image, push to GHCR and DockerHub with `<version>-r<rev>` and `latest` tags, create annotated git tag and GitHub Release, record image digest in the Release body |

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

A configuration audit shall be performed:
- Before each production release to verify the published image matches the tagged source
- After any change to the build environment (base image update, cppcheck version bump)
- As part of the internal ASPICE audit process

The audit checks:
- Published image digest matches the CI-produced digest for the release commit
- `cppcheck --version` output in the published image matches `CPPCHECK_VERSION` in the tagged `Dockerfile`
- All CI jobs passed for the release commit

---

*End of CCD-SUP8-001 v1.03*
