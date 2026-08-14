# CI Workflow Reference

The single workflow file [`.github/workflows/build.yml`](https://github.com/dermot-murphy/CppCheckDocker/blob/main/.github/workflows/build.yml) drives every automated check, publish, and monitoring artefact.

## Triggers

- Every push to `main`, `develop`, `feature/**`, and `hotfix/**`.
- Every pull request targeting `main` or `develop`.

## Jobs

| Job | Runs when | Purpose |
|:----|:----------|:--------|
| `Lint` | Every push / PR | Runs the full pre-commit hook set (hadolint, yamllint, hygiene fixers). |
| `Build-Image` | Every push / PR | Builds the runtime image, measures its size, and fails on `size > 200 MB` (SR-060 gate). Publishes the image tarball as a job artifact. |
| `Verify-Version` | After `Build-Image` | Runs `cppcheck --version` inside the built image and checks the string against the pinned `CPPCHECK_VERSION`. |
| `Run-Integration-Tests` | After `Build-Image` | Executes `test/integration/run.sh` against the built image. Upload of the log is retained 30 days. |
| `Scan-Image` | After `Build-Image` | Two Trivy passes: an informational report at all severities (uploaded, 90-day retention), and a gating pass that fails on `HIGH` or `CRITICAL` CVEs. Suppressions live in `.trivyignore` with rationale + expiry. |
| `Release` | Push to `main`, and only when an image-affecting file changed | Publishes `<version>-r<rev>` and `latest` to GHCR + Docker Hub, creates the git tag and GitHub Release, and runs the SUP.8 §7 configuration audits (digest round-trip + version smoke). |
| `Publish-Wiki` | Push to `main` or `develop` | Regenerates the User Guide + ASPICE CL2 wiki structure from `documents/user_guide/` and `documents/aspice/` (recursive). |
| `Track-Image-Size` | Push to `main` or `develop` | Appends a `timestamp,commit,branch,size_bytes` row to `image_size_history.csv` on the `gh-pages` branch and re-renders `image_size_trend.svg`. |
| `AllChecksPassed` | After the four required jobs | Aggregator — the branch protection gate. |

## Required for merge

Branch protection on `main` and `develop` requires `AllChecksPassed`. That in turn requires `Lint`, `Verify-Version`, `Run-Integration-Tests`, and `Scan-Image` to pass.

`Track-Image-Size` and `Publish-Wiki` are post-merge monitoring / publishing jobs — they run after the merge has landed and do not block merges.

## Secrets

| Secret | Used by | Purpose |
|:-------|:--------|:--------|
| `GITHUB_TOKEN` | Every job | Built-in; automatic per workflow run. Used for GHCR login, GitHub Release creation, and `gh-pages` pushes. |
| `WIKI_TOKEN` | `Publish-Wiki` | Classic PAT with `repo` scope. `GITHUB_TOKEN` cannot push to the `.wiki.git` endpoint. See [CppCheckDocker_SUP8_CM_Plan §5.4](CppCheckDocker_SUP8_CM_Plan) for setup. |
| `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` | `Release` | Docker Hub push credentials. |
