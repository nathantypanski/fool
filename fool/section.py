"""Fool sections."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import fool.conf

class SectionDirectory(fool.objects.DirectoryObject):
    """A directory containing information about a fool section.

    A section is an abstract "collection" of files that have an associated
    destination directory.
    """

    def __init__(self, name):
        conf = fool.conf.ConfigDirectories()
        def dirpath_func(name):
            """The path to the section."""
            path = (conf.section_dir / name).normpath().abspath()
            return path
        super(self.__class__, self).__init__(name, dirpath_func)
