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
