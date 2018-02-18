import sys

PY3 = sys.version_info[0] >= 3

with open('opts.cfg', 'r') as f:
    exec(f.read())

# set include directory to a useful default if it evaluates as false
substs = dict(
    INCOMPLETE = 'False' if GETSET else 'True',
    SWIGCMD = SWIGCMD, CXX = CXX,
    PCGHEADERS = PCGHEADERS,
    PYHEADERS  = PYHEADERS or \
    '/usr/include/python{0}.{1}'.format(*sys.version_info))
