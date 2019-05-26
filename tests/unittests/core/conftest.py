# -*- coding: utf-8 -*-
"""Extend root conftest with core specific root setup."""

import logging
import os
import sys

import pytest

from projectx.exceptions import ProjectXException


logger = logging.getLogger(__name__)


@pytest.fixture
def test_directory(repository_directory):
    return os.path.join(repository_directory, "tests", "unittests", "core")


@pytest.fixture
def raise_on_ui_import():
    """Aggressively raise on any ui import during core tests. This is an
    attempt to enforce a clean separation of core and ui.

    Notes:
        This fixture will not be used when running kernel tests explicitly for
        plugins or utilities, but will always run when executing the whole
        kernel test suite, because tests are collected on all given paths
        beforehand and ui imports will occur then, that remain in the
        interpreter environment.
    """

    def _raise_on_ui_import():
        """Raise if any module import paths contain 'ui'."""
        import_paths = [
            module_import_path for module_import_path in sys.modules
            if ("ui" in module_import_path.split("."))
        ]

        if (len(import_paths) > 0):
            msg = "Invalid ui imports in kernel unit tests:\n{0}"
            msg = msg.format("\n".join(import_paths))
            raise ProjectXException(msg)

    _raise_on_ui_import()
    yield
    _raise_on_ui_import()


# autouse fixtures for the whole test suite.
# They are supposed to be overwritten on subpackage level for customization.
# Here the main goal is test isolation.


@pytest.fixture(autouse=True)
def reset_state_for_function(reset_state_for_function, raise_on_ui_import):
    """Extend root conftest with core package exclusive setup/teardown."""
    pass
