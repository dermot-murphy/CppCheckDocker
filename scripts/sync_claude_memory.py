#!/usr/bin/env python3
"""Mirror Claude Code user-scope memory into the repo.

Claude Code stores per-project memory under
``~/.claude/projects/<slug>/memory/`` where ``<slug>`` is the repo's absolute
path with ``:`` and path separators replaced by ``-``. Those files (the
``MEMORY.md`` index plus individual memory records) are user-scoped by default
and therefore invisible to other machines, teammates, and the ASPICE audit
trail.

This script mirrors that directory into ``documents/aspice/claude_memory/``
inside the repo and stages any changes. It is invoked by a ``pre-commit`` local
hook so the mirror stays in step with each commit automatically; it is also
safe to run by hand.

Exit codes follow the pre-commit convention: ``0`` = nothing changed, ``1`` =
files were updated (pre-commit reports the hook as failed so the developer
re-runs ``git commit`` to pick up the freshly staged copies).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    out = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()
    return Path(out)


def claude_slug(repo: Path) -> str:
    resolved = str(repo.resolve())
    return (
        resolved.replace(":", "-").replace("\\", "-").replace("/", "-")
    )


def user_memory_dir(repo: Path) -> Path:
    return Path.home() / ".claude" / "projects" / claude_slug(repo) / "memory"


def sync(src: Path, dst: Path) -> list[Path]:
    dst.mkdir(parents=True, exist_ok=True)
    changed: list[Path] = []
    src_names = {p.name for p in src.glob("*.md") if p.name != "README.md"}
    for name in src_names:
        s = src / name
        d = dst / name
        if not d.exists() or s.read_bytes() != d.read_bytes():
            shutil.copy2(s, d)
            changed.append(d)
    for d in dst.glob("*.md"):
        if d.name == "README.md":
            continue
        if d.name not in src_names:
            d.unlink()
            changed.append(d)
    return changed


def main() -> int:
    repo = repo_root()
    user_dir = user_memory_dir(repo)
    repo_dir = repo / "documents" / "aspice" / "claude_memory"

    user_has_memory = user_dir.is_dir() and any(user_dir.glob("*.md"))
    repo_has_memory = repo_dir.is_dir() and any(
        p.name != "README.md" for p in repo_dir.glob("*.md")
    )

    if not user_has_memory and repo_has_memory:
        user_dir.mkdir(parents=True, exist_ok=True)
        restored = sync(repo_dir, user_dir)
        if restored:
            print(
                "claude-memory-sync: restored user-scope memory from repo mirror:",
                file=sys.stderr,
            )
            for p in sorted(restored):
                print(f"  {p}", file=sys.stderr)
        return 0

    if not user_has_memory:
        print(
            f"claude-memory-sync: no memory to mirror ({user_dir} empty).",
            file=sys.stderr,
        )
        return 0

    changed = sync(user_dir, repo_dir)
    if not changed:
        return 0

    print("claude-memory-sync: mirrored memory files:")
    for p in sorted(changed):
        print(f"  {p.relative_to(repo).as_posix()}")

    subprocess.run(
        ["git", "add", "--", str(repo_dir.relative_to(repo).as_posix())],
        cwd=repo,
        check=True,
    )
    print(
        "claude-memory-sync: staged updated files; re-run `git commit` to include them.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
