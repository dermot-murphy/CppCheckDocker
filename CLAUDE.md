This Product:
- A Docker image for CppCheck V2.21.1 for use on GitHub Actions

Files & Folders:
- For file and folder names use lower_snake_case except where a tool or convention mandates otherwise (Dockerfile, README.md, CLAUDE.md, LICENSE, GitHub Actions workflow filenames, and
  ASPICE deliverables which follow <Project>_<Process>_<Title>.md)

Git:
- This file lives at the root of the GitHub repo
- Before each commit, warn me to close SourceTree and Segger to avoid Windows file locks that break pre-commit's stash/restore. SourceTree stays open the rest of the time for observation only.
- To keep pre-commit's own stash/restore off files another process might lock, run `git stash push -u` before `git commit` and `git stash pop` after. That way pre-commit finds a clean tree and never tries to move unstaged files itself.
- If a pre-commit failure leaves the working tree in a mixed state, look for the orphaned patch in `~/.cache/pre-commit/patch*` and `git apply` it before doing anything else. Do not `git reset`, `git checkout .`, or otherwise touch the tree until the orphaned patch is either recovered or confirmed empty.
- Assume more than one Claude session may be editing this repo (only one commits or pushes at a time). Always run `git status` before staging or committing; don't assume files are in the state you left them.
- When creating a PR, add a section listing each commit with its binary-impact and risk.
- Issues are stored on GitHub
- All Changes must track to a GitHub issue.  The GitHub issue number and abstract will be the HotFix or Feature branch name, and must appear in the PR when merging to develop or main
- Add a .pre-commit-config.yaml file if one is not present
- Add a .dockerignore file if it is not present
- Add a .gitignore file if it is not present
- Always add the --base option when creating a PR
- Only create PRs from feature branches to develop; hotfix branches target main (see Workflow)

Programming Languages:
- The project is a Dockerfile but uses some Python, and C source files for testing

Workflow:
The workflow is gitflow:
- a new branch name for a bug fix (issue label bug) is "feature/BUGFIX-"<Github issue number>-<github issue abstract>
- a new branch name for a new feature request (issue label feature) is "feature/FEATURE-"<Github issue number>-<github issue abstract>
- a new branch name for a change-request or enhancement (issue label change-request) is "feature/CR-"<Github issue number>-<github issue abstract>
- if the fix is a hotfix (issue label hotfix), the new branch name is  hotfix/HOTFIX-"<Github issue number>-<github issue abstract>
- the github issue abstract has spaces, colons, underscores replaced with underscore
- for a feature or bug fix:
-- Branch from develop to feature/<feature branch name>
-- Make the changes
-- Break the changes into multiple commits to help the reviewer
-- Check that there will be no merge conflicts and if so, fix these first
-- Push and create a PR
-- Monitor the PR to ensure that GitHub actions all pass
-- Approval is when the PR is manually merged.
- for hotfix:
-- branch from main/master to hotfix/<hotfix branch name>
-- Make the changes
-- Break the changes into multiple commits to help the reviewer
-- Push and create a PR. PRs target develop by default; hotfix branches target main (and then a follow-up PR syncs develop)
-- Monitor the PR to ensure that GitHub actions all pass
-- Approval is when the PR is manually merged.
-- Create a PR to sync the changes back to develop
- for a release:
-- the ASPICE documents must be up to date including the Software Version Description

Standards:
- Semantic versioning is used.
- Conventional Commit message format is used.
- ASPICE V4 L2
- All source files including .c and .h files must only use ASCII characters

Publication:
- GitHub Wiki
- GitHub home page

Tools:
- documents are here documents

Coding Standard:
-  YAML files (yamllint) and Dockerfiles (hadolint) must be checked prior to commit; see pre-commit config.

Build:
- The primary build action is .github/workflows/build.yml

CI:
- When verifying a workflow run is annotation-free, sweep EVERY job in the run, not just one. Annotations are per-job — warnings on the Verify/Test/Wiki jobs are invisible when you only query the Build job's check-run ID. Enumerate with `gh api repos/<owner>/<repo>/actions/runs/<run>/jobs --jq '.jobs[].id'` then query `check-runs/<id>/annotations` for each.

