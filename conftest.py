"""
`pytest` runtime configuration.

There you can place hooks to add custom `pytest` behavior.
"""
import io
import os

import pytest
from django.core.cache import cache
from django.utils.encoding import force_str


@pytest.fixture(autouse=True)
def setup_test_cache_isolation():
    """
    This `pytest` autouse fixture guarantees test cache isolation
    (prevents dirty state of cache remained from previously executed
    tests).

    Added as a fix for parallel tests execution (the tests pass
    when are run sequentially, but unpredictably fail when are
    run in parallel; so this autouse fixture clears cache before
    each test).
    """
    cache.clear()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    Prints pytest re-run command after each test
    """

    report = (yield).get_result()

    if report.when == "call" and report.failed:
        report.sections.append(("Re-run shortcut", f"$ pytest {item.nodeid}\n "))


def pytest_terminal_summary(terminalreporter):
    """
    Puts all failed tests into `test-failures-{env_name}.txt`
    and stores a list of failed tests in `test-rerun-{env_name}.txt`
    so they could be executed later, e.g.

        $ pipenv run test $(cat test-rerun-local.txt)

    """
    env_name = os.getenv("VIRTUALENV_NAME", "local")
    failed_tests = terminalreporter.stats.get("failed", [])

    with io.open(f"test-failures-{env_name}.txt", "w") as f:
        for test in failed_tests:
            f.write("-" * 120)
            f.write(f"\n[TEST] >>> {test.nodeid}\n")
            try:
                f.write(force_str(test.longreprtext) + "\n\n")
            except UnicodeEncodeError:
                f.write("!!! UnicodeEncodeError of test output")

    rerun = "\n".join(sorted([test.nodeid for test in failed_tests]))

    if failed_tests:
        terminalreporter.section("Failed tests")
        terminalreporter.write_line(rerun + "\n")

    with io.open(f"test-rerun-{env_name}.txt", "w") as f:
        f.write(rerun)
