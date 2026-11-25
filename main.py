#!/usr/bin/env python3
"""Entry point for the news-image-20261125 bounty.

Copies the pre-rendered poster (entry.png, produced by draw.py) to the
output directory. Standard library only, no network, deterministic.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # Verify the copy: re-read the written file and check its size and
    # contents match the source exactly.
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(dst)
    assert dst_size == src_size, "size mismatch: %d != %d" % (dst_size, src_size)
    with open(SRC, "rb") as f:
        src_bytes = f.read()
    with open(dst, "rb") as f:
        dst_bytes = f.read()
    assert dst_bytes == src_bytes, "content mismatch after copy"
    print("wrote", dst, "(%d bytes, verified)" % dst_size)


if __name__ == "__main__":
    main()
