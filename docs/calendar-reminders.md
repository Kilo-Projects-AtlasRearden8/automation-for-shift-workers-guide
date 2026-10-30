# Calendar Reminders

Never miss an appointment, bill, shift start, or due date — even when your
sleep schedule shifts around. This guide covers reminders in your calendar app
plus a tiny local script that reads a plain-text reminders file and tells you
what's due today, coming up, or overdue.

## Reminders in your calendar app

Use whatever calendar you already use (phone, Google Calendar, Outlook,
Apple Calendar). Set reminders relative to your shift, not to a fixed time of
day:

- **Before a night shift:** "Sleep before night shift" — 2 hours before shift
  start
- **After a night shift:** "Sleep in / no alarms" — day after your shift ends
- **Before rotating onto nights:** "Adjust bedtime" — 3 days before the
  rotation starts
- **Bills:** due date minus 3 days, so you pay before payday lands
- **Shift swap reply by:** the day your coworker asked for an answer

Set recurring reminders for things that repeat each shift cycle (payday,
license renewal check, CE credits due).

---

## Local reminders script (`scripts/calendar_reminders.py`)

If you prefer a plain-text list that lives on your computer, there's a small
script for it. It reads `reminders.txt` (one line per reminder) and prints
what's due today, upcoming within N days, or overdue.

Each line looks like:

```
name | due date (YYYY-MM-DD) | message
```

Example:

```
Electric bill | 2026-11-05 | Pay the electric bill
Night shift starts | 2026-11-07 | Sleep by 8 AM tomorrow
Shift swap reply due | 2026-11-03 | Reply to Maya about the 11th
```

Run it:

```
python3 scripts/calendar_reminders.py reminders.txt
```

It defaults to a dry-run: prints each reminder and a `mailto:` link you can
click to email yourself — it sends nothing. With `--apply` and SMTP
environment variables set in your own shell (never in this file), it can send
for real.

```
python3 scripts/calendar_reminders.py reminders.txt --within 14 --apply
```

Options:
- `--within N` — report reminders due within N days (default 7)
- `--apply` — send via SMTP using `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`,
  `SMTP_PASS`, `FROM_EMAIL`, `TO_EMAIL` environment variables
- `--dry-run` (default) — print only, send nothing

### Shift-work tip

Put reminders in `reminders.txt` keyed to your roster rather than calendar
dates when you can: "the Monday after my last night shift" works better than
a date that changes every rotation. Update the file when your schedule comes
out.

## Troubleshooting

- **Nothing shows up:** Check the date format is `YYYY-MM-DD` and that lines
  have three `|`-separated parts. Malformed lines are skipped with a warning.
- **mailto: link doesn't open anything:** Your computer needs a default email
  app set. You can also copy the reminder text and paste it into your email
  app yourself.
- **--apply sends nothing:** SMTP environment variables must be set in your
  shell. Nothing is hardcoded, and no credentials are stored in this project.

Calendar reminders are an organizational tool, not medical advice. If sleep
or fatigue is a concern, talk to a qualified clinician.
