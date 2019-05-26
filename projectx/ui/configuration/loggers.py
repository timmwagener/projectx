# -*- coding: utf-8 -*-
"""logging setup and primitives for ui."""

import logging
import threading

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal

from projectx.core.configuration.loggers import ShortNameFilter
from projectx.core.configuration.loggers import LogLevelColorFilter
from projectx.core.configuration.loggers import StringIOStreamHandler


logger = logging.getLogger(__name__)


class QtSignaler(QObject):

    log = Signal(str)
    log_from_main_thread = Signal(str)
    log_from_worker_thread = Signal(str)


class QtSignalHandler(logging.Handler):
    """Observable that emits signal with log record as formatted unicode text,
    that observers may connect to.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signaler = QtSignaler()

    def emit(self, record):
        formatted_record = self.format(record)
        formatted_record = f"{formatted_record}"

        is_main_thread = threading.current_thread() is threading.main_thread()

        # thread specific signals
        if (is_main_thread is True):
            self.signaler.log_from_main_thread.emit(formatted_record)
        else:
            self.signaler.log_from_worker_thread.emit(formatted_record)

        # thread agnostic signal, as not all slots may care about the thread
        # the signal was emitted from
        self.signaler.log.emit(formatted_record)


class QtSignalHandlerHTML(QtSignalHandler):
    """QtSignalHandlerHTML exists just for type checks, to easily differentiate
    it from QtSignalHandler when clients look for registration at runtime.
    """


class BackupHandlerHTML(StringIOStreamHandler):
    """Special subclass of StringIOStreamHandler for explicit type checking.

    The HTMLBackupHandler is used as an always functional storage for html
    formatted records. Clients can read from it via `getvalue()` and get
    already formatted content.
    """


def extend_logging():

    FORMAT_MESSAGE_ONLY = '%(message)s'
    FORMAT_DEFAULT_HTML = "<i>%(asctime)s</i> <b><font color=\"%(log_level_color)s\">[%(levelname)s]</font></b> <i>%(short_name)s:</i> %(message)s"

    logger = logging.getLogger()  # root logger

    # qt_signal_handler_text
    handler = QtSignalHandler()
    handler.setFormatter(logging.Formatter(FORMAT_MESSAGE_ONLY))
    handler.addFilter(ShortNameFilter())
    logger.addHandler(handler)

    # qt_signal_handler_html
    handler = QtSignalHandlerHTML()
    handler.setFormatter(logging.Formatter(FORMAT_DEFAULT_HTML))
    handler.addFilter(ShortNameFilter())
    handler.addFilter(LogLevelColorFilter())
    logger.addHandler(handler)

    # backup_handler_html
    handler = BackupHandlerHTML()
    handler.setFormatter(logging.Formatter(FORMAT_DEFAULT_HTML))
    handler.addFilter(ShortNameFilter())
    handler.addFilter(LogLevelColorFilter())
    logger.addHandler(handler)
