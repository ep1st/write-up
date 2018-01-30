#!/usr/bin/python
import sys
import hashlib

fix = "0e"

for x in xrange(1000,10000000000):
    #fix += str(hex(x)[2:])
    fix += str(x)
    h = hashlib.md5()
    h.update(fix)
    if(str(h.hexdigest())[:2] == "0e"):
	if(str(h.hexdigest())[2:].isdigit()==True):
	    print fix + " " + h.hexdigest()
	    print "flag is " + fix
	    sys.exit(1)
    fix = fix[:2]
