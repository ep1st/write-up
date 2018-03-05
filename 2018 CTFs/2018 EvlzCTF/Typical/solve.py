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
