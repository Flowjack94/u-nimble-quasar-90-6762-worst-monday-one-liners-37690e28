#!/usr/bin/env python3
"""Worst Monday One-Liners — entry generator.

Writes the one-line entry to the output directory only
($MAKEFUN_OUTPUT_DIR, default /output), validating the competition gate:
exactly one line, 1-140 characters, valid UTF-8, non-blank, no
leading/trailing whitespace, no BOM. Then reads the file back and verifies
it is byte-identical to the entry (sha256 digest match) before reporting
success. The repository directory is never written to: the grader mounts
it read-only.
"""

import hashlib
import os
import sys

ENTRY = "Monday again \u2014 my alarm filed ticket #4821, the coffee machine resigned, and git blame says I approved all of it at 3 a.m."

MAX_CHARS = 140


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    text = ENTRY
    if not text or text.strip() != text:
        print("entry must be non-blank with no leading/trailing whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be exactly one line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= MAX_CHARS:
        print(f"entry length {len(text)} outside 1-{MAX_CHARS} chars", file=sys.stderr)
        return 1
    data = text.encode("utf-8")
    if data.startswith(b"\xef\xbb\xbf"):
        print("entry must not start with a BOM", file=sys.stderr)
        return 1
    if data.decode("utf-8") != text:
        print("entry fails UTF-8 round-trip", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        print("entry must not contain control characters", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    with open(out_path, "rb") as f:
        out = f.read()
    if out != data or sha256_hex(out) != sha256_hex(data):
        print("output entry.txt disagrees with ENTRY", file=sys.stderr)
        return 1
    print(f"entry ok: {len(text)} chars, sha256 {sha256_hex(data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
