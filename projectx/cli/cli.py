# -*- coding: utf-8 -*-
import logging

import click

# There can be no explicit relative imports in modules that are used directly
# as PyInstaller entrypoint scripts (or as scripts in general).
# (Package internal explicit relative imports are fine though).
from . import core
from . import gui
from .utilities import version_option
from .utilities import config_option


logger = logging.getLogger(__name__)


@click.command(
    cls=click.CommandCollection,
    context_settings=dict(help_option_names=['-h', '--help'])
)
@version_option
@config_option
def cli():
    """projectx.

    Command Line Interface for projectx.
    """


cli.add_source(core.cli)
cli.add_source(gui.cli)


if (__name__ == "__main__"):

    # This is the entry point for setup.py. The decorated function `cli`
    # is a click Command that provides command line parsing from used decorators.
    # Calling it without arguments will use sys.argv[1:] by default, which are
    # the arguments provided by the OS process infrastructure.
    cli()
