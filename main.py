#!/usr/bin/env python3
"""Entry point: write the 21 November 2026 news image to /output/entry.png.

The image is drawn fresh on every run by generate.py (no network, no clock,
no randomness), so two runs produce identical bytes. Outside the grader,
MAKEFUN_OUTPUT_DIR stands in for /output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    entry = os.path.join(HERE, "entry.png")
    if not os.path.exists(entry):
        sys.path.insert(0, HERE)
        import generate

        generate.build(entry)
    shutil.copyfile(entry, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
