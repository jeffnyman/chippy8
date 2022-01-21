"""Generic tests for ChipPy-8 execution."""

from expects import equal, expect


def test_report_package_version() -> None:
    """Package reports its current version."""

    from chippy8 import __version__

    expect(__version__).to(equal("0.1.0"))
