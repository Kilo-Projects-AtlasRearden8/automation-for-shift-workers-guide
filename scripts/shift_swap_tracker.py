#!/usr/bin/env python3
"""Shift-swap tracker for irregular schedules.

Keeps shift swaps in a local CSV file (swaps.csv by default) on your computer:
my_date, their_date, coworker, status, approved_by, notes.

Nothing is uploaded, nothing is hardcoded, and swaps.csv is ignored by git.
Commands:

  add <my_date> <their_date> <coworker> [status] [approved_by] [notes]
      Record a new swap. Dates in YYYY-MM-DD format. Status defaults to pending.
  list [--status STATUS]     List swaps, optionally filtered by status.
  upcoming [--within N]      List pending/approved swaps within N days (default 7).
  status <row> <status>      Mark row N (from list) as approved/denied/done.
  export <path>              Export swaps to a CSV file (spreadsheet-friendly).

Standard library only. Everything stays on your computer. Test on a copy of
swaps.csv first; nothing patient-related belongs in this file.
"""

import csv
import os
import sys

DEFAULT_CSV = "swaps.csv"
FIELDNAMES = ["my_date", "their_date", "coworker", "status",
              "approved_by", "notes"]
VALID_STATUSES = {"pending", "approved", "denied", "done"}


def load_swaps(path):
    """Load swaps from CSV. Returns a list of dicts; missing file is empty."""
    swaps = []
    if not os.path.exists(path):
        return swaps
    with open(path, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if not any((value or "").strip() for value in row.values()):
                continue
            swaps.append({
                "my_date": (row.get("my_date") or "").strip(),
                "their_date": (row.get("their_date") or "").strip(),
                "coworker": (row.get("coworker") or "").strip(),
                "status": (row.get("status") or "pending").strip(),
                "approved_by": (row.get("approved_by") or "").strip(),
                "notes": (row.get("notes") or "").strip(),
            })
    return swaps


def save_swaps(path, swaps):
    """Write swaps back to CSV (rewrites the whole file)."""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for swap in swaps:
            writer.writerow({field: swap.get(field, "") for field in FIELDNAMES})


def valid_date(value):
    try:
        from datetime import date
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def cmd_add(args, path):
    if len(args) < 3:
        print("Usage: shift_swap_tracker.py add <my_date> <their_date> "
              "<coworker> [status] [approved_by] [notes]", file=sys.stderr)
        return 1
    my_date, their_date, coworker = args[0], args[1], args[2]
    if not valid_date(my_date) or not valid_date(their_date):
        print("Error: dates must be YYYY-MM-DD", file=sys.stderr)
        return 1
    status = args[3] if len(args) > 3 and args[3] in VALID_STATUSES else "pending"
    approved_by = args[4] if len(args) > 4 else ""
    notes = args[5] if len(args) > 5 else ""

    swaps = load_swaps(path)
    swaps.append({
        "my_date": my_date, "their_date": their_date, "coworker": coworker,
        "status": status, "approved_by": approved_by, "notes": notes,
    })
    save_swaps(path, swaps)
    print(f"Added swap: {my_date} <-> {their_date} with {coworker} ({status})")
    return 0


def cmd_list(args, path):
    status_filter = None
    i = 0
    while i < len(args):
        if args[i] == "--status" and i + 1 < len(args):
            status_filter = args[i + 1]
            i += 2
        else:
            i += 1
    swaps = load_swaps(path)
    if status_filter:
        swaps = [s for s in swaps if s["status"] == status_filter]
    if not swaps:
        print("No swaps found." + (f" (status: {status_filter})" if status_filter else ""))
        return 0
    for idx, swap in enumerate(swaps, start=1):
        print(f"{idx}. {swap['my_date']} <-> {swap['their_date']} — "
              f"{swap['coworker']} — {swap['status']}"
              + (f" — approved by {swap['approved_by']}" if swap['approved_by'] else "")
              + (f" — {swap['notes']}" if swap['notes'] else ""))
    return 0


def cmd_upcoming(args, path):
    within_days = 7
    i = 0
    while i < len(args):
        if args[i] == "--within" and i + 1 < len(args):
            try:
                within_days = int(args[i + 1])
            except ValueError:
                print("Error: --within must be a number", file=sys.stderr)
                return 1
            i += 2
        else:
            i += 1
    from datetime import date, timedelta
    today = date.today()
    limit = today + timedelta(days=within_days)
    swaps = load_swaps(path)
    upcoming = []
    for swap in swaps:
        if swap["status"] not in ("pending", "approved"):
            continue
        for d in (swap["my_date"], swap["their_date"]):
            if valid_date(d):
                due = date.fromisoformat(d)
                if today <= due <= limit:
                    upcoming.append((due, swap))
                    break
    upcoming.sort(key=lambda item: item[0])
    if not upcoming:
        print(f"No swaps within the next {within_days} day(s).")
        return 0
    print(f"Swaps within {within_days} day(s):")
    for due, swap in upcoming:
        day_word = "today" if due == today else ("tomorrow" if (due - today).days == 1
                                                   else f"in {(due - today).days} day(s)")
        print(f"  - {swap['my_date']} <-> {swap['their_date']} — {swap['coworker']} "
              f"— {swap['status']} ({day_word})")
    return 0


def cmd_status(args, path):
    if len(args) < 2:
        print("Usage: shift_swap_tracker.py status <row> <status>", file=sys.stderr)
        return 1
    try:
        row = int(args[0])
    except ValueError:
        print("Error: row must be a number", file=sys.stderr)
        return 1
    new_status = args[1]
    if new_status not in VALID_STATUSES:
        print(f"Error: status must be one of {', '.join(sorted(VALID_STATUSES))}",
              file=sys.stderr)
        return 1

    swaps = load_swaps(path)
    if row < 1 or row > len(swaps):
        print(f"Error: no swap row {row}", file=sys.stderr)
        return 1
    old = swaps[row - 1]["status"]
    swaps[row - 1]["status"] = new_status
    save_swaps(path, swaps)
    print(f"Row {row}: {old} -> {new_status}")
    return 0


def cmd_export(args, path):
    if len(args) < 1:
        print("Usage: shift_swap_tracker.py export <path>", file=sys.stderr)
        return 1
    out_path = args[0]
    swaps = load_swaps(path)
    save_swaps(out_path, swaps)
    print(f"Exported {len(swaps)} swap(s) to {out_path}")
    return 0


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "upcoming": cmd_upcoming,
    "status": cmd_status,
    "export": cmd_export,
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    path = DEFAULT_CSV
    command = None
    command_args = []

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--csv" and i + 1 < len(argv):
            path = argv[i + 1]
            i += 2
        elif not arg.startswith("-"):
            command = arg
            command_args = argv[i + 1:]
            break
        else:
            print(f"Error: unknown option: {arg}", file=sys.stderr)
            return 1

    if command is None or command not in COMMANDS:
        print("Usage: python3 shift_swap_tracker.py [--csv <path>] "
              "<command> [args]", file=sys.stderr)
        print("\nCommands:")
        print("  add <my_date> <their_date> <coworker> [status] [approved_by] [notes]")
        print("  list [--status STATUS]")
        print("  upcoming [--within N]")
        print("  status <row> <status>")
        print("  export <path>")
        print(f"\nDefault CSV: {path} (stays on your computer, ignored by git)")
        print("\nSafety: nothing is uploaded. Never record patient information.")
        return 1

    return COMMANDS[command](command_args, path)


if __name__ == "__main__":
    sys.exit(main())
