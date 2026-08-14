---
name: github-closes-keyword-per-issue
description: "When a PR closes multiple issues on merge, put a `Closes`/`Fixes` keyword before EACH issue number, not just the first — otherwise GitHub only auto-closes the first."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f3044413-d8e6-454b-bc4d-561cb55b656b
  modified: 2026-08-13T15:59:44.788Z
---

When writing a PR body that should auto-close multiple issues, put a `Closes`/`Fixes`/`Resolves` keyword before **each** issue number. A comma-separated list after one keyword closes only the first issue.

**Wrong (only #21 closes):**
> Closes #21, #23, #24.

**Right (all three close):**
> Closes #21, closes #23, closes #24.

Or one line each:
> Closes #21.
> Closes #23.
> Closes #24.

**Why:** GitHub's linked-issue parser is per-token, not per-list. Cost of learning: on PR #27 (develop -> main sync), only #21 auto-closed; #23 and #24 had to be closed manually with a reference to the merge.

**How to apply:** any time a PR body cites more than one closing issue. Especially load-bearing on this repo because [[project-issues-close-on-main-merge]] — issues stay open through develop merges and rely on the final main-merge PR to close them; if that PR's body is malformed, the whole batch stays open.
