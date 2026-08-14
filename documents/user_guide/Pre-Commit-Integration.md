# Pre-commit Integration

Install [pre-commit](https://pre-commit.com/) once per clone to catch the same lint issues locally that the CI `Lint` job would catch on push.

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Hooks in this repo

Configured in [`.pre-commit-config.yaml`](https://github.com/dermot-murphy/CppCheckDocker/blob/main/.pre-commit-config.yaml):

- `hadolint` — Dockerfile best-practice linting (config: `.hadolint.yaml`).
- `yamllint` — YAML syntax and style (config: `.yamllint.yaml`).
- `trailing-whitespace`, `end-of-file-fixer`, `mixed-line-ending` — hygiene fixers (`documents/assets/` and `documents/aspice/claude_memory/` are excluded so vendored / auto-mirrored content is not rewritten).
- `check-added-large-files`, `check-merge-conflict` — safety nets.
- `claude-memory-sync` (local) — mirrors Claude Code per-project memory into `documents/aspice/claude_memory/`. Fires only when the developer has that memory dir; no-ops otherwise.

## hadolint runs in Docker

The `hadolint-docker` hook shells out to Docker, so Docker Desktop (or a Linux daemon) must be running when pre-commit fires. CI already runs Docker; locally, the same daemon that builds the image serves the lint hook.

## Windows lock hygiene

On Windows, close SourceTree and Segger before committing — both hold file locks that break pre-commit's stash/restore step. As an extra guard, prefer `git stash push -u` before `git commit` and `git stash pop` after, which keeps pre-commit's own stash logic off any file that another process might touch.

## What runs in CI

The same hooks fire in the `Lint` job on every push and PR — locally passing checks means the CI lint gate should pass too.
