"""Conflict resolvers.

These classes are used to resolve conflicts between source and destination
files during a group sync.
"""

import fool.files

class ConflictResolver(object):

    def __init__(self, source, destination):
        self.source = fool.files.FoolPath(source)
        self.destination = fool.files.FoolPath(destination)


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
