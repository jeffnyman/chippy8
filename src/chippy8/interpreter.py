"""Module for CHIP-8 interpreter abstraction."""

import contextlib
import os
from pathlib import Path

from chippy8.errors import UnableToAccessRomProgramError, UnableToLocateRomProgramError
from chippy8.fonts import font_set
from chippy8.messages import cyan_bold, yellow_bold

from logzero import logger

with contextlib.redirect_stdout(None):
    import pygame

pygame.init()


class Interpreter:
    """Abstraction for a CHIP-8 interpreter."""

    MEMORY_START_ADDRESS = 0x200
    FONT_SET_START_ADDRESS = 0x50
    CHIP8_WIDTH = 64
    CHIP8_HEIGHT = 32
    SCALE = 25
    SCREEN_WIDTH = CHIP8_WIDTH * SCALE
    SCREEN_HEIGHT = CHIP8_HEIGHT * SCALE

    def __init__(self, rom: str) -> None:
        self._rom: str = rom
        self.file: str = ""
        self.data: bytes = b""

        # CHIP-8 specification variables.

        self.memory = [0x00] * 4096

        self._locate_rom()
        self._read_memory()
        self._populate_memory()
        self._populate_fonts()

        self.display = [0] * (Interpreter.CHIP8_WIDTH * Interpreter.CHIP8_HEIGHT)
        self.screen = (Interpreter.SCREEN_WIDTH, Interpreter.SCREEN_HEIGHT)

    def _locate_rom(self) -> None:
        """
        Determine if a ROM program exists.

        Raises:
            UnableToLocateRomProgramError: if ROM program cannot be found
        """

        paths = [os.curdir]
        paths.append(str(Path(os.path.expandvars("$CHIP8_ROM_PATH"))))

        for path in paths:
            found = os.path.isfile(os.path.join(path, self._rom))

            if found:
                self.file = os.path.join(path, self._rom)

                logger.debug(f"rom file: {self.file}")

                return

        raise UnableToLocateRomProgramError(
            f"\nUnable to find the ROM program: {yellow_bold(self._rom)}"
            f"\nChecked in: {cyan_bold(paths)}",
        )

    def _read_memory(self) -> None:
        """
        Read ROM program memory.

        Memory in the context of a CHIP-8 ROM program is a simply a
        serialiation of state, encoded as binary data.

        Raises:
            UnableToAccessRomProgramError: if ROM program cannot be opened or read
        """

        try:
            with open(self.file, "rb") as rom_program:
                self.data = rom_program.read()
        except OSError as exc:
            raise UnableToAccessRomProgramError(
                f"Unable to access the ROM program: {yellow_bold(self.file)}",
            ) from exc

    def _populate_memory(self) -> None:
        """Populate memory array with ROM binary data."""

        operations = [int("{:02X}".format(b), 16) for b in self.data]

        self.memory[
            Interpreter.MEMORY_START_ADDRESS : Interpreter.MEMORY_START_ADDRESS
            + len(operations)
        ] = operations

    def _populate_fonts(self) -> None:
        """Populate memory array with font set data."""

        self.memory[
            Interpreter.FONT_SET_START_ADDRESS : Interpreter.FONT_SET_START_ADDRESS
            + len(font_set)
        ] = font_set
