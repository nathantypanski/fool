"""Fool sections."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import fool.conf
import fool.files

class SectionList(fool.objects.DirectoryObject):
    """A directory containing a list of fool sections.
    """

    def __init__(self):
        conf = fool.conf.ConfigDirectories()
        def dirpath_func(name):
            """The path to the list of sections."""
            path = (conf.config_dir / name).normpath().abspath()
            return path
        super(self.__class__, self).__init__('sections', dirpath_func)

class SectionPointer(object):
    """A pointer from one file to another in a Fool section.

    These are represented on the file system as symbolic links.
    """

    def __init__(self, source):
        self._source = fool.files.FoolPath(source)
        assert self._source.islink()
        self._destination = source.realpath()

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination


class Section(object):
    """A fool section.
    """

    def __init__(self, name, source, destination):
        self.name = name
        self.source = source
        self.destination = destination
