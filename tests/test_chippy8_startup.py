"""Tests for starting the ChipPy-8 interpreter."""

import sys
from unittest import mock

from expects import contain, equal, expect

import pytest


def test_chippy8_startup_banner(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 provides a minimal banner upon startup."""

    from chippy8.__main__ import main

    with mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main()

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain("ChipPy-8 (CHIP-8 Emulator and Interpreter)"))


def test_bad_python_version(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 determines if minimal Python version is met."""

    from chippy8.__main__ import main

    with mock.patch.object(sys, "version_info", (3, 5)), pytest.raises(
        SystemExit,
    ) as pytest_wrapped_e:
        main()

    terminal_text = capsys.readouterr()
    expect(terminal_text.err).to(contain("ChipPy-8 requires Python 3.7"))

    expect(pytest_wrapped_e.type).to(equal(SystemExit))
    expect(pytest_wrapped_e.value.code).to(equal(1))
