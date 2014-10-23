""" Git helper functions and all that jazz.
"""

import distutils.spawn
import subprocess
import os

def which_git():
    return distutils.spawn.find_executable('git')
