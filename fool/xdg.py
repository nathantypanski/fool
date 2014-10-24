""" XDG Base Directory Specification for fools """

import os

class XDG(object):
    def __init__(self):
        self._home = None
        self._data_home = None
        self._config_home = None

    @property
    def environ(self):
        return os.environ

    @property
    def home(self):
        return self.environ['HOME']

    def _xdg_env(self, attr, env, default):
        if getattr(self, attr) is not None:
            return getattr(self, attr)
        else:
            try:
                setattr(self, attr, self.environ['XDG_DATA_HOME'])
            except KeyError:
                setattr(self, attr, self.home + default)
            return getattr(self, attr)

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

class XDGConfig(object):
    def __init__(self, xdg=None):
        if xdg is None:
            xdg = XDG()
        self.xdg = xdg
        self._config_name = 'fool'
        self._data_name = 'fool'

    @property
    def home_dir(self):
        return self.xdg.config_home

    @property
    def config_dir(self):
        return self.xdg.config_home + '/' + self._config_name

    @property
    def data_dir(self):
        return self.xdg.data_home + '/' + self._data_name
