"""Tests for CHIP-8 opcodes."""

import os

from expects import be_true, expect

import pytest


def test_OP_00E0(capsys: pytest.CaptureFixture) -> None:
    """Handling the CLS (clear the display) opcode."""

    from chippy8.interpreter import Interpreter

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "BC_test.ch8")

    interpreter = Interpreter(file_path)
    interpreter.display = [1] * len(interpreter.display)
    interpreter.tick()

    expect(not any(interpreter.display)).to(be_true)
