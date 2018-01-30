#!/usr/bin/env python

keyset = '5A12640444791601'
flag = '0x00CTF{'
password = ''

key = [keyset[i:i+2] for i in range(0, len(keyset), 2)]
key.reverse()

for x,y in enumerate(key):
	password += str(chr(int(ord(flag[x]))^int(y,16)))

print password
