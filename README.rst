
Various `SWIG`_ bindings to the `PCG`_ suite of psuedo-random number generators. Not all features are necessarily available in a give set of bindings, and the available subset will vary from language to language. See the READMEs in each subdirectory for details.

Python bindings can be found here, and Java support is planned.

To build, you'll need the contents of the include directory from `pcg-cpp`_. The repository includes a reference back there as a submodule, so if you've cloned this repository, you can get that folded in neatly with a couple of git commands:

::
  git submodule init
  git submodule update

This makes it easier to stay up-to-date with pgc-cpp, and also provides some data that could be useful for automated testing, when that gets implemented.

.. _PCG: http://www.pcg-random.org/
.. _SWIG: http://www.swig.org/
.. _pcg-cpp: https://github.com/imneme/pcg-cpp
