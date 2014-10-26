"""fool file groups."""

import collections
import re

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

    @classmethod
    def from_config_file(cls, config):
        """Rebuild the GroupConfig from a supplied ConfigParser.

        If successful, the state of the group config will be reset.

        Args:
            config: ConfigParser orbject containing group definitions.

        Returns:
            New GroupConfig object with settings from config file.
        """
        groupmatch = re.compile(r'group\.(.*)')
        groups = []
        for section in config.sections():
            try:
                match = groupmatch.match(section)
                name = match.group(1)
                source = config.get(section, 'source')
                destination = config.get(section, 'destination')
                groups.append(Group(name, source, destination))
            except TypeError:
                pass # not a group
        cls.clear_state()
        return GroupConfig(groups)

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
        """Add a group to the GroupConfig.

        Args:
           group: a Group object to be added.
        """
        self[group.name] = group

    def discard(self, group):
        """Remove a group from the GroupConfig.

        Args:
           group: a Group object to be deleted.
        """
        del self[group]

    def prepare_write(self):
        config = self._clear_config_parser()
        for name, group in self.items():
            section = 'group.{}'.format(name)
            config.add_section(section)
            config.set(section, 'source', group.source)
            config.set(section, 'destination', group.destination)


class Group(object):
    """Fool file group.

    Args:
        name: unique name of this group
        source: source folder for this group

    Keyword args:
         dest: destination directory for these files. Defaults to XDG home.
    """
    def __init__(self, name, source, destination=None):
        xdg_config = fool.xdg.XDGConfig()
        self.name = name
        self.source = source
        if destination is None:
            destination = xdg_config.home
        self.destination = destination
