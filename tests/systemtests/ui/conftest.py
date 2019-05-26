# -*- coding: utf-8 -*-
"""Extend root conftest of system test suite with setup for ui system
tests. Those tests are basically meant to operate the program
application as close to as a user would. Either through clicking in the UI or
by executing commands and macros. This is why by default every test starts up
a new main window and all the operations are displayed in the ui.
."""

import logging
import os

import pytest

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow

from projectx.ui.configuration.startup import ApplicationGuiContext


logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def application_gui_context():
    """Extend preparation of interpreter process for ui system tests.
    This also creates the custom application QApplication.
    """
    with ApplicationGuiContext(start_eventloop=False) as application:
        yield application


@pytest.fixture(scope='session')
def qapp(application_gui_context):
    """This overrides the default pytest-qt fixture to provide a custom
    QApplication.
    """
    application = application_gui_context

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
    return os.path.join(repository_directory, "tests", "systemtests", "ui")


@pytest.fixture
def application_window(qtbot):
    """This is only a stand-in for the main application window."""
    widget = QMainWindow()
    widget.setAttribute(Qt.WA_DeleteOnClose)
    widget.show()
    qtbot.wait_for_window_shown(widget)

    yield widget

    def is_dead():
        try:
            widget.objectName()
        except RuntimeError as exception_instance:
            return True
        else:
            return False

    widget.close()
    qtbot.waitUntil(is_dead, timeout=500)


# TODO: Setup of ui could possibly be a module level function (however qtbot
#  being a function scoped fixture causes issues).
@pytest.fixture
def setup_ui(
        application_window,
):
    pass


@pytest.fixture(scope="session", autouse=True)
def reset_state_for_session(reset_state_for_session, qapp, ):
    pass


@pytest.fixture(autouse=True)
def reset_state_for_function(setup_ui, ):
    pass
