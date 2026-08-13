# Software Detailed Design Document
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SWE3-001 |
| **Version** | v1.02 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.3 — Software Detailed Design and Unit Construction |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added §3.5 MISRA C:2012 Rule-Texts and Shim Addon; updated §3.4 layer summary and traceability rows for SR-028/SR-029. |
| v1.02 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Design Conventions](#2-design-conventions)
3. [Dockerfile Detailed Design](#3-dockerfile-detailed-design)
4. [.dockerignore Detailed Design](#4-dockerignore-detailed-design)
5. [CI Workflow Detailed Design](#5-ci-workflow-detailed-design)
6. [Test Harness Detailed Design](#6-test-harness-detailed-design)
7. [Error Handling Design](#7-error-handling-design)
8. [Requirements Traceability](#8-requirements-traceability)

---

## 1. Introduction

This document is the Software Detailed Design Document (SDDD) for the CppCheckDocker project. It is produced in accordance with ASPICE v4 process SWE.3 (Software Detailed Design and Unit Construction).

The SDDD describes the internal design of each deliverable file: the Dockerfile instruction-by-instruction, the `.dockerignore` rules, the GitHub Actions workflow jobs, and the test harness. It provides the complete specification from which unit verification (CCD-SWE4-001) is derived.

**Parent document:** CCD-SWE2-001 Software Architectural Design Document
**Child document:** CCD-SWE4-001 Software Unit Verification Plan

---

## 2. Design Conventions

### 2.1 Dockerfile Conventions

| Item | Convention |
|:--------------|:------------|
| Syntax pragma | `# syntax=docker/dockerfile:1.7` at the top of the file to enable modern buildkit features |
| ARG placement | Global ARGs before first `FROM`; per-stage ARGs re-declared inside each stage that uses them |
| RUN grouping | Related shell commands combined into a single `RUN` with `\` continuations to reduce layer count |
| apt hygiene | Every `apt-get install` is preceded by `apt-get update` and followed by `rm -rf /var/lib/apt/lists/*` in the same `RUN` |
| Package install flags | `--no-install-recommends` always; `-y` to avoid interactive prompts; `DEBIAN_FRONTEND=noninteractive` as an ARG |
| Instructions vs shell | Prefer exec-form JSON arrays for `ENTRYPOINT`, `CMD` — no shell wrapping |
| Label conventions | `org.opencontainers.image.*` keys only |

### 2.2 Naming Conventions

| Item | Convention | Example |
|:--------------|:------------|:------------|
| Build stage names | Lowercase, hyphenless | `builder`, `runtime` |
| ARG names | Uppercase snake_case | `CPPCHECK_VERSION`, `UBUNTU_VERSION` |
| Install prefix | `/opt/cppcheck` | Predictable, avoids collision with system paths |
| Runtime user | `cppcheck` | Matches the tool name |
| Runtime WORKDIR | `/work` | Short, distinct from `/tmp` or `/home/*` |

### 2.3 File Structure

```
Repository root/
├── Dockerfile               — main deliverable
├── .dockerignore            — build-context exclusions
├── README.md                — user-facing summary
├── .github/
│   └── workflows/
│       └── build.yml        — CI pipeline
├── test/
│   ├── run.sh               — integration test driver
│   ├── samples/
│   │   ├── clean.c          — file that produces no findings
│   │   ├── buggy.c          — file that produces known findings
│   │   └── ...
│   └── expected/            — expected output snippets
└── documents/
    └── aspice/              — ASPICE work products (this document set)
```

---

## 3. Dockerfile Detailed Design

**File:** `Dockerfile`
**Architecture ref:** ARC-IMG-001, ARC-IMG-002

### 3.1 Header and Global ARGs (ARC-IMG-001)

```dockerfile
# syntax=docker/dockerfile:1.7

ARG UBUNTU_VERSION=24.04
ARG CPPCHECK_VERSION=2.21.1
```

**Rationale:**
- Buildkit syntax pragma enables cache mounts, heredocs, and other modern features.
- Global ARGs declared before `FROM` so they can be used in the `FROM` line itself.
- `CPPCHECK_VERSION` default is the latest tagged release at the time of the last documentation update. Bumping this value is the primary maintenance operation for this project.

### 3.2 Builder Stage (ARC-BLD-*)

```dockerfile
FROM ubuntu:${UBUNTU_VERSION} AS builder

ARG CPPCHECK_VERSION
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ninja-build \
        git \
        ca-certificates \
        libpcre3-dev \
        python3 \
    && rm -rf /var/lib/apt/lists/*
```

**Design notes:**
- `ARG CPPCHECK_VERSION` re-declared inside the stage — Dockerfile scoping requires this to make the global ARG visible after `FROM`.
- `DEBIAN_FRONTEND=noninteractive` set as an ARG (not ENV) so it does not persist beyond build time. This suppresses interactive prompts (`tzdata`, `keyboard-configuration`) during `apt install`.
- The apt install list is alphabetised for readability and git-diff friendliness.

```dockerfile
WORKDIR /src
RUN git clone --depth 1 --branch "${CPPCHECK_VERSION}" \
        https://github.com/danmar/cppcheck.git .
```

**Design notes:**
- `WORKDIR /src` — clone target; distinct from `/opt/cppcheck` (install prefix).
- `--depth 1` — shallow; the tag alone is sufficient.
- `--branch "${CPPCHECK_VERSION}"` — this works for both branches and tags in `git clone`.

```dockerfile
RUN cmake -S . -B build -G Ninja \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/cppcheck \
        -DHAVE_RULES=ON \
        -DUSE_MATCHCOMPILER=ON \
        -DFILESDIR=/opt/cppcheck/share/cppcheck \
    && cmake --build build --parallel \
    && cmake --install build

RUN /opt/cppcheck/bin/cppcheck --version
```

**Design notes:**
- Three cmake calls combined into one `RUN` — they share nothing with what follows and produce a single layer.
- `--parallel` uses all available cores automatically (default is `nproc`).
- `FILESDIR` set explicitly so the runtime binary knows where to find cfgs regardless of `CMAKE_INSTALL_PREFIX` — this insulates against future upstream default changes.
- The final `RUN /opt/cppcheck/bin/cppcheck --version` is a build-time smoke test. If cppcheck cannot be invoked, the build fails immediately in the builder stage with a clear error before the runtime stage even starts.

### 3.3 Runtime Stage (ARC-RUN-*)

```dockerfile
FROM ubuntu:${UBUNTU_VERSION} AS runtime

ARG CPPCHECK_VERSION
ARG DEBIAN_FRONTEND=noninteractive

LABEL org.opencontainers.image.title="cppcheck" \
      org.opencontainers.image.description="Static analysis tool for C/C++ (cppcheck) on Ubuntu" \
      org.opencontainers.image.source="https://github.com/danmar/cppcheck" \
      org.opencontainers.image.licenses="GPL-3.0-or-later"
```

**Design notes:**
- Labels placed early so they are captured even if later instructions fail.
- Licence is `GPL-3.0-or-later` — inherited from cppcheck. Ubuntu's own licence terms are permissive for base-image redistribution.

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpcre3 \
        python3 \
    && rm -rf /var/lib/apt/lists/*
```

**Design notes:**
- Runtime-only shared libraries; strictly a subset of what the builder needed.
- `libpcre3` — cppcheck's rules engine dynamically links against this.
- `python3` — required by cppcheck addons (misra, y2038, threadsafety, …).

```dockerfile
COPY --from=builder /opt/cppcheck /opt/cppcheck

ENV PATH="/opt/cppcheck/bin:${PATH}"
```

**Design notes:**
- Single-line copy — no filtering necessary because the builder installed exactly what runtime needs.
- `PATH` prepended so callers can invoke `cppcheck` without full path.

```dockerfile
RUN useradd --create-home --shell /bin/bash cppcheck
USER cppcheck
WORKDIR /work

ENTRYPOINT ["cppcheck"]
CMD ["--help"]
```

**Design notes:**
- `useradd --create-home` — supplies `/home/cppcheck`; needed because some cppcheck output helpers look up `$HOME`.
- `USER cppcheck` — all subsequent instructions and the container's default runtime identity are non-root.
- `WORKDIR /work` — created implicitly if missing; consumers bind-mount their source here.
- `ENTRYPOINT` as exec-form JSON — no `/bin/sh -c` wrapping, so signals are delivered directly to `cppcheck`.
- `CMD ["--help"]` — usage help when no args are supplied.

### 3.4 Dockerfile — Complete Layer Summary

| Layer | Instruction group | Approximate size |
|:--------------|:------------------|:-----------------|
| 1 | Base image `ubuntu:${UBUNTU_VERSION}` | ~80 MB |
| 2 | `libpcre3` + `python3` install | ~10 MB |
| 3 | `COPY --from=builder /opt/cppcheck` | ~40 MB |
| 4 | `COPY misra_c_2012_for_cppcheck.txt` + shim `printf` | ~20 KB |
| 5 | `useradd cppcheck` | < 1 MB |
| 6..8 | ENV, WORKDIR, ENTRYPOINT/CMD, LABEL | metadata only |

Total: ~130 MB (matches SR-060 target of ≤ 200 MB with margin).

### 3.5 MISRA C:2012 Rule-Texts and Shim Addon

**Design intent:** consumers should be able to invoke MISRA analysis with a single flag pair (`--enable=style --addon=misra-c2012`) without having to source the rule-texts file, choose a mount location for it, or edit the addons directory.

**Runtime files added:**

| Path | Source | Owner |
|:--------------|:------------|:------------|
| `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt` | Copied from `documents/assets/misra_c_2012_for_cppcheck.txt` in the build context | root:root, world-readable |
| `/opt/cppcheck/share/cppcheck/addons/misra-c2012.py` | Generated in the same layer with `printf` | root:root, world-executable |

**Dockerfile fragment (runtime stage, after `COPY --from=builder`):**

```dockerfile
COPY documents/assets/misra_c_2012_for_cppcheck.txt \
     /opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt
RUN printf '%s\n' \
    '#!/usr/bin/env python3' \
    'import os, sys' \
    'here = os.path.dirname(os.path.abspath(__file__))' \
    'rule_texts = "/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt"' \
    'os.execvp(sys.executable, [sys.executable, os.path.join(here, "misra.py"),' \
    '                           "--rule-texts=" + rule_texts, *sys.argv[1:]])' \
    > /opt/cppcheck/share/cppcheck/addons/misra-c2012.py \
 && chmod +x /opt/cppcheck/share/cppcheck/addons/misra-c2012.py
```

**Behaviour of the shim:** when cppcheck runs an addon, it invokes the script with the `.dump` file (and other cppcheck-supplied arguments) as its command-line arguments. The shim `os.execvp`s the Python interpreter to run cppcheck's stock `misra.py` in the same directory (`here`), prepending `--rule-texts=<path>` and forwarding the rest of `sys.argv[1:]` unchanged. `execvp` (rather than `subprocess.run`) replaces the current process image so cppcheck sees the same exit code path.

**`.dockerignore` change to permit the asset through:**

```
documents
!documents/assets/misra_c_2012_for_cppcheck.txt
```

Docker's `.dockerignore` supports negation with `!`. The negation re-includes the single named file even though the parent directory is excluded. All other content under `documents/` (ASPICE docs) remains excluded from the build context.

**Consumer invocation:**

```bash
docker run --rm -v "$(pwd):/work:ro" cppcheck:<tag> \
    --enable=style --addon=misra-c2012 --cppcheck-build-dir=/tmp src/
```

`--cppcheck-build-dir=/tmp` names a writable directory for the addon's `.dump` files; the default is next to the source, which fails when `/work` is bind-mounted read-only.

**Rationale for `.py` shim vs. `.json` config:** cppcheck's `--addon=<name>` resolver only searches for `<name>.py`; a `<name>.json` next to `misra.py` is silently ignored. A shim `.py` is therefore the minimum surface area that lets consumers use a symbolic addon name. The upstream `misra.py` is not modified — the shim wraps it.

---

## 4. .dockerignore Detailed Design

**File:** `.dockerignore`
**Architecture ref:** ARC-IMG-003

```
.git
.gitignore
.github
README.md
documents
test
*.md
```

**Rules:**
- `.git`, `.gitignore` — Git internals; the Dockerfile does not need repository history.
- `.github` — CI workflows; used by GitHub Actions runner, not by the image.
- `documents` — this ASPICE document set; never referenced by the image build.
- `test` — test harness assets; run by CI after the image is built, not inside it.
- `*.md` — README and other Markdown; never referenced by the image build.

**Result:** the build context transferred to the Docker daemon is essentially empty (the Dockerfile itself is not part of the context — it is read separately). This makes builds fast and prevents accidental inclusion of ASPICE documents in the image via `COPY .` (which the Dockerfile does not use, but this is defence in depth).

---

## 5. CI Workflow Detailed Design

**File:** `.github/workflows/build.yml` (to be created)
**Architecture ref:** ARC-INT-001

### 5.1 Trigger

```yaml
on:
  push:
    branches: [main, develop, "feature/**", "hotfix/**"]
  pull_request:
    branches: [main, develop]
```

### 5.2 Job — Build-Image

```yaml
Build-Image:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: docker/setup-buildx-action@v3
    - name: Build image
      run: |
        docker build \
          --build-arg CPPCHECK_VERSION=${{ env.CPPCHECK_VERSION }} \
          --build-arg UBUNTU_VERSION=${{ env.UBUNTU_VERSION }} \
          -t cppcheck:ci .
    - name: Save image
      run: docker save cppcheck:ci -o /tmp/image.tar
    - uses: actions/upload-artifact@v4
      with:
        name: cppcheck-image
        path: /tmp/image.tar
```

**Env values `CPPCHECK_VERSION`, `UBUNTU_VERSION`** are declared at workflow scope for a single point of change.

### 5.3 Job — Verify-Version

```yaml
Verify-Version:
  needs: Build-Image
  runs-on: ubuntu-latest
  steps:
    - uses: actions/download-artifact@v4
      with: { name: cppcheck-image, path: /tmp }
    - run: docker load -i /tmp/image.tar
    - name: cppcheck --version
      run: |
        actual=$(docker run --rm cppcheck:ci --version)
        expected="Cppcheck ${{ env.CPPCHECK_VERSION }}"
        [ "$actual" = "$expected" ] || { echo "Got: $actual"; exit 1; }
```

### 5.4 Job — Run-Integration-Tests

```yaml
Run-Integration-Tests:
  needs: Build-Image
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/download-artifact@v4
      with: { name: cppcheck-image, path: /tmp }
    - run: docker load -i /tmp/image.tar
    - run: test/run.sh cppcheck:ci
```

### 5.5 Job — Release (main only)

```yaml
Release:
  if: github.ref == 'refs/heads/main'
  needs: [Verify-Version, Run-Integration-Tests]
  runs-on: ubuntu-latest
  permissions:
    packages: write
  steps:
    - uses: actions/download-artifact@v4
      with: { name: cppcheck-image, path: /tmp }
    - run: docker load -i /tmp/image.tar
    - name: Log in to ghcr.io
      run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    - name: Tag and push
      run: |
        IMG=ghcr.io/${{ github.repository_owner }}/cppcheckdocker
        docker tag cppcheck:ci $IMG:${{ env.CPPCHECK_VERSION }}-r${{ env.REVISION }}
        docker tag cppcheck:ci $IMG:latest
        docker push $IMG:${{ env.CPPCHECK_VERSION }}-r${{ env.REVISION }}
        docker push $IMG:latest
```

### 5.6 Job — AllChecksPassed

```yaml
AllChecksPassed:
  needs: [Verify-Version, Run-Integration-Tests]
  runs-on: ubuntu-latest
  steps:
    - run: echo "All required checks passed"
```

This job is the required check in the branch protection rule for `develop` and `main`.

---

## 6. Test Harness Detailed Design

**Directory:** `test/`
**Architecture ref:** ARC-INT-002

### 6.1 test/run.sh

```bash
#!/usr/bin/env bash
set -euo pipefail
IMAGE="${1:?usage: test/run.sh <image-tag>}"
FAIL=0

run_case() {
    local name="$1"; shift
    local expected_exit="$1"; shift
    local expected_snippet="$1"; shift
    echo "▶ $name"
    output=$(docker run --rm -v "$(pwd)/test/samples:/work:ro" "$IMAGE" "$@" 2>&1) && actual_exit=0 || actual_exit=$?
    if [ "$actual_exit" -ne "$expected_exit" ]; then
        echo "  FAIL: expected exit $expected_exit, got $actual_exit"; FAIL=1
    fi
    if ! grep -qE "$expected_snippet" <<< "$output"; then
        echo "  FAIL: expected output matching /$expected_snippet/"; FAIL=1
    fi
}

run_case "INT-001 version" 0 "^Cppcheck [0-9]" --version
run_case "INT-002 clean.c produces no findings" 0 "^$|no issues" --enable=all clean.c
run_case "INT-003 buggy.c out-of-bounds detected" 0 "arrayIndexOutOfBounds" --enable=all buggy.c
run_case "INT-004 --error-exitcode=1 flags return non-zero" 1 "arrayIndexOutOfBounds" --enable=all --error-exitcode=1 buggy.c

exit $FAIL
```

**Design notes:**
- `set -euo pipefail` — strict shell hygiene.
- `run_case` takes name, expected exit code, expected regex, and cppcheck args.
- All samples are mounted read-only via `-v $(pwd)/test/samples:/work:ro`.
- Exit code = number of failed cases (or 0 if all pass).

### 6.2 test/samples/clean.c

```c
#include <stdio.h>

int main(void) {
    puts("hello");
    return 0;
}
```

No findings expected under `--enable=all`.

### 6.3 test/samples/buggy.c

```c
#include <stdlib.h>

int main(void) {
    int *p = malloc(sizeof(int) * 10);
    p[10] = 0;      /* out-of-bounds write */
    return 0;       /* memory leak */
}
```

Expected findings: `arrayIndexOutOfBounds`, `memleak`, `nullPointerOutOfMemory`.

---

## 7. Error Handling Design

### 7.1 Build-Time Errors

| Failure Mode | Detection | Reporter |
|:--------------|:------------|:------------|
| Base image pull fails | `docker build` non-zero exit | CI job fails |
| apt install fails | `RUN apt-get …` non-zero exit | Layer build fails |
| Git clone fails (tag missing) | `RUN git clone --branch …` non-zero exit | Layer build fails; suggests the tag does not exist upstream |
| CMake configure/build/install fails | `RUN cmake …` non-zero exit | Layer build fails |
| Post-install smoke test fails | `RUN /opt/cppcheck/bin/cppcheck --version` non-zero exit | Fails builder stage — runtime stage never starts |

All build-time failures are surfaced as `docker build` non-zero exit codes and captured in the `Build-Image` CI job log.

### 7.2 Runtime Errors (Consumer)

The image is a thin packaging layer; runtime error semantics are those of cppcheck itself:

| Consumer scenario | Behaviour |
|:--------------|:------------|
| No arguments | `--help` printed (default `CMD`); exit 0 |
| Unknown argument | cppcheck usage message on stderr; exit 1 |
| Analysis completes without findings | Exit 0 |
| Analysis completes with findings, no `--error-exitcode` | Exit 0; findings on stdout |
| Analysis completes with findings, `--error-exitcode=N` | Exit N |
| Cannot read source file | Error on stderr; exit 1 |

### 7.3 Publish-Time Errors

| Failure Mode | Detection | Reporter |
|:--------------|:------------|:------------|
| `docker login ghcr.io` fails | `docker login` non-zero exit | Release job fails; typically an `GITHUB_TOKEN` permission problem |
| `docker push` fails | `docker push` non-zero exit | Release job fails |

---

## 8. Requirements Traceability

| SR ID | Requirement Summary | Design Section |
|:--------------|:---------------------|:---------------|
| SR-001 | Ubuntu LTS base | §3.1, §3.2, §3.3 |
| SR-002 | Multi-stage build | §3.2, §3.3 |
| SR-003 | Builder apt packages | §3.2 |
| SR-004 | Source clone at tag | §3.2 |
| SR-005 | CMake build options | §3.2 |
| SR-006 | Install prefix | §3.2 |
| SR-007 | Runtime apt packages | §3.3 |
| SR-008 | COPY --from=builder | §3.3 |
| SR-009 | No build tools in runtime | §3.3, §3.4 |
| SR-010 | .dockerignore | §4 |
| SR-020 | cppcheck on PATH | §3.3 (ENV PATH) |
| SR-021 | ENTRYPOINT | §3.3 (ENTRYPOINT/CMD) |
| SR-022 | CMD --help | §3.3 |
| SR-023 | --version returns pinned | §3.2 (smoke test), §5.3 |
| SR-024–SR-025 | cfg / platforms present | §3.2 (FILESDIR) |
| SR-026 | python3 runtime | §3.3 |
| SR-027 | --enable=all works | §3.2 (HAVE_RULES=ON), §6.1 |
| SR-028 | MISRA rule-texts bundled | §3.5 |
| SR-029 | misra-c2012 shim addon | §3.5 |
| SR-030–SR-031 | Non-root user; WORKDIR | §3.3 (useradd, USER, WORKDIR) |
| SR-032 | Analyse mounted /work | §6.1 (-v test/samples:/work:ro) |
| SR-033–SR-034 | Exit codes | §6.1 (INT-003, INT-004), §7.2 |
| SR-035 | Output formats | §7.2 |
| SR-036 | GHA container step | §5 |
| SR-040 | No secrets | §4, §7.1 |
| SR-041 | No .git | §3.3 (no COPY of git tree), §4 |
| SR-042–SR-043 | Non-root default; no ports | §3.3 |
| SR-044 | OCI labels | §3.3 (LABEL) |
| SR-050 | ARGs | §3.1 |
| SR-051 | Default version current | §3.1 |
| SR-052 | Image tag format | §5.5 |
| SR-053 | Digest recorded in release | §5.5 |
| SR-054 | Reproducibility | §3.1, §3.2 |
| SR-060 | Image size | §3.4 |
| SR-061 | Cold build time | §5.2 (CI infrastructure) |
| SR-062 | --version time | §3.2 (smoke test observed) |
| SR-063 | Integration suite time | §6.1 |

*Full traceability provided in CCD-RTM-001.*

---

*End of CCD-SWE3-001 v1.02*
