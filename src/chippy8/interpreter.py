"""Module for CHIP-8 interpreter abstraction."""

import os
from pathlib import Path

from logzero import logger


class Interpreter:
    """Abstraction for a CHIP-8 interpreter."""

    def __init__(self, rom: str) -> None:
        self._rom: str = rom
        self.file: str = ""

        self._locate_rom()

    def _locate_rom(self) -> None:
        """Determine if a ROM program exists."""

        paths = [os.curdir]
        paths.append(str(Path(os.path.expandvars("$CHIP8_ROM_PATH"))))

        for path in paths:
            found = os.path.isfile(os.path.join(path, self._rom))

            if found:
                self.file = os.path.join(path, self._rom)

                logger.debug(f"rom file: {self.file}")

                return

        print(
            f"Unable to find the ROM file: {self._rom}" f"\nChecked in: {paths}",
        )
