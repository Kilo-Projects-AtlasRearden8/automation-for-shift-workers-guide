# Shift-Swap Tracking

Shift swaps happen on paper, in texts, and from memory — until someone
forgets who owes whom. This guide shows you a tiny local tracker that keeps
swaps in a plain CSV file on your computer (`swaps.csv`), plus what to write
down for every swap so nothing slips through the cracks.

## What to record for every swap

| Field | What it means |
|-------|-------------|
| My date | The date of your shift being swapped |
| Their date | The date of their shift being swapped |
| Coworker | Who you're swapping with |
| Status | `pending`, `approved`, `denied`, `done` |
| Approved by | Manager or charge nurse who signed off (if required) |
| Notes | Unit, shift type (days/evenings/nights), any conditions |

Never put patient names, room numbers, or any health information in the swap
tracker. It's for dates and names only.

## Local tracker script (`scripts/shift_swap_tracker.py`)

The script keeps swaps in `swaps.csv` (comma-separated, easy to open in a
spreadsheet) on your computer. Nothing is uploaded, and nothing is hardcoded.

Add a swap:

```
python3 scripts/shift_swap_tracker.py add "2026-11-07" "2026-11-10" Maya pending "Charge nurse approved"
```

List swaps:

```
python3 scripts/shift_swap_tracker.py list
```

List only swaps needing attention (pending or upcoming within N days):

```
python3 scripts/shift_swap_tracker.py upcoming --within 7
```

Mark a swap approved or done:

```
python3 scripts/shift_swap_tracker.py status 1 approved
python3 scripts/shift_swap_tracker.py status 1 done
```

The number (`1`, `2`, ...) is the row number from `list`.

Export to a spreadsheet-friendly CSV:

```
python3 scripts/shift_swap_tracker.py export swaps-backup.csv
```

Every command defaults to a preview where it makes sense; nothing is changed
until you confirm. `swaps.csv` lives on your computer — it's ignored by git
and never meant to be committed.

## Example tracker

```
my_date,their_date,coworker,status,approved_by,notes
2026-11-07,2026-11-10,Maya,pending,Charge nurse,Nights, unit 4B
2026-11-14,2026-11-08,Jamal,approved,J. Miller,Evenings for days
```

## Tips

- Add swaps as soon as they're discussed, while details are fresh.
- Review `upcoming --within 7` at the start of each week so approvals don't
  lapse.
- Keep `swaps.csv` backed up however you back up your other files — it's just
  a text file.
- Shift-swap tracking is an organizational tool, not a scheduling system. Your
  unit's official schedule and approval process always win.
