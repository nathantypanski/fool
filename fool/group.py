"""fool file groups."""
from __future__ import division
from __future__ import unicode_literals

import collections
import re
import sys

import six

import fool.conf
import fool.xdg
import fool.files


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
    def from_config_file(cls, config):
        """Rebuild the GroupListConfig from a supplied ConfigParser.

        If successful, the state of the group config will be reset.

        Args:
            config: ConfigParser orbject containing group definitions.

        Returns:
            New GroupListConfig object with settings from config file.
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
        for name, group in self.items():
            section = six.text_type('group.{}'.format(name))
            config.add_section(section)
            config.set(section, 'source', six.text_type(group.source))
            config.set(section, 'destination', six.text_type(group.destination))


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
        self.source = fool.files.FoolPath(source)
        if destination is None:
            destination = xdg_config.home
        self.destination = destination

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
            gobj = GroupObject(path, self.destination / relpath)
            yield gobj

    def sync(self, resolver=None):
        """Sync the files in this group.

        Keyword args:
            resolver: Resolver class used to handle flile conflicts.
        """
        for group_object in self.group_objects():
            group_object.sync(resolver=resolver)

    def __repr__(self):
        return ('Group(name={}, source={}, destination={})'
                .format(self.name, self.source, self.destination))