Learning:
Rules accumulated from prior sessions. Each entry states what to do and why, so it can be applied to edge cases rather than followed blindly.
- Verify third-party GitHub Action tag names before pinning. Do not guess. Query `gh api repos/<owner>/<action>/tags --jq '.[0:5][] | .name'` first. Some actions publish tags as bare `X.Y.Z`, others as `vX.Y.Z`; a wrong prefix fails with `Unable to resolve action`. Cost of learning: two failed CI runs on PR #12 with trivy-action before the tag list was checked.
- When adding pre-commit hooks that fix line endings, add `.gitattributes` first. On a Windows-authored repo, `mixed-line-ending --fix=lf` touches nearly every file. Landing `.gitattributes` (with `* text=auto eol=lf`, plus `*.bat`/`*.cmd`/`*.ps1` as `text eol=crlf`) in the same or earlier commit locks the state and prevents CRLF re-appearing on every subsequent Windows edit. Otherwise every future PR resurrects the same normalisation churn.
- Third-party assets need `-text` in `.gitattributes` AND regex excludes in `.pre-commit-config.yaml`. The bundled MISRA rule-texts file (CC BY-NC-ND 4.0) must be preserved as delivered. `-text` marks it binary so git never rewrites line endings; the hook exclude (e.g. `^documents/assets/`) prevents pre-commit's whitespace/EOF/EOL fixers from modifying content. Same pattern applies to any redistributed OSS asset.
- `git stash push -u` moves in-flight edits to the stash and leaves the working tree clean. If a stash is taken to protect pre-commit's own stash/restore, remember to `git stash pop` immediately after to restore the edit. Confirm with `git status` before the next Edit — a stray reset can silently discard work in progress.
- Merge order matters when multiple concurrent PRs touch `.github/workflows/build.yml`. Every PR that adds a new job also amends `AllChecksPassed`'s `needs:` list — that line will three-way-merge conflict on every subsequent PR after the first same-file merge lands. Recommended order: (a) doc-only PRs first, (b) new-file-only PRs next (e.g. new workflow files), (c) build.yml-modifying PRs serialised last. Expect to resolve conflicts locally for each PR after the first.
- Ruleset `required_status_checks` requires the branch to be up-to-date at merge time. After every merge to `develop`, remaining PRs report `mergeStateStatus: BEHIND` and merge fails with `Required status check 'All checks passed' is expected.` Fix: `gh pr update-branch <n>`, then watch `gh pr checks <n> --watch` for the fresh CI run, then merge.
- When a build.yml merge conflict involves your branch adding one job and develop adding another, take `--theirs` wholesale and re-insert your job by hand. Cleaner than resolving inline conflict markers around a large multi-step job block. Command: `git checkout --theirs .github/workflows/build.yml`, then Edit to re-insert the missing job at the correct location, then update the `AllChecksPassed` `needs:` list to name every job.
- GHCR rejects mixed-case repository names. When pushing to `ghcr.io/<owner>/<repo>`, lowercase the owner and repo first: `lower_repo=$(echo "${{ github.repository }}" | tr '[:upper:]' '[:lower:]')`. GitHub itself accepts mixed case in the repo name; GHCR does not.
- `GITHUB_TOKEN` cannot push to `.wiki.git` and cannot trigger workflow runs from PRs it opens. The wiki push requires a classic PAT with `repo` scope stored as a separate secret (`WIKI_TOKEN`). PRs opened by scheduled workflows using `GITHUB_TOKEN` will merge quietly with zero CI runs — the workflow that opens the PR must flag this in the PR body so a human triggers CI manually (close/reopen, empty commit, or Re-run all jobs).
- When a workflow creates branches and PRs, add `permissions: {contents: write, pull-requests: write}` at the workflow (or job) level. Default `GITHUB_TOKEN` permissions are read-only in many repos; without explicit write grants, `git push` and `gh pr create` fail with 403.
- Always pair `schedule:` triggers with `workflow_dispatch:`. A cron-only workflow is untestable without waiting for the next fire. `workflow_dispatch:` costs nothing and enables ad-hoc runs from the Actions tab.
- Trivy exit-code split — one run for the report, one for the gate. Trivy cannot both emit a full report at all severities and fail only on HIGH/CRITICAL in a single invocation. Run twice: first with `severity: LOW,MEDIUM,HIGH,CRITICAL; exit-code: '0'` for the artefact, then with `severity: HIGH,CRITICAL; exit-code: '1'` for the merge gate.
- Derive image revision from git tags, not from a checked-in file. `existing=$(git tag --list "v${VERSION}-r*" | wc -l); revision=$((existing + 1))`. No manual bookkeeping, and the resulting `v<version>-r<n>` tag is self-authoritative — the next release always increments correctly.
- Hadolint `DL3008` (pin apt-get versions) is intentionally suppressed for this project. The image's CVE posture depends on the Ubuntu base image being rebuilt to pick up upstream fixes; pinning apt-get versions in the Dockerfile would freeze packages against that mechanism. The compensating control is the `Scan-Image` trivy gate. Do not "fix" this by adding version pins — document any additional suppression in `.hadolint.yaml` with the same rationale style.
- On Git Bash under Windows, `pwd` returns POSIX paths that Docker Desktop cannot mount. Detect Git Bash with `if pwd -W >/dev/null 2>&1`, then use `pwd -W` for the Windows path (`U:/...`) and set `MSYS_NO_PATHCONV=1` to stop MSYS from mangling `/work` in Docker arguments. See `test/integration/run.sh`.

ASPICE:
- ASPICE V4 compliance must be Fully Implemented on all processes required for Level 2

Rules:
- Make no changes to the disk outside of this repo folder
- Make no changes to any github repo other than CppCheckDocker
- Never merge a PR unless explicitly told to do so
- Only push when told to do so
- Only create a PR when told to do so
- Only make changes when told to do so - sometimes I want to work out an idea first
- Never ever push to main/master or make them the target of a PR unless told to do so

Goals:
The goal is full automation of:
- generation of the dockerfile
- testing
- publication to the GitHub Wiki
- publication to both DockerHub and GHCR
- consistent and up to date: WIKI, ReadMe and ASPICE documents

Permissions:
- You have permission to make changes as needed restricted to this repo folder and below
- You may run PowerShell, DOS, Ubuntu, Python, CPPCheck, Doxygen locally on this machine but changes are restricted to this repo folder and below
- You may spawn subagents (the Agent tool) without asking first, for example to fan out read-only searches or investigations

Other:
- This is a Windows machine, but other team members may use ubuntu
