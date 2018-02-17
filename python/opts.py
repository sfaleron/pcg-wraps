import sys

# support for serialization
# does not work for generators with 128 bits of state
GETSET     = True

# must be a valid string
SWIGOPTS   = '-O -Wall'

# relative to the directory with build.py
PCGHEADERS = '../../include'

PYHEADERS  = '/usr/include/python3.6m' if sys.version_info.major==3 else None

# set include directory to a useful default if it evaluates as false
opts = dict(
    INCOMPLETE = 'False' if GETSET else 'True',
    PCGHEADERS = PCGHEADERS,
    PYHEADERS  = PYHEADERS or \
    '/usr/include/python{0}.{1}'.format(*sys.version_info))

