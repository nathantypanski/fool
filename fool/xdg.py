""" XDG Base Directory Specification for fools """

import os

class XDGConfig(object):
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            self._home = None
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
        self._home = value

    @property
    def data_home(self):
        return self._xdg_env('_data_home', 'XDG_DATA_HOME', '/.local/share')

    @data_home.setter
    def data_home(self, value):
        self._data_home = value

    @property
    def config_home(self):
        return self._xdg_env('_config_home', 'XDG_CONFIG_HOME', '/.config')

    @config_home.setter
    def config_home(self, value):
        self._config_home = value

    def _xdg_env(self, attr, env, default):
        if getattr(self, attr) is not None:
            return getattr(self, attr)
        else:
            try:
                setattr(self, attr, self.environ[env])
            except KeyError:
                setattr(self, attr, self.home + default)
            return getattr(self, attr)
