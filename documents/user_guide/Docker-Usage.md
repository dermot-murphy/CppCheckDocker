# Docker Usage

Ways to invoke the image outside a bare `docker run`, plus the mount and permission details you need to know.

## As a GitHub Actions step container

The image can host every step in a job:

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

The container inherits the workspace at `/__w/<repo>/<repo>`, and GitHub sets that as the WORKDIR for the run — you do not need to bind-mount `/work`.

## As a one-off `docker run`

```bash
docker run --rm -v "$(pwd):/work:ro" ghcr.io/dermot-murphy/cppcheckdocker:latest \
    --enable=all --error-exitcode=1 src/
```

- `:ro` mount is safe for pure analysis. Drop it (or use `:rw`) if cppcheck must write output (SARIF/XML redirected to a mounted path, or the MISRA addon's `.dump` directory).
- The default WORKDIR is `/work`. Every relative path in the cppcheck command line resolves there.
- The entrypoint is `cppcheck` — every argument after the image name goes straight to the analyser.

## Exit codes and output formats

Cppcheck exits `0` by default, even on findings. Force a non-zero exit when the build should fail:

```bash
cppcheck --enable=all --error-exitcode=1 src/
```

Machine-readable output:

```bash
# SARIF (for the GitHub code-scanning UI)
cppcheck --enable=all --output-format=sarif --output-file=/work/out.sarif src/

# XML
cppcheck --enable=all --xml --output-file=/work/out.xml 2> src/
```

Both require a writable mount (drop `:ro` on the `-v` argument).

## Non-root by default

Container UID is the `cppcheck` user, not root. If your workflow needs to touch host-owned files with a specific UID, either run under `user:` in the workflow or `docker run --user "$(id -u):$(id -g)"` locally.

## Local build (Windows / Linux / macOS)

For iterating on the Dockerfile itself:

```bash
docker build -t cppcheck:local .
./test/integration/run.sh cppcheck:local
```

On Windows use `build-and-test.bat` (Git Bash + Docker Desktop required — see the top-level README for prerequisites).

To pin a different cppcheck release, override the build arg:

```bash
docker build --build-arg CPPCHECK_VERSION=2.20.0 -t cppcheck:2.20.0 .
```

`CPPCHECK_VERSION` accepts any git tag from [danmar/cppcheck](https://github.com/danmar/cppcheck/tags).
