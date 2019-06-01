# -*- coding: utf-8 -*-
import logging
from importlib.resources import path as resource_path

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon

from projectx import __application__ as application_name
from projectx import __version__ as application_version
from projectx import __organization__ as organization_name
from projectx import __domain__ as organization_domain

from projectx.data.images import icons


logger = logging.getLogger(__name__)


class ProjectXApplication(QApplication):
    """Application specific QApplication subclass."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_ui()
        self.connect_ui()

    def setup_ui(self):

        # application data
        self.setApplicationName(application_name)
        self.setApplicationVersion(application_version)
        self.setOrganizationName(organization_name)
        self.setOrganizationDomain(organization_domain)

        # icon
        with resource_path(icons, "application.ico") as _path:
            icon = QIcon(_path.as_posix())
        self.setWindowIcon(icon)

    def connect_ui(self):
        self.aboutToQuit.connect(self.teardown)

    def teardown(self):
        """Method that can be called directly from unittests."""
        logger.info("teardown")  # Quit threads here for example
