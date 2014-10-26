"""fool file groups."""

import collections

import fool.conf
import fool.xdg


class GroupConfig(fool.conf.ConfigFile,
                  collections.MutableMapping,
                  collections.MutableSet):
    """Dotfile group configuration file.
    """
    __shared_state = {}

    def __init__(self, groups=None):
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            self.config_directories = fool.conf.ConfigDirectories()
            if groups is None:
                self.groups = {}
            elif isinstance(groups, dict):
                self.groups = {key: val for key, val in groups.items()}
            else:
                self.groups = {group.name: group for group in groups}
        super(GroupConfig, self).__init__('groups',
                                          self.config_directories.config_dir)

    @classmethod
    def clear_state(cls):
        """Clear the internal shared state of the group configuration."""
        cls.__shared_state.clear()

    def __getitem__(self, group):
        """Return the group associated with a given name."""
        if isinstance(group, fool.group.Group):
            return self.groups[group.name]
        else:
            return self.groups[group]

    def __setitem__(self, name, group):
        """Return the group associated with a given name."""
        if not isinstance(group, fool.group.Group):
            raise TypeError('can only add groups')
        if not isinstance(name, str):
            raise TypeError('groups can only be keyed by strings')
        self.groups[group.name] = group

    def __delitem__(self, group):
        del self.groups[group]

    def __contains__(self, group):
        if isinstance(group, fool.group.Group):
            return group in self.groups.values()
        else:
            return group in self.groups

    def __iter__(self):
        return iter(self.groups)

    def __len__(self):
        return len(self.groups)

    def add(self, group):
        self[group.name] = group

    def discard(self, group):
        del self[group]

    def prepare_write(self):
        config = self._clear_config_parser()
        for name, group in self.items():
            section = 'group.{}'.format(name)
            config.add_section(section)
            config.set(section, 'source', group.source)
            config.set(section, 'dest', group.dest)


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
        self.dest = dest
