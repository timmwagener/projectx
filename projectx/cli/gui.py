# -*- coding: utf-8 -*-
import logging

import click

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
    """Run projectx in GUI mode."""

    print(verbosity)

    # with GeneralPurposeNodesContext(verbosity):
    #     with GeneralPurposeNodesGuiContext() as application:
    #
    #         # create mainwindow
    #         main_window = GeneralPurposeNodesWindow()
    #         main_window.close_event_received.connect(main_window.persist)
    #         application.aboutToQuit.connect(main_window.persist)
    #
    #         # restore, there is no event loop yet
    #         if (main_window.restore() is False):
    #             rectangle = half_screen() if (screensize == "half") else full_screen()
    #             main_window.setGeometry(rectangle)
    #
    #         # source_file supplied?
    #         if (isinstance(source_file, str)):
    #             load_ui_scene(source_file)
    #
    #         # show
    #         main_window.show()


if (__name__ == "__main__"):

    # This is the entry point for PyInstaller or debugging via PyCharm. The
    # decorated function `cli` is a click Command that provides command line
    # parsing from used decorators.
    # Calling it without arguments will use sys.argv[1:] by default, which are
    # the arguments provided by the OS process infrastructure.
    gui()
