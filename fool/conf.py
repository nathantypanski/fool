"""Fool configuration"""

import os

import fool.xdg

class ConfigDirectories(object):

    def __init__(self, directory_mode=0o700, xdg_config=None):
        if xdg_config is None:
            xdg_config = fool.xdg.XDGConfig()
        self.xdg_config = xdg_config
        self.directory_mode = directory_mode

    @property
    def config_dir(self):
        return self.xdg_config.config_dir

    @property
    def data_dir(self):
        return self.xdg_config.data_dir

    def create_config_dir(self):
        """ Create the configuration directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        os.mkdir(self.config_dir, self.directory_mode)

    def create_data_dir(self):
        """ Create the data directory.

        Uses the permissions given by the directory_mode attribute of this
        object.

        Raises:

            OSError if the directory exists or could not be created.
        """
        os.mkdir(self.data_dir, self.directory_mode)

