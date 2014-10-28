from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import fool.conf
import fool.files
import fool.objects


class Chapter(fool.objects.DirectoryObject):
    """A chapter of sections in the filesystem.

    A chapter is an abstract "collection" of Fool sections that can be
    activated or deactivated arbitrarily.
    """

    def __init__(self, name):
        conf = fool.conf.ConfigDirectories()
        def dirpath_func(name):
            """The path to the chapter."""
            path = (conf.chapter_dir / name).normpath().abspath()
            return path
        super(Chapter, self).__init__(name, dirpath_func)
