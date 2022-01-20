from expects import contain, equal, expect


def test_report_package_version() -> None:
    from chippy8 import __version__

    expect(__version__).to(equal("0.1.0"))


def test_quendor_startup_banner(capsys) -> None:
    from chippy8.__main__ import main

    main()

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain("ChipPy-8 (CHIP-8 Emulator and Interpreter)"))
