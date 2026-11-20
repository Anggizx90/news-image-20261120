#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261120 bounty.

Copies the front page this repository holds (entry.png, drawn by
draw_poster.py) to the output directory. Standard library only, no
network, deterministic: every run writes the same bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(OUT, "entry.png")
    shutil.copyfile(src, dst)
    print(dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
