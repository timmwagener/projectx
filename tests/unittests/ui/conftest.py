# -*- coding: utf-8 -*-
"""Extend root conftest with ui specific root setup."""

import logging
import os

import pytest

from projectx.ui.core.application import ProjectXApplication


logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def qapp(qapp_args):
    """This overrides the default pytest-qt fixture to provide a custom
    QApplication.

    See Also:
        https://github.com/pytest-dev/pytest-qt/issues/172
    """

    application = ProjectXApplication(qapp_args)

    # the original fixture is a yield too although it has no teardown
    try:
        yield application

    finally:
        # Call application teardown. This usually happens in QApplication.exec()
        # but since pytest-qt doesn't start the application event loop, no
        # `aboutToQuit` is emitted. Therefore we call teardown ourselves.
        application.teardown()


@pytest.fixture
def test_directory(repository_directory):
    return os.path.join(repository_directory, "tests", "unittests", "ui")
