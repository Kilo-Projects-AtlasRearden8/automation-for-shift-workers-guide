# No-Code Automation for Shift Workers

A beginner-friendly manual on automating life around irregular schedules —
night shifts, rotating rosters, overtime, and shift swaps — using tools you
already have plus tiny, auditable scripts you can read end to end. Test on
copies, never move originals. Everything stays on your computer unless you
choose otherwise.

You don't need to be a programmer. You don't need to have used the command
line before. If you can copy and paste, you can use this manual. Plain
English, step by step, never condescending.

**Credit:** This manual is published by **Asdale Dynamics, LLC** (Indiana,
formed October 2026), founded by Dylan Asdale — a registered nurse turned AI
author and founder of Asdale Dynamics, LLC. Dylan writes and teaches AI "like
a friend would": plain English, step by step, never condescending. Learn more
at dylanasdale.github.io.

---

## Who this is for

Anyone whose schedule doesn't run 9-to-5:

- Nurses, EMTs, and other healthcare staff on rotating or night shifts
- Shift workers whose sleep, meals, and errands revolve around the roster
- Anyone juggling shift bids, overtime, and shift swaps
- People who need reminders tied to their next shift, not to Monday at 9 AM

You don't need to buy anything, create any accounts, or share any personal
data. Everything in this manual runs locally on your own computer.

---

## What you need

- A computer (Windows, Mac, or Linux)
- Python 3 (already on most Macs and Linux PCs; download it free from python.org if you need it)
- About twenty minutes to read the safety page first

That's it. No paid accounts, no API keys, no subscriptions.

---

## What's inside

| Topic | What it does | Where |
|-------|-------------|-------|
| Safety first | The rules to follow before you automate anything | `docs/safety.md` |
| Email rules | Sort incoming email automatically (Gmail, Outlook, Apple Mail) | `docs/email-rules.md` |
| Calendar reminders | Reminders tied to shifts, appointments, bills, due dates | `docs/calendar-reminders.md` + `scripts/calendar_reminders.py` |
| Shift-swap tracking | Track swaps, approvals, and who owes whom | `docs/shift-swap-tracking.md` + `scripts/shift_swap_tracker.py` |
| File organization | Sort shift paperwork into folders: schedules, pay stubs, certs | `docs/file-organization.md` + `scripts/organize_files.py` |
| Printable planner | A shift-work automation planner to print and fill in by hand | `static/planner.html` |

---

## Your first week — a complete example

Here's how one shift worker might use this manual across a single shift cycle.
You can follow along with your own roster.

**Monday — Set up email rules.** After a string of night shifts, your inbox is
a jumble. Follow `docs/email-rules.md` to create two Gmail/Outlook rules:
one that files newsletters into a `Reading` label, and one that flags anything
with `invoice` or `bill` in the subject as `Bills` so you don't miss a due
date while you're sleeping.

**Tuesday — Set up reminders.** Your next night shift starts Friday. Follow
`docs/calendar-reminders.md` to add a reminder to `reminders.txt`:

```
Night shift starts | 2026-11-06 | Sleep by 8 AM Thursday
Electric bill      | 2026-11-05 | Pay the electric bill
```

Run `python3 scripts/calendar_reminders.py reminders.txt` to see what's due
today and coming up. It's a dry-run by default — it prints a `mailto:` link
you can click, but sends nothing.

**Wednesday — Track a shift swap.** A coworker asks to trade your Saturday
day shift for their Sunday night shift. Follow
`docs/shift-swap-tracking.md` and record it:

```
python3 scripts/shift_swap_tracker.py add "2026-11-07" "2026-11-08" Maya pending "Unit 4B"
```

Then list your pending swaps:

```
python3 scripts/shift_swap_tracker.py upcoming --within 7
```

**Thursday — Organize shift paperwork.** Your Downloads folder is full of
rosters, pay stubs, and certification PDFs. Follow
`docs/file-organization.md` to sort them:

```
python3 scripts/organize_files.py ~/Downloads --apply
```

Always test on a copy first — run without `--apply` to preview.

**Friday — Print the planner.** Open `static/planner.html`, print it (Letter
size), and fill in your shifts, tasks, and swaps for the coming cycle. The
printable planner has day / evening / night / off blocks and a swap tracker.

That's one full cycle: email sorted, reminders set, swaps tracked, paperwork
organized, and a plan for next week. Small and steady beats big and
overwhelming.

---

## How to use this manual

1. **Read the safety page first** (`docs/safety.md`). The golden rule: test on
   copies, never move originals.
2. Pick a topic and read its guide in `docs/`. Each one is step by step and
   written for irregular schedules, not 9-to-5 routines.
3. Where a script is involved, run it on a test copy of your files first, then
   decide whether to use it on your real files.
4. Print `static/planner.html` and use it to plan which automations to set up
   this shift cycle.

You can read the Markdown files in `docs/` directly, or open the fully static
HTML site at `static/index.html` in any browser — no build step, no server,
nothing to install.

---

## Privacy promise

Nothing in this manual sends your files, email, calendar data, or shift
information anywhere. Every script runs locally on your computer. The only
email that ever goes out is one you choose to send yourself, using your own
settings — nothing is hardcoded. No API keys, no accounts, no secrets, no
personal data in this project. Swap and reminder data lives in files on your
computer (`swaps.csv`, `reminders.txt`) that are ignored by git and never
meant to be committed.

---

## About Asdale Dynamics, LLC

This manual is published by **Asdale Dynamics, LLC** (Indiana, formed October
2026), founded by Dylan Asdale — a registered nurse turned AI author and
founder of Asdale Dynamics, LLC. Dylan writes and teaches AI "like a friend
would": plain English, step by step, never condescending.

Asdale Dynamics, LLC focuses on beginner-friendly AI education, books and
guides, and practical tools the LLC can publish or sell. This manual is part of
that mission: practical, tested, local-first automation anyone can use.

Learn more at dylanasdale.github.io.

This guide is education only, not medical advice. If you have questions about
shift work, sleep, or fatigue, talk to a qualified clinician.

---

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE` for the
full text.
