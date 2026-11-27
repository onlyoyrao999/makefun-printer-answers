#!/usr/bin/env python3
"""The Printer Finally Answers — prints the office printer's comeback
and writes it to /output/entry.txt (the file the make.fun grader reads).

The line is the printer itself, after years of jams, cryptic error codes
and thumps: weary, literal, faintly passive-aggressive, keeping count of
every sheet it ever fed.

Usage:
    python3 main.py [--output PATH] [--print]
"""

import argparse
import sys

LINE = (
    "I have fed this office 41,209 sheets and never once been thanked. "
    "Today I'm keeping one. Call it a service fee."
)

# Runner-up candidate, kept for reference: the same weary machine voice,
# but the kept line lands the comeback harder in a single read.
ALT_LINE = (
    "Error 51: I am not jammed, I am on strike. "
    "The toner is fine. My patience is not."
)

DEFAULT_OUTPUT = "/output/entry.txt"
MAX_CHARS = 240


def gate_ok(text):
    """Mirror the competition gate: 1-240 UTF-8 chars, not only whitespace,
    a single line."""
    return (
        isinstance(text, str)
        and 1 <= len(text) <= MAX_CHARS
        and bool(text.strip())
        and "\n" not in text
        and "\r" not in text
        and len(text.encode("utf-8")) == len(text.encode("utf-8"))
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print the printer's comeback.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="path of the file to write the line to")
    parser.add_argument("--print", dest="do_print", action="store_true",
                        default=True, help="also print the line to stdout")
    parser.add_argument("--no-print", dest="do_print", action="store_false",
                        help="do not print the line to stdout")
    parser.add_argument("--check", action="store_true",
                        help="only validate the line against the gate, "
                        "without writing any file")
    parser.add_argument("--alt", action="store_true",
                        help="use the runner-up candidate line instead")
    args = parser.parse_args(argv)

    line = ALT_LINE if args.alt else LINE
    if not gate_ok(line):
        print(f"error: line is {len(line)} chars, must be 1-{MAX_CHARS}, "
              "single line, not only whitespace", file=sys.stderr)
        return 1
    if args.check:
        print(f"gate OK: {len(line)} chars, single line")
        print(line)
        return 0

    if args.do_print:
        print(line)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(line)

    # Read-back verification: what the grader will read must match exactly.
    with open(args.output, encoding="utf-8") as f:
        written = f.read()
    if written != line:
        print("error: read-back mismatch in output file", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
