# Claude Code Memory Mirror

This directory mirrors the per-project Claude Code memory that lives under
`~/.claude/projects/<slug>/memory/` on each developer's workstation. It is
kept in the repo so that:

- lessons learned survive a fresh clone on a new machine,
- teammates and future Claude sessions see the same accumulated context, and
- the ASPICE audit trail includes the retrospective knowledge Claude has
  captured while working on this codebase.

## How the mirror stays current

`scripts/sync_claude_memory.py` copies `.md` files from the user-scope memory
directory into this folder. It is invoked by the `claude-memory-sync` local
hook in `.pre-commit-config.yaml` on every commit, so any new or updated
memory record is staged automatically. If the sync produces changes, the hook
exits non-zero (pre-commit convention) so the developer re-runs `git commit`
with the freshly staged copies included.

The script is safe to run manually:

```bash
python scripts/sync_claude_memory.py
```

## Contents

- `MEMORY.md` - Claude's per-project index; always auto-loaded by Claude Code.
- Individual memory records (`feedback_*.md`, `project_*.md`, `user_*.md`,
  `reference_*.md`) - one per rule, fact, or lesson.

Files here are managed by the sync script; edits made directly in this
directory are overwritten on the next commit. Author memories through Claude
Code (which writes them to the user-scope location) and let the mirror follow.
