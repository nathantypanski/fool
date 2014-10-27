"""Conflict resolvers.

These classes are used to resolve conflicts between source and destination
files during a group sync.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import abc

import fool.files

def __ConflictResolver___init__(self, source, destination):
    self.source = fool.files.FoolPath(source)
    self.destination = fool.files.FoolPath(destination)

@abc.abstractmethod
def __ConflictResolver_resolve(self):
    """Resolve this directory"""
    pass

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

    def __init__(self, source, destination):
        super(OverwriteResolver, self).__init__(source, destination)

    def resolve(self):
        with fool.files.temporary_directory() as tempdir:
            _, destname = self.destination.split()
            tempdest = tempdir / destname
            self.source.symlink(tempdest)
            tempdest.rename(self.destination)
