# **TimeWarp**

#### tag : scripting

-----------------------------------------------

#### Description

>Oh no! A t3mp0ral anoma1y has di5rup7ed the timeline! Y0u'll have to 4nswer the qu3stion5 before we ask them!
>
>nc tw.sunshinectf.org 4101
>
>Author: Mesaj2000

-----------------------------------------------

#### Solution

```python
from pwn import *

context.log_level = 'debug'
rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

# prepare some answer
d = [39, 61, 267]

while True:

	# connect to server
	r = remote('tw.sunshinectf.org', 4101)

	# receive title message
	rr('\n')

	# send answer list to server with last worng answer
	p = '\n'.join(str(i) for i in d) + '\n1000\n'
	ss(p)

	# receive echo answer
	for i in range(0,len(d)*2):
		rr('\n')
	rr('\n')

	# add last correct answer and append to answer list
	d.append(int(rr('\n').split('\n')[0]))

	# check
	print d, len(d)

# sun{derotser_enilemit_1001130519}
```
**sun{derotser_enilemit_1001130519}**
