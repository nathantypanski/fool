"""Fool configuration"""

import errno
import os
import os.path

try:
    import ConfigParser
    configparser = ConfigParser
except ImportError:
    import configparser

import fool.xdg
import fool.group


def create_subdirs(path):
    """Create necessary subdirectories leading up to path.

    Args:
        path: path to which directories will be created. Note that path
            itself will not be created.
    """
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise exception
        else:
            pass


class ConfigDirectories(object):
    __shared_state = {}

    def __init__(self, directory_mode=0o700, xdg_config=None):
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            if xdg_config is None:
                xdg_config = fool.xdg.XDGConfig()
            self.xdg_config = xdg_config
            self.directory_mode = directory_mode
            self._config_name = 'fool'

    @classmethod
    def clear_state(cls):
        """Clear the internal shared state of the directory configuration."""
        cls.__shared_state.clear()

    @property
    def home_dir(self):
        return self.xdg_config.home

    @property
    def config_dir(self):
        """fool's config directory"""
        return self.xdg_config.config_home + '/' + self._config_name

    @property
    def data_dir(self):
        """fool's data directory"""
        return self.xdg_config.data_home + '/' + self._config_name

    def create_config_dir(self):
        """Create the configuration directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        create_subdirs(self.config_dir)
        print('creating directory {}'.format(self.config_dir))
        os.mkdir(self.config_dir, self.directory_mode)

    def create_data_dir(self):
        """Create the data directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        create_subdirs(self.data_dir)
        print('creating directory {}'.format(self.data_dir))
        os.mkdir(self.data_dir, self.directory_mode)


class ConfigFile(object):
    """A configuration file object.

    Keyword args:

        directory: if provided, path is set relative to this directory.
            Otherwise path will be used as given.

    """

    def __init__(self, path, directory=None):
        if directory:
            self._path = os.path.join(directory, path)
        else:
            self._path = path

    @property
    def path(self):
        return self._path

    @property
    def exists(self):
        """True if the configuration file exists"""
        return os.path.exists(self._path)

    def create(self):
        """Create an empty configuration file if it does not exist.
        """
        create_subdirs(self._path)
        os.mknod(self._path)


class GroupConfig(ConfigFile):
    """Dotfile group configuration file.
    """
    __shared_state = {}

    def __init__(self, groups=None, config_directories=None):
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            if config_directories is None:
                config_directories = ConfigDirectories()
            self.config_directories = config_directories
            if groups is None:
                groups = []
            self.groups = groups

    @classmethod
    def clear_state(cls):
        """Clear the internal shared state of the group configuration."""
        cls.__shared_state.clear()

    def create_group(self, name, path):
        self.groups.append(fool.group.Group(name, path))
