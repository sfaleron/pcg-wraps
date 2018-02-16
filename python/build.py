# hide the ugly stuff!
from subcmd import exthdlr

from opts import *

import sys

# strings of zeros or ones of total length equal to the
# number of generators (12, 18 with 128 bit state generators)
mask = ''.join(sys.argv[1:])

import os.path as osp
import os

templates = os.listdir('templates')

with open('hasstreams.txt', 'r') as f:
    hasstreams = set()
    f.readline()
    for line in f:
        hasstreams.add(line.strip())

os.chdir('build')

with open('../generators.txt', 'r') as fvar:
    masked = False
    i = 0
    for line in fvar:
        generator = line.strip()
        if not generator or generator.startswith('#'):
            continue

        if generator in ('-', '+'):
            masked = (generator == '-')
            continue

        if masked:
            continue

        if not int(mask[i]):
            i += 1
            continue

        opts['PCGx'] = generator
        opts['GETSET'] = 'true' if GETSET else ''
        opts['STREAMS'] = 'true' if STREAMSON and generator in hasstreams else ''

        for filename in templates:
            with open(osp.join('../templates', filename), 'r') as fin:
                with open(filename, 'w') as fout:
                    s = fin.read()
                    for key, value in opts.items():
                        s = s.replace('[{}]'.format(key), value)

                    fout.write(s)

        print('\n', generator)
        os.chdir('..')
        exthdlr(['/bin/sh', 'build/make.sh'])
        os.chdir('build')
        i += 1
