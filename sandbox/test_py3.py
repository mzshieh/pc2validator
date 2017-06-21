#!/usr/bin/env python3
import os, sys
from os import fork

BOX = 500
try:
    BOX = int(sys.argv[1])
    sys.argv.pop(1)
    if BOX > 1000:
        BOX = 1000
except:
    pass

for i in range(BOX):
    os.mkdir('r{:03d}'.format(i))
    pid = fork()
    if pid == 0:
        os.chdir('r{:03d}'.format(i))
        os.system('cp ../{} .'.format(sys.argv[1]))
        os.system('cp ../{} .'.format(sys.argv[2]))
        os.system('ioibox -b={} python3 {} < {} > SANDBOX_OUTPUT'
                  .format(i,sys.argv[1],sys.argv[2]))
        break
