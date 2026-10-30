# File Organization

Shift work creates a lot of paper: shift schedules, pay stubs, time-off
requests, certifications, license renewals, CE credits, immunization records,
tax forms. This guide shows you how to sort a messy folder into tidy
subfolders — by hand or with a tiny script — so you can find what you need
when you need it.

## Suggested folders for shift paperwork

- `Schedules/` — rosters, shift bids, time-off requests
- `Pay/` — pay stubs, direct deposit notices
- `Certs/` — certifications, license renewals, CE credits
- `Health/` — immunization records, physicals (nothing patient-related)
- `Taxes/` — W-2s, quarterly estimates, receipts you might deduct
- `Archive/` — anything older than a year

Rename files as you file them: `2026-11-paystub.pdf` beats `scan_042.pdf`.
A little naming goes a long way on irregular schedules.

## Local organizer script (`scripts/organize_files.py`)

There's a small script that sorts a folder into type-based subfolders based on
file extension. It defaults to a dry-run: it prints what it would do without
moving anything.

Run it on a test copy first:

```
python3 scripts/organize_files.py ~/Downloads
```

Preview shows what would move. When you're sure:

```
python3 scripts/organize_files.py ~/Downloads --apply
```

It skips the destination folders themselves and avoids overwriting files by
adding a number if a name already exists. Standard library only — nothing to
install, nothing uploaded.

## Troubleshooting

- **Nothing moved:** You ran the preview. Add `--apply` to actually move
  files, and test on a copy first.
- **File already exists:** The script adds `-1`, `-2`, etc. to avoid
  overwriting. Check the destination folder.
- **Destination folders skipped:** The organizer won't sort into its own
  output folders, so running it twice on the same folder is safe.

File organization is an organizational tool, not financial or medical advice.
Keep originals of anything legally important (license, certifications,
tax forms) somewhere safe — the script moves copies within a folder you point
it at, and you should test on copies first.
