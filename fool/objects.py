
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import sys

import six

import fool.files

class GroupObject(object):
    """An object for syncing with fool.

    A GroupObject is pathname and a destination link pathname, representing
    the source pathname and the destination pathname of a desired link.

    Args:
        source: source pathname for this GroupObject.
        destination: destination pathname for this GroupObject.
    """

    def __init__(self, source, destination):
        self.source = fool.files.FoolPath(source)
        self.destination = fool.files.FoolPath(destination)

    @property
    def synced(self):
        """Test whether the destination is a symlink to the source."""
        return (self.destination.islink()
                and self.source == self.destination.realpath())

    def sync(self, resolver=None):
        """Create a symbolic link from the source to destination.

        Do nothing if already synced.

        Keyword args:
            resolver: Resolver class used to handle flile conflicts.
        """
        if self.synced:
            return
        if resolver is not None and not hasattr(resolver, 'resolve'):
            raise TypeError('resolver must have a resolve() method')
        try:
            self.source.symlink(self.destination)
        except OSError as exception:
            if resolver is not None:
                resolver(self.source, self.destination, exception).resolve()
            else:
                six.reraise(*sys.exc_info())

    def tuple(self):
        """Return a tuple of source, destination."""
        return self.source, self.destination

    def __repr__(self):
        return "GroupObject({}, {})".format(self.source, self.destination)

