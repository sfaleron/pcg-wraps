
swig -c++ -python [SWIGOPTS] -outdir [PCGx] -o pcggen_wrap.cxx [PCGx]/pcgxpy.i

g++ -Wall -O2 -fPIC -std=c++11 -I../[PCGHEADERS] -o pcggen_wrap.o \
    -I[PYHEADERS] -c pcggen_wrap.cxx

g++ -shared pcggen_wrap.o -o [PCGx]/_[PCGx].so
