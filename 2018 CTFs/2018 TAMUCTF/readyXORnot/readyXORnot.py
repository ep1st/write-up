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
	
		
