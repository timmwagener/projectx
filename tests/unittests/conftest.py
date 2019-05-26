# -*- coding: utf-8 -*-
"""Root conftest for all unittests in the test suite, core and ui."""

import logging
import os

import pytest


logger = logging.getLogger(__name__)


@pytest.fixture
def repository_directory():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def test_data_directory(test_directory):
    """Uses test_directory fixture defined in specific ui or core conftests."""
    return os.path.join(test_directory, "test_data")


# autouse fixtures for the whole test suite.
# They are supposed to be overwritten on subpackage level for customization.
# At this level, the main goal is test isolation.


@pytest.fixture(scope="session", autouse=True)
def reset_state_for_session():
    pass


@pytest.fixture(scope="module", autouse=True)
def reset_state_for_module():
    pass


@pytest.fixture(autouse=True)
def reset_state_for_function():
    pass
