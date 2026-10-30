# STATUS — No-Code Automation for Shift Workers

## What was built

A beginner manual on no-code automation for irregular schedules — night shifts,
rotating rosters, overtime, and shift swaps — not 9-to-5 routines, published by
**Asdale Dynamics, LLC** (credit to Dylan Asdale, registered nurse turned AI
author and founder of Asdale Dynamics, LLC). Covers four topics: email rules,
calendar reminders, shift-swap tracking, and file organization, plus a
printable shift-work automation planner.

**Project contents**

- `README.md` — overview, how to use, credits Asdale Dynamics, LLC.
- `LICENSE` — MIT License, copyright line exactly
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `docs/` — beginner manual in Markdown:
  - `overview.md` — welcome, table of contents, printable planner, about Asdale
    Dynamics, LLC, license
  - `safety.md` — safety first (test on copies, preview before act, read
    scripts, start small, nothing leaves your computer)
  - `email-rules.md` — Gmail, Outlook, and Apple Mail rules with step-by-step
    instructions and example rules, written for shift-work inboxes
  - `calendar-reminders.md` — calendar reminders tied to shifts plus the local
    `reminders.txt` script
  - `shift-swap-tracking.md` — what to record for every swap plus the local
    CSV tracker
  - `file-organization.md` — suggested folders for shift paperwork plus the
    local organizer script
- `scripts/` — tiny, auditable Python scripts (standard library only; no
  `pip install`, no API keys, no secrets):
  - `organize_files.py` — sort a folder into type-based subfolders, dry-run by
    default, `--apply` to move
  - `calendar_reminders.py` — reminders from a local `reminders.txt`, dry-run
    by default, SMTP send only with `--apply` and env vars
  - `shift_swap_tracker.py` — add/list/upcoming/status/export for `swaps.csv`
- `tests/` — test suite for each script plus a static-site verification test:
  - `test_organize_files.py`
  - `test_calendar_reminders.py`
  - `test_shift_swap_tracker.py`
  - `test_static_site.py` — HTML pages parse, internal links resolve, every
    page credits Asdale Dynamics, LLC and carries the copyright line
- `static/` — fully static HTML site mirroring the docs (no build step, no
  server needed):
  - `index.html`, `safety.html`, `email-rules.html`, `calendar-reminders.html`,
    `shift-swap-tracking.html`, `file-organization.html`, `planner.html`,
    `style.css`
- `static/planner.html` — printable shift-work automation planner with day /
  evening / night / off shift blocks, a swap tracker table, weekly check-in,
  and print CSS that hides on-screen buttons
- `.gitignore` — excludes `__pycache__`, `.env`, `.venv`, `node_modules`, and
  personal data files (`swaps.csv`, `reminders.txt`)
- `STATUS.md` — this file

## How to run it

### Read the manual

- Markdown: open any file in `docs/`.
- HTML: open `static/index.html` in any browser. The site is fully static — no
  build step, no server needed. All pages link to one another.

### Run the scripts

Each script is plain Python 3, standard library only. No `pip install`, no
API keys, no secrets.

```
python3 scripts/organize_files.py <folder> [--apply]
python3 scripts/calendar_reminders.py <reminders.txt> [--within N] [--apply]
python3 scripts/shift_swap_tracker.py [--csv <path>] <command> [args]
```

Commands for `shift_swap_tracker.py`: `add`, `list`, `upcoming`, `status`,
`export`. Default CSV is `swaps.csv` on your computer.

**Safety:** every script defaults to a non-destructive preview (dry-run) and
works on copies by default. Always test on a copy first. See `docs/safety.md`.
`calendar_reminders.py --apply` only sends when `SMTP_*` environment variables
are set in your own shell; nothing is hardcoded.

### Run the tests

```
python3 tests/test_organize_files.py
python3 tests/test_calendar_reminders.py
python3 tests/test_shift_swap_tracker.py
python3 tests/test_static_site.py
```

### Print the planner

Open `static/planner.html` and print from your browser (Letter size). Print
styles hide on-screen buttons automatically.

## Verification results

All checks pass:

- `tests/test_organize_files.py` — PASS (extension grouping, dry-run moves
  nothing, --apply moves files, duplicate avoidance with -1/-2 suffixes,
  misc fallback for unknown extensions)
- `tests/test_calendar_reminders.py` — PASS (parsing, malformed lines and bad
  dates skipped, today/upcoming/overdue categorization, mailto uses TO_EMAIL,
  dry-run sends nothing)
- `tests/test_shift_swap_tracker.py` — PASS (add/reject bad dates, list,
  status change, upcoming filtering, export to CSV)
- `tests/test_static_site.py` — PASS (7 HTML pages parse cleanly, all internal
  links resolve, every page credits Asdale Dynamics, LLC and carries the
  copyright line)
- All Python files compile cleanly (`py_compile`).
- CLI smoke test: `organize_files.py --apply` moves files into `Misc/`;
  `calendar_reminders.py` reports upcoming/overdue correctly;
  `shift_swap_tracker.py add`/`list` works against a temp CSV.
- No build step, no dependencies beyond Python 3. No `.github/workflows` files
  (by design). No secrets, API keys, or personal data in any committed file.

The repo was initialized and committed locally as one plain commit using the
existing git identity; nothing was pushed and no remote was created.

## Known gaps

- `calendar_reminders.py` SMTP sending requires the user to set `SMTP_*`
  environment variables in their own shell; not exercised end-to-end against a
  real mail server (no credentials available, by design).
- Reminder data (`reminders.txt`) and swap data (`swaps.csv`) live on the
  user's computer and must not be committed — already ignored by `.gitignore`.
- The organizer script guesses categories from filename keywords; files with
  unrecognized names land in `Misc/`. No image content inspection.
- Shift-swap tracking is an organizational tool, not a scheduling system; the
  unit's official schedule and approval process always win.
- The HTML site is hand-written (not generated from Markdown), so `docs/` and
  `static/` must be kept in sync manually.
- Email rules, calendar reminders, shift-swap tracking, and file organization
  are organizational tools, not financial or medical advice (noted in the
  docs). This guide is education only, not medical advice.
