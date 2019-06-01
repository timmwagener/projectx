# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

import projectx
from projectx.cli import gui as entrypoint


logger = logging.getLogger(__name__)


logger.info("")
logger.info("Running build for projectx")


# application
ENTRYPOINT = Path(entrypoint.__file__).as_posix()  # script run by PyInstaller
APPLICATION_NAME = f"{projectx.__application__}"
APPLICATION_VERSION = f"{projectx.__version__}"
COLLECT_NAME = f"{APPLICATION_NAME}-{APPLICATION_VERSION}"


# read environment
BLOCK_CIPHER_KEY = os.environ["BLOCKCIPHER"]
EXE_DEBUG = bool(int(os.environ["EXE_DEBUG"]))
EXE_CONSOLE = bool(int(os.environ["EXE_CONSOLE"]))
PYINSTALLER_HOOKS = Path(os.environ["PYINSTALLER_HOOKS"]).as_posix()


# log environment
logger.info("")
logger.info(f"APPLICATION_NAME: {APPLICATION_NAME}")
logger.info(f"APPLICATION_VERSION: {APPLICATION_VERSION}")
logger.info(f"COLLECT_NAME: {COLLECT_NAME}")
logger.info(f"ENTRYPOINT: {ENTRYPOINT}")

logger.info("")

logger.info(f"BLOCK_CIPHER_KEY: {BLOCK_CIPHER_KEY}")
logger.info(f"EXE_DEBUG: {EXE_DEBUG}")
logger.info(f"EXE_CONSOLE: {EXE_CONSOLE}")
logger.info(f"PYINSTALLER_HOOKS: {PYINSTALLER_HOOKS}")
logger.info("")


# encryption
# block_cipher = pycryptodome.PyiBlockCipher(key=BLOCK_CIPHER_KEY)


# pyinstaller machinery
a = Analysis(
    [ENTRYPOINT, ],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[PYINSTALLER_HOOKS, ],
    runtime_hooks=None,
    excludes=None,
    win_no_prefer_redirects=None,
    win_private_assemblies=None,
    # cipher=block_cipher
)


pyz = PYZ(
    a.pure,
    a.zipped_data,
    # cipher=block_cipher
)


exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=APPLICATION_NAME,
    debug=EXE_DEBUG,
    strip=None,
    upx=True,
    console=EXE_CONSOLE,
    # icon=f"icons/{projectx.__application__}.ico"
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=None,
    upx=True,
    name=COLLECT_NAME
)
