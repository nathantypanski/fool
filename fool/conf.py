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
import fool.files


def create_subdirs(path):
    """Create necessary subdirectories leading up to path.

    Args:
        path: path to which directories will be created. Note that path
            itself will not be created.
    """
    try:
        os.makedirs(str(fool.files.Path(path).dirname))
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
        return self.xdg_config.config_home / self._config_name

    @property
    def data_dir(self):
        """fool's data directory"""
        return self.xdg_config.data_home / self._config_name

    def create_config_dir(self):
        """Create the configuration directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        create_subdirs(self.config_dir)
        print('creating directory {}'.format(self.config_dir))
        os.mkdir(str(self.config_dir), self.directory_mode)

    def create_data_dir(self):
        """Create the data directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        create_subdirs(self.data_dir)
        print('creating directory {}'.format(self.data_dir))
        os.mkdir(str(self.data_dir), self.directory_mode)


class ConfigFile(object):
    """A configuration file object.

    Keyword args:

        directory: if provided, path is set relative to this directory.
            Otherwise path will be used as given.

    """

    def __init__(self, path, directory=None):
        if directory:
            self._path = fool.files.Path(directory) / fool.files.Path(path)
        else:
            self._path = fool.files.Path(path)
        self.configparser = configparser.SafeConfigParser()

    def _clear_config_parser(self):
        """Clear and return the new config parser for this configfile"""
        self.configparser = configparser.SafeConfigParser()
        return self.configparser

    def prepare_write(self):
        pass

    @property
    def path(self):
        return self._path

    @property
    def exists(self):
        """True if the configuration file exists"""
        return self._path.exists

    def write(self):
        """Create an empty configuration file if it does not exist.
        """
        self.prepare_write()
        create_subdirs(self._path)
        with self.path.open('wb') as configfile:
            self.configparser.write(configfile)
