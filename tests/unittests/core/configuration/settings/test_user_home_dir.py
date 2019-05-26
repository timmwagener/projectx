# -*- coding: utf-8 -*-

import logging
import os

from projectx.core.configuration import settings


logger = logging.getLogger(__name__)


def test_user_home_directory():
    """Just assert that a correct user home dir. is found in settings. Correct
    here means an existing dir. on the filesystem. Pythons canonical way
    `os.path.expanduser("~")` failed in tests run with tox.
    """
    assert os.path.isdir(settings.USER_HOME_DIRECTORY)
