"""Tests for loading ROM files into the ChipPy-8 interpreter."""

import os

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


def test_unable_to_access_rom() -> None:
    """ChipPy-8 informs the user if a ROM program could not be accessed."""

    from chippy8.interpreter import Interpreter
    from chippy8.errors import UnableToAccessRomProgramError

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "BC_test.ch8")

    interpreter = Interpreter(file_path)
    interpreter._locate_rom()
    interpreter.file = "badprogram.ch8"

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        interpreter._read_memory()

    error_type = pytest_wrapped_e.value.args[0]
    error_message = "".join(pytest_wrapped_e.value.args[0].args)

    expect(error_type).to(be_an(UnableToAccessRomProgramError))
    expect(error_message).to(contain("Unable to access the ROM program"))


def test_locate_and_access_valid_program() -> None:
    """ChipPy-8 can locate and access a valid ROM program."""

    from chippy8.interpreter import Interpreter

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "BC_test.ch8")

    interpreter = Interpreter(file_path)

    expect(interpreter.file).to(contain("BC_test.ch8"))
    expect(interpreter.data).to(be_an(bytes))
