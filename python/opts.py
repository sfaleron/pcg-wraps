STREAMS   = True
SWIGOPTS  = ''
PYHEADERS = '/usr/include/python3.6m'

import sys

# sets a useful default if evaluates as false
opts = dict(PYHEADERS = PYHEADERS or \
    '/usr/include/python{1}.{2}'.format(
        sys.version_info.major,
        sys.version_info.minor
    )
)
