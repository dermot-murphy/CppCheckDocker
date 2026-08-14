# Quick Start

CppCheckDocker packages the latest release of [cppcheck](https://github.com/danmar/cppcheck) into an Ubuntu container image so GitHub Actions workflows on Linux runners can call a recent cppcheck without waiting for upstream Linux packages to catch up. The image also bundles the MISRA C:2012 rule-texts file (CC BY-NC-ND 4.0) so `--addon=misra-c2012` returns human-readable guideline text out of the box.

- **Cppcheck version:** 2.21.1 (pinned via build arg)
- **Base:** `ubuntu:24.04`
- **Image size:** ~130 MB (SR-060 caps runtime at 200 MB — see the [Runtime image size trend](https://github.com/dermot-murphy/CppCheckDocker#runtime-image-size-trend) chart on the repo README for the current curve)
- **Non-root by default** (`cppcheck` user)

## Pull the image

The image is published to two registries; pick whichever is closer to your build:

```bash
docker pull ghcr.io/dermot-murphy/cppcheckdocker:latest
# or
docker pull docker.io/dermotmurphy/cppcheckdocker:latest
```

Immutable, per-release tags follow the pattern `<cppcheck-version>-r<revision>` (for example `2.21.1-r1`). Pin to those tags — or to the image digest — for reproducible pipelines. `latest` is best-effort and moves as new revisions publish.

## Analyse a local source tree

```bash
docker run --rm -v "$(pwd):/work:ro" ghcr.io/dermot-murphy/cppcheckdocker:latest \
    --enable=all --error-exitcode=1 src/
```

- Everything after the image name is passed straight to `cppcheck` — the entrypoint is `cppcheck`.
- `/work` is the WORKDIR; bind-mount your source tree there.
- Mount read-only (`:ro`) unless cppcheck needs to write intermediate output (see [MISRA C:2012](MISRA-C-2012)).

## Next steps

- [Docker Usage](Docker-Usage) — mount modes, GHA `container:` example, exit codes, output formats
- [MISRA C:2012](MISRA-C-2012) — invoking the bundled addon and rule-texts
- [Pre-commit Integration](Pre-Commit-Integration) — running the same lint gates locally
- [Image Tags and Publication](Image-Tags-And-Publication) — tag conventions and provenance
- [CI Workflow Reference](CI-Workflow-Reference) — every CI job explained
