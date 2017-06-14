#!/usr/bin/env python3
import sys, os

verdict = '<?xml version="1.0"?><result outcome="%s" security="'
verdict += sys.argv[4]
verdict +='"> %s </result>'

def isAC():
    try:
        ## Line-based checking while ignore leading and trailing white spaces
        ## strip() removes ' ', '\n', '\r'
        IN = [line.strip() for line in open(sys.argv[1],'rt')]
        ANS = [line.strip() for line in open(sys.argv[3],'rt')]
        OUT = [line.strip() for line in open(sys.argv[2],'rt')]
        if len(ANS) != len(OUT): ## must have same number of lines
            raise 
        if any(ans != out for ans, out in zip(ANS,OUT)):
            ## NOT OK
            raise
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
    try:
        limit = float(sys.argv[5])
    except:
        limit = 10.0
    for line in open('SANDBOX_VERDICT','rt'):
        pass
    if line.startswith('Time'):
        return True
    if line.startswith('OK'):
        return float(line.replace('(',' ').split()[1]) > limit
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
    verdict %= ('Yes',)*2
else:
    verdict %= ('No - Wrong Answer',)*2

result = open(sys.argv[4],'w')
print(verdict,file=result)
result.close()
print(verdict[:-1].split('>')[-1].split('<')[0].strip())
