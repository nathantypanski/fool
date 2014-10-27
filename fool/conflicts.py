"""Conflict resolvers.

These classes are used to resolve conflicts between source and destination
files during a group sync.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import abc

import fool.files


__all__ = [
    'ConflictResolver',
    'OverwriteResolver',
]


def __ConflictResolver___init__(self, source, destination, exception=None):
    self.source = fool.files.FoolPath(source)
    self.destination = fool.files.FoolPath(destination)
    self.exception = exception


@abc.abstractmethod
def __ConflictResolver_resolve(self):
    """Resolve this directory"""
    pass


# We need to declare ConflictResolver like this in order to achieve full
# compatibility between Python versions.
#
# Here, we're calling the metaclass with the name of the new type and
# supplying the dictionary of arguments required to construct the
# ConflictResolver type. See
# <https://wiki.python.org/moin/PortingToPy3k/BilingualQuickRef#metaclasses>
# for more information on building metaclasses this way.
ConflictResolver = abc.ABCMeta(str('ConflictResolver'), (),
    {
        '__init__': __ConflictResolver___init__,
        '__doc__':
            """Class for resolving of file conflicts.

            All subclasses are required to define a resolve() method
            that is used to handle file conflicts.
            """,
        'resolve': __ConflictResolver_resolve,
    })


class OverwriteResolver(ConflictResolver):
    """A ConflictResolver that always overwrites the destination.
    """

    def __init__(self, source, destination, exception=None):
        super(OverwriteResolver, self).__init__(source, destination, exception)

    def resolve(self):
        with fool.files.temporary_directory() as tempdir:
            _, destname = self.destination.split()
            tempdest = tempdir / destname
            self.source.symlink(tempdest)
            tempdest.rename(self.destination)
