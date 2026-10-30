# Safety First

The golden rule of automation: **test on copies, never move originals.**

Before you automate anything with a script in this manual:

1. **Make a test copy.** Point the script at a folder copy, not your real
   files. Confirm it does what you expect.
2. **Use the preview (dry-run) first.** Every script here shows what it would
   do without changing anything. Add `--apply` only when you're sure.
3. **Read the script.** Every script is plain Python 3 you can read end to
   end. No hidden behavior, no API keys, nothing uploaded.
4. **Start small.** Automate one folder, one reminder, or one email rule at a
   time. Small and steady beats big and overwhelming.
5. **Nothing leaves your computer.** Scripts run locally. Your shift
   schedules, swap data, and reminders stay in files on your computer
   (`swaps.csv`, `reminders.txt`) that are ignored by git.

Email rules, calendar reminders, and file organization are organizational
tools — not financial or medical advice. If you have questions about shift
work, sleep, or fatigue, talk to a qualified clinician.

## Why this matters for shift work

Irregular schedules mean less margin for error. A script that moves the wrong
folder or a reminder that fires at the wrong hour can cost sleep or a shift.
That's why every script in this manual previews before it acts, and why you
should always test on a copy of your schedule or paperwork first.
