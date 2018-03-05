# **readyXORnot**

#### tag : crypto

-----------------------------------------------

#### Description

>original data: "El Psy Congroo"
>encrypted data: "IFhiPhZNYi0KWiUcCls="
>encrypted flag: "I3gDKVh1Lh4EVyMDBFo="

>The flag is not in the traditional gigem{flag} format.

-----------------------------------------------

#### Solution

It's simple xor crypto. First, I have to find key of xor encryption by xor-ing original data and encryption data. Then I can find flag by xor-ing encrypted flag and key.

This is solution script:

~~~

import base64

msg = "El Psy Congroo"
enc = "IFhiPhZNYi0KWiUcCls="
flag_enc = "I3gDKVh1Lh4EVyMDBFo="

enc = base64.b64decode(enc)
flag_enc = base64.b64decode(flag_enc)


print len(msg), len(enc), len(flag_enc)

key = ''
for i, j in enumerate(enc):
	key += chr(ord(msg[i]) ^ ord(j))

print key

flag = ''
for i, j in enumerate(flag_enc):
	flag += chr(ord(key[i]) ^ ord(j))

print flag

~~~

~~~

$ python ./readyXORnot.py
14 14 14
e4Bne4Bne4Bne4
FLAG=Alpacaman

~~~

**Alpacaman**
