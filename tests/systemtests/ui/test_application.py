# -*- coding: utf-8 -*-
"""Test the custom QApplication subclass used for application."""

import logging

import pytest
from PySide2.QtCore import QCoreApplication
from PySide2.QtWidgets import QApplication

from projectx.ui.core.application import ProjectXApplication


logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    'callback',
    [
        QApplication.instance,
        QCoreApplication.instance
    ],
    ids=[
        'QApplication.instance',
        'QCoreApplication.instance',
    ]
)
def test_qapplication_from_pytest_is_expected_subclass_instance(qtbot, callback):
    """The `qapp()` fixture was overridden in order to provide a
    `GeneralPurposeNodesApplication` instead of a `QtGui.QApplication`.
    """
    qapplication = callback()
    assert isinstance(qapplication, ProjectXApplication)
    assert len(qapplication.topLevelWindows()) == 1
