from . [PCGx] import *

discard_after_use = generator()

info = dict(
    name = '[PCGx]',
    bits = cvar.bits,
    largest = discard_after_use.max(),
    period_pow2 = discard_after_use.period_pow2(),
    streams_pow2 = discard_after_use.streams_pow2(),
    incomplete = [INCOMPLETE]
)

del discard_after_use

__all__ = ('generator', 'info',
    ( 'Almost' if [INCOMPLETE] else '') + 'Random' )
