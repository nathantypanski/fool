import os
import os.path

class Path(object):
    """Wrapper around os.path for ease of use."""

    def __init__(self, pathname):
        if isinstance(pathname, Path):
            pathname = pathname.pathname
        self.pathname = pathname

    @property
    def abspath(self):
        return Path(os.path.abspath(self.pathname))

    @property
    def basename(self):
        return Path(os.path.basename(self.pathname))

    @property
    def dirname(self):
        return Path(os.path.dirname(self.pathname))

    @property
    def exists(self):
        return os.path.exists(self.pathname)

    @property
    def lexists(self):
        return os.path.lexists(self.pathname)

    @property
    def expanduser(self):
        return Path(os.path.expanduser(self.pathname))

    @property
    def expandvars(self):
        return Path(os.path.expandvars(self.pathname))

    @property
    def atime(self):
        return os.path.getatime(self.pathname)

    @property
    def mtime(self):
        return os.path.getmtime(self.pathname)

    @property
    def ctime(self):
        return os.path.getctime(self.pathname)

    @property
    def size(self):
        return os.path.getsize(self.pathname)

    @property
    def isabs(self):
        return os.path.isabs(self.pathname)

    @property
    def isfile(self):
        return os.path.isfile(self.pathname)

    @property
    def isdir(self):
        return os.path.isdir(self.pathname)

    @property
    def islink(self):
        return os.path.islink(self.pathname)

    @property
    def ismount(self):
        return os.path.ismount(self.pathname)

    def join(self, *paths):
        return Path(os.path.join(self.pathname, *paths))

    @property
    def normpath(self):
        return Path(os.path.normpath(self.pathname))

    @property
    def realpath(self):
        return Path(os.path.realpath(self.pathname))

    def open(self, *args, **kwargs):
        return open(self.pathname, *args, **kwargs)

    def samefile(self, other):
        return os.path.samefile(self.pathname, other)

    def split(self):
        head, tail = os.path.split(self.pathname)
        return Path(head), Path(tail)

    def splitext(self):
        head, tail = os.path.splitext(self.pathname)
        return head, tail

    def splitunc(self):
        head, tail = os.path.splitunc(self.pathname)
        return Path(head), Path(tail)

    def walk(self, topdown=True, onerror=None, followlinks=False):
        return (Path(path) for path in
                os.walk(self.pathname, topdown, onerror, followlinks))

    def startswith(self, value):
        return self.pathname.startswith(value)

    def endswith(self, value):
        return self.pathname.endswith(value)

    def rfind(self, value):
        return self.pathname.rfind(value)

    def __getitem__(self, value):
        return self.pathname[value]

    def __str__(self):
        return self.pathname

    def __repr__(self):
        return 'Path("{}")'.format(str(self))

    def __add__(self, other):
        return self / other

    def __eq__(self, other):
        if isinstance(other, str):
            return self.pathname == other
        else:
            try:
                return self.pathname == other.pathname
            except AttributeError:
                return False

    def __div__(self, other):
        if isinstance(other, Path):
            return Path(os.path.join(self.pathname, other.pathname))
        else:
            return Path(os.path.join(self.pathname, other))
