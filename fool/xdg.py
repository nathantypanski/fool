""" XDG Base Directory Specification for fools """

from __future__ import division
from __future__ import unicode_literals

import os

import fool.files

class XDGConfig(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            self._home = None
            self._custom_home = False
            self._data_home = None
            self._config_home = None

    @classmethod
    def clear_state(cls):
        """Clear the internal shared state of the directory configuration."""
        cls.__shared_state.clear()

    @property
    def environ(self):
        return os.environ

    @property
    def home(self):
        return self._xdg_env('_home', 'HOME', '')

    @home.setter
    def home(self, value):
        self._home = fool.files.FoolPath(value)
        self._custom_home = True

    @property
    def data_home(self):
        return self._xdg_env('_data_home', 'XDG_DATA_HOME', '.local/share')

    @data_home.setter
    def data_home(self, value):
        self._data_home = fool.files.FoolPath(value)

    @property
    def config_home(self):
        return self._xdg_env('_config_home', 'XDG_CONFIG_HOME', '.config')

    @config_home.setter
    def config_home(self, value):
        self._config_home = fool.files.FoolPath(value)

    def _xdg_env(self, attr, env, default):
        if getattr(self, attr) is not None:
            return getattr(self, attr)
        else:
            if not self._custom_home:
                try:
                    setattr(self, attr, fool.files.FoolPath(self.environ[env]))
                except KeyError:
                    setattr(self, attr, self.home / default)
            else:
                setattr(self, attr, self.home / default)
            return getattr(self, attr)
