"""Entry point module for ChipPy-8."""

import sys

from chippy8.cli import process_options
from chippy8.logging import setup_logging

from logzero import logger


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

    cli = process_options(args)

    setup_logging(cli["loglevel"])

    logger.debug(f"Argument count: {'':>4}" + str(len(args)))

    for i, arg in enumerate(args):
        logger.debug(f"Argument {i}: {'':>8}" + arg)

    logger.debug(f"Parsed arguments: {'':>2}" + f"{cli}")

    return 0
