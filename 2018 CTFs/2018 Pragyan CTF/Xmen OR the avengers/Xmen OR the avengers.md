# **Xmen OR the avengers**

#### tag : crypto

-----------------------------------------------

#### Description

>The legion of doom is expecting an impending attack from a group of superheroes. they are not sure if it is the Xmen OR the avengers. They have received some information from a spy, a zip file containing the following files:

>info_crypt.txt

>info_clear.txt

>superheroes_group_info_crypt.txt

>Help the legion of doom in decrypting the last file so they can prepare themselves and prevent their impending doom.

-----------------------------------------------

#### Solution

Key of xor info_clear.txt and info_crypt.txt is:

~~~

i am a hydra agenT, coverly spying on the superHeroes. I am aware of the group that iS going to aTtack you...but Hydra has had its diffErences with you in the past, so i'm not going to maKe it vEry simple for You ....ecb...aes(I Vouch for this: 12345)...md5(this)...base64...

~~~

From key, I can find superheroes_group_info_crypt is encrypted by base64 and aes-ecb (key is md5(key of xor)). I can decrypt messages to use same way.

This is solution script:

~~~

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

~~~

~~~

$ python Xmen\ OR\ the\ avengers.py
[*] flag : pctf{it's_the_justice_league_DC_for_life_hellya}

~~~

**pctf{it's_the_justice_league_DC_for_life_hellya}**
