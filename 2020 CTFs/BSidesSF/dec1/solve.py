import json
import hashlib
import itertools

# prefix = '7b0a202020202266696c656e616d65223a2022'.decode('hex')
# with open('flag.txt.enc', 'r') as f:
#     d = (f.read()).decode('utf-8')
#     x = []
#     for a,b in zip(prefix,d[:len(prefix)]):
#         x.append(chr(ord(a)^ord(b)))
#     print bytearray(x)
# key 'n0t4=l4g'


key = 'n0t4=l4g'
with open('flag.txt.enc', 'r') as f:
    d = (f.read()).decode('utf-8')
    x = []
    for a,b in zip(itertools.cycle(key),d):
        x.append(chr(ord(a)^ord(b)))
    print bytearray(x)
