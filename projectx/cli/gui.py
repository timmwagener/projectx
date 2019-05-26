# -*- coding: utf-8 -*-
import logging

from PySide2.QtWidgets import QLabel

import click

from projectx.core.configuration.startup import ApplicationCoreContext
from projectx.ui.configuration.startup import ApplicationGuiContext

# There can be no explicit relative imports in modules that are used directly
# as PyInstaller entrypoint scripts (or as scripts in general).
# (Package internal explicit relative imports are fine though).
from projectx.cli.utilities import logging_option
from projectx.cli.utilities import version_option
from projectx.cli.utilities import config_option


logger = logging.getLogger(__name__)


@click.group()
def cli():
    """cli"""


@cli.command('gui', context_settings=dict(help_option_names=['-h', '--help']))
@version_option
@logging_option
@config_option
def gui(verbosity, ):
    """Run application in gui mode."""

    with ApplicationCoreContext(verbosity):
        with ApplicationGuiContext() as application:

            # label
            label = QLabel("gui")
            label.show()


if (__name__ == "__main__"):

    # This is the entry point for PyInstaller or debugging via PyCharm. The
    # decorated function `cli` is a click Command that provides command line
    # parsing from used decorators.
    # Calling it without arguments will use sys.argv[1:] by default, which are
    # the arguments provided by the OS process infrastructure.
    gui()
