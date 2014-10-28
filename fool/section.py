"""Fool sections."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import fool.conf

class Section(object):
    """A section is a group of files that get symlinked to the same root.

    Sections are the elements that comprise a Chapter.
    """

    def __init__(self, name):
        self.dirconfig = fool.conf.ConfigDirectories()
        self._name = name

    @property
    def name(self):
        """Name of this section."""
        return self._name

    def rename(self, newname):
        """Rename this section."""
        self._name = newname
