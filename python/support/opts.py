
with open('opts.cfg', 'r') as f:
    exec(f.read())

if not PYHEADERS:
    try:
        import sysconfig
        PYHEADERS = sysconfig.get_path('include')
    except ImportError:
        import sys
        PYHEADERS = '/usr/include/python{0}.{1}'.format(*sys.version_info)

# set include directory to a useful default if it evaluates as false
substs = dict(
    INCOMPLETE = 'False' if GETSET else 'True',
    SWIG = SWIG, CXX = CXX, CXXOPTS = CXXOPTS,
    PCGHEADERS = PCGHEADERS,
    PYHEADERS  = PYHEADERS)
