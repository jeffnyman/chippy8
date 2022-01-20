import nox
from nox_poetry import session

nox.options.stop_on_first_error = True
nox.options.error_on_external_run = True

locations = "src", "tests", "noxfile.py"


@session
def testing(session) -> None:
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
def typechecking(session) -> None:
    args = session.posargs or locations
    session.install("mypy", "types-colorama")
    session.run("mypy", "--install-types", "--non-interactive", *args)
