#!/usr/bin/env python3
"""Tests for organize_files.py.

Run: python3 tests/test_organize_files.py
"""

import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import organize_files  # noqa: E402


def write_files(tmp, mapping):
    for name, content in mapping.items():
        path = os.path.join(tmp, name)
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(name) else None
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return tmp


def test_plan_moves_groups_by_extension():
    tmp = tempfile.mkdtemp()
    try:
        write_files(tmp, {
            "roster.pdf": "x",
            "paystub.pdf": "x",
            "photo.jpg": "x",
            "notes.txt": "x",
        })
        moves = organize_files.plan_moves(tmp)
        destinations = {os.path.basename(d) for _, d in moves}
        assert "roster.pdf" in destinations
        assert "paystub.pdf" in destinations
        assert "photo.jpg" in destinations
        assert "notes.txt" in destinations
        # No source is inside a destination folder
        for source, dest in moves:
            assert not os.path.basename(source).startswith("Schedules")
    finally:
        shutil.rmtree(tmp)


def test_dry_run_moves_nothing():
    tmp = tempfile.mkdtemp()
    try:
        write_files(tmp, {"roster.pdf": "x"})
        before = set(os.listdir(tmp))
        moves = organize_files.plan_moves(tmp)
        after = set(os.listdir(tmp))
        assert before == after
        assert len(moves) == 1
    finally:
        shutil.rmtree(tmp)


def test_apply_moves_and_avoids_duplicates():
    tmp = tempfile.mkdtemp()
    try:
        write_files(tmp, {"roster.pdf": "x", "roster-1.pdf": "y"})
        moves = organize_files.plan_moves(tmp)
        count = organize_files.apply_moves(moves)
        assert count == 2
        sched_dir = os.path.join(tmp, "Schedules")
        assert os.path.exists(os.path.join(sched_dir, "roster.pdf"))
        assert os.path.exists(os.path.join(sched_dir, "roster-1.pdf"))
        assert not os.path.exists(os.path.join(tmp, "roster.pdf"))
    finally:
        shutil.rmtree(tmp)


def test_unknown_extension_goes_to_misc():
    tmp = tempfile.mkdtemp()
    try:
        write_files(tmp, {"weird.xyz": "x"})
        moves = organize_files.plan_moves(tmp)
        assert len(moves) == 1
        dest = moves[0][1]
        assert "Misc" in dest
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    test_plan_moves_groups_by_extension()
    test_dry_run_moves_nothing()
    test_apply_moves_and_avoids_duplicates()
    test_unknown_extension_goes_to_misc()
    print("All organize_files tests passed.")
