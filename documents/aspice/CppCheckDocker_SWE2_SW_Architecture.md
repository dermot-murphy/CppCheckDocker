# Software Architectural Design Document
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SWE2-001 |
| **Version** | v1.02 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.2 — Software Architectural Design |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added ARC-RUN-010 (MISRA shim addon) covering SR-028/SR-029 introduced in SRS v1.01. |
| v1.02 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architectural Objectives and Constraints](#2-architectural-objectives-and-constraints)
3. [Logical Architecture Overview](#3-logical-architecture-overview)
4. [Component Definitions and Responsibilities](#4-component-definitions-and-responsibilities)
5. [Image-Level Architecture](#5-image-level-architecture)
6. [Builder Stage Architecture](#6-builder-stage-architecture)
7. [Runtime Stage Architecture](#7-runtime-stage-architecture)
8. [External Interfaces](#8-external-interfaces)
9. [CI/CD Integration Architecture](#9-cicd-integration-architecture)
10. [Data Flow](#10-data-flow)
11. [Filesystem and User Model](#11-filesystem-and-user-model)
12. [Requirements Traceability](#12-requirements-traceability)

---

## 1. Introduction

This document is the Software Architectural Design Document (SADD) for the CppCheckDocker project — an Ubuntu-based Docker image packaging the cppcheck static analysis tool. It is produced in accordance with ASPICE v4 process SWE.2 (Software Architectural Design).

The SADD describes the decomposition of the deliverable into logical components (image stages, external interfaces, published tags, CI jobs) and their responsibilities. It provides the architectural basis from which the Software Detailed Design Document (CCD-SWE3-001) is derived, and establishes the component structure used for integration testing (CCD-SWE5-001).

**Parent document:** CCD-SWE1-001 Software Requirements Specification
**Child document:** CCD-SWE3-001 Software Detailed Design Document

---

## 2. Architectural Objectives and Constraints

### 2.1 Objectives

| Objective | Description |
|:--------------|:-------------|
| **Minimalism** | The runtime image must contain only what is required to execute cppcheck: the binary, its cfg/addons/platforms, and the runtime libraries it links against. |
| **Reproducibility** | Given the same Git commit and the same build ARGs, two builds must produce functionally equivalent images. This is achieved by pinning the base image tag and the cppcheck source tag. |
| **Isolation** | The build stage must not leak into the runtime stage. All build-only tooling (compilers, source trees, CMake) must remain in the discarded builder layer. |
| **CI-friendliness** | The image must be usable by GitHub Actions `container:` and step-container mechanisms without host-side dependency setup. |
| **Security** | Non-root execution by default; no long-running daemons; no embedded credentials. |
| **Portability** | The image must run unmodified on any OCI-compliant runtime (Docker Engine, containerd, Podman) on Linux amd64. |

### 2.2 Constraints

| Constraint | Description |
|:--------------|:-------------|
| **Base OS** | Ubuntu 24.04 LTS (parametrised via `ARG UBUNTU_VERSION`) |
| **CPU architecture** | linux/amd64 for the initial release; multi-arch (arm64) is a future feature flag |
| **Registry** | GitHub Container Registry (`ghcr.io`) — free public and reasonable-limit private hosting |
| **Runner** | GitHub Actions `ubuntu-latest` hosted runners for CI builds |
| **Upstream cppcheck build system** | CMake with Ninja — the Dockerfile follows cppcheck's supported build path |
| **Language** | The deliverable is a Dockerfile, not source code — no MISRA or C-style coding standard applies |

---

## 3. Logical Architecture Overview

The CppCheckDocker deliverable is composed of three externally visible artefacts and one internal build pipeline:

```
┌────────────────────────────────────────────────────────────────────────┐
│                 EXTERNAL ARTEFACTS (versioned via Git)                 │
├────────────────────────────────────────────────────────────────────────┤
│  Dockerfile   +   .dockerignore   +   .github/workflows/               │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ docker build
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          BUILD PIPELINE                                │
│  ┌──────────────────────────┐          ┌──────────────────────────┐   │
│  │  Stage 1: BUILDER        │  copy    │  Stage 2: RUNTIME        │   │
│  │  ubuntu:24.04            │──────▶   │  ubuntu:24.04            │   │
│  │  + build-essential       │  /opt/   │  + libpcre3              │   │
│  │  + cmake, ninja, git     │ cppcheck │  + python3               │   │
│  │  + libpcre3-dev, python3 │          │  + non-root user         │   │
│  │  + cppcheck source (tag) │          │  + ENTRYPOINT cppcheck   │   │
│  │  + compile → /opt/cppcheck│         │                          │   │
│  └──────────────────────────┘          └──────────┬───────────────┘   │
└──────────────────────────────────────────────────┼─────────────────────┘
                                                    │ docker push
                                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               PUBLISHED IMAGE (versioned via registry tag)             │
│         ghcr.io/<owner>/cppcheckdocker:<cppcheck-version>-r<rev>       │
│         ghcr.io/<owner>/cppcheckdocker:latest                          │
└────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ docker run … (consumer projects)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                            CONSUMER USE                                │
│    docker run --rm -v <src>:/work:ro <image> --enable=all <path>       │
│    or:  container: <image>  in a GitHub Actions job step                │
└────────────────────────────────────────────────────────────────────────┘
```

Dependencies flow strictly downward: the builder stage produces `/opt/cppcheck`; the runtime stage consumes it; the published image is consumed by external projects. There is no upward path.

---

## 4. Component Definitions and Responsibilities

| Component | Tag | Responsibility | Rules |
|:--------------|:------------|:---------------|:------------|
| Dockerfile | IMG | Declaratively defines both build stages and their inputs, outputs, and metadata | Uses only supported Dockerfile syntax (`# syntax=docker/dockerfile:1.7` pragma) |
| .dockerignore | IMG | Controls the build context so that project documents and Git history are not sent to the daemon | Must exclude anything not needed by any stage |
| Builder stage | BLD | Installs build tools, clones cppcheck source at pinned tag, configures with CMake, compiles, installs to `/opt/cppcheck` | Must not leave artefacts that could bloat runtime; all cleanup must occur in the same `RUN` layer |
| Runtime stage | RUN | Installs only runtime shared libraries (`libpcre3`, `python3`), copies `/opt/cppcheck` from builder, sets non-root user, working directory, ENTRYPOINT and CMD | Must not install compilers, source, or dev-headers |
| CI Workflow (`build.yml`) | INT | Builds the image on every push; runs unit and integration tests; on merges to `main` publishes to `ghcr.io` | Uses only GitHub-hosted runners; no self-hosted infrastructure required |
| Test harness (`test/`) | TST | Runs the built image against known-good and known-defective sample sources and compares to expected outputs | Must be executable both in CI and by developers locally |

---

## 5. Image-Level Architecture

### 5.1 Multi-Stage Structure (ARC-IMG-001, ARC-IMG-002)

```
┌───────────────────────────────────────────────┐
│  FROM ubuntu:${UBUNTU_VERSION} AS builder     │  ARC-BLD-*
│  (~700 MB layer stack; discarded)             │
└───────────────────────────────────────────────┘
                    │  COPY --from=builder /opt/cppcheck
                    ▼
┌───────────────────────────────────────────────┐
│  FROM ubuntu:${UBUNTU_VERSION} AS runtime     │  ARC-RUN-*
│  (~130 MB total; published)                   │
└───────────────────────────────────────────────┘
```

Only the runtime stage is tagged and pushed. The builder stage exists ephemerally in the local build cache.

### 5.2 Build Context Isolation (ARC-IMG-003)

The `.dockerignore` file at the repository root restricts the build context to only what the Dockerfile needs. Excluded items:
- `.git` (avoid leaking history and unnecessary transfer)
- `documents/` (ASPICE documents; not required at build time)
- `test/` (test assets; run by CI outside the image)
- `*.md` (README and similar; not required)

### 5.3 Image Metadata (ARC-IMG-004)

The runtime stage sets OCI-standard labels via `LABEL org.opencontainers.image.*`:
- `title`, `description`, `source` — machine-readable identity
- `licenses` — SPDX identifier of the effective licence (GPL-3.0-or-later, inherited from cppcheck)

---

## 6. Builder Stage Architecture

### 6.1 Build Dependencies (ARC-BLD-001)

Installed at build time only:

| Package | Purpose |
|:--------------|:------------|
| `build-essential` | GCC, g++, make, standard C/C++ headers |
| `cmake` | Build system generator used by cppcheck |
| `ninja-build` | Fast build backend (`cmake -G Ninja`) |
| `git` | Clones the cppcheck source at a specified tag |
| `ca-certificates` | HTTPS trust for `git clone` |
| `libpcre3-dev` | Development headers for PCRE (required by `HAVE_RULES=ON`) |
| `python3` | Sanity — some cppcheck build steps invoke Python; also used at runtime |

Removed after install via `rm -rf /var/lib/apt/lists/*` in the same `RUN` layer.

### 6.2 Source Acquisition (ARC-BLD-002)

The cppcheck source is fetched by:
```
git clone --depth 1 --branch "${CPPCHECK_VERSION}" \
    https://github.com/danmar/cppcheck.git .
```

- `--depth 1` — shallow clone (no history)
- `--branch "${CPPCHECK_VERSION}"` — pin to a tag

The `.git` directory is discarded when the builder stage is not carried into the runtime image. It never appears in the final image.

### 6.3 Compile (ARC-BLD-003)

```
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/cppcheck \
    -DHAVE_RULES=ON \
    -DUSE_MATCHCOMPILER=ON \
    -DFILESDIR=/opt/cppcheck/share/cppcheck
cmake --build build --parallel
cmake --install build
```

Key options:
- `HAVE_RULES=ON` — enables the PCRE-based custom rules feature
- `USE_MATCHCOMPILER=ON` — enables the token-match compiler for higher analysis speed
- `FILESDIR` — tells cppcheck at runtime where to find cfg and platforms XMLs

### 6.4 Install Layout (ARC-BLD-004)

After `cmake --install`, the tree at `/opt/cppcheck/` is:

```
/opt/cppcheck/
├── bin/
│   └── cppcheck                     — the executable
└── share/
    └── cppcheck/
        ├── cfg/                     — library configuration XMLs (std, posix, qt, …)
        ├── platforms/               — platform XMLs (arm32, riscv64, …)
        └── addons/                  — Python addons (misra, threadsafety, …)
```

This is the only content carried into the runtime stage.

---

## 7. Runtime Stage Architecture

### 7.1 Runtime Dependencies (ARC-RUN-001)

| Package | Purpose |
|:--------------|:------------|
| `libpcre3` | Shared library that cppcheck links against for rule matching |
| `python3` | Interpreter for cppcheck addons (misra, y2038, …) |

No compilers, no dev headers, no CMake, no source.

### 7.2 Payload Import (ARC-RUN-002)

```
COPY --from=builder /opt/cppcheck /opt/cppcheck
```

This is the only inter-stage dependency. The runtime image size is dominated by the base Ubuntu layer (~80 MB) plus this payload (~40 MB) plus `libpcre3` and `python3` (~10 MB).

### 7.3 Absence of Build Artefacts (ARC-RUN-003)

The runtime stage is a fresh `FROM ubuntu:${UBUNTU_VERSION}` — nothing carries over from the builder except what is explicitly `COPY --from=builder`ed. This guarantees SR-009 (no build tools) and SR-041 (no `.git`).

### 7.4 Executable Exposure (ARC-RUN-004)

```
ENV PATH="/opt/cppcheck/bin:${PATH}"
```

The `cppcheck` binary is on `PATH`, so calling `cppcheck` from any working directory resolves to `/opt/cppcheck/bin/cppcheck`.

### 7.5 Entrypoint (ARC-RUN-005)

```
ENTRYPOINT ["cppcheck"]
CMD ["--help"]
```

- `ENTRYPOINT` as JSON exec form — no shell wrapping, arguments passed directly.
- `CMD ["--help"]` — running the container with no additional arguments prints usage.

### 7.6 Default Command (ARC-RUN-006)

Documented in §7.5 — the default `CMD` is `--help`, so `docker run <image>` prints the cppcheck help text.

### 7.7 Analysis Behaviour (ARC-RUN-007)

Cppcheck exit codes and output formats are governed by cppcheck itself, not by the image. The image is a thin packaging layer. Callers use standard cppcheck flags such as `--error-exitcode=1`, `--xml`, `--enable=all`.

### 7.8 User and Working Directory (ARC-RUN-008)

```
RUN useradd --create-home --shell /bin/bash cppcheck
USER cppcheck
WORKDIR /work
```

The `cppcheck` user owns its own home; `/work` is the default working directory where consumers bind-mount their source tree. Consumers may override `-u`, `-w`, `--user` as needed.

### 7.9 Volume-Based Analysis (ARC-RUN-009)

The image does not create a volume — it does not need to. Consumers pass source via `-v <host>:/work[:ro]`; the working directory ensures cppcheck reads from there by default.

### 7.10 MISRA C:2012 Support (ARC-RUN-010)

The runtime stage bundles the MISRA-supplied rule-texts file and registers a shim addon so consumers can run MISRA C:2012 analysis without downloading additional assets.

**Components:**

| Path | Purpose |
|:--------------|:------------|
| `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt` | MISRA Consortium's official rule-texts file (CC BY-NC-ND 4.0). Not modified from the upstream release. |
| `/opt/cppcheck/share/cppcheck/addons/misra-c2012.py` | Shim script that invokes `misra.py` with `--rule-texts=/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt` prepended, then forwards all other cppcheck-supplied arguments unchanged via `os.execvp`. |

**Consumer invocation:**

```
cppcheck --enable=style --addon=misra-c2012 --cppcheck-build-dir=<dir> <src>
```

`--enable=style` is required because MISRA violations are emitted at severity `style`. `--cppcheck-build-dir=<dir>` names a writable directory for the addon's intermediate `.dump` files; this is essential when `/work` is bind-mounted read-only.

**Design rationale — why a `.py` shim rather than a `.json` config:** cppcheck's `--addon=<name>` resolver looks for `<name>.py` only. A `<name>.json` next to `misra.py` in the addons directory would be silently ignored. The shim is the smallest surface area that gives consumers a clean invocation while leaving cppcheck's stock `misra.py` unmodified.



The image does not create a volume — it does not need to. Consumers pass source via `-v <host>:/work[:ro]`; the working directory ensures cppcheck reads from there by default.

---

## 8. External Interfaces

### 8.1 Container Registry Interface

| Interface | Detail |
|:--------------|:------------|
| Registry | `ghcr.io/<owner>/cppcheckdocker` |
| Tags | `<cppcheck-version>-r<revision>`, `latest`, `<cppcheck-major>.<minor>` |
| Auth (push) | GitHub Actions `GITHUB_TOKEN` with `packages: write` permission |
| Auth (pull) | Public — no auth required for public images |
| Manifest format | OCI |

### 8.2 Consumer Interface

Consumers interact with the image in two forms:

**Form 1 — `docker run`:**
```
docker run --rm -v "${PWD}:/work:ro" ghcr.io/<owner>/cppcheckdocker:<tag> \
    --enable=all --error-exitcode=1 src/
```

**Form 2 — GitHub Actions step container:**
```yaml
jobs:
  cppcheck:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/<owner>/cppcheckdocker:<tag>
    steps:
      - uses: actions/checkout@v4
      - run: cppcheck --enable=all --error-exitcode=1 src/
```

### 8.3 Upstream Cppcheck Interface

Read-only. The Dockerfile depends on `danmar/cppcheck` at a specified tag. Upstream API surface consumed:
- `git clone --branch <tag>` — releases named `<major>.<minor>[.<patch>]`
- CMake build options — the Dockerfile depends on `HAVE_RULES`, `USE_MATCHCOMPILER`, `CMAKE_INSTALL_PREFIX`, `FILESDIR` remaining stable option names

---

## 9. CI/CD Integration Architecture

### 9.1 CI Jobs (ARC-INT-001)

```
    push / pull_request
           │
           ▼
    ┌──────────────┐
    │ Build-Image  │  docker build …
    └──────┬───────┘
           │
           ▼
    ┌────────────────┐
    │ Verify-Version │  docker run … --version
    └──────┬─────────┘
           │
           ▼
    ┌───────────────────────┐
    │ Run-Integration-Tests │  test/run.sh
    └──────┬────────────────┘
           │
           ▼   (only on main)
    ┌──────────────┐
    │  Release     │  docker push ghcr.io/…
    └──────────────┘
```

### 9.2 Test Harness (ARC-INT-002)

The test harness at `test/` contains:
- Sample `.c` and `.cpp` files with known defects
- Expected output snippets
- A driver script that invokes the built image, captures output, and asserts

The harness is executed both in CI and by developers locally with a single command:
```
test/run.sh <image-tag>
```

---

## 10. Data Flow

### 10.1 Build-Time Data Flow

```
GitHub (danmar/cppcheck.git @ tag)
    │
    │ git clone --depth 1 --branch <tag>
    ▼
Builder container /src
    │
    │ cmake configure + build + install
    ▼
Builder container /opt/cppcheck
    │
    │ COPY --from=builder /opt/cppcheck /opt/cppcheck
    ▼
Runtime image /opt/cppcheck
    │
    │ docker push
    ▼
ghcr.io/<owner>/cppcheckdocker:<tag>
```

### 10.2 Runtime Data Flow (Consumer)

```
Host filesystem: src/*.c
    │
    │ -v <src>:/work:ro
    ▼
Runtime container /work
    │
    │ cppcheck --enable=all src/
    ▼
stdout: analysis results
stderr: progress / errors
exit code: 0 (default) or as per --error-exitcode
```

---

## 11. Filesystem and User Model

### 11.1 Runtime Image Filesystem (relevant paths)

| Path | Owner | Content |
|:--------------|:------------|:------------|
| `/opt/cppcheck/bin/` | root:root | `cppcheck` executable |
| `/opt/cppcheck/share/cppcheck/cfg/` | root:root | Library configuration XMLs |
| `/opt/cppcheck/share/cppcheck/platforms/` | root:root | Platform XMLs |
| `/opt/cppcheck/share/cppcheck/addons/` | root:root | Python addons |
| `/home/cppcheck/` | cppcheck:cppcheck | Home directory (empty) |
| `/work/` | root:root (empty) | Default working directory; typically bind-mounted at runtime |

`/opt/cppcheck` remains root-owned but world-readable and world-executable — the `cppcheck` user can run the binary without needing ownership.

### 11.2 User Model

- **Default runtime user:** `cppcheck` (non-root)
- **Shell:** `/bin/bash` (available because `useradd --create-home --shell /bin/bash`)
- **Consumer override:** `docker run -u 0:0 …` (root) or `-u $(id -u):$(id -g) …` (host user) is supported

---

## 12. Requirements Traceability

The table below maps software requirements from CCD-SWE1-001 to the architectural elements defined in this document.

| SR ID | Requirement Summary | Architecture Element(s) |
|:--------------|:---------------------|:------------------------|
| SR-001 | Ubuntu LTS base | ARC-IMG-001, ARC-BLD-002, ARC-RUN-002 |
| SR-002 | Multi-stage build | ARC-IMG-001, ARC-IMG-002 |
| SR-003 | Builder apt packages | ARC-BLD-001 |
| SR-004 | Source clone at tag | ARC-BLD-002 |
| SR-005 | CMake build options | ARC-BLD-003 |
| SR-006 | Install prefix | ARC-BLD-004 |
| SR-007 | Runtime apt packages | ARC-RUN-001 |
| SR-008 | COPY --from=builder | ARC-RUN-002 |
| SR-009 | No build tools in runtime | ARC-RUN-003 |
| SR-010 | .dockerignore | ARC-IMG-003 |
| SR-020 | cppcheck on PATH | ARC-RUN-004 |
| SR-021 | ENTRYPOINT | ARC-RUN-005 |
| SR-022 | CMD --help | ARC-RUN-006 |
| SR-023 | --version returns pinned | ARC-BLD-002, ARC-RUN-004 |
| SR-024–SR-025 | cfg / platforms present | ARC-BLD-004 |
| SR-026 | python3 runtime | ARC-RUN-001 |
| SR-027 | --enable=all works | ARC-RUN-007 |
| SR-028 | MISRA rule-texts bundled | ARC-RUN-010 |
| SR-029 | misra-c2012 shim addon | ARC-RUN-010 |
| SR-030–SR-031 | Non-root user; WORKDIR | ARC-RUN-008 |
| SR-032 | Analyse mounted /work | ARC-RUN-009 |
| SR-033–SR-035 | Exit codes / output formats | ARC-RUN-007 |
| SR-036 | GHA container step | ARC-INT-001 |
| SR-040 | No secrets | ARC-IMG-003, ARC-RUN-003 |
| SR-041 | No .git | ARC-RUN-003 |
| SR-042–SR-043 | Non-root default; no ports | ARC-RUN-005, ARC-RUN-008 |
| SR-044 | OCI labels | ARC-IMG-004 |
| SR-050–SR-054 | Reproducibility / versioning | ARC-BLD-002, ARC-INT-001 |
| SR-060 | Image size | ARC-RUN-002 |
| SR-061 | Cold build time | ARC-BLD-003 |
| SR-062 | --version time | ARC-RUN-004 |
| SR-063 | Integration suite time | ARC-INT-002 |

*Full traceability provided in CCD-RTM-001.*

---

*End of CCD-SWE2-001 v1.02*
