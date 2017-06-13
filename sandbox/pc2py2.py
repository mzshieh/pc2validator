#!/usr/bin/env python3

import sys, os
from random import randint as ri
from subprocess import run

## initialize the filenames

INIT_LOG = 'SANDBOX_INIT.log'
BOX_PATH_FILENAME = 'SANDBOX_PATH_FILENAME'
RESULT_FILE = 'SANDBOX_RESULT'
USR_OUTPUT = 'SANDBOX_OUTPUT_%016X'%ri(0,2**64-1)
USR_ERROR = 'SANDBOX_ERROR_%016X'%ri(0,2**64-1)
TEST_INPUT = 'SANDBOX_INPUT_%016X'%ri(0,2**64-1)

## parameters

TIME_LIMIT = 10
SPACE_LIMIT = 1024
MEM_LIMIT = 512*1024

## consume the input

test_input = open(TEST_INPUT,'wt')
for line in sys.stdin:
    print(line,end='',file=test_input)
test_input.close()

## Setup the parameters for isolate
isolate = ['isolate','--cg']
time_limit = ['--time={}'.format(TIME_LIMIT),'--wall-time={}'.format(2*TIME_LIMIT),'--extra-time=5']
space_limit = ['--fsize={}'.format(SPACE_LIMIT)]
mem_limit = ['--cg-mem={}'.format(MEM_LIMIT),'--mem={}'.format(MEM_LIMIT)]
proc_limit = ['--processes=4']
limit = proc_limit + time_limit + space_limit + mem_limit
io = ['--stdin='+TEST_INPUT,'--stdout='+USR_OUTPUT,'--stderr='+USR_ERROR]
run_env = ['-e','--run','/usr/bin/env','--']
python = ['python2']

## clean up
null = open('/dev/null','w')
cleanup = isolate + ['--cleanup']
while run(cleanup,stderr=null).returncode==0:
    pass
null.close()

## init
init_log = open(INIT_LOG,'wt')
box_path_file = open(BOX_PATH_FILENAME,'wt')
init = isolate + ['--init']
init_proc = run(init,stdout=box_path_file)
print('init return code: {}'.format(init_proc.returncode),file=init_log)
box_path_file.close()
init_log.close()

# fail to run: 255
exitcode = 255
result = open(RESULT_FILE, 'wt')
if init_proc.returncode:
    print('Initialization failed',file=result)
elif len(sys.argv)<2:
    print('Missing source code',file=result)
else:
    ## if initialization is sucessful, run the program
    for box_path in open(BOX_PATH_FILENAME,'rt'):
        pass
    box_path = box_path[:-1] + '/box'
    os.system('cp {} {}'.format(sys.argv[1],box_path))
    os.system('mv {} {}'.format(TEST_INPUT,box_path))
    run_code = isolate+limit+io+run_env+python+sys.argv[1:]
    exitcode = run(run_code,stderr=result).returncode
    run(['/usr/bin/env','head','--bytes={}'.format(1024*SPACE_LIMIT),box_path+'/'+USR_OUTPUT])
result.close()
sys.exit(exitcode)
