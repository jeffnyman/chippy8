"""Message display module."""

from typing import List, Union

from termcolor import colored


def yellow_bold(message: str) -> str:
    """Display message in bolded yellow text."""

    return colored(message, "yellow", attrs=["bold"])


def cyan_bold(message: Union[List[str], str]) -> str:
    """Display message in bolded cyan text."""

    if isinstance(message, list):
        message = ", ".join(map(str, message))

    return colored(message, "cyan", attrs=["bold"])
