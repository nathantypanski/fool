"""fool file groups."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import collections

import six
from six.moves import configparser

import fool.conf
import fool.xdg
import fool.files
import fool.objects


class GroupListConfig(fool.conf.ConfigFile,
                      collections.MutableMapping,
                      collections.MutableSet):
    """Dotfile group configuration file.

    Keyword args:
        groups: A list of groups to initialize the group configuration.
            Only valid for the first instantiation of this object, or after
            the state has been cleared.
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
        super(GroupListConfig, self).__init__('groups',
            self.config_directories.config_dir)

    @classmethod
    def clear_state(cls):
        """Clear the internal shared state of the group configuration."""
        cls.__shared_state.clear()

    @classmethod
    def from_config_file(cls, config=None):
        """Rebuild the GroupListConfig from a supplied ConfigParser.

        If successful, the state of the group config will be reset.

        Keyword args:
            config: ConfigParser orbject containing group definitions.

        Returns:
            New GroupListConfig object with settings from config file.
        """
        try:
            if config is None:
                config = fool.conf.FoolConfigParser()
                group_list_path = fool.conf.ConfigDirectories().group_list_path
                group_list_path = six.text_type(group_list_path)
                config.read(group_list_path)
            groups = []
            for grouprc_path, _ in config.items('groups'):
                grouprc_config = fool.conf.FoolConfigParser()
                grouprc_config.read(str(grouprc_path))
                groups.append(Group.from_config_file(grouprc_config))
        except configparser.NoSectionError:
            pass
        cls.clear_state()
        return GroupListConfig(groups)

    def __getitem__(self, group):
        """Return the group associated with a given name."""
        if isinstance(group, fool.group.Group):
            return self.groups[group.name]
        else:
            return self.groups[group]

    def __setitem__(self, name, group):
        """Set the group associated with a given name.

        Args:
            name: the name for this group.
            group: Group object to associate with this name.
        """
        if not isinstance(group, fool.group.Group):
            raise TypeError('can only add groups')
        if not isinstance(name, six.string_types):
            raise TypeError('groups can only be keyed by strings')
        if not name == group.name:
            raise ValueError('name argument must match group name')
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
        """Add a group to the GroupListConfig.

        Args:
           group: Group object to be added.
        """
        self[group.name] = group

    def discard(self, group):
        """Remove a group from the GroupListConfig.

        Args:
           group: Group object to be deleted.
        """
        del self[group]

    def prepare_write(self):
        config = self._clear_config_parser()
        groups_section = six.text_type('groups')
        config.add_section(groups_section)
        for name, group in self.items():
            group.write()
            path = six.text_type(group.path.expanduser().abspath())
            config.set(groups_section, path)


class Group(fool.conf.ConfigFile):
    """Fool file group.

    Args:
        name: unique name of this group
        source: source folder for this group

    Keyword args:
         dest: destination directory for these files. Defaults to XDG home.
    """
    def __init__(self, name, source, destination=None):
        xdg_config = fool.xdg.XDGConfig()
        self._name = name
        self._source = fool.files.FoolPath(source).expanduser().abspath()
        if destination:
            self._destination = fool.files.FoolPath(destination).expanduser().abspath()
        else:
            self._destination = xdg_config.home.expanduser().abspath()
        config_file_path = fool.files.FoolPath(source) / '.foolrc'
        super(Group, self).__init__(config_file_path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = fool.files.FoolPath(value)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = fool.files.FoolPath(value)

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = fool.files.FoolPath(value)

    def files(self, topdown=True, onerror=None, followlinks=False):
        """Walk the source files in this group.

        Keyword args:
            topdown: see os.walk()
            onerror: see os.walk()
            followlinks: see os.walk()

        Yields:
            Source files in this group, per os.walk().
        """
        return self.source.walk_files()

    def group_objects(self):
        """Get the GroupObjects associated with this group.

        Yields:
            GroupObject items for each pair of source and destination paths
            in this group.
        """
        for path in self.source.walk_files():
            relpath = path.relpath(self.source)
            gobj = fool.objects.GroupObject(path, self.destination / relpath)
            yield gobj

    def sync(self, resolver=None):
        """Sync the files in this group.

        Keyword args:
            resolver: Resolver class used to handle flile conflicts.
        """
        for group_object in self.group_objects():
            group_object.sync(resolver=resolver)

    @classmethod
    def from_config_file(cls, config):
        """Rebuild the GroupListConfig from a supplied ConfigParser.

        If successful, the state of the group config will be reset.

        Args:
            config: ConfigParser orbject containing group definitions.

        Returns:
            New GroupListConfig object with settings from config file.
        """
        name = config.get('group', 'name')
        source = config.get('group', 'source')
        destination = config.get('group', 'destination')
        return Group(name, source, destination)

    def prepare_write(self):
        config = self._clear_config_parser()
        group_section = six.text_type('group')
        config.add_section(group_section)
        config.set(group_section, 'destination', six.text_type(self.destination))
        config.set(group_section, 'source', six.text_type(self.source))
        config.set(group_section, 'name', six.text_type(self.name))

    def __eq__(self, other):
        names_match = self.name == other.name
        sources_match = self.source == other.source
        destinations_match = self.destination == other.destination
        return names_match and sources_match and destinations_match

    def __repr__(self):
        return ('Group(name={}, source={}, destination={})'
                .format(self.name, self.source, self.destination))
