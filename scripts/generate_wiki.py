#!/usr/bin/env python3
"""Regenerate the CppCheckDocker wiki from the repo.

Copies:

- ``documents/user_guide/*.md`` -> ``<wiki>/<basename>.md``  (User Guide)
- ``documents/aspice/**/*.md``  -> ``<wiki>/<basename>.md``  (ASPICE CL2, recursive)

Then generates the three navigation pages:

- ``_Sidebar.md``       — always-visible left navigation (User Guide + ASPICE
  CL2 grouped by ISO/IEC 33020 process category, plus Deviations / Internal
  Audits / Release Records / Capability Records / Traceability).
- ``Home.md``           — landing page with a short intro and top-level links.
- ``ASPICE-Index.md``   — flat table of every ASPICE page with process tag.

Wiki page names are the source file's basename (without ``.md``) — GitHub Wiki
does not preserve subdirectories, so ``documents/aspice/records/CCD-SVD-2.21.1-r1.md``
becomes wiki page ``CCD-SVD-2.21.1-r1``.

Usage::

    python scripts/generate_wiki.py --repo . --wiki wiki

Called by the ``Publish-Wiki`` job in ``.github/workflows/build.yml``. Safe to
run locally against a scratch checkout of the wiki repo.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

USER_GUIDE_ORDER = [
    "Quick-Start",
    "Docker-Usage",
    "MISRA-C-2012",
    "Pre-Commit-Integration",
    "Image-Tags-And-Publication",
    "CI-Workflow-Reference",
]

ASPICE_GROUPS_ORDER = [
    "System Engineering",
    "Software Engineering",
    "Management",
    "Support Processes",
    "Acquisition",
    "Software Release",
    "Capability Records",
    "Deviations",
    "Internal Audits",
    "Release Records",
    "Traceability",
]


def classify(stem: str) -> tuple[str, int]:
    """Return (group name, sort key) for an ASPICE file basename (no extension)."""
    if stem.startswith("CppCheckDocker_SYS_"):
        return "System Engineering", 0
    if stem.startswith("CppCheckDocker_SWE1_"):
        return "Software Engineering", 1
    if stem.startswith("CppCheckDocker_SWE2_"):
        return "Software Engineering", 2
    if stem.startswith("CppCheckDocker_SWE3_"):
        return "Software Engineering", 3
    if stem.startswith("CppCheckDocker_SWE4_"):
        return "Software Engineering", 4
    if stem.startswith("CppCheckDocker_SWE5_"):
        return "Software Engineering", 5
    if stem.startswith("CppCheckDocker_SWE6_"):
        return "Software Engineering", 6
    if stem.startswith("CppCheckDocker_MAN3_"):
        return "Management", 1
    if stem.startswith("CppCheckDocker_MAN5_"):
        return "Management", 5
    if stem.startswith("CppCheckDocker_SUP1_"):
        return "Support Processes", 1
    if stem.startswith("CppCheckDocker_SUP8_"):
        return "Support Processes", 8
    if stem.startswith("CppCheckDocker_SUP9_"):
        return "Support Processes", 9
    if stem.startswith("CppCheckDocker_ACQ4_"):
        return "Acquisition", 4
    if stem.startswith("CppCheckDocker_SPL2_"):
        return "Software Release", 2
    if stem.startswith("CppCheckDocker_SVD_"):
        return "Software Release", 9
    if stem.startswith("CppCheckDocker_PA2_"):
        return "Capability Records", 2
    if stem.startswith("CppCheckDocker_DEV"):
        return "Deviations", int(re.search(r"DEV(\d+)", stem).group(1))
    if stem.startswith("CppCheckDocker_AUD_") or stem.startswith("CppCheckDocker_AUD-"):
        return "Internal Audits", 0
    if stem.startswith("CCD-SVD-") or stem.startswith("CCD-QTR-"):
        return "Release Records", 0
    if stem.startswith("CppCheckDocker_RTM_"):
        return "Traceability", 0
    return "Traceability", 99  # fallback; keeps unknown items visible


def display_title(stem: str) -> str:
    """Human-friendly title for a page derived from its filename stem."""
    if stem.startswith("CppCheckDocker_"):
        rest = stem[len("CppCheckDocker_") :]
        return rest.replace("_", " ")
    if stem.startswith("CCD-"):
        return stem
    return stem.replace("-", " ").replace("_", " ")


def extract_process_tag(md: Path) -> str:
    text = md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(
        r"^\|\s*\*\*ASPICE Process\*\*\s*\|\s*(.+?)\s*\|",
        text,
        re.MULTILINE,
    )
    return m.group(1).strip() if m else "—"


def copy_docs(sources: list[Path], wiki: Path) -> list[Path]:
    copied: list[Path] = []
    for src in sources:
        dst = wiki / src.name
        shutil.copyfile(src, dst)
        copied.append(dst)
    return copied


def emit_sidebar(wiki: Path, user_guide: list[Path], aspice_groups: dict[str, list[Path]], ref: str, sha: str) -> None:
    lines: list[str] = []
    lines.append("### CppCheckDocker")
    lines.append(f"_Auto-published from `{ref}@{sha[:7]}`._")
    lines.append("")
    lines.append("**[Home](Home)**")
    lines.append("")
    lines.append("**User Guide**")
    user_pages_by_stem = {p.stem: p for p in user_guide}
    for stem in USER_GUIDE_ORDER:
        if stem in user_pages_by_stem:
            lines.append(f"- [{stem.replace('-', ' ')}]({stem})")
    for stem, _ in sorted(user_pages_by_stem.items()):
        if stem not in USER_GUIDE_ORDER:
            lines.append(f"- [{stem.replace('-', ' ')}]({stem})")
    lines.append("")
    lines.append("**ASPICE CL2**")
    lines.append("- [ASPICE Index](ASPICE-Index)")
    for group in ASPICE_GROUPS_ORDER:
        pages = aspice_groups.get(group, [])
        if not pages:
            continue
        lines.append(f"- _{group}_")
        for p in pages:
            stem = p.stem
            lines.append(f"  - [{display_title(stem)}]({stem})")
    (wiki / "_Sidebar.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def emit_home(wiki: Path, ref: str, sha: str) -> None:
    body = f"""# CppCheckDocker

