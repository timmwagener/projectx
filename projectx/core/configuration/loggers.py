# -*- coding: utf-8 -*-
"""logging setup and primitives for core."""

import datetime
import logging
import logging.config
import os
import re
import threading
from io import StringIO

import projectx
from projectx.exceptions import ProjectXException
from projectx.exceptions import AmbiguityException
from projectx.exceptions import NotFoundException

from .settings import APPLICATION_LOG_DIRECTORY
from .settings import SESSION_UUID


logger = logging.getLogger(__name__)


def create_logfile_name(session_uuid, suffix=None):
    """Return name of logfile.

    Examples:
        2017_06_27_23_37_23_999999_5e12ce9354.log
        2017_06_27_23_37_23_999999_5e12ce9354_warnings.log
    """
    suffix = f"_{suffix}" if (isinstance(suffix, str)) else ""
    timestamp = f"{datetime.datetime.now():%Y_%m_%d_%H_%M_%S_%f}"
    process_id = os.getpid()
    thread_id = threading.current_thread().name
    extension = "log"

    return f"{timestamp}_{session_uuid}{suffix}.{extension}"


def get_logfile(directory, session_uuid, suffix=None):

    # regex
    REGEX_LOGFILE = r"\A(?P<date>[\d]{4}_[\d]{2}_[\d]{2}_[\d]{2}_[\d]{2}_[\d]{2}_[\d]{6})_(?P<session_uuid>[0-9a-f]{10})[\.](?P<extension>log)\Z"
    REGEX_LOGFILE_SUFFIX = r"\A(?P<date>[\d]{4}_[\d]{2}_[\d]{2}_[\d]{2}_[\d]{2}_[\d]{2}_[\d]{6})_(?P<session_uuid>[0-9a-f]{10})_(?P<suffix>[\w]*)(?P<extension>[\.]{1}log)\Z"

    if (isinstance(suffix, str)):
        regex_object = re.compile(REGEX_LOGFILE_SUFFIX)
    else:
        regex_object = re.compile(REGEX_LOGFILE)

    # directory exists?
    if (os.path.isdir(directory) is False):
        msg = "Logfile directory does not exist {0}"
        msg = msg.format(directory)
        raise ProjectXException(msg)

    # directory and possible logfiles
    root_directory, _, logfiles = next(os.walk(directory))

    # filter logfiles
    logfiles = ((logfile, regex_object.match(logfile)) for logfile in logfiles)
    logfiles = ((logfile, match_object) for logfile, match_object in logfiles
                if (match_object is not None))
    logfiles = ((logfile, match_object) for logfile, match_object in logfiles
                if (match_object.group("session_uuid") == session_uuid))
    if (isinstance(suffix, str)):
        logfiles = ((logfile, match_object) for logfile, match_object in logfiles
                    if (match_object.group("suffix") == suffix))
    logfiles = sorted(logfile for logfile, _ in logfiles)

    # no logfile found
    if (len(logfiles) < 1):
        msg = "No logfile found for session {} and suffix {} in {}"
        msg = msg.format(session_uuid, suffix, directory)
        raise NotFoundException(msg)

    # too many logfiles found
    elif (len(logfiles) > 1):
        msg = "Too many logfiles found for session {0} and suffix {1} in {2}"
        msg = msg.format(session_uuid, suffix, directory)
        raise AmbiguityException(msg)

    # one logfile found
    else:
        return os.path.join(root_directory, logfiles[0])


def create_logfile_name_for_session(suffix=None):
    return create_logfile_name(SESSION_UUID, suffix=suffix)


def get_logfile_for_session(suffix=None):
    return get_logfile(
        APPLICATION_LOG_DIRECTORY,
        SESSION_UUID,
        suffix=suffix
    )


def read_logfile_for_session(suffix=None):
    logfile = get_logfile_for_session(suffix=suffix)
    with open(logfile, "r") as logfile_handle:
        return logfile_handle.read()


