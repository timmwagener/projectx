# -*- coding: utf-8 -*-

import logging

import pytest
from click.testing import CliRunner

from projectx.cli.cli import cli
from projectx.cli.gui import gui


logger = logging.getLogger(__name__)


@pytest.fixture(params=['-h', '--help'])
def help_cli_flag(request):
    return request.param


@pytest.fixture(params=[cli, gui, ])
def cmd(request):
    return request.param


def test_cli_help(cmd, help_cli_flag):
    runner = CliRunner()
    result = runner.invoke(cmd, [help_cli_flag, ])
    assert result.exit_code == 0
    assert result.output.startswith('Usage')
