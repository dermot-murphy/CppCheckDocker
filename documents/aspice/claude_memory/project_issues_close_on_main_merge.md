---
name: project-issues-close-on-main-merge
description: "On CppCheckDocker, GitHub issues close when the fix reaches main, not when the feature PR merges to develop."
metadata: 
  node_type: memory
  type: project
  originSessionId: f3044413-d8e6-454b-bc4d-561cb55b656b
  modified: 2026-08-13T16:01:12.715Z
---

On this repo, GitHub issues are expected to close on merge to `main`, not on merge to `develop`.

**Why:** the gitflow model (see CLAUDE.md Workflow section) means feature PRs land on `develop` first and only reach `main` at release-cut time; the user treats "issue closed" as "shipped", not "code accepted". They confirmed this convention explicitly.

**How to apply:**
- Do NOT offer to manually close issues after their feature/hotfix PR merges to `develop` — that's expected behaviour, not a bug.
- **Immediately after a feature/hotfix PR merges to `develop`, add the `pending-merge` label to the underlying GitHub issue** (`gh issue edit <n> --add-label pending-merge`). This marks the issue as corrected-on-develop-but-awaiting-release. Do this without being asked; it is part of the merge workflow, not an optional cleanup step.
- The `pending-merge` label exists on the repo; do not recreate it. Its description: "Issue corrected, merged to develop, will close on merge to main".
- The final `develop -> main` PR is the one whose body must carry `Closes #N` for every pending-merge issue (see [[github-closes-keyword-per-issue]] for the per-issue keyword requirement).
- After the develop -> main PR merges, verify every listed issue actually closed; the parser is fragile. The `pending-merge` label falls off automatically only if the issue closes — if the auto-close missed one, close it manually AND the label goes with it.
