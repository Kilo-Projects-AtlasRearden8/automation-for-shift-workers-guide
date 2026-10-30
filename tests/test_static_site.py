#!/usr/bin/env python3
"""Static site verification.

Checks that every HTML page in static/ parses, all internal links resolve to
existing files, and every page credits Asdale Dynamics, LLC and carries the
copyright line.

Run: python3 tests/test_static_site.py
"""

import os
import re
import sys
from html.parser import HTMLParser

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

CREDIT = "Asdale Dynamics, LLC"
COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"


class LinkCollector(HTMLParser):
    """Collects href attributes from anchor and link tags."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ("a", "link"):
            for attr, value in attrs:
                if attr == "href":
                    self.links.append(value)


def parse_html(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    errors = []
    html_files = sorted(f for f in os.listdir(STATIC_DIR) if f.endswith(".html"))
    if not html_files:
        errors.append("No HTML files found in static/")
    for name in html_files:
        path = os.path.join(STATIC_DIR, name)
        content = parse_html(path)

        # Every page must carry the credit and copyright line.
        if CREDIT not in content:
            errors.append(f"{name}: missing credit '{CREDIT}'")
        if COPYRIGHT not in content:
            errors.append(f"{name}: missing copyright line '{COPYRIGHT}'")

        # Collect and resolve internal links.
        parser = LinkCollector()
        parser.feed(content)
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = os.path.join(STATIC_DIR, href)
            if not os.path.exists(target):
                errors.append(f"{name}: broken link '{href}' -> {target}")

    if errors:
        print("Static site verification FAILED:")
        for err in errors:
            print("  -", err)
        return 1

    print(f"Static site verification PASSED: {len(html_files)} HTML pages, "
          f"all links resolve, every page credits {CREDIT}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
