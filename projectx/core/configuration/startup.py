# -*- coding: utf-8 -*-

import datetime
import errno
import locale
import logging
import os

from .settings import APPLICATION_HOME_DIRECTORY
from .settings import APPLICATION_VERSION_DIRECTORY
from .settings import APPLICATION_LOG_DIRECTORY
from .loggers import setup_logging


logger = logging.getLogger(__name__)


def create_directory(directory):
    """Threadsafe directory creation."""

    try:
        os.makedirs(directory)
    except OSError as exception_instance:
        if (exception_instance.errno != errno.EEXIST):
            raise


class ApplicationCoreContext:
    """Setup and teardown for the interpreter process that runs
    the application.
    """

    def __init__(self, verbosity):
        self.verbosity = verbosity

    def __enter__(self):
        """Setup the interpreter process or raise application exception
        upon expected error condition.
        """

        # set locale for all categories from user system setting
        locale.setlocale(locale.LC_ALL, '')

        # create directories
        create_directory(APPLICATION_HOME_DIRECTORY)
        create_directory(APPLICATION_VERSION_DIRECTORY)
        create_directory(APPLICATION_LOG_DIRECTORY)

        # TODO: Setup/add sys.excepthook

        # setup logging
        setup_logging(self.verbosity)

        # log timestamp
        timestamp = datetime.datetime.now()
        timestamp = f'{timestamp:%Y.%m.%d %H:%M:%S:%f}'
        msg = f"Session started: {timestamp}"
        logger.info(msg)

    def __exit__(self, exception_type, exception_instance, exception_traceback):
        """Teardown for the interpreter process."""

        # log
        timestamp = datetime.datetime.now()
        timestamp = f'{timestamp:%Y.%m.%d %H:%M:%S:%f}'
        msg = f"Session finished: {timestamp}"
        logger.info(msg)
