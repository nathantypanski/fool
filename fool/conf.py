"""Fool configuration"""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os
import os.path

import six
from six.moves import configparser

import fool.xdg
import fool.files


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
    def chapter_dir(self):
        """fool's chapter list directory"""
        return self.xdg_config.config_home / 'fool' / 'chapters'

    @property
    def group_list_path(self):
        """fool's group list config file"""
        return self.config_dir / 'groups'

    @property
    def data_dir(self):
        """fool's data directory"""
        return self.xdg_config.data_home / self._config_name

    def _create_directory(self, dirpath):
        fool.files.create_subdirs(dirpath)
        dirpath.mkdir(self.directory_mode)

    def create_config_dir(self):
        """Create the configuration directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        self._create_directory(self.config_dir)

    def create_data_dir(self):
        """Create the data directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        self._create_directory(self.data_dir)


class FoolConfigParser(configparser.SafeConfigParser):

    def __init__(self, allow_no_value=True):
        configparser.SafeConfigParser.__init__(self,
                                               allow_no_value=allow_no_value)
        self.optionxform = str


class ConfigFile(object):
    """A configuration file object.

    Keyword args:
        directory: if provided, path is set relative to this directory.
            Otherwise path will be used as given.

    """

    def __init__(self, path, directory=None):
        if directory:
            self._path = (fool.files.FoolPath(directory)
                          / fool.files.FoolPath(path))
        else:
            self._path = fool.files.FoolPath(path)
        self.configparser = FoolConfigParser()

    def _clear_config_parser(self):
        """Clear and return the new config parser for this configfile."""
        self.configparser = FoolConfigParser()
        return self.configparser

    def prepare_write(self):
        pass

    @property
    def path(self):
        return self._path

    def exists(self):
        """True if the configuration file exists."""
        return self._path.exists()

    def write(self):
        """Create an empty configuration file if it does not exist.
        """
        self.prepare_write()
        fool.files.create_subdirs(self._path)
        with self.path.open('w') as configfile:
            self.configparser.write(configfile)
