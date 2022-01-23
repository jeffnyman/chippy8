"""Tests for loading ROM files into the ChipPy-8 interpreter."""

from expects import be_an, contain, expect

import pytest


def test_unable_to_locate_program(capsys: pytest.CaptureFixture) -> None:
    """ChipPy-8 informs the user if a program could not be located."""

    from chippy8.__main__ import main
    from chippy8.errors import UnableToLocateRomProgramError

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["missing.ch8"])

    error_type = pytest_wrapped_e.value.args[0]
    error_message = "".join(pytest_wrapped_e.value.args[0].args)

    expect(error_type).to(be_an(UnableToLocateRomProgramError))
    expect(error_message).to(contain("Unable to find the ROM program"))
    expect(error_message).to(contain("Checked in"))
