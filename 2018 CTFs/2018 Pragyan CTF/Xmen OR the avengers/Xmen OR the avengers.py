import base64
import hashlib
from Crypto.Cipher import AES

def genkey():

	enc = open('info_crypt.txt', 'r')
	dec = open('info_clear.txt', 'r')
	key = open('key', 'w')

	data1 = dec.read(1)
	while data1 != '':
		data2 = enc.read(1)
		key.write(chr(ord(data1)^ord(data2)))
		data1 = dec.read(1)

	dec.close()
	enc.close()
	key.close()

def decrypt():

	enc = open('superheroes_group_info_crypt.txt', 'r')
	key = open('key', 'r')

	flag =  AES.new(hashlib.md5(key.readline()[:-1]).hexdigest().encode(), AES.MODE_ECB).decrypt(base64.b64decode(enc.readline()))

	print '[*] flag :', flag

def main():
	genkey()
	decrypt()

main()
