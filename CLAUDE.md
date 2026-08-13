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
- a new branch name for a change request or enhancement (issue label enhancement) is "feature/CR-"<Github issue number>-<github issue abstract>
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
