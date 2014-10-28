import errno
import sys

import six

import fool.conf
import fool.files

class PureChapter(object):
    """A chapter of sections, in the abstract sense of the word.

    Pure chapters do not modify the underlying filesystem.
    """

    def __init__(self, name):
        self.dirconfig = fool.conf.ConfigDirectories()
        self._name = name

    @property
    def name(self):
        """Name of this chapter."""
        return self._name

    def rename(self, newname):
        """Rename this chapter."""
        self._name = newname

class Chapter(PureChapter):
    """A chapter of sections in the filesystem.

    A chapter is an abstract "collection" of Fool sections that can be
    activated or deactivated arbitrarily.
    """

    def __init__(self, name):
        super(Chapter, self).__init__(name)
        fool.files.create_subdirs(self.dirpath)
        if not self.dirpath.exists():
            self.dirpath.mkdir()

    @property
    def dirpath(self):
        """The path to the chapter."""
        path = (self.dirconfig / self.name).normpath().abspath()
        return path

    def rename(self, newname):
        """Rename this chapter."""
        try:
            self.dirpath.rename(newname)
        except OSError as exception:
            if exception.errno == errno.EEXIST:
                msg = 'Chapter {} already exists'.format(self.name)
                raise ChapterExistsError(msg)
            else:
                six.reraise(*sys.exc_info())
        super(Chapter, self).rename(newname)

class ChapterExistsError(Exception):
    """Error raised when a chapter exists and an overwrite is attempted."""
    pass