# Software Integration Test Plan
## CppCheckDocker — Ubuntu Docker Image for Latest Cppcheck

| Field | Value |
|:--------------|:------------|
| **Document ID** | CCD-SWE5-001 |
| **Version** | v1.02 |
| **Date** | 2026-08-13 |
| **Author** | Dermot Murphy |
| **Reviewer** | Dermot Murphy |
| **Status** | Released |
| **Classification** | Internal |
| **ASPICE Process** | SWE.5 — Software Integration and Integration Test |

---

## Document Control

| Version | Date | Author | Change Description |
|:--------------|:------------|:------------|:--------------------|
| v1.00 | 2026-08-13 | Dermot Murphy | Initial issue |
| v1.01 | 2026-08-13 | Dermot Murphy | Added Phase 5 (Addons) with INT-040 (MISRA C:2012 addon end-to-end) covering SR-028/SR-029. |
| v1.02 | 2026-08-13 | Dermot Murphy | Promote Draft -> Released as part of the ASPICE audit-readiness sweep (issue #23); corrected trailing "End of" version citation. |

---

## 1. Introduction

This document is the Software Integration Test Plan (ITP) for the CppCheckDocker project. It defines the strategy and test cases for verifying that the built Docker image, its cppcheck payload, its runtime dependencies, and its GitHub Actions workflow integrate correctly to deliver end-to-end static analysis of C/C++ source code, in accordance with ASPICE v4 process SWE.5.

Integration testing exercises the image in three phases:
1. **Image + volume** — cppcheck against a bind-mounted source tree
2. **Image + arguments** — output formats, exit codes, mode flags
3. **Image + GitHub Actions** — the image invoked as a step container from a workflow

Integration tests run on the same GitHub-hosted `ubuntu-latest` runners used for the build; no self-hosted infrastructure is required.

**Parent document:** CCD-SWE2-001 SADD
**Test location:** `test/integration/` (samples in `test/samples/`; expected outputs in `test/expected/`)
**CI job:** `Run-Integration-Tests`

---

## 2. Integration Test Strategy

### 2.1 Single-Tier Model

The deliverable is small enough that a smoke/component split adds no value; the entire integration suite runs on every push and must fit within the 3-minute time budget (SR-063).

```
┌────────────────────────────────────────────────────────────────────────┐
│                         CI TRIGGER                                     │
│              Every push                    Pull request                │
├─────────────────────────────┬──────────────────────────────────────────┤
│  INTEGRATION (< 3 min)                                                 │
│  • cppcheck vs. sample source trees                                    │
│  • output formats and exit codes                                       │
│  • image usable as GHA step container                                  │
│  Status: ACTIVE                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Integration Order

Integration proceeds bottom-up, mirroring the architectural dependency order:

```
Phase 1: Image + cppcheck binary (in-container execution)
Phase 2: Image + mounted source tree (bind mount)
Phase 3: Image + cppcheck arguments (formats, exit codes, addons)
Phase 4: Image + GitHub Actions (step container)
```

Each phase's tests must pass before the next phase is executed.

### 2.3 Test Method

Tests are executed using:
- **bash** driver script `test/integration/run.sh` invoked by CI job `Run-Integration-Tests`
- **docker run** with `-v` bind mounts for source-tree tests
- **A dedicated `.github/workflows/self-test.yml` workflow** for Phase 4 that consumes the freshly built image as a step container

### 2.4 Pass Criteria

A test passes when the actual response matches the expected response for exit code and expected output snippet (regex match).

**Integration gate:** All integration tests must pass. A failure on `develop`/`main` blocks merge.

---

## 3. Integration Test Cases

### Phase 1 — Image and Cppcheck Binary

| Test ID | Title | Procedure | Expected Result | SR Ref |
|:--------------|:------------|:------------|:-----------------|:------------|
| INT-001 | Cppcheck on PATH | `docker run --rm --entrypoint sh cppcheck:ci -c 'which cppcheck'` | Output = `/opt/cppcheck/bin/cppcheck` | SR-020 |
| INT-002 | Entrypoint forwards arguments | `docker run --rm cppcheck:ci --version` | Output starts with `Cppcheck ` | SR-021 |
| INT-003 | Default CMD prints help | `docker run --rm cppcheck:ci` | Output contains `Cppcheck - a tool for static C/C++ code analysis.` | SR-022 |
| INT-004 | cfg files accessible to cppcheck | `docker run --rm cppcheck:ci --check-config test/samples/clean.c` 2>&1 | No `Cppcheck cannot find` messages | SR-024 |
| INT-005 | Platforms XML usable | `docker run --rm cppcheck:ci --platform=arm32-wchar_t4 --check-config test/samples/clean.c` 2>&1 | Exit 0; no unknown-platform error | SR-025 |
| INT-006 | python3 available for addons | `docker run --rm --entrypoint python3 cppcheck:ci --version` | Output starts with `Python 3.` | SR-026 |
| INT-007 | --enable=all accepted | `docker run --rm -v $PWD/test/samples:/work:ro cppcheck:ci --enable=all clean.c` | Exit 0 | SR-027 |

### Phase 2 — Image and Mounted Source Tree

| Test ID | Title | Procedure | Expected Result | SR Ref |
|:--------------|:------------|:------------|:-----------------|:------------|
| INT-010 | Read-only mount analysis | Bind-mount `test/samples/` as `/work:ro`; run `cppcheck --enable=all clean.c` | Exit 0; no findings | SR-032 |
| INT-011 | Non-zero exit on findings with `--error-exitcode=1` | Run against `buggy.c` with `--error-exitcode=1` | Exit 1; output contains `arrayIndexOutOfBounds` | SR-033 |
| INT-012 | Zero exit on findings without `--error-exitcode` | Run against `buggy.c` without `--error-exitcode` | Exit 0; output contains `arrayIndexOutOfBounds` | SR-034 |
| INT-013 | XML output format | Run with `--xml --enable=all buggy.c 2>&1` | Output contains `<?xml version="1.0"` and `<errors>` | SR-035 |
| INT-014 | Recursive directory analysis | Bind-mount a directory tree; run `cppcheck --enable=all .` | Exit 0; findings from files in subdirectories present | SR-032 |
| INT-015 | Analysis of C++ source | Run against `test/samples/buggy.cpp` | Findings reported for a known C++ defect | SR-027, SR-032 |

### Phase 3 — Image and Cppcheck Arguments

| Test ID | Title | Procedure | Expected Result | SR Ref |
|:--------------|:------------|:------------|:-----------------|:------------|
| INT-020 | Cold build within budget | Timed `docker build --no-cache …` on a clean runner | Duration ≤ 10 minutes; recorded in CI job log | SR-061 |
| INT-021 | `--version` latency | Time `docker run --rm cppcheck:ci --version` after `docker load` | ≤ 3 seconds | SR-062 |
| INT-022 | Integration suite duration | Time the `Run-Integration-Tests` job | ≤ 3 minutes | SR-063 |
| INT-023 | Suppression flag honoured | Run against `buggy.c` with `--suppress=arrayIndexOutOfBounds` | Output does not contain `arrayIndexOutOfBounds` | SR-027 |
| INT-024 | MISRA addon (if selected) | Run with `--addon=misra` against a MISRA-violating sample | Addon output referenced in results | SR-026 |
| INT-025 | Consumer overrides user | Run with `-u 0:0`; cppcheck still functions | Exit 0; `--version` returns expected string | SR-042 (documented override) |

### Phase 5 — MISRA C:2012 Addon (bundled rule-texts)

| Test ID | Title | Procedure | Expected Result | SR Ref |
|:--------------|:------------|:------------|:-----------------|:------------|
| INT-040 | MISRA addon + bundled rule-texts | Bind-mount `test/samples/` as `/work:ro`; run `cppcheck --enable=style --addon=misra-c2012 --cppcheck-build-dir=/tmp misra_bad.c`. Sample file contains a MISRA Rule 15.1 (`goto`) violation. | Exit 0; stdout contains both the readable text `"The goto statement should not be used"` and the rule tag `[misra-c2012-15.1]`. | SR-028, SR-029 |

The assertion on the human-readable rule text ("The goto statement should not be used") is deliberate: this text is only emitted when `misra.py` loads a valid `--rule-texts` file. The test therefore fails loudly if the rule-texts file is missing, if the shim addon is missing or misconfigured, if `python3` is missing at runtime, or if the cppcheck build lacks addon-execution support.

### Phase 4 — Image as GitHub Actions Step Container

| Test ID | Title | Procedure | Expected Result | SR Ref |
|:--------------|:------------|:------------|:-----------------|:------------|
| INT-030 | `container:` job runs the image | A dedicated `self-test.yml` workflow declares `container: cppcheck:ci` and runs `cppcheck --version` in a step | Job succeeds; log line matches `Cppcheck <version>` | SR-036 |
| INT-031 | Actions-checkout works inside the container | Same workflow includes `actions/checkout@v4`; then `cppcheck --enable=all .` | Job succeeds | SR-036 |
| INT-032 | Analysis produces expected findings in CI context | `self-test.yml` runs against a committed defective sample | Job step fails when `--error-exitcode=1` set on defective input | SR-033, SR-036 |

---

## 4. Integration Test Artefacts

| Artefact | CI Job | Location | Status |
|:--------------|:------------|:------------|:------------|
| Integration test log | `Run-Integration-Tests` | `Integration_Test_Output` artefact | Active |
| Self-test workflow log | `self-test.yml` (separate workflow) | Actions run log | Active |
| Sample sources | — | `test/samples/` | Active |
| Expected outputs | — | `test/expected/` | Active |
| Test driver script | — | `test/integration/run.sh` | Active |

---

## 5. Timing Budget Summary

| Environment | Tests Included | Target Duration | CI Job | Status |
|:--------------|:---------------|:----------------|:------------|:------------|
| GHA `ubuntu-latest` | INT-001..INT-025 | < 3 minutes | `Run-Integration-Tests` | Active |
| GHA `ubuntu-latest` | INT-030..INT-032 | < 2 minutes | `self-test.yml` (parallel) | Active |
| GHA `ubuntu-latest` | INT-020 (cold build) | < 10 minutes | `Build-Image` | Active |

---

## 6. Traceability Summary

| Test ID Range | Integration Phase | SR IDs Covered |
|:---------------|:------------------|:---------------|
| INT-001–007 | Image + binary | SR-020, SR-021, SR-022, SR-024, SR-025, SR-026, SR-027 |
| INT-010–015 | Image + mount | SR-027, SR-032, SR-033, SR-034, SR-035 |
| INT-020–025 | Image + arguments | SR-027, SR-042, SR-061, SR-062, SR-063 |
| INT-030–032 | Image + GHA | SR-033, SR-036 |
| INT-040 | MISRA addon | SR-028, SR-029 |

*Full traceability in CCD-RTM-001.*

---

*End of CCD-SWE5-001 v1.02*
