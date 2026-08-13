# CppCheckDocker

Ubuntu Docker image that ships the latest release of [cppcheck](https://github.com/danmar/cppcheck) — a static analysis tool for C and C++. Built to give GitHub Actions workflows on Linux runners a recent cppcheck (upstream Linux packages tend to lag Windows releases) with MISRA C:2012 rule-text support already wired up.

- **Cppcheck version:** 2.21.1 (pinned; overridable via build arg)
- **Base:** `ubuntu:24.04`
- **Image size:** ~130 MB
- **Non-root by default** (`cppcheck` user)
- **MISRA C:2012 addon** bundled with the MISRA Consortium's official rule-texts file (CC BY-NC-ND 4.0)

## Quick start

### Analyse a local source tree

```bash
docker run --rm -v "$(pwd):/work:ro" ghcr.io/dermot-murphy/cppcheckdocker:latest \
    --enable=all --error-exitcode=1 src/
```

### In a GitHub Actions job

```yaml
jobs:
  static-analysis:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/dermot-murphy/cppcheckdocker:latest
    steps:
      - uses: actions/checkout@v4
      - run: cppcheck --enable=all --error-exitcode=1 src/
```

### With the bundled MISRA C:2012 addon

```bash
docker run --rm -v "$(pwd):/work:ro" ghcr.io/dermot-murphy/cppcheckdocker:latest \
    --enable=style --addon=misra-c2012 --cppcheck-build-dir=/tmp src/
```

Output includes the human-readable MISRA guideline text, e.g.:

```
src/main.c:6:5: style: The goto statement should not be used [misra-c2012-15.1]
```

`--cppcheck-build-dir=/tmp` is required whenever `/work` is bind-mounted read-only — cppcheck's addon step needs a writable location for its intermediate `.dump` files.

## What's inside the image

| Path | Purpose |
|:-----|:--------|
| `/opt/cppcheck/bin/cppcheck` | The cppcheck executable |
| `/opt/cppcheck/share/cppcheck/cfg/` | Library configuration XMLs (std, posix, qt, …) |
| `/opt/cppcheck/share/cppcheck/platforms/` | Platform XMLs (arm32, riscv64, …) |
| `/opt/cppcheck/share/cppcheck/addons/` | Cppcheck addons (misra.py, naming.py, y2038.py, …) |
| `/opt/cppcheck/share/cppcheck/addons/misra-c2012.py` | Shim addon — runs `misra.py` with the bundled rule-texts pre-supplied |
| `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt` | MISRA C:2012 rule-texts file (CC BY-NC-ND 4.0) |
| `/home/cppcheck/` | Home directory for the non-root `cppcheck` user |
| `/work/` | Default working directory — bind-mount your source tree here |

## Local build

### Windows (Docker Desktop)

```cmd
build-and-test.bat
```

The batch file builds the image and runs the integration test suite. It requires Docker Desktop and Git Bash (bundled with Git for Windows).

### Linux / macOS / WSL

```bash
docker build -t cppcheck:local .
./test/integration/run.sh cppcheck:local
```

### Overriding the cppcheck version

```bash
docker build --build-arg CPPCHECK_VERSION=2.20.0 -t cppcheck:2.20.0 .
```

`CPPCHECK_VERSION` accepts any git tag from [danmar/cppcheck](https://github.com/danmar/cppcheck/tags).

## Continuous integration

The [`.github/workflows/build.yml`](.github/workflows/build.yml) workflow builds the image, runs the integration tests, and — on pushes to `main` or `develop` — publishes the ASPICE documentation set to the repository's GitHub Wiki.

Wiki publishing requires a `WIKI_TOKEN` repository secret; see [CppCheckDocker_SUP8_CM_Plan.md §5.4](documents/aspice/CppCheckDocker_SUP8_CM_Plan.md) for the one-time setup.

## ASPICE compliance

The project targets ASPICE v4 Level 2. The complete document set lives under [`documents/aspice/`](documents/aspice/) and is auto-published to the [project wiki](https://github.com/dermot-murphy/CppCheckDocker/wiki):

| Document | Process |
|:---------|:--------|
| [MAN.3 Project Management Plan](documents/aspice/CppCheckDocker_MAN3_Project_Management_Plan.md) | Project management |
| [SUP.1 Software Quality Assurance Plan](documents/aspice/CppCheckDocker_SUP1_Quality_Assurance_Plan.md) | Quality assurance |
| [SUP.8 Configuration Management Plan](documents/aspice/CppCheckDocker_SUP8_CM_Plan.md) | Configuration management |
| [SUP.9 Problem Resolution & Change Request Plan](documents/aspice/CppCheckDocker_SUP9_Problem_Resolution_Plan.md) | Problem / change management |
| [SWE.1 Software Requirements](documents/aspice/CppCheckDocker_SWE1_SW_Requirements.md) | Requirements analysis |
| [SWE.2 Software Architecture](documents/aspice/CppCheckDocker_SWE2_SW_Architecture.md) | Architectural design |
| [SWE.3 Detailed Design](documents/aspice/CppCheckDocker_SWE3_Detailed_Design.md) | Detailed design |
| [SWE.4 Unit Verification Plan](documents/aspice/CppCheckDocker_SWE4_Unit_Verification.md) | Unit verification |
| [SWE.5 Integration Test Plan](documents/aspice/CppCheckDocker_SWE5_Integration_Test.md) | Integration test |
| [SWE.6 Qualification Test Specification](documents/aspice/CppCheckDocker_SWE6_Qualification_Test.md) | Qualification test |
| [ACQ.4 Supplier Monitoring Plan](documents/aspice/CppCheckDocker_ACQ4_Supplier_Monitoring_Plan.md) | Supplier monitoring |
| [SPL.2 Software Release Plan](documents/aspice/CppCheckDocker_SPL2_Software_Release_Plan.md) | Software release |
| [SVD Software Version Description (template)](documents/aspice/CppCheckDocker_SVD_Software_Version_Description.md) | Per-release record (populated instances under `documents/aspice/records/`) |
| [RTM Master Traceability Matrix](documents/aspice/CppCheckDocker_RTM_Master_Traceability_Matrix.md) | End-to-end traceability |

## Licensing

- **Dockerfile, workflows, test harness, ASPICE documents** — this repository's contents; unless a file states otherwise, treat as internal-use.
- **cppcheck** — GPL-3.0-or-later, © cppcheck team. Redistributed unmodified.
- **Ubuntu base image** — Canonical, standard Ubuntu terms.
- **MISRA C:2012 rule-texts file** (`misra_c_2012_for_cppcheck.txt`) — © MISRA Consortium Limited; redistributed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Not a substitute for the full MISRA C:2012 guidelines document, which must be purchased separately from [misra.org.uk](https://misra.org.uk/) for commercial use.
