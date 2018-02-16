from distutils.core import setup, Extension

pcg64_module = Extension('_pcg64',
    sources=['pcg64_wrap.cxx'],
    include_dirs=['../../../include']
)

setup(
    name='pcg64',
    author='Chris Fuller',
    description="Wrapper of the PGC PRNG C++ library by Melissa O'Neill",
    ext_modules=[pcg64_module],
    py_modules=('pcg64',)
)
