# -*- coding: utf-8 -*-

import logging

from PySide2.QtWidgets import QApplication

from projectx import __application__ as application_name
from projectx import __version__ as application_version
from projectx import __organization__ as organization_name
from projectx import __domain__ as organization_domain


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

    def connect_ui(self):
        self.aboutToQuit.connect(self.teardown)

    def teardown(self):
        """Method that can be called directly from unittests."""
        logger.info("teardown")  # Quit threads here for example
