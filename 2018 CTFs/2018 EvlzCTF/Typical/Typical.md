# **Typical**

#### tag : crypto

-----------------------------------------------

#### Description

>>Easy and Peasy

>>nc 35.200.197.38 8003

>>Europe: nc 35.231.8.67 8003

-----------------------------------------------

#### Solution

~~~

$ nc 35.200.197.38 8003
Your Ciphertext is:3e1614393b04041217000b151e051c Your key is:465259735a7741
Enter plaintext in hex:

~~~

It's simple xor encryption. But ciphertext is given randomly. So I make simple brute force code to get flag.

~~~

from pwn import *
from itertools import cycle

r = remote('35.200.197.38', 8003)

def getCipher():
	r.recvuntil('Ciphertext is:')
	return r.recvuntil(' ')

def getSession():
	r.recvuntil('key is:')
	return r.recvuntil('\n')

def run(cipher, key):
	plain = ''
	for i, j in zip(cycle(key), cipher):
		plain += chr(ord(i) ^ ord(j))

	print '[*] plain', plain

	r.recvuntil('hex:')
	r.sendline(plain.encode('hex'))

def main():

	for i in range(0,255):
		run(getCipher()[:-1].decode('hex'), getSession()[:-1].decode('hex'))

main()

~~~

~~~

$ python ./solve.py
[+] Opening connection to 35.200.197.38 on port 8003: Done
[*] plain VfAIyGgJKTV
[*] plain DQAkwcuIxYiQhK
[*] plain uXWNOAhceL
[*] plain xvgkLtAuhtG
[*] plain evlz{placed_somewhere_random}ctf
[*] plain XbwpKdNYSESU
[*] plain EZBhjsvhkMksYhZ
[*] plain DJjUkUDOWZdaoL
[*] plain cWflDpwbnV
[*] plain dUgdNQYBIb
[*] plain YHPKuQVXaM
[*] plain mUHOfhbVuS
[*] plain neFwludJVvrP
[*] plain cVGHlJWpmXmQdNq
[*] plain SInjGBSnoteTCY
[*] plain lkkxtZrZVvjQpH
[*] plain VmyHMFSywJ
[*] plain nUXKlSKSRNFII
...

~~~

**evlz{placed_somewhere_random}ctf**
