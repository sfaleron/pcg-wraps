
PYVER=[PYVER]
PYCMD=[PYCMD]

GETSET=[GETSET]
STREAMS=[STREAMS]

SWIGOPTS=

if [ -z $GETSET ]; then
  SWIGOPTS="$SWIGOPTS -DGETSET"
fi

if [ -z $STREAMS ]; then
  SWIGOPTS="$SWIGOPTS -DSTREAMS"
fi

mkdir -p [PCGx]

swig -Wall -c++ -python $SWIGOPTS -outdir [PCGx] -o build/pcgvar_wrap.cxx build/pcgxpy.i

#mv [PCGx]/[PCGx].py [PCGx]/__init__.py
mv build/__init__.py [PCGx]

g++ -Wall -O2 -fPIC -std=c++11 -I../../include -o build/pcgvar_wrap.o \
    -I/usr/include/python$PYVER -c build/pcgvar_wrap.cxx

g++ -shared -lm build/pcgvar_wrap.o -o [PCGx]/_[PCGx].so

if [ -z $STREAMS ]; then
  $PYCMD test.py [PCGx]     && find build -type f | xargs rm
else
  $PYCMD test.py [PCGx]
  $PYCMD test.py [PCGx] 137 && find build -type f | xargs rm
fi

