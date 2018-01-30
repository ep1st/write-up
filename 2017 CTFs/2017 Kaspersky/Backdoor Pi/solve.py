import sys
import os
import time
import hashlib

user = "b4ckd00r_us3r"

def check_creds(user, pincode):
    if len(pincode) <= 8 and pincode.isdigit():
        val = '{}:{}'.format(user, pincode)
        key = hashlib.sha256(val).hexdigest()
        if key == '34c05015de48ef10309963543b4a347b5d3d20bbe2ed462cf226b1cc8fff222e':
            return 'Congr4ts, you found the b@ckd00r. The fl4g is simply : {}:{}'.format(user, pincode)
	return -1

for x in range(100000000):
    pincode = str(x)
    if(check_creds(user, pincode) != -1):
        print check_creds(user, pincode)
	break;
