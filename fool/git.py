""" Git helper functions and all that jazz.
"""

from __future__ import division
from __future__ import unicode_literals

import distutils.spawn
import subprocess
import os

def which_git():
    """Find the location of the git executable"""
    return distutils.spawn.find_executable('git')
