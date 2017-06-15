#!/usr/bin/env python3
import sys, os
from math import fabs

TIME_LIMIT = 10.0 if len(sys.argv)<6 else float(sys.argv[5])
EPS = 5e-7 if len(sys.argv) < 7 else float(sys.argv[6])

verdict = '<?xml version="1.0"?><result outcome="%s" security="'
verdict += sys.argv[4]
verdict +='"> %s </result>'

def far(x,y):
    return fabs(x-y) > EPS and (fabs(y)==0 or fabs(x-y)/fabs(y) > EPS)

def raiseIfInvalid(IN, OUT, ANS):
    if len(ANS) != len(OUT): ## must have same number of lines
        raise 
    for ans, out in zip(ANS,OUT):
        ans, out = ans.split(), out.split()
        if len(ans) != len(out) or any(far(float(x),float(y)) for x, y in zip(ans,out)):
            ## NOT OK
            raise

def isAC():
    try:
        ## Line-based checking while ignore leading and trailing white spaces
        ## strip() removes ' ', '\n', '\r'
        IN = [line.strip() for line in open(sys.argv[1],'rt')]
        ANS = [line.strip() for line in open(sys.argv[3],'rt')]
        OUT = [line.strip() for line in open(sys.argv[2],'rt')]
        raiseIfInvalid(IN,ANS,OUT)
    except:
        return False
    return True

def isOCS():
    if os.path.exists('EXITCODE.TXT'):
        for line in open('EXITCODE.TXT','rt'):
            pass
        return not line == '0x1'
    return False

def isTLE():
    for line in open('SANDBOX_VERDICT','rt'):
        pass
    if line.startswith('Time'):
        return True
    if line.startswith('OK'):
        return float(line.replace('(',' ').split()[1]) > TIME_LIMIT
    return False

def isRE():
    return os.path.exists('EXITCODE.TXT')

if isOCS():
    verdict %= ('No - Other - Contact Staff',)*2
elif isTLE():
    verdict %= ('No - Time Limit Exceeded',)*2
elif isRE():
    verdict %= ('No - Run-time Error',)*2
elif isAC():
    verdict %= ('accepted','Yes')
else:
    verdict %= ('No - Wrong Answer',)*2

result = open(sys.argv[4],'w')
print(verdict,file=result)
result.close()
print(verdict[:-1].split('>')[-1].split('<')[0].strip())
for line in open('SANDBOX_RESULT'):
    print(line.strip())
