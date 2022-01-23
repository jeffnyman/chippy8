"""Tests for loading ROM files into the ChipPy-8 interpreter."""

import sys
from unittest import mock

from expects import contain, expect

import pytest


def test_unable_to_locate_program(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 informs the user if a program could not be located."""

    from chippy8.__main__ import main

    with mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main(["missing.ch8"])

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain("Unable to find the ROM file"))
