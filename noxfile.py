import nox
from nox_poetry import session

nox.options.stop_on_first_error = True
nox.options.error_on_external_run = True


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
