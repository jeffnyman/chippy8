"""Tests for the ChipPy-8 CLI option handling."""

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
