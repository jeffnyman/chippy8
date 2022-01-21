"""Entry point module for ChipPy-8."""

import sys

from chippy8.cli import process_options


def main(args: list = None) -> int:
    """Entry point function for ChipPy-8."""

    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"

    if sys.version_info < (3, 7):
        sys.stderr.write("\nChipPy-8 requires Python 3.7 or later.\n")
        sys.stderr.write(f"Your current version is {python_version}\n\n")
        sys.exit(1)

    print("\nChipPy-8 (CHIP-8 Emulator and Interpreter)\n")

    if not args:
        args = sys.argv[1:]

    process_options(args)

    return 0
