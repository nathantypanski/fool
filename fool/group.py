"""fool file groups."""

import fool.xdg

class Group(object):
    """Fool file group.

    Args:

        name: unique name of this group
        source: source folder for this group

    Keyword args:

         dest: destination directory for these files.
    """
    def __init__(self, name, source, dest=None):
        xdg_config = fool.xdg.XDGConfig()
        self.name = name
        self.source = source
        if dest is None:
            dest = xdg_config.home

