"""Module for CHIP-8 interpreter abstraction."""

import os
from pathlib import Path

from chippy8.errors import UnableToLocateRomProgramError
from chippy8.messages import cyan_bold, yellow_bold


from logzero import logger


class Interpreter:
    """Abstraction for a CHIP-8 interpreter."""

    def __init__(self, rom: str) -> None:
        self._rom: str = rom
        self.file: str = ""

        self._locate_rom()

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