class LogLevelColorFilter(logging.Filter):
    """Add HTML color attribute depending on log level of record."""

    # mapping of log levels to HTML colors (https://www.w3schools.com/colors/colors_names.asp)
    log_level_color = {
        logging.CRITICAL: "Red",
        logging.ERROR: "FireBrick",
        logging.WARNING: "Gold",
        logging.INFO: "Green",
        logging.DEBUG: "DarkCyan",
        logging.NOTSET: "Grey",
    }

    unknown_color = "DeepPink"

    def filter(self, record):
        record.log_level_color = self.log_level_color.get(record.levelno, self.unknown_color)
        return True


# TODO: Make ShortNameFilter smarter so values like below don't fail anymore
#  path.of.module.SaveUIScene(filepath=D:/gpn_scenes/ascii_art_image_and_image_viewer.gpn)
class ShortNameFilter(logging.Filter):
    """Add short name attribute to log record to avoid long logger names."""

    def filter(self, record):
        record.short_name = record.name.split(".")[-1]
        return True


class StringIOStreamHandler(logging.StreamHandler):
    """StreamHandler that uses a StringIO file-like object as stream."""

    def __init__(self, *args, **kwargs):
        super().__init__(stream=StringIO(), *args, **kwargs)

    def getvalue(self):
        return self.stream.getvalue()

    def clear(self):
        """Thread safe clearing of buffer for StringIO stream."""
        self.acquire()
        try:
            self.stream.truncate(0)
        finally:
            self.release()


def set_log_level(level):
    """Set log level at runtime."""

    # convert string to int if needed
    if (isinstance(level, str)):
        level = getattr(logging, level)

    # set general_purpose_nodes logger level
    root_logger = logging.getLogger()
    logger = root_logger.getChild(projectx.__name__)
    logger.setLevel(level)


def get_log_level():
    """Get log level for general_purpose_nodes."""

    root_logger = logging.getLogger()
    logger = root_logger.getChild(projectx.__name__)
    return logger.getEffectiveLevel()


def get_handlers_by_type(cls):
    """Return all handlers registered under root logger filtered by type."""

    return [
        handler
        for handler in logging.getLogger().handlers
        if (isinstance(handler, cls))
    ]


def get_one_handler_by_type(cls):
    """Return exactly one handler registered under root logger for given type.
    Raise on ambiguity or if nothing found.
    """

    handlers = get_handlers_by_type(cls)

    # raise on too many instances
    if (len(handlers) > 1):
        msg = f"Too many instances found. ({cls.__name__}, {len(handlers)})"
        raise AmbiguityException(msg)

    # raise on no instances
    elif (len(handlers) < 1):
        msg = f"No instance found. ({cls.__name__})"
        raise NotFoundException(msg)

    # exact 1 found
    else:
        return handlers[0]


LOGGING_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            'format': '[%(levelname)s] %(short_name)s: %(message)s',
        },
        "detailed": {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(threadName)s %(name)s: %(message)s',
        },
    },
    'filters': {
        'short_name_filter': {
            '()': f'{__name__}.ShortNameFilter',
        },
    },
    "handlers": {
        "stream": {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'filters': [
                'short_name_filter',
            ],
        },
        "logfile": {
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': os.path.join(
                APPLICATION_LOG_DIRECTORY,
                create_logfile_name_for_session()
            ),
            'encoding': "utf8"
        },
        "logfile_warnings_only": {
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'level': "WARNING",
            'filename': os.path.join(
                APPLICATION_LOG_DIRECTORY,
                create_logfile_name_for_session("warnings")
            ),
            'encoding': "utf8"
        }
    },

    # all loggers inherit log level WARNING. application logging is adjusted
    # initially in setup_logging() and can be modified at runtime via
    # set_log_level/get_log_level.
    "loggers": {
        '': {
            'handlers': [
                'stream',
                'logfile',
                'logfile_warnings_only',
            ],
            'level': 'WARNING',
        },
    },
}


def setup_logging(level, logging_configuration=None):
    if (logging_configuration is None):
        logging_configuration = LOGGING_CONFIGURATION
    logging.config.dictConfig(logging_configuration)
    set_log_level(level)
