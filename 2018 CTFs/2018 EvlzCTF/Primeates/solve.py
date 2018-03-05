from pwn import *

r = remote('35.200.197.38', 8005)

def enc(dec):
	r.recvuntil('>>>')
	r.sendline('1')
	r.recvuntil('number ')
	r.sendline(str(dec))
	return r.recvline()[20:-1]

def dec(enc):
	r.recvuntil('>>>')
	r.sendline('2')
	r.recvuntil('ciphertext ')
	r.sendline(str(enc))
	return r.recvline()[19:-1]

def main():
	n = int(r.recvline()[6:-1])
	e = int(r.recvline()[6:-1])
	c = int(r.recvline()[16:-1])
	
	for i in range(0, 10):
		print 'enc : ', i, enc(i)
		print 'dec : ', i, dec(i)
	
main()

#Enter the password 723233204932732303232804824329562012733423232323723208322321218403
#evlz{my_very_oracle_attack}ctf

