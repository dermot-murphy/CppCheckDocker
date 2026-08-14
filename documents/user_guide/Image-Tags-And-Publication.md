# Image Tags and Publication

## Tag scheme

Every release publishes the same digest under four tags across two registries:

| Registry | Tag | Guarantee |
|:---------|:----|:----------|
| GHCR | `ghcr.io/dermot-murphy/cppcheckdocker:<version>-r<rev>` | Immutable |
| GHCR | `ghcr.io/dermot-murphy/cppcheckdocker:latest` | Floating |
| Docker Hub | `docker.io/dermotmurphy/cppcheckdocker:<version>-r<rev>` | Immutable |
| Docker Hub | `docker.io/dermotmurphy/cppcheckdocker:latest` | Floating |

- `<version>` is the pinned upstream cppcheck version (currently `2.21.1`).
- `<rev>` starts at `1` for each new cppcheck version and increments on any change to the Dockerfile, base image, or build options that alters the resulting image. Revision is derived from git tags at release time — no manual bookkeeping.
- **Consumers that need reproducibility should pin to `<version>-r<rev>` or to the image digest.** `latest` is best-effort and moves as new revisions publish.

## When a release fires

The `Release` job in `.github/workflows/build.yml` runs on every push to `main`, but only publishes when the merged diff touches an image-affecting file:

- `Dockerfile`
- `.dockerignore`
- `documents/assets/misra_c_2012_for_cppcheck.txt`
- `.github/workflows/build.yml`

Doc-only, test-only, or workflow changes that do not alter the image itself do not consume a revision. See [CppCheckDocker_SPL2_Software_Release_Plan §5.1](CppCheckDocker_SPL2_Software_Release_Plan) for the skip rules.

## Post-release configuration audit

After each publish, the `Release` job runs two audits (SUP.8 §7):

1. **Registry digest round-trip** — inspects each pushed tag on GHCR and Docker Hub and confirms the manifest digest matches what `docker/build-push-action` reported. Fails the release on any mismatch.
2. **Version smoke** — pulls the published GHCR tag and runs `cppcheck --version`; fails on mismatch with the pinned `CPPCHECK_VERSION` build arg.

Both audits are executed automatically; there is no manual step.

## Where the release evidence lives

- **GitHub Release notes** — the resolved image digest, both registry tags, and a link to the SVD.
- **`documents/aspice/records/CCD-SVD-<tag>.md`** — the ASPICE Software Version Description for that release.
- **`documents/aspice/records/CCD-QTR-<tag>.md`** — the Qualification Test Record for that release.
- **`image_size_history.csv` on the `gh-pages` branch** — per-merge image size row (see the trend chart on the repo README).
