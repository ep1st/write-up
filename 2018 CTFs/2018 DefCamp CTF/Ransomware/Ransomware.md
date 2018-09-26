# **Ransomware**

#### tag : reversing, xor, pdf, guess

-----------------------------------------------

#### Description

>Someone encrypted my homework with this rude script. HELP!
>
>Author: Lucian Nitescu

-----------------------------------------------

#### Solution

Ok, I can get `ransomeware.pyc` and `youfoo!.exe` from link. I can find `youfoo!.exe` is not exe file. So, I trying to decompile pyc to py. I use `decompyle6` to decompile pyc code. Then, I can get this below script.

Ok, It make me crazy... There is no way to recover xor-key from ordinary way. So I have to guess one by one from pdf file made. (I have to get hint from pdf header, guessable string, guessable format guessable whatever)

```python

# uncompyle6 version 3.2.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Dec  4 2017, 14:50:18)
# [GCC 5.4.0 20160609]
# Embedded file name: ransomware.py
# Compiled at: 2018-09-04 06:35:11
import string
from random import *
import itertools

def caesar_cipher(buf, pw):
    pw = pw * (len(buf) / len(pw) + 1)
    return ('').join((chr(ord(var1) ^ ord(var2)) for var1, var2 in itertools.izip(buf, pw)))


f = open('./FlagDCTF.pdf', 'r')
buf = f.read()
f.close()
allchar = string.ascii_letters + string.punctuation + string.digits
password = ('').join((choice(allchar) for var3 in range(randint(60, 60))))
buf = caesar_cipher(buf, password)
f = open('./youfool!.exe', 'w')
buf = f.write(buf)
f.close()
# okay decompiling /home/epist/CTF/reversing/ransomware/ransomware.pyc

```

It's very sucking script. But it recover pdf file correctly.

```python

import string
import itertools

def caesar_cipher(buf, pw):
    pw = pw * (len(buf) / len(pw) + 1)
    return ('').join((chr(ord(var1) ^ ord(var2)) for var1, var2 in itertools.izip(buf, pw)))

f = open('reversing/ransomware/youfool!.exe', 'r').read()

allchar = string.ascii_letters + string.punctuation + string.digits

password = ''
for i,j in zip(f[:7], '%PDF-1.'):
    password += chr(ord(i) ^ ord(j))

password += chr(0x47 ^ ord('e'))
password += chr(0x3b ^ ord('b'))
password += chr(0x5b ^ ord('j'))
password += chr(0x3f ^ ord('t'))
password += chr(0x4c ^ ord('h'))
password += chr(0x3a ^ ord('a'))
password += chr(0x3f ^ ord('g'))
password += chr(0x4c ^ ord('e'))
password += chr(0x07 ^ ord('a'))
password += chr(0x0a ^ ord('m'))
password += chr(0x31 ^ ord('j'))
password += chr(0x1d ^ ord('a'))
password += chr(0x5a ^ ord('x'))
password += chr(0x5a ^ ord('t'))
password += chr(0x4c ^ ord('x'))
password += chr(0x50 ^ ord('e'))
password += chr(0x2b ^ ord('r'))
password += chr(0x1e ^ ord('o'))
password += chr(0x5d ^ ord('d'))
password += chr(0x0c ^ ord('e'))
password += chr(0x51 ^ ord('o'))
password += chr(0x01 ^ ord('d'))
password += chr(0x33 ^ ord('e'))
password += chr(0x41 ^ ord('h'))
password += chr(0x59 ^ ord('e'))
password += chr(0x42 ^ ord('r'))
password += chr(0x22 ^ ord('a'))
password += chr(0x5d ^ ord('g'))
password += chr(0x4d ^ ord('e'))

for i,j in zip('\x16\x17\x07\x0A\x60\x6E\x5C\x21\x52\x4A\x76\x07', '1f3d054f6e3b'):
    password += chr(ord(i) ^ ord(j))

password += '\x00' * (60 -len(password)-12 )

password += chr(0x1d ^ ord('E'))
password += chr(0x4e ^ ord('e'))
password += chr(0x2b ^ ord('n'))
password += chr(0x53 ^ ord('d'))
password += chr(0x5f ^ ord('s'))
password += chr(0x46 ^ ord('t'))
password += chr(0x3d ^ ord('r'))
password += chr(0x61 ^ ord('C'))
password += chr(0x44 ^ ord('o'))
password += chr(0x54 ^ ord('n'))
password += chr(0x2f ^ ord('t'))
password += chr(0x41 ^ ord('s'))

print len(password)
print password

data = caesar_cipher(f, password)

r = open('./FlagDCTF.pdf', 'w')
r.write(data)
r.close()

```

**DCTF{d915b5e076215c3efb92e5844ac20d0620d19b15d427e207fae6a3b894f91333}**
