"""Fool sections."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import fool.conf

class Section(fool.objects.DirectoryObject):
    """A section of files in the filesystem.

    A section is an abstract "collection" of files that have an associated
    destination directory.
    """

    def __init__(self, name):
        conf = fool.conf.ConfigDirectories()
        def dirpath_func(name):
            """The path to the section."""
            path = (conf.section_dir / name).normpath().abspath()
            return path
        super(Section, self).__init__(name, dirpath_func)
