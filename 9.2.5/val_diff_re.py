#!/usr/bin/env python3
import sys, os

verdict = '<?xml version="1.0"?><result outcome="%s" security="'
verdict += sys.argv[4]
verdict +='"> %s </result>'

IN = []
ANS = []
OUT = []

try:
    ## Line-based checking while ignore leading and trailing white spaces
    ## strip() removes ' ', '\n', '\r'
    IN = [line.strip() for line in open(sys.argv[1],'rt')]
    ANS = [line.strip() for line in open(sys.argv[3],'rt')]
    OUT = [line.strip() for line in open(sys.argv[2],'rt')]
    if len(ANS) != len(OUT): ## must have same number of lines
        raise 
    for ans, out in zip(ANS,OUT):
        if ans != out: ## NOT OK if the lines are different
            raise
    if os.path.exists('EXITCODE.TXT'):
        ## Non-zero exit code always causes No
        raise
    verdict %= ('Yes',)*2
except:
    if not os.path.exists('EXITCODE.TXT'): 
        ## If exit code is zero, then EXITCODE.TXT does not exist.
        verdict %= ('No - Wrong Answer',)*2
    else:
        ## Runtime Error
        ## The exit code is non-zero and the program is not terminated by PC^2
        verdict %= ('No - Run-time Error',)*2

result = open(sys.argv[4],'w')
print(verdict,file=result)
result.close()
