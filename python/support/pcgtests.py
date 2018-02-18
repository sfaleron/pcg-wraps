from __future__ import print_function

import pickle

from opts import GETSET

def run(*args):
    m = args[0]
    print(m.info)
    constructor = m.generator

    args = (42,)+args[1:]

    # seeding at or after instantiation
    rng1 = constructor(*args)
    rng2 = constructor()
    print(rng1==rng2, rng2==rng1)
    rng2.seed(*args)
    print(rng1==rng2, rng2==rng1)

    if GETSET:
        print(rng2)

    # copy constructor
    rng3 = constructor(rng2)
    print(rng2==rng3); rng3.discard(1)
    print(rng2==rng3, rng3==rng2)

    # generator characteristics
    print('bits:', rng1.bits)
    print('range:', rng1.min(), rng2.max())
    print('base-two logarithm of period:', rng1.period_pow2())
    print('base-two logarithm of stream count:', rng1.streams_pow2())

    # get some random ints or floats, compare
    print(rng1.next_as_float(), rng2())
    print(rng2==rng2, rng1==rng2)

    rng1.backstep(1); rng2.backstep(1)

    print(rng1(), rng2.next_as_float())
    print(rng2==rng2, rng2==rng1)

    print(rng1(1000), rng2(1000))
    print(rng2==rng2, rng2==rng1)

    # subtract returns how much to advance rhs.. so is that equal
    # to backtracking lhs? note that these take unsigned arguments!

    rng2.seed(*args)
    one2 = rng1-rng2
    two1 = rng2-rng1
    period = 2**rng1.period_pow2()

    print(one2,two1,period)

    if GETSET:
        state = rng1.get_state()
    else:
        rng3 = constructor(rng1)

    rng2.advance(one2)
    print(rng1==rng2, rng2==rng1)

    rng2.seed(*args)

    if GETSET:
        rng1.set_state(state)
    else:
        rng1 = rng3

    one2 = rng1-rng2
    two1 = rng2-rng1
    print(one2, two1)

    #if 
    #    rng1.backstep(period-two1)
    #    print(rng1==rng2, rng2==rng1)
    #except OverflowError:
    #    print('period overflows C type')
