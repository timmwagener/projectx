# -*- coding: utf-8 -*-

import logging
import sys

import qdarkstyle

from projectx.ui.core.application import ProjectXApplication

from .loggers import extend_logging


logger = logging.getLogger(__name__)


class ApplicationGuiContext:

    def __init__(self, start_eventloop=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_eventloop = start_eventloop

    def __enter__(self):
        """Setup for the interpreter process. Raise application exception upon
        handled error conditions.
        """

        # add gui logging
        extend_logging()

        # application
        self.application = ProjectXApplication()

        # set dark style
        stylesheet = qdarkstyle.load_stylesheet()
        self.application.setStyleSheet(stylesheet)

        return self.application

    def __exit__(self, exception_type, exception_instance, exception_traceback):
        """Teardown for the interpreter process."""

        # if there was an exception in context, bubble straight up
        if (exception_type is not None):
            return

        # enter Qt event loop
        if (self.start_eventloop is True):
            # enclosing contexts __exit__ blocks are still executed
            sys.exit(self.application.exec_())
