"""Tests for starting the ChipPy-8 interpreter."""

import os
import sys
from unittest import mock

from expects import contain, equal, expect

import pytest


def test_chippy8_startup_banner(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 provides a minimal banner upon startup."""

    from chippy8.__main__ import main

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "BC_test.ch8")

    with pytest.raises(SystemExit), mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main([file_path])

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


def test_startup_no_rom(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 must be started with a ROM program specified."""

    from chippy8.__main__ import main

    with pytest.raises(SystemExit) as pytest_wrapped_e, mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main()

    expect(pytest_wrapped_e.type).to(equal(SystemExit))
    expect(pytest_wrapped_e.value.code).to(equal(2))

    captured = capsys.readouterr()
    result = captured.err

    expect(result).to(contain("the following arguments are required: rom_file"))
