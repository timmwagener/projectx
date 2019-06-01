# -*- coding: utf-8 -*-

import logging

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs


logger = logging.getLogger(__name__)


PACKAGE_NAME = "projectx"


logger.info("")
logger.info(f"Running hooks for module {PACKAGE_NAME}")


# hidden imports
hiddenimports = collect_submodules(PACKAGE_NAME)


# datas
datas = collect_data_files(PACKAGE_NAME)

# add repository level assets.
# application level assets should be located in the package
# and accessed via importlib.resources
datas.extend([
    ('docs/build', 'docs/build'),
])

# log
logger.info("")
logger.info(f"Collected data files for {PACKAGE_NAME}:")
for source, destination in datas:
    msg = f"{source} {destination}"
    logger.info(msg)


# binaries
binaries = collect_dynamic_libs(PACKAGE_NAME)

# log
logger.info("")
logger.info(f"Found binaries for {PACKAGE_NAME}")
for source, destination in binaries:
    msg = f"{source} {destination}"
    logger.info(msg)
