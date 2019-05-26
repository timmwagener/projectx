# -*- coding: utf-8 -*-
import logging

import click

from projectx.core.configuration.startup import ApplicationCoreContext

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


@cli.command('core', context_settings=dict(help_option_names=['-h', '--help']))
@version_option
@logging_option
@config_option
def core(verbosity, ):
    """Run application in core mode. This serves as an example for a command that
    doesn't involve any gui code and should only import from the core package.
    In a real application this could be commands to convert the application
    data formats or other utilities.
    """

    with ApplicationCoreContext(verbosity):
        logger.info(verbosity)


if (__name__ == "__main__"):

    # This is the entry point for PyInstaller or debugging via PyCharm. The
    # decorated function `cli` is a click Command that provides command line
    # parsing from used decorators.
    # Calling it without arguments will use sys.argv[1:] by default, which are
    # the arguments provided by the OS process infrastructure.
    core()
