
mkdir -p [PCGx]

swig -Wall -c++ -python [SWIGOPTS] -outdir [PCGx] -o build/pcggen_wrap.cxx build/pcgxpy.i

mv build/__init__.py [PCGx]

g++ -Wall -O2 -fPIC -std=c++11 -I../../include -o build/pcggen_wrap.o \
    -I[PYHEADERS] -c build/pcggen_wrap.cxx

g++ -shared build/pcggen_wrap.o -o [PCGx]/_[PCGx].so
