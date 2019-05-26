# -*- coding: utf-8 -*-
"""Package __init__ for projectx. Central spot to define package
metadata like version, author etc.

Notes:
    This should be the only spot where version data is maintained. All other
    places should read from here if possible.
"""

import logging


# add NullHandler to avoid missing logger error messages before any actual
# logger setup
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


__author__ = "Timm Wagener"
__email__ = "wagenertimm@gmail.com"
__application__ = "projectx"
__version__ = "0.1.0"
__organization__ = "timmwagener"
__domain__ = "http://timmwagener.com/"

__description__ = "Python3/Pyside2 GUI project to use as template for cookiecutter"
__description_detailed__ = "Python3/Pyside2 GUI project to use as template for cookiecutter"
