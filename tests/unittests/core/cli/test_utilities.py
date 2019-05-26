# -*- coding: utf-8 -*-
"""Test generic click utility decorators."""

import logging
import json
import os

import pytest
import click
from click.testing import CliRunner

from projectx import __version__

from projectx.cli.utilities import version_option
from projectx.cli.utilities import config_option
from projectx.cli.utilities import logging_option
from projectx.cli.utilities import mandatory_source_file
from projectx.cli.utilities import optional_source_file


logger = logging.getLogger(__name__)


@pytest.mark.parametrize("flag", ["-V", "--version"])
def test_version_option_evaluated_eagerly(flag):

    output = "output"

    @click.command()
    @version_option
    def cmd():
        click.echo(output)

    runner = CliRunner()
    result = runner.invoke(cmd, [flag, ])
    assert result.exit_code == 0
    assert result.output.rstrip() == __version__


def test_version_option_not_evaluated():

    output = "output"

    @click.command()
    @version_option
    def cmd():
        click.echo(output)

    runner = CliRunner()
    result = runner.invoke(cmd, [])
    assert result.exit_code == 0
    assert result.output.rstrip() == output


@pytest.mark.parametrize("flag", ["-C", "--config"])
def test_config_option_evaluated_eagerly(flag):

    output = "output"

    @click.command()
    @config_option
    def cmd():
        click.echo(output)

    runner = CliRunner()
    result = runner.invoke(cmd, [flag, ])

    assert result.exit_code == 0
    settings_dict = json.loads(result.output.rstrip())
    assert settings_dict == {"__version__": __version__}


def test_config_option_not_evaluated():

    output = "output"

    @click.command()
    @config_option
    def cmd():
        click.echo(output)

    runner = CliRunner()
    result = runner.invoke(cmd, [])
    assert result.exit_code == 0
    assert result.output.rstrip() == output


@pytest.mark.parametrize("flag", ["-v", "--verbosity"])
@pytest.mark.parametrize("value", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_logging_option_evaluated(flag, value):

    @click.command()
    @logging_option
    def cmd(verbosity):
        click.echo(verbosity)

    runner = CliRunner()
    result = runner.invoke(cmd, [flag, value])

    assert result.exit_code == 0
    assert result.output.rstrip() == value


@pytest.mark.parametrize("flag", ["-v", "--verbosity"])
@pytest.mark.parametrize("value", ["debug", "", "WWARNING", "EROR", "20"])
def test_logging_option_returns_on_false_input(flag, value):

    @click.command()
    @logging_option
    def cmd(verbosity):
        click.echo(verbosity)

    runner = CliRunner()
    result = runner.invoke(cmd, [flag, value])

    assert result.exit_code == 2
    msg = f"Error: Invalid value for \"-v\" / \"--verbosity\": invalid choice: "
    msg += f"{value}. (choose from DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    assert result.output.rstrip().endswith(msg)


def test_mandatory_source_file_fails_if_file_not_given():

    @click.command()
    @mandatory_source_file
    def cmd(source_file):
        click.echo(source_file)

    runner = CliRunner()
    result = runner.invoke(cmd, [])

    assert result.exit_code == 2
    msg = f"Error: Missing argument \"SOURCE_FILE\"."
    assert result.output.rstrip().endswith(msg)


def test_mandatory_source_file_fails_if_file_doesnt_exist(tmpdir):
    filepath = tmpdir.join("file.gpn")
    filepath = f"{filepath}"
    assert os.path.exists(filepath) is False

    @click.command()
    @mandatory_source_file
    def cmd(source_file):
        click.echo(source_file)

    runner = CliRunner()
    result = runner.invoke(cmd, [filepath])

    assert result.exit_code == 2
    msg = f"Error: Invalid value for \"SOURCE_FILE\": File \"{filepath}\" "
    msg += f"does not exist."
    assert result.output.rstrip().endswith(msg)


def test_mandatory_source_file_fails_if_path_is_directory(tmpdir):
    filepath = f"{tmpdir}"
    assert os.path.isdir(filepath) is True

    @click.command()
    @mandatory_source_file
    def cmd(source_file):
        click.echo(source_file)

    runner = CliRunner()
    result = runner.invoke(cmd, [filepath])

    assert result.exit_code == 2
    msg = f"Error: Invalid value for \"SOURCE_FILE\": File \"{filepath}\" "
    msg += f"is a directory."
    assert result.output.rstrip().endswith(msg)


def test_mandatory_source_file_suceeds(tmpdir):
    filepath = tmpdir.join("file.gpn")
    filepath.write("")
    filepath = f"{filepath}"
    assert os.path.isfile(filepath) is True
    assert os.path.isdir(filepath) is False

    @click.command()
    @mandatory_source_file
    def cmd(source_file):
        click.echo(source_file)

    runner = CliRunner()
    result = runner.invoke(cmd, [filepath])

    assert result.exit_code == 0
    assert result.output.rstrip() == filepath


def test_optional_source_file_suceeds_if_filepath_given(tmpdir):
    filepath = tmpdir.join("file.gpn")
    filepath.write("")
    filepath = f"{filepath}"
    assert os.path.isfile(filepath) is True
    assert os.path.isdir(filepath) is False

    @click.command()
    @optional_source_file
    def cmd(source_file):
        click.echo(source_file)

    runner = CliRunner()
    result = runner.invoke(cmd, [filepath])

    assert result.exit_code == 0
    assert result.output.rstrip() == filepath


def test_optional_source_file_suceeds_if_filepath_not_given():

    @click.command()
    @optional_source_file
    def cmd(source_file):
        click.echo(source_file)

    runner = CliRunner()
    result = runner.invoke(cmd, [])

    assert result.exit_code == 0
    assert result.output.rstrip() == ""
