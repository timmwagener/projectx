# -*- coding: utf-8 -*-
import logging
import json
import re
from functools import wraps

import click

import projectx


logger = logging.getLogger(__name__)


def version_option(func):
    """Decorate func with version query."""

    @click.version_option(
        projectx.__version__,
        '-V', '--version', message='%(version)s', help='Show the version and exit'
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def config_option(func):
    """Decorate func with configuration query."""

    @click.version_option(
        json.dumps(
            {
                key: value
                for key, value
                in projectx.__dict__.items()
                if (re.match(r"\A[_]{2}version[_]{2}\Z", key))
            }
            , sort_keys=True, indent=4),
        '-C', '--config', message='%(version)s', help='Show the config and exit'
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def logging_option(func):
    """Decorate func with options for logging."""

    @click.option(
        "-v", '--verbosity', 'verbosity', help='Verbosity level',
        default=logging.getLevelName(logging.INFO), show_default=True,
        type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def mandatory_source_file(func):
    """Decorate func with common shared options file io."""

    @click.argument(
        "source_file", nargs=1, required=True,
        type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False, )
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def optional_source_file(func):
    """Decorate func with common shared options file io."""

    @click.argument(
        "source_file", nargs=1, required=False,
        type=click.Path(exists=True, resolve_path=True, file_okay=True, dir_okay=False, )
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def optional_output_file(func):
    """Decorate func with common shared options file io."""

    @click.argument(
        "output", required=False, type=click.Path(exists=False, )
    )
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped


def mandatory_source_optional_output_file(func):
    """Decorate func with common shared options file io."""

    @mandatory_source_file
    @optional_output_file
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped
