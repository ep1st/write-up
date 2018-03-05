# **Counter**

#### tag : crypto

-----------------------------------------------

#### Description

>>nc 35.200.197.38 8004

>>Europe: nc 35.231.8.67 8004

-----------------------------------------------

#### Solution

~~~

$ nc 35.200.197.38 8004
Here is your ciphertext:d81718505048f6db3bee023f225ee5f13644b17bc0e25b2be772b48ea7921d85b54eca04058549bc107a91a7f5
1:I like it
2:I don't like it
>>>

~~~

This prob is simple xor encryption too, but I have to get key to solve it. To get key, I use xor 'A' with all elements of cipher.

~~~

from pwn import *

r = remote('35.200.197.38', 8004)

cipher = 'd81718505048f6db3bee023f225ee5f13644b17bc0e25b2be772b48ea7921d85b54eca04058549bc107a91a7f5'
#key = 'dc00154b4a50f8cf05eb0a3a1c51ebe4084bb57fc5dc4e25d97eb484a3ac088cbd5cf40d059458b81f6693b2f2'


def confirm(plain):
	r.sendline('1')
	r.recvuntil('plaintext:')
	r.sendline(plain)
	r.recv(256)

def change(a,b):
	r.recvuntil('>>>')
	r.sendline('2')
	r.recvuntil('honey:')
	r.sendline(a)
	r.recvuntil('to?')
	r.sendline(b)

def genkey():
	key = ''
	for i in range(0, len(cipher)/2):
		change(str(i+1),'a')
	r.recvuntil('ciphertext:')
	key = str(r.recv(90))
	return key

def main():
	flag = ''
	for i, j in zip(cipher.decode('hex'), genkey().decode('hex')):
		flag += chr(ord(i) ^ ord(j) ^ ord('a'))
	print flag

main()

~~~

~~~

$ python ./solve.py
[+] Opening connection to 35.200.197.38 on port 8004: Done
evlz{you_did_not_need_to_make_this_happen}ctf
[*] Closed connection to 35.200.197.38 port 8004

~~~

**evlz{you_did_not_need_to_make_this_happen}ctf**
