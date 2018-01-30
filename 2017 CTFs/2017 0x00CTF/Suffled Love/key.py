#!/usr/bin/env python

pinset = [ 3, 7, 1, 1, 7, 3 ]
keyset = [ 1, 2, 1, 3, 2, 5 , 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
password = 0

for i in range(0,6):
	password += int((keyset[((i+3)^6)] * pinset[(i+2)%6] ^ pinset[i])*pow(10,i))

print password
