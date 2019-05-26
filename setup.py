# -*- coding: utf-8 -*-
"""Setup file for projectx.

Note:
    Use `pip install -e .[dev]` to install development dependencies for example
    to get code completion.
"""

import ast
import logging
import os
from pathlib import Path

import pip
from setuptools import setup
from setuptools import find_packages


# import parse_requirements. This is an internal API of pip, and it is not!
# recommended to use it
try:  # pip <= 9
    from pip.req import parse_requirements
except ImportError:  # pip > 9
    from pip._internal.req import parse_requirements


SETUP_DIRECTORY = Path(os.path.dirname(__file__))
PACKAGE_DIRECTORY = SETUP_DIRECTORY / "projectx"
REQUIREMENTS_DEFAULT = SETUP_DIRECTORY / "requirements.txt"
REQUIREMENTS_DEV = SETUP_DIRECTORY / "requirements_dev.txt"
PACKAGE_INIT_FILE = PACKAGE_DIRECTORY / "__init__.py"


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AssignmentVisitor(ast.NodeVisitor):
    """Traverse module ast to inspect assignments. This does not execute the
    module.
    """

    def __init__(self):
        self.result = {}

    def visit_Assign(self, node):
        key = node.targets[0].id
        value = node.value.s if(hasattr(node.value, "s")) else None  # only grab strings
        self.result[key] = value


def get_requirements_list(requirements_file):
    """Parse requirements.txt file into a list of requirement names"""

    if (isinstance(requirements_file, Path)):
        requirements_file = requirements_file.as_posix()

    requirement_generator = parse_requirements(requirements_file, session=False)
    """Returns generator of pip.req.InstallRequirement objects"""

    install_requires = ["{}".format(requirement.req) for requirement in requirement_generator]
    """List of requirements like ['click==1.5.1', 'PySide==1.2.2'...]"""

    return install_requires


# install_requires
install_requires = get_requirements_list(REQUIREMENTS_DEFAULT)
dev_dependencies = get_requirements_list(REQUIREMENTS_DEV)


# read content from package __init__ without executing the module
text = PACKAGE_INIT_FILE.read_text()
tree = ast.parse(text)
visitor = AssignmentVisitor()
visitor.visit(tree)  # traverse all assign nodes and collect results


# read data from visitor (any missing dict. lookup will result in failure of
# the process).
name = visitor.result["__application__"]
version = visitor.result["__version__"]
author = visitor.result["__author__"]
email = visitor.result["__email__"]
description = visitor.result["__description__"]
description_detailed = visitor.result["__description_detailed__"]


setup(
    name=name,
    version=version,
    description=description,
    long_description=description_detailed,
    author=author,
    author_email=email,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,  # pip install -e . | pip install .
    extras_require={
        'dev': dev_dependencies,  # pip install -e .[dev]
    },
    zip_safe=False,
    test_suite='tests',
    keywords=name,
    entry_points={
        'console_scripts': [
            'projectx=projectx.cli.cli:cli',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
