# Software Requirements Specification
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SWE1-001 |
| **Version** | v1.02 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.1 — Software Requirements Analysis |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added FEAT-011 (MISRA C:2012 support) and SR-028/SR-029 (bundled rule-texts file and `misra-c2012` shim addon); added corresponding traceability rows. |
| v1.02 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Scope](#2-scope)
3. [Terms and Abbreviations](#3-terms-and-abbreviations)
4. [References](#4-references)
5. [Product Feature Requirements](#5-product-feature-requirements)
6. [Software Requirements — Image Build](#6-software-requirements--image-build)
7. [Software Requirements — Cppcheck Provisioning](#7-software-requirements--cppcheck-provisioning)
8. [Software Requirements — Runtime Behaviour](#8-software-requirements--runtime-behaviour)
9. [Software Requirements — Security](#9-software-requirements--security)
10. [Software Requirements — Reproducibility and Versioning](#10-software-requirements--reproducibility-and-versioning)
11. [Software Requirements — Performance and Size](#11-software-requirements--performance-and-size)
12. [Software Requirements — Non-Functional Requirements](#12-software-requirements--non-functional-requirements)
13. [Requirements Traceability Summary](#13-requirements-traceability-summary)

---

## 1. Introduction

This document is the Software Requirements Specification (SRS) for the CppCheckDocker project — a Docker image that packages the latest release of the cppcheck static analysis tool on an Ubuntu LTS base for consumption by other projects in GitHub Actions CI pipelines. It is produced in accordance with ASPICE v4 process SWE.1 (Software Requirements Analysis).

The SRS defines all software requirements derived from the project's product features and stakeholder needs. It forms the primary input to the Software Architectural Design Document (CCD-SWE2-001) and provides the top-level traceability anchor for all subsequent work products.

---

## 2. Scope

**Deliverable:** OCI-compliant container image
**Base:** Ubuntu 24.04 LTS (parametrised)
**Payload:** cppcheck built from upstream source at a pinned release tag
**Distribution:** GitHub Container Registry (`ghcr.io`) — free for public and reasonable-limit private images
**Consumer:** GitHub Actions workflows in other Sensoteq (and third-party) repositories

This SRS covers the Dockerfile, its `.dockerignore`, the CI workflows that build and publish the image, and the test assets that verify it. It excludes the upstream cppcheck source (owned by the `danmar/cppcheck` project) and the Ubuntu base image (owned by Canonical), both of which are treated as third-party COTS components.

---

## 3. Terms and Abbreviations

| Term | Definition |
|:--------------|:------------|
| ARG | Docker build-time argument declared with the `ARG` instruction |
| ASPICE | Automotive SPICE (Software Process Improvement and Capability dEtermination) |
| CI | Continuous Integration |
| COTS | Commercial Off-The-Shelf |
| CMake | Cross-platform build system generator used by cppcheck |
| CVE | Common Vulnerabilities and Exposures |
| Dockerfile | Text file that defines a Docker image build |
| Entrypoint | Docker image `ENTRYPOINT` instruction — the executable run when the container starts |
| GHCR | GitHub Container Registry (`ghcr.io`) |
| LTS | Long Term Support (Ubuntu release designation) |
| OCI | Open Container Initiative image specification |
| PCRE | Perl-Compatible Regular Expressions library — optional cppcheck dependency |
| SDK | Software Development Kit |

---

## 4. References

| Req Identifier | Document | Number |
|:--------------|:------------|:------------|
| REF-01 | Software Architectural Design Document | CCD-SWE2-001 |
| REF-02 | Software Detailed Design Document | CCD-SWE3-001 |
| REF-03 | Software Unit Verification Plan | CCD-SWE4-001 |
| REF-04 | Software Integration Test Plan | CCD-SWE5-001 |
| REF-05 | Software Qualification Test Specification | CCD-SWE6-001 |
| REF-06 | Configuration Management Plan | CCD-SUP8-001 |
| REF-07 | Software Quality Assurance Plan | CCD-SUP1-001 |
| REF-08 | Master Traceability Matrix | CCD-RTM-001 |
| REF-09 | Upstream cppcheck project | https://github.com/danmar/cppcheck |
| REF-10 | Cppcheck manual | https://cppcheck.sourceforge.io/manual.pdf |
| REF-11 | Ubuntu base image | https://hub.docker.com/_/ubuntu |
| REF-12 | OCI Image Specification | https://github.com/opencontainers/image-spec |

---

## 5. Product Feature Requirements

The following product feature requirements are the primary inputs to the software requirements. They are derived from the project rationale (see README and MAN.3 §2) and stakeholder needs.

| Feature ID  | Feature Requirement | Priority |
|:--------------|:---------------------|:------------|
| **FEAT-001** | The image shall provide a working `cppcheck` executable inside an Ubuntu Linux container. | Mandatory |
| **FEAT-002** | The image shall provide a cppcheck version at least as recent as the newest release available on the upstream project at the time of image build. | Mandatory |
| **FEAT-003** | The image shall be runnable on GitHub Actions hosted Linux runners (`ubuntu-latest`) without additional package installation. | Mandatory |
| **FEAT-004** | The image shall support analysis of C and C++ source trees mounted from the host filesystem via a bind mount. | Mandatory |
| **FEAT-005** | The image shall be reproducible: two builds from the same Git commit and the same build arguments shall produce functionally equivalent images. | Mandatory |
| **FEAT-006** | The image shall be publishable to GitHub Container Registry (`ghcr.io`) with immutable version tags. | Mandatory |
| **FEAT-007** | The image shall be usable as the container of a GitHub Actions step via `container:` or `uses: docker://…` syntax. | Mandatory |
| **FEAT-008** | The image shall run as a non-root user by default to reduce security exposure on shared runners. | Mandatory |
| **FEAT-009** | The image shall not contain build tools, source trees, or credentials after the build completes. | Mandatory |
| **FEAT-010** | The image shall provide the standard cppcheck addons and cfg files necessary for the tool's advertised functionality. | Mandatory |
| **FEAT-011** | The image shall enable MISRA C:2012 static analysis via cppcheck's `misra` addon, using the MISRA-supplied rule-texts file so violations are reported with the readable guideline text (not only rule numbers). | Mandatory |

---

## 6. Software Requirements — Image Build

| Req Identifier | Requirement | Source | Priority | Verification |
|:--------------|:-------------|:------------|:------------|:--------------|
| **SR-001** | The Dockerfile shall use an Ubuntu LTS base image, parameterised via `ARG UBUNTU_VERSION` with a default of `24.04`. | FEAT-001, FEAT-005 | Mandatory | Review |
| **SR-002** | The Dockerfile shall use a multi-stage build: one stage (builder) installs build tools and compiles cppcheck; a second stage (runtime) contains only the runtime artefacts. | FEAT-009 | Mandatory | Review |
| **SR-003** | The builder stage shall install `build-essential`, `cmake`, `ninja-build`, `git`, `ca-certificates`, `libpcre3-dev`, and `python3` via `apt-get` and shall delete the apt lists after installation. | FEAT-001 | Mandatory | Review |
| **SR-004** | The builder stage shall clone the upstream cppcheck source at the tag specified by `ARG CPPCHECK_VERSION`. | FEAT-002, FEAT-005 | Mandatory | Test |
| **SR-005** | The builder stage shall build cppcheck using CMake with `CMAKE_BUILD_TYPE=Release`, `HAVE_RULES=ON`, and `USE_MATCHCOMPILER=ON`. | FEAT-001, FEAT-010 | Mandatory | Review |
| **SR-006** | The builder stage shall install cppcheck to `/opt/cppcheck` with files (cfg, platforms, addons) placed at `/opt/cppcheck/share/cppcheck/`. | FEAT-010 | Mandatory | Test |
| **SR-007** | The runtime stage shall install `libpcre3` and `python3` via `apt-get` and shall delete the apt lists after installation. | FEAT-001, FEAT-010 | Mandatory | Review |
| **SR-008** | The runtime stage shall copy `/opt/cppcheck` from the builder stage using `COPY --from=builder`. | FEAT-009 | Mandatory | Review |
| **SR-009** | The runtime stage shall not contain any of: `apt-get` sources for build dependencies, the cppcheck git working tree, CMake, or build compilers. | FEAT-009 | Mandatory | Test |
| **SR-010** | The `.dockerignore` file shall exclude `.git`, `documents/`, `test/`, and Markdown files from the build context. | FEAT-005, FEAT-009 | Mandatory | Review |

---

## 7. Software Requirements — Cppcheck Provisioning

| Req Identifier | Requirement | Source | Priority | Verification |
|:--------------|:-------------|:------------|:------------|:--------------|
| **SR-020** | The image shall expose the `cppcheck` executable on the `PATH` for interactive use. | FEAT-001 | Mandatory | Test |
| **SR-021** | The image `ENTRYPOINT` shall be set to `cppcheck` so that arguments passed to `docker run <image> …` are forwarded to cppcheck. | FEAT-007 | Mandatory | Test |
| **SR-022** | The image `CMD` shall default to `--help` so that `docker run <image>` with no arguments prints usage. | FEAT-001 | Mandatory | Test |
| **SR-023** | Running `cppcheck --version` inside the image shall return the version string corresponding to the pinned `CPPCHECK_VERSION`. | FEAT-002 | Mandatory | Test |
| **SR-024** | The image shall include the standard cppcheck `cfg` library files (e.g., `std.cfg`, `posix.cfg`, `windows.cfg`, `qt.cfg`) at `/opt/cppcheck/share/cppcheck/cfg/`. | FEAT-010 | Mandatory | Test |
| **SR-025** | The image shall include the cppcheck `platforms` XML files (e.g., `arm32-wchar_t4.xml`) at `/opt/cppcheck/share/cppcheck/platforms/`. | FEAT-010 | Mandatory | Test |
| **SR-026** | The image shall include `python3` at runtime so that cppcheck addons requiring Python (e.g., misra, y2038) can be invoked. | FEAT-010 | Mandatory | Test |
| **SR-027** | The image shall support cppcheck's `--enable=all` mode without missing configuration errors for standard C/C++ code. | FEAT-004, FEAT-010 | Mandatory | Test |
| **SR-028** | The image shall include the MISRA-supplied rule-texts file `misra_c_2012_for_cppcheck.txt` at `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt`. The file is redistributed under the MISRA Consortium's CC BY-NC-ND 4.0 licence. | FEAT-011 | Mandatory | Test |
| **SR-029** | The image shall provide an addon shim `/opt/cppcheck/share/cppcheck/addons/misra-c2012.py` that invokes cppcheck's stock `misra.py` with `--rule-texts` pre-supplied. Callers shall be able to invoke `cppcheck --enable=style --addon=misra-c2012 <src>` and receive MISRA rule violations tagged with their human-readable guideline text. | FEAT-011 | Mandatory | Test |

---

## 8. Software Requirements — Runtime Behaviour

| Req Identifier | Requirement | Source | Priority | Verification |
|:--------------|:-------------|:------------|:------------|:--------------|
| **SR-030** | The image shall define a non-root user named `cppcheck` with a shell of `/bin/bash` and a home directory of `/home/cppcheck`. | FEAT-008 | Mandatory | Test |
| **SR-031** | The image's default working directory shall be `/work`, and the container shall run as the `cppcheck` user by default. | FEAT-004, FEAT-008 | Mandatory | Test |
| **SR-032** | The image shall correctly analyse source files mounted at `/work` via `docker run -v <host>:/work[:ro]`. | FEAT-004 | Mandatory | Test |
| **SR-033** | The image shall return a non-zero exit code when cppcheck reports findings and the caller requests it via `--error-exitcode=<n>`. | FEAT-004 | Mandatory | Test |
| **SR-034** | The image shall return zero exit code when cppcheck completes analysis without findings, or when findings are present but the caller has not set `--error-exitcode`. | FEAT-004 | Mandatory | Test |
| **SR-035** | The image shall accept and correctly produce output in text, XML (`--xml`), and SARIF-compatible formats supported by the pinned cppcheck version. | FEAT-004 | Desirable | Test |
| **SR-036** | The image shall support invocation as a GitHub Actions step container: `container: ghcr.io/<owner>/cppcheckdocker:<tag>`. | FEAT-007 | Mandatory | Test |

---

## 9. Software Requirements — Security

| Req Identifier | Requirement | Source | Priority | Verification |
|:--------------|:-------------|:------------|:------------|:--------------|
| **SR-040** | The image shall not contain SSH keys, API tokens, cloud credentials, or `.env` files. | FEAT-009 | Mandatory | Review |
| **SR-041** | The image shall not contain a `.git` directory or Git history from either the CppCheckDocker repository or the cloned cppcheck source. | FEAT-009 | Mandatory | Test |
| **SR-042** | The image shall not run as `root` by default (see SR-030). Callers may still override with `--user 0:0` for special cases (this is not the default). | FEAT-008 | Mandatory | Test |
| **SR-043** | The image shall not open any network ports. It shall not include or start any long-running daemon. | FEAT-008 | Mandatory | Review |
| **SR-044** | The published image shall carry OCI image labels identifying its title, description, source repository, and licence. | FEAT-006 | Mandatory | Test |

---

## 10. Software Requirements — Reproducibility and Versioning

| Req Identifier | Requirement | Source | Priority | Verification |
|:--------------|:-------------|:------------|:------------|:--------------|
| **SR-050** | The Dockerfile shall accept `CPPCHECK_VERSION` and `UBUNTU_VERSION` as build ARGs so that the same source can produce images pinned to different upstream versions. | FEAT-005 | Mandatory | Test |
| **SR-051** | The default value of `CPPCHECK_VERSION` shall correspond to a released tag published by the upstream project at the time of the last update to this repository. | FEAT-002, FEAT-005 | Mandatory | Review |
| **SR-052** | The published image tag shall follow the format `<cppcheck-version>-r<revision>`; see CMP §4.1. | FEAT-006 | Mandatory | Review |
| **SR-053** | The published image digest shall be recorded in the GitHub Release notes for that release. | FEAT-005, FEAT-006 | Mandatory | Review |
| **SR-054** | Two consecutive builds of the same Git commit with the same build ARGs shall produce images whose runtime behaviour is functionally equivalent (the cppcheck binary and cfg content shall be byte-identical). | FEAT-005 | Desirable | Test |

---

## 11. Software Requirements — Performance and Size

| Req Identifier | Requirement | Source | Priority | Verification |
|:--------------|:-------------|:------------|:------------|:--------------|
| **SR-060** | The runtime image size shall not exceed 200 MB uncompressed. Regressions past this threshold require investigation and reviewer sign-off. | FEAT-009 | Mandatory | Test |
| **SR-061** | An end-to-end image build (cold cache) on a GitHub-hosted `ubuntu-latest` runner shall complete within 10 minutes. | FEAT-006 | Mandatory | Test |
| **SR-062** | Running `cppcheck --version` inside a freshly started container shall return within 3 seconds. | FEAT-001, FEAT-007 | Mandatory | Test |
| **SR-063** | The image's integration test suite shall complete within 3 minutes on a GitHub-hosted `ubuntu-latest` runner. | FEAT-004 | Mandatory | Test |

---

## 12. Software Requirements — Non-Functional Requirements

Non-functional requirements (NFRs) define the quality attributes and constraints that apply to the entire deliverable rather than to a specific functional capability. They are mandatory unless stated otherwise.

| Req Identifier | Non-Functional Requirement | Priority | Verification |
|:--------------|:----------------------------|:------------|:--------------|
| **NFR-001** | The Dockerfile shall conform to reasonable Docker best practices as enforced by hadolint at its default rule set (see QAPLAN §5.1). Zero errors permitted; warnings require justification. | Mandatory | Analysis |
| **NFR-002** | The published image shall have no known CVEs at CRITICAL or HIGH severity at the time of release, as assessed by trivy or Docker Scout (see QAPLAN §5.2). Exceptions require documented risk acceptance. | Mandatory | Analysis |
| **NFR-003** | The Dockerfile shall not use tag `:latest` for the base image; the base image tag shall be pinned via `ARG UBUNTU_VERSION`. | Mandatory | Review |
| **NFR-004** | The Dockerfile shall not install optional recommended packages via apt; `--no-install-recommends` shall be used on every `apt-get install`. | Mandatory | Review |
| **NFR-005** | All apt operations that install packages shall be followed by `rm -rf /var/lib/apt/lists/*` in the same `RUN` layer to avoid retaining apt indexes in the final image. | Mandatory | Review |
| **NFR-006** | The Dockerfile shall be authored so that layer count is kept low by combining related operations into a single `RUN` instruction where doing so improves cache efficiency without harming readability. | Desirable | Review |
| **NFR-007** | All documented requirements verifiable only by inspection (marked "Review") shall have a corresponding entry in the review checklist executed at each PR review. | Mandatory | Review |
| **NFR-008** | The Dockerfile shall carry `LABEL` metadata conforming to the OCI image-spec pre-defined annotation keys (`org.opencontainers.image.*`). | Mandatory | Test |
| **NFR-009** | The project shall not require a proprietary licence to build or use the image. All included components (Ubuntu base, cppcheck, dependencies) shall be under permissive or copyleft open-source licences compatible with redistribution. | Mandatory | Review |

---

## 13. Requirements Traceability Summary

The table below maps each software requirement to its parent feature and to the downstream work products that verify it. Non-functional requirements (NFR-001–NFR-009) are cross-cutting; they are verified by static analysis, CI gates, and design review rather than individual test cases. Full traceability is maintained in CCD-RTM-001.

| SR ID | Description Summary | Feature | Architecture Ref | Test Ref |
|:--------------|:---------------------|:------------|:-----------------|:------------|
| SR-001 | Ubuntu LTS base | FEAT-001 | ARC-IMG-001 | UVT-001 |
| SR-002 | Multi-stage build | FEAT-009 | ARC-IMG-002 | UVT-002 |
| SR-003 | Builder apt packages | FEAT-001 | ARC-BLD-001 | UVT-003 |
| SR-004 | Cppcheck source clone at tag | FEAT-002 | ARC-BLD-002 | UVT-004 |
| SR-005 | CMake build options | FEAT-001 | ARC-BLD-003 | UVT-005 |
| SR-006 | Install prefix /opt/cppcheck | FEAT-010 | ARC-BLD-004 | UVT-006 |
| SR-007 | Runtime apt packages | FEAT-001 | ARC-RUN-001 | UVT-007 |
| SR-008 | COPY --from=builder | FEAT-009 | ARC-RUN-002 | UVT-008 |
| SR-009 | No build tools in runtime | FEAT-009 | ARC-RUN-003 | UVT-009 |
| SR-010 | .dockerignore | FEAT-005 | ARC-IMG-003 | UVT-010 |
| SR-020 | cppcheck on PATH | FEAT-001 | ARC-RUN-004 | INT-001 |
| SR-021 | ENTRYPOINT=cppcheck | FEAT-007 | ARC-RUN-005 | INT-002 |
| SR-022 | CMD=--help | FEAT-001 | ARC-RUN-006 | INT-003 |
| SR-023 | --version returns pinned string | FEAT-002 | ARC-RUN-004 | QT-001 |
| SR-024 | cfg files present | FEAT-010 | ARC-BLD-004 | INT-004 |
| SR-025 | platforms XML present | FEAT-010 | ARC-BLD-004 | INT-005 |
| SR-026 | python3 at runtime | FEAT-010 | ARC-RUN-001 | INT-006 |
| SR-027 | --enable=all works | FEAT-004 | ARC-RUN-007 | INT-007 |
| SR-028 | MISRA rule-texts bundled | FEAT-011 | ARC-RUN-010 | UVT-060 |
| SR-029 | misra-c2012 shim addon | FEAT-011 | ARC-RUN-010 | UVT-061, INT-020, QT-015 |
| SR-030 | Non-root user cppcheck | FEAT-008 | ARC-RUN-008 | UVT-020 |
| SR-031 | WORKDIR /work | FEAT-004 | ARC-RUN-008 | UVT-021 |
| SR-032 | Analyse mounted /work | FEAT-004 | ARC-RUN-009 | INT-010 |
| SR-033 | Non-zero exit with --error-exitcode | FEAT-004 | ARC-RUN-007 | INT-011 |
| SR-034 | Zero exit without --error-exitcode | FEAT-004 | ARC-RUN-007 | INT-012 |
| SR-035 | XML / SARIF output | FEAT-004 | ARC-RUN-007 | INT-013 |
| SR-036 | Usable as GHA step container | FEAT-007 | ARC-INT-001 | QT-002 |
| SR-040 | No secrets | FEAT-009 | ARC-IMG-003 | UVT-030 |
| SR-041 | No .git directories | FEAT-009 | ARC-RUN-003 | UVT-031 |
| SR-042 | Runs non-root by default | FEAT-008 | ARC-RUN-008 | UVT-032 |
| SR-043 | No network ports | FEAT-008 | ARC-RUN-005 | UVT-033 |
| SR-044 | OCI labels | FEAT-006 | ARC-IMG-004 | UVT-034 |
| SR-050 | CPPCHECK_VERSION / UBUNTU_VERSION ARGs | FEAT-005 | ARC-BLD-002 | UVT-040 |
| SR-051 | Default CPPCHECK_VERSION current | FEAT-002 | ARC-BLD-002 | — |
| SR-052 | Image tag format | FEAT-006 | ARC-INT-001 | — |
| SR-053 | Digest recorded in release | FEAT-005 | ARC-INT-001 | — |
| SR-054 | Reproducible builds | FEAT-005 | ARC-BLD-002 | UVT-041 |
| SR-060 | Image size ≤ 200 MB | FEAT-009 | ARC-RUN-002 | UVT-050 |
| SR-061 | Cold build ≤ 10 min | FEAT-006 | ARC-BLD-003 | INT-020 |
| SR-062 | --version ≤ 3 s | FEAT-001 | ARC-RUN-004 | INT-021 |
| SR-063 | Integration suite ≤ 3 min | FEAT-004 | ARC-INT-002 | INT-022 |

*Full traceability is provided in CCD-RTM-001 — Master Traceability Matrix.*

---

*End of CCD-SWE1-001 v1.02*
