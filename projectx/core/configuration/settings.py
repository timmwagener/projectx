# -*- coding: utf-8 -*-
"""Central place for settings roughly like Djangos settings.py"""

import os
import sys
from uuid import uuid4

import projectx


SESSION_UUID = f"{uuid4().hex}"[:10]


# user home directory structure
USER_HOME_DIRECTORY = os.path.expanduser("~")

APPLICATION_HOME_DIRECTORY_NAME = ".projectx"
APPLICATION_HOME_DIRECTORY = os.path.join(
    USER_HOME_DIRECTORY,
    APPLICATION_HOME_DIRECTORY_NAME)

APPLICATION_VERSION = f"{projectx.__version__}"
APPLICATION_VERSION_DIRECTORY = os.path.join(
    APPLICATION_HOME_DIRECTORY,
    APPLICATION_VERSION)
"""APPLICATION_VERSION_DIRECTORY is always the active root home
directory for the current gui session.
"""

APPLICATION_LOG_DIRECTORY_NAME = "log"
APPLICATION_LOG_DIRECTORY = os.path.join(
    APPLICATION_VERSION_DIRECTORY,
    APPLICATION_LOG_DIRECTORY_NAME)


# repository or executable root directory structure

# Set root differently if packaged as .exe via PyInstaller
# The root meaning the repository directory or the directory where the .exe is
# in, not the Python package root.
if (getattr(sys, 'frozen', False)):
    ROOT_DIR = os.path.dirname(sys.executable)
else:
    ROOT_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)))))


PACKAGE_FOLDER_NAME = 'projectx'
PACKAGE_DIR = os.path.join(ROOT_DIR, PACKAGE_FOLDER_NAME)


DOCS_FOLDER_NAME = 'docs'
DOCS_DIR = os.path.join(ROOT_DIR, DOCS_FOLDER_NAME)
DOCS_BUILD_DIR = os.path.join(DOCS_DIR, 'build')
DOCS_HTML_DIR = os.path.join(DOCS_BUILD_DIR, 'html')
DOCS_HTML_INDEX = os.path.join(DOCS_HTML_DIR, 'index.html')


STATIC_FOLDER_NAME = 'static'
STATIC_DIR = os.path.join(ROOT_DIR, STATIC_FOLDER_NAME)


FONTS_DIR = os.path.join(STATIC_DIR, 'fonts')
ICONS_DIR = os.path.join(STATIC_DIR, 'icons')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
QT_DESIGNER_DIR = os.path.join(STATIC_DIR, 'qt_designer')
