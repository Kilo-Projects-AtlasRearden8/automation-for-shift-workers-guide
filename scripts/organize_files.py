#!/usr/bin/env python3
"""File organizer for shift paperwork.

Sorts a folder into type-based subfolders by file extension. Suggested
categories for shift work: schedules, pay stubs, certifications, health
records, taxes, archive.

Standard library only. Defaults to a dry-run (preview): prints what it would
do without moving anything. With --apply it moves files, never overwriting
(duplicate names get -1, -2, ...). Destination folders are skipped, so running
twice on the same folder is safe.

No credentials, API keys, or personal data are stored in this script or the
repo. Test on a copy of your files first.
"""

import os
import shutil
import sys

EXTENSION_GROUPS = {
    "schedules": [".pdf", ".png", ".jpg", ".jpeg", ".ics", ".csv"],
    "pay": [".pdf", ".png", ".jpg", ".jpeg", ".csv"],
    "certs": [".pdf", ".png", ".jpg", ".jpeg", ".docx", ".doc"],
    "health": [".pdf", ".png", ".jpg", ".jpeg"],
    "taxes": [".pdf", ".png", ".jpg", ".jpeg", ".csv"],
    "archive": [".pdf", ".png", ".jpg", ".jpeg", ".csv", ".docx", ".doc"],
}

CATEGORY_KEYWORDS = {
    "schedules": ["schedule", "roster", "shift", "bid", "time-off", "timeoff"],
    "pay": ["paystub", "pay stub", "paycheck", "pay slip", "payslip", "deposit"],
    "certs": ["cert", "license", "ce ", "continuing", "renewal", "bnls", "acls",
              "pal", "rn", "lpn"],
    "health": ["immunization", "vaccine", "physical", "tb ", "titer", "flu"],
    "taxes": ["w-2", "w2", "tax", "1099", "estimated", "deduct"],
}

DEFAULT_CATEGORY = "misc"


def category_for_name(name):
    """Guess a category from the filename; falls back to misc."""
    lower = name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lower:
                return category
    return DEFAULT_CATEGORY


def destination_folder(category, dest_root):
    return os.path.join(dest_root, category.title())


def unique_path(path):
    """Return a non-existing path by appending -1, -2, ... before the suffix."""
    if not os.path.exists(path):
        return path
    root, ext = os.path.splitext(path)
    counter = 1
    while True:
        candidate = f"{root}-{counter}{ext}"
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def plan_moves(folder):
    """Return a list of (source, destination) move plans without moving."""
    moves = []
    for entry in sorted(os.listdir(folder)):
        source = os.path.join(folder, entry)
        if os.path.isdir(source):
            continue
        _, ext = os.path.splitext(entry)
        category = category_for_name(entry) if ext.lower() in (
            ".pdf", ".png", ".jpg", ".jpeg", ".ics", ".csv", ".docx", ".doc"
        ) else DEFAULT_CATEGORY
        dest_dir = destination_folder(category, folder)
        dest = unique_path(os.path.join(dest_dir, entry))
        moves.append((source, dest))
    return moves


def apply_moves(moves):
    """Execute the planned moves, creating folders as needed."""
    moved = 0
    for source, dest in moves:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.move(source, dest)
        moved += 1
    return moved


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    apply_mode = False
    folder = None

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--apply", "-a"):
            apply_mode = True
        elif arg in ("--dry-run", "-n"):
            apply_mode = False
        elif not arg.startswith("-"):
            folder = arg
        else:
            print(f"Error: unknown option: {arg}", file=sys.stderr)
            return 1
        i += 1

    if folder is None:
        print("Usage: python3 organize_files.py <folder> [--apply]", file=sys.stderr)
        print("\nDry-run by default: shows what would move, moves nothing.")
        print("--apply: actually moves files into type-based subfolders.")
        print("\nSafety: test on a copy first. Destination folders are skipped.")
        return 1

    if not os.path.isdir(folder):
        print(f"Error: not a directory: {folder}", file=sys.stderr)
        return 1

    moves = plan_moves(folder)

    if not moves:
        print("No files to organize in", folder)
        return 0

    if apply_mode:
        count = apply_moves(moves)
        print(f"Moved {count} file(s) in {folder}")
    else:
        print(f"Would move {len(moves)} file(s) in {folder} (dry-run):")
        for source, dest in moves:
            rel_source = os.path.relpath(source, folder)
            rel_dest = os.path.relpath(dest, folder)
            print(f"  {rel_source}  ->  {rel_dest}")
        print("\n(No files were moved. Pass --apply to apply.)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
