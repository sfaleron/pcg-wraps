
%module [PCGx]

%include <stdint.i>

%typemap(in) [PCGx]::state_type {
  $1 = PyLong_AsUnsignedLongLong($input);
}

%typemap(in) [PCGx]::result_type {
  $1 = PyLong_AsUnsignedLongLong($input);
}

%typemap(out) [PCGx]::state_type {
  $result = PyLong_FromUnsignedLongLong($1);
}

%typemap(out) [PCGx]::result_type {
  $result = PyLong_FromUnsignedLongLong($1);
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_INTEGER) [PCGx]::state_type {
  $1 = (PyInt_Check($input) || PyLong_Check($input)) ? 1 : 0;
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_INTEGER) [PCGx]::state_type {
  $1 = (PyInt_Check($input) || PyLong_Check($input)) ? 1 : 0;
}

%begin %{
#define SWIG_PYTHON_STRICT_BYTE_CHAR
%}

%typemap(out) std::string {
%#if PY_MAJOR_VERSION >= 3
    $result = PyBytes_FromString($1.c_str());
%#else
    $result = PyString_FromString($1.c_str());
%#endif
}

%pythonbegin %{
import sys
%}

%header %{

#include <iostream>
#include <sstream>
#include <climits>
#include <string>

#include "pcg_random.hpp"

%}

%inline %{
    size_t bits = sizeof([PCGx]::result_type) * CHAR_BIT;
%}

%rename("generator") [PCGx];

class [PCGx] {
    public:
        [PCGx]();
        [PCGx]([PCGx]::state_type seed);
#ifdef STREAMS
        [PCGx]([PCGx]::state_type seed, [PCGx]::state_type stream);
#endif
        [PCGx](const [PCGx]& orig);
        void seed();
        void seed([PCGx]::state_type seed);
#ifdef STREAMS
        void seed([PCGx]::state_type seed, [PCGx]::state_type stream);
#endif

        void discard([PCGx]::state_type n);

        // "extra"

        size_t period_pow2();
#ifdef STREAMS
        void set_stream([PCGx]::state_type stream);
        size_t streams_pow2();
#endif
        bool wrapped();
        void advance([PCGx]::state_type delta);
        void backstep([PCGx]::state_type delta);
%extend {
#ifndef STREAMS
        size_t streams_pow2() { return 0; }
#endif
        // preserve the API and maximum SWIG warning level,
        // but also stay clean of warnings..
        // sneaky tricks to the rescue!

        [PCGx]::result_type _min() { return self->min(); }
        [PCGx]::result_type _max() { return self->max(); }

        [PCGx]::result_type _call_bare()
            { return $self->operator()(); }

        [PCGx]::result_type _call_arg([PCGx]::result_type upper_bound)
            { return $self->operator()(upper_bound); }

        double next_as_float()
            // The suggested ldexp() approach does not compile for
            // the pcg128 variants
            { return ((double) $self->operator()()) / $self->max(); }
}

%pythoncode %{
        def __call__(self, arg=None):
            return self._call_bare() if arg is None else self._call_arg(arg)

        def __sub__(self, other):
            return subtract(self, other)

        def min(self):
            return self._min()

        def max(self):
            return self._max()

        @property
        def bits(self):
            return cvar.bits

        def __eq__(self, other):
            return test_equality(self, other)

        def __ne__(self, other):
            return test_inequality(self, other)
%}

#ifdef GETSET
%pythoncode %{
        def __str__(self):
            bytes = get_state(self)
            if sys.version_info[0]==2:
                bytes = map(ord, bytes)

            return ''.join(['%02x' % (i,) for i in bytes])

        def get_state(self):
            return get_state(self)

        def set_state(self, state):
            set_state(self, state)

        # For pickle/unpickle
        #

        def __getstate__(self):
            return self.get_state()

        def __setstate__(self, state):
            self.__init__()
            self.set_state(state)
%}
#endif
};

#ifdef GETSET
%inline %{

template <typename T>
std::string get_state(const T& rng)
{
    std::ostringstream os;
    os << rng;
    return os.str();
}

template <typename T>
void set_state(T& rng, const char *state)
{
    std::istringstream is(state);
    is >> rng;
    return;
}

%}

%template(get_state) get_state<[PCGx]>;
%template(set_state) set_state<[PCGx]>;
#endif

// operator overloading at module/global level does not translate to python
// also, the new names are only visible in the Python code
%rename("test_equality") operator==;
bool operator==(const [PCGx]& lhs, const [PCGx]& rhs);

%rename("test_inequality") operator!=;
bool operator!=(const [PCGx]& lhs, const [PCGx]& rhs);

%rename("subtract") operator-;
[PCGx]::state_type operator-(const [PCGx]& lhs, const [PCGx]& rhs);

#ifdef GETSET
%pythoncode %{
import random

class Random(random.Random):
    def __init__(self, *args):
        self._rng = [PCGx](*args)

    def seed(self, *args):
        self._rng.seed(*args)

    #def getrandbits(self):
    #    pass

    def random(self):
        return self._rng.next_as_float()

    def getstate(self):
        return self._rng.get_state()

    def setstate(self, state):
        return self._rng.set_state(state)
%}
#else
%pythoncode %{
import random

class AlmostRandom(random.Random):
    def __init__(self, *args):
        self._rng = [PCGx](*args)

    def seed(self, *args):
        self._rng.seed(*args)

    #def getrandbits(self):
    #    pass

    def random(self):
        return self._rng.next_as_float()
%}
#endif
