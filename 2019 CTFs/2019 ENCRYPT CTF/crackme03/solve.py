from pwn import *

context.log_level = 'debug'
r = remote('104.154.106.182', 7777)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

s1 = 'CRACKME02'
s2 = 0xdeadbeef
s3 = 'ZXytUb9fl78evgJy3KJN'
s4 = 1
s5 = [chr(i) for i in [ 127, 127, 127, 127, 105, (201-127), (231-127), (206-127), (213-127)]]

rr(': ')
ss(s1)
rr(': ')
ss(p32(s2))
rr(': ')
ss(s3)
rr(': ')
ss(s4)
rr(': ')
ss(''.join(s5))

r.interactive()
