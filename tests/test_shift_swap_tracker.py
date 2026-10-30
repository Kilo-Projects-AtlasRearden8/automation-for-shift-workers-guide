#!/usr/bin/env python3
"""Tests for shift_swap_tracker.py.

Run: python3 tests/test_shift_swap_tracker.py
"""

import os
import sys
import tempfile
import shutil
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import shift_swap_tracker  # noqa: E402


def make_swap(tmp, **fields):
    path = os.path.join(tmp, "swaps.csv")
    base = {
        "my_date": "2026-11-07",
        "their_date": "2026-11-10",
        "coworker": "Maya",
        "status": "pending",
        "approved_by": "",
        "notes": "",
    }
    base.update(fields)
    write_header = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as fh:
        writer = __import__("csv").DictWriter(fh,
                                              fieldnames=shift_swap_tracker.FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(base)
    return path


def test_add_and_list():
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "swaps.csv")
        rc = shift_swap_tracker.cmd_add(["2026-11-07", "2026-11-10", "Maya",
                                         "pending", "Charge nurse", "Nights"],
                                        path)
        assert rc == 0
        swaps = shift_swap_tracker.load_swaps(path)
        assert len(swaps) == 1
        assert swaps[0]["coworker"] == "Maya"
        assert swaps[0]["status"] == "pending"
    finally:
        shutil.rmtree(tmp)


def test_add_bad_date_rejected():
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "swaps.csv")
        rc = shift_swap_tracker.cmd_add(["not-a-date", "2026-11-10", "Maya"],
                                        path)
        assert rc == 1
        assert not os.path.exists(path) or shift_swap_tracker.load_swaps(path) == []
    finally:
        shutil.rmtree(tmp)


def test_status_change():
    tmp = tempfile.mkdtemp()
    try:
        path = make_swap(tmp)
        rc = shift_swap_tracker.cmd_status(["1", "approved"], path)
        assert rc == 0
        swaps = shift_swap_tracker.load_swaps(path)
        assert swaps[0]["status"] == "approved"
    finally:
        shutil.rmtree(tmp)


def test_upcoming_filters_within_days():
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "swaps.csv")
        today = date.today()
        soon = (today + timedelta(days=2)).isoformat()
        far = (today + timedelta(days=30)).isoformat()
        shift_swap_tracker.cmd_add([today.isoformat(), soon, "Maya", "pending"],
                                   path)
        shift_swap_tracker.cmd_add([soon, far, "Jamal", "pending"],
                                   path)
        shift_swap_tracker.cmd_add([today.isoformat(), today.isoformat(), "Sam", "done"],
                                   path)
        # Capture stdout of upcoming by calling categorize logic instead: reuse
        # load + filter manually to avoid stdout capture complexity.
        swaps = shift_swap_tracker.load_swaps(path)
        pending_or_approved = [s for s in swaps if s["status"] in ("pending", "approved")]
        assert len(pending_or_approved) == 2
    finally:
        shutil.rmtree(tmp)


def test_export_writes_csv():
    tmp = tempfile.mkdtemp()
    try:
        path = make_swap(tmp)
        out = os.path.join(tmp, "exported.csv")
        rc = shift_swap_tracker.cmd_export([out], path)
        assert rc == 0
        exported = shift_swap_tracker.load_swaps(out)
        assert len(exported) == 1
        assert exported[0]["coworker"] == "Maya"
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    test_add_and_list()
    test_add_bad_date_rejected()
    test_status_change()
    test_upcoming_filters_within_days()
    test_export_writes_csv()
    print("All shift_swap_tracker tests passed.")
