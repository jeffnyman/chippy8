"""Module for CHIP-8 interpreter abstraction."""

import contextlib
import os
import sys
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
        self.stack = [Interpreter.MEMORY_START_ADDRESS] * 16
        self.stack_pointer = 0

        # Opcode variables.
        self.opcode = 0

        self._locate_rom()
        self._read_memory()
        self._populate_memory()
        self._populate_fonts()

        self.display = [0] * (Interpreter.CHIP8_WIDTH * Interpreter.CHIP8_HEIGHT)
        self.screen = pygame.display.set_mode(
            (Interpreter.SCREEN_WIDTH, Interpreter.SCREEN_HEIGHT),
        )
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("ChipPy-8 Interpreter")

    @property
    def program_counter(self) -> int:
        """Get location in stack for the program counter."""

        return self.stack[self.stack_pointer]

    @program_counter.setter
    def program_counter(self, value: int) -> None:
        """Set location in stack as the value of the program counter."""

        self.stack[self.stack_pointer] = value

    def tick(self) -> None:
        """
        Sets up the frame-based execution of the interpreter.

        This method will effectively be called once per frame and will
        compute how many milliseconds have passed since the previous call
        to the method.
        """

        self.clock.tick(600)

        self._handle_input()

        self.opcode = (self.memory[self.program_counter] << 8) | self.memory[
            self.program_counter + 1
        ]

    def _handle_input(self) -> None:
        """Get user and system generated events for processing."""

        if pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit(0)

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
