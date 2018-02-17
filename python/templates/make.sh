
PYVER=[PYVER]
PYCMD=[PYCMD]

mkdir -p [PCGx]

swig -Wall -c++ -python [SWIGOPTS] -outdir [PCGx] -o build/pcggen_wrap.cxx build/pcgxpy.i

mv build/__init__.py [PCGx]

g++ -Wall -O2 -fPIC -std=c++11 -I../../include -o build/pcggen_wrap.o \
    -I/usr/include/python$PYVER -c build/pcggen_wrap.cxx

g++ -shared -lm build/pcggen_wrap.o -o [PCGx]/_[PCGx].so

$PYCMD test.py [PCGx] 137 && find build -type f | xargs rm
