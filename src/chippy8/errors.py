"""Error module for ChipPy-8 specific exceptions."""

import inspect
import ntpath
import sys

from termcolor import colored


class Chippy8Error(Exception):
    """Raise ChipPy-8 specific execption."""

    def __init__(self, msg: str) -> None:
        try:
            source_name = inspect.currentframe().f_back.f_code.co_name  # type: ignore
            source_file = ntpath.basename(
                inspect.currentframe().f_back.f_code.co_filename,  # type: ignore
            )
            source_line = sys.exc_info()[-1].tb_lineno  # type: ignore
        except AttributeError:
            source_line = inspect.currentframe().f_back.f_lineno  # type: ignore

        error = colored(type(self).__name__, "red", attrs=["bold"])
        msg = colored(msg, "red", attrs=["bold"])
        source_name = colored(source_name, "yellow")
        source_file = colored(source_file, "yellow")

        self.args = (
            "\nChipPy-8 Problem: {0}\nOccurred in: {1} in {2} (line {3})\n{4}\n".format(
                error,
                source_name,
                source_file,
                source_line,
                msg,
            ),
        )

        sys.exit(self)


class UnableToLocateRomProgramError(Chippy8Error):
    """Raise for a ROM program file that cannot be located."""
