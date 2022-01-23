"""Tests for the ChipPy-8 CLI option handling."""

import os
import sys
from unittest import mock

from expects import contain, equal, expect

import pytest


def test_chippy8_cli_version(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 can report its version from the cli."""

    import chippy8
    from chippy8.__main__ import main

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["--version"])

    expect(pytest_wrapped_e.type).to(equal(SystemExit))
    expect(pytest_wrapped_e.value.code).to(equal(0))

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain(f"Version: {chippy8.__version__}"))


def test_debug_logging(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 can display debug log information."""

    from chippy8.__main__ import main

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "BC_test.ch8")

    with mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main([file_path, "-d"])

    captured = capsys.readouterr()
    result = captured.err

    expect(result).to(contain("Parsed arguments:"))
