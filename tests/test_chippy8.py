"""Generic tests for ChipPy-8 execution."""

from expects import contain, equal, expect

import pytest


def test_report_package_version() -> None:
    """Package reports its current version."""

    from chippy8 import __version__

    expect(__version__).to(equal("0.1.0"))


def test_quendor_startup_banner(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 provides a minimal banner upon startup."""

    from chippy8.__main__ import main

    main()

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain("ChipPy-8 (CHIP-8 Emulator and Interpreter)"))
