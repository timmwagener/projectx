# -*- coding: utf-8 -*-
"""All exceptions are named .*Exception instead of .*Error. This is to contrast
them with standard library exceptions and enable projectx exceptions like
AttributeException.
"""


class ProjectXException(Exception):
    """Base exception for projectx."""
