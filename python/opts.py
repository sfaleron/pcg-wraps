import sys

GETSET    = True
STREAMS   = True
SWIGOPTS  = ''
PYHEADERS = '/usr/include/python3.6m' if sys.version_info.major==3 else None

import sys

# sets a useful default if evaluates as false
opts = dict(PYHEADERS = PYHEADERS or \
    '/usr/include/python{0}.{1}'.format(*sys.version_info))
