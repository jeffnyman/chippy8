"""Command line interface module for ChipPy-8."""

import argparse
import sys
import textwrap

from chippy8 import __version__

import logzero


def process_options(args: list) -> dict:
    """
    Process all command line options and arguments.

    An argument is a single part of a command line, delimited by blanks.
    An option is a particular type of argument that takes a parameter.
    A parameter is a value for an option.

    An option generally modifies the behavior of the command line. A parameter
    generally provides additional information to a single option.

    This function places all values (argument, option, parameter) into a
    dictionary. This function also handles the display of the values via
    the command line.

    Args:
        args: The arguments passed in via the command line.

    Returns:
        A dictionary of the arguments and any associated values.
    """

    parser = argparse.ArgumentParser(
        prog="chippy8",
        description="Execute a CHIP-8 ROM",
        epilog=textwrap.dedent("""Enjoy your nostalgia trip!"""),
    )

    parser.add_argument(
        "rom_file",
        action="store",
        type=str,
        help="ROM program to load",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="version information",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logzero.DEBUG,
        help="print debug logging",
    )

    parser.add_argument(
        "-i",
        "--info",
        action="store_const",
        dest="loglevel",
        const=logzero.INFO,
        help="print informative logging",
    )

    if "-v" in args or "--version" in args:
        print(f"Version: {__version__}\n")
        sys.exit(0)

    options = parser.parse_args(args)

    return vars(options)