Auto-published from `documents/user_guide/` and `documents/aspice/` on branch `{ref}` at commit `{sha[:7]}`.

CppCheckDocker packages the latest [cppcheck](https://github.com/danmar/cppcheck) release into an Ubuntu container image so GitHub Actions workflows on Linux runners can call a recent cppcheck without waiting for upstream Linux packages to catch up. The image also bundles the MISRA C:2012 rule-texts file (CC BY-NC-ND 4.0).

## User Guide

Start with [Quick Start](Quick-Start). From there:

- [Docker Usage](Docker-Usage) — mount modes, exit codes, GHA container example
- [MISRA C:2012](MISRA-C-2012) — bundled addon and rule-texts
- [Pre-commit Integration](Pre-Commit-Integration) — running the same lint gates locally
- [Image Tags and Publication](Image-Tags-And-Publication) — tag scheme and provenance
- [CI Workflow Reference](CI-Workflow-Reference) — every CI job explained

## ASPICE CL2

CppCheckDocker targets ASPICE v4 Level 2. Start with the [ASPICE Index](ASPICE-Index) for a flat list of every process document, or navigate the sidebar by ISO/IEC 33020 process category. Capability ratings are consolidated on the [PA2 Capability Records](CppCheckDocker_PA2_Capability_Records) page.
"""
    (wiki / "Home.md").write_text(body, encoding="utf-8")


def emit_aspice_index(wiki: Path, all_aspice: list[Path], ref: str, sha: str) -> None:
    lines: list[str] = []
    lines.append("# ASPICE Index")
    lines.append("")
    lines.append(f"Auto-generated from `documents/aspice/` on branch `{ref}` at commit `{sha[:7]}`.")
    lines.append("")
    lines.append("| Document | ASPICE Process |")
    lines.append("|:---------|:----------------|")
    for p in sorted(all_aspice, key=lambda x: x.stem):
        stem = p.stem
        proc = extract_process_tag(p)
        lines.append(f"| [{display_title(stem)}]({stem}) | {proc} |")
    (wiki / "ASPICE-Index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".", type=Path, help="Repo root")
    ap.add_argument("--wiki", default="wiki", type=Path, help="Wiki checkout dir")
    ap.add_argument("--ref", default="HEAD", help="Ref name to record in generated pages")
    ap.add_argument("--sha", default="0000000", help="Commit sha to record in generated pages")
    args = ap.parse_args(argv)

    repo = args.repo.resolve()
    wiki = args.wiki.resolve()
    wiki.mkdir(parents=True, exist_ok=True)

    user_guide_dir = repo / "documents" / "user_guide"
    aspice_dir = repo / "documents" / "aspice"

    user_guide_sources = sorted(p for p in user_guide_dir.glob("*.md") if p.name != "README.md")
    # Directories under documents/aspice/ that are NOT auditable ASPICE deliverables
    # and must not be re-published to the wiki. `claude_memory/` mirrors the
    # per-project Claude Code memory (issue #44) and lives under aspice/ only for
    # SUP.8 configuration control - it is not a wiki-facing ASPICE work product.
    aspice_wiki_excludes = {"claude_memory"}
    aspice_sources: list[Path] = []
    for p in aspice_dir.rglob("*.md"):
        if p.name == "README.md":
            continue
        rel = p.relative_to(aspice_dir)
        if rel.parts and rel.parts[0] in aspice_wiki_excludes:
            continue
        aspice_sources.append(p)

    if not aspice_sources:
        print("generate_wiki: no ASPICE sources found", file=sys.stderr)
        return 1

    copied_user = copy_docs(user_guide_sources, wiki)
    copied_aspice = copy_docs(aspice_sources, wiki)

    groups: dict[str, list[Path]] = {}
    for p in copied_aspice:
        group, sort_key = classify(p.stem)
        groups.setdefault(group, []).append((sort_key, p))
    grouped_sorted: dict[str, list[Path]] = {
        g: [p for _, p in sorted(items, key=lambda x: (x[0], x[1].stem))]
        for g, items in groups.items()
    }

    emit_sidebar(wiki, copied_user, grouped_sorted, args.ref, args.sha)
    emit_home(wiki, args.ref, args.sha)
    emit_aspice_index(wiki, copied_aspice, args.ref, args.sha)

    print(
        f"generate_wiki: wrote {len(copied_user)} user-guide pages, "
        f"{len(copied_aspice)} aspice pages, plus _Sidebar / Home / ASPICE-Index."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
