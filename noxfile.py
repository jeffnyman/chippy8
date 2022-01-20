"""Provide executable sessions for project automation."""

import nox
from nox_poetry import Session, session

nox.options.stop_on_first_error = True
nox.options.error_on_external_run = True

locations = "src", "tests", "noxfile.py"


@session
def testing(session: Session) -> None:
    """Run the test suite (using pytest)."""

    args = session.posargs or [
        "--cov",
        "--spec",
        "--cov-report",
        "html",
        "--cov-report",
        "term",
    ]
    session.install("pytest", "pytest-cov", "pytest-spec", "expects", ".")
    session.run("pytest", *args)


@session
def typechecking(session: Session) -> None:
    """Run type checks (using mypy)."""

    args = session.posargs or locations
    session.install("mypy", "types-colorama")
    session.run("mypy", "--install-types", "--non-interactive", *args)


@session
def linting(session: Session) -> None:
    """Run linting checks (using flake8)."""

    args = session.posargs or locations
    session.install(*flake8_plugins)
    session.run(
        "autoflake",
        "--recursive",
        "--in-place",
        "--remove-all-unused-imports",
        "--remove-unused-variables",
        "src/chippy8/",
    )
    session.run("flake8", "--format=pylint", *args)


@session
def lintingreport(session: Session) -> None:
    """Run linting checks with HTML report (using flake8)."""

    args = session.posargs or locations
    session.install(
        *flake8_plugins,
        "flake8-html",
    )
    session.run(
        "autoflake",
        "--recursive",
        "--in-place",
        "--remove-all-unused-imports",
        "--remove-unused-variables",
        "src/chippy8/",
    )
    session.run("flake8", "--format=html", *args)


flake8_plugins = (
    "autoflake",
    "darglint",
    "flake8",
    "flake8",
    "flake8-2020",
    "flake8-alphabetize",
    "flake8-annotations",
    "flake8-annotations-complexity",
    "flake8-annotations-coverage",
    "flake8-bandit",
    "flake8-black",
    "flake8-broken-line",
    "flake8-bugbear",
    "flake8-builtins",
    "flake8-coding",
    "flake8-cognitive-complexity",
    "flake8-commas",
    "flake8-comprehensions",
    "flake8-eradicate",
    "flake8-expression-complexity",
    "flake8-docstrings",
    "flake8-functions",
    "flake8-multiline-containers",
    "flake8-mutable",
    "flake8-printf-formatting",
    "flake8-pytest-style",
    "flake8-quotes",
    "flake8-return",
    "flake8-simplify",
    "flake8-string-format",
    "flake8-use-fstring",
    "flake8-variables-names",
    "pep8-naming",
)
