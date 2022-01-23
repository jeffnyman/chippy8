"""Module for CHIP-8 interpreter abstraction."""


class Interpreter:
    """Abstraction for a CHIP-8 interpreter."""

    def __init__(self, rom: str) -> None:
        self._rom: str = rom
