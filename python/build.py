import os.path as osp
import shutil
import sys
import os

from importlib import import_module

sys.path.append('support')
d=osp.abspath(osp.dirname(__file__))
sys.path.append(d)
print(d)

# hide the ugly stuff!
from subcmd import exthdlr

from opts import *
import pcgtests as test

with open(osp.join('support', 'hasstreams.txt'), 'r') as f:
    hasstreams = set()
    f.readline()
    for line in f:
        hasstreams.add(line.strip())


templates = os.listdir('templates')

if osp.exists('pcgrng'):
    shutil.rmtree('pcgrng')

os.mkdir('pcgrng')

with open(osp.join('pcgrng', '__init__.py'), 'w') as fmain:
    fmain.write('generators = {}\n')

os.chdir('pcgrng')

with open('../generators.txt', 'r') as fgens:
    masked = False
    for line in fgens:
        generator = line.strip()
        if not generator or generator.startswith('#'):
            continue

        if generator in ('-', '+'):
            masked = (generator == '-')
            continue

        if masked:
            continue

        opts['PCGx'] = generator

        opts['SWIGOPTS'] = SWIGOPTS

        if  generator in hasstreams:
            opts['SWIGOPTS'] += ' -DSTREAMS'

        if  GETSET:
            opts['SWIGOPTS'] += ' -DGETSET'

        os.mkdir(generator)

        with open('__init__.py', 'a') as fmain:
            fmain.write("from . import {0}\ngenerators['{0}']={0}\n".format(generator))

        for filename in templates:
            with open(osp.join('../templates', filename), 'r') as fin:
                with open(osp.join(generator, filename), 'w') as fout:
                    s = fin.read()
                    for key, value in opts.items():
                        s = s.replace('[{}]'.format(key), value)

                    fout.write(s)

        print(opts)
        print('\n', generator)
        exthdlr(['/bin/sh', osp.join(generator, 'make.sh')])

        m = import_module('pcgrng.'+generator)

        test.run(m)

        if generator in hasstreams:
            test.run(m, 137)

        for filename in templates:
            os.remove(osp.join(generator, filename))

        for filename in ['pcggen_wrap.'+i for i in ('cxx', 'o')]:
            if not filename.startswith('__'):
                os.remove(filename)


