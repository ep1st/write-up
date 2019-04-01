# subtraction table in .data
t = [7, 04, 03, 01, 04, 06, 03, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 01, 01, 01, 02, 02, 02, 03, 04, 05, 02, 05, 02, 02, 02, 02, 02] 

# encrypted flag in .data
f = 'zyq|Xu3Px~_{Uo}TmfUq2E3piVtJ2nf!}'

# decrypt by subtraction
flag = ''
for i,j in zip(f[:0x1e+1],t):
	flag += chr(ord(i)-j)
print flag + f[0x1e+1:] 
