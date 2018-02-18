
from __future__ import print_function

import os.path as osp
import subprocess
import shutil
import shlex
import sys
import os

from importlib import import_module

sys.path.append('support')
d=osp.abspath(osp.dirname(__file__))
sys.path.append(d)
print(d)

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

        substs['PCGx'] = generator

        substs['SWIGOPTS'] = SWIGOPTS

        if  generator in hasstreams:
            substs['SWIGOPTS'] += ' -DSTREAMS'

        if  GETSET:
            substs['SWIGOPTS'] += ' -DGETSET'

        os.mkdir(generator)

        with open('__init__.py', 'a') as fmain:
            fmain.write("from . import {0}\ngenerators['{0}']={0}\n".format(generator))

        for filename in templates:
            with open(osp.join('../templates', filename), 'r') as fin:
                with open(osp.join(generator, filename), 'w') as fout:
                    s = fin.read()
                    for key, value in substs.items():
                        s = s.replace('[{}]'.format(key), value)

                    fout.write(s)

        print(substs)
        print('\n', generator)

        with open(osp.join(generator, 'make'), 'r') as fmake:
            append = False
            cmds = []

            for line in fmake:
                cmd = line.strip()

                if not cmd:
                    continue

                if append:
                    cmds[-1] += cmd
                else:
                    cmds.append(cmd)

                append = cmd.endswith('\\')

        for cmd in cmds:
            subprocess.check_call(shlex.split(cmd))

        m = import_module('pcgrng.'+generator)

        test.run(m)

        if generator in hasstreams:
            test.run(m, 137)

        for filename in templates:
            if not filename.startswith('__'):
                os.remove(osp.join(generator, filename))

        for filename in ['pcggen_wrap.'+i for i in ('cxx', 'o')]:
            os.remove(filename)
