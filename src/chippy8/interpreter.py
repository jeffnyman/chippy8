"""Module for CHIP-8 interpreter abstraction."""

import os
from pathlib import Path

from chippy8.errors import UnableToAccessRomProgramError, UnableToLocateRomProgramError
from chippy8.messages import cyan_bold, yellow_bold


from logzero import logger


class Interpreter:
    """Abstraction for a CHIP-8 interpreter."""

    def __init__(self, rom: str) -> None:
        self._rom: str = rom
        self.file: str = ""
        self.data: bytes = b""

        self._locate_rom()
        self._read_memory()

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
