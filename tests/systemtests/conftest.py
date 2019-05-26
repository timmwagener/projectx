# -*- coding: utf-8 -*-
"""Root conftest for all system tests in the test suite, core and ui.

The system tests mimic an as complete as possible program session and therefore
try to invoke the complete startup/teardown procedures as accurate as possible.
"""

import logging
import os

import pytest

from projectx.core.configuration.startup import ApplicationCoreContext


logger = logging.getLogger(__name__)


# TODO: Adjust settings to use temp. directory as USER_HOME_DIRECTORY for tests
#  which might involve finding a way to set an env. variable to tmpdir_factory
#  fixture before an import of settings (as import time assignment made it
#  impossible to just monkeypatch settings.USER_HOME_DIRECTORY)


def pytest_addoption(parser):
    """Pytest command line option to customize verbosity of the
    GeneralPurposeNodesContext that adjusts logging before the application is
    started. Setting this value is like starting GPN with the --verbosity
    command line option. The value of this setting should not influence any test
    results. It should only enable more verbose test output.
    """
    choices = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL",)
    parser.addoption(
        "--verbosity-project", action="store", type=str,
        choices=choices, default=choices[1],
        help=("Verbosity level used by 'setup_logging' fixture.")
    )


@pytest.fixture(scope='session')
def verbosity_for_session(request):
    """Make verbosity fixture work with session scope."""
    return request.config.getoption("--verbosity-project")


@pytest.fixture
def repository_directory():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def test_data_directory(test_directory):
    """Uses test_directory fixture defined in specific ui or core conftests."""
    return os.path.join(test_directory, "test_data")


@pytest.fixture(scope='session')
def application_core_context(verbosity_for_session):
    """Prepare interpreter process for systemtests session. This sets up
    things like directories, logging etc.
    """
    with ApplicationCoreContext(verbosity_for_session):
        yield


# autouse fixtures for the whole test suite.
# They are supposed to be overwritten/extended on subpackage level for
# customization. At this level, the main goal is test isolation.


@pytest.fixture(scope="session", autouse=True)
def reset_state_for_session(application_core_context, ):
    pass


@pytest.fixture(scope="module", autouse=True)
def reset_state_for_module():
    pass


@pytest.fixture(autouse=True)
def reset_state_for_function():
    pass
