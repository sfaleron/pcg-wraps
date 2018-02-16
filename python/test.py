from __future__ import print_function

from importlib import import_module
import pickle
import sys
import os

from opts import GETSET

def add_stream(f):
    def g(*args):
        args = args+((int(sys.argv[2]),) if len(sys.argv)==3 else ())
        print(args)
        return f(*args)

    return g

def run(pcg):
    m = import_module(pcg)
    constructor = getattr(m, 'generator')

    if GETSET:
        print(m)

    # seeding at or after instantiation
    rng1 = add_stream(constructor)(42)
    rng2 = add_stream(constructor)()
    print(rng1==rng2, rng1!=rng2)
    add_stream(rng2.seed)(42)
    print(rng1==rng2, rng1!=rng2)

    # copy constructor
    rng3 = add_stream(constructor)(rng2)
    print(rng2==rng3); rng3.discard(1)
    print(rng2==rng3, rng2!=rng3)

    # generatotr characteristics
    print('bits:', rng1.bits)
    print('range:', rng1.min(), rng2.max())
    print('base-two logarithm of period:', rng1.period_pow2())
    print('base-two logarithm of stream count:', rng1.streams_pow2())

    # get some random ints or floats, compare
    print(rng1.next_as_float(), rng2())
    print(rng2==rng2, rng1!=rng2)

    rng1.backstep(1); rng2.backstep(1)

    print(rng1(), rng2.next_as_float())
    print(rng2==rng2, rng1!=rng2)

    print(rng1(1000), rng2(1000))
    print(rng2==rng2, rng1!=rng2)

    # subtract returns how much to advance rhs.. so is that equal
    # to backtracking lhs? note that these take unsighned arguments!
    print('period:', 2**rng1.period_pow2())

    add_stream(rng2.seed)(42)
    one2 = rng1-rng2
    two1 = rng2-rng1
    print(one2, two1)

    if GETSET:
        rng3 = add_stream(constructor)(rng1)
    else:
        state = rng1.get_state()

    rng2.advance(one2)
    print(rng1==rng2, rng1!=rng2)

    add_stream(rng2.seed)(42)

    if GETSET:
        rng1 = rng3
    else:
        rng1.set_state(state)

    one2 = rng1-rng2
    two1 = rng2-rng1
    print(one2, two1)

    rng1.backstep(two1)
    print(rng1==rng2, rng1!=rng2)

if __name__ == '__main__':
    run(sys.argv[1])
