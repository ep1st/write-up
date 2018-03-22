with open('Hexer.txt', 'r') as a:
	with open('Hexer', 'w') as b:
		b.write((''.join((a.readlines()[0]).split(' ')[:-1])).decode('hex'))

cipher = '21133d5763137e11671a7b2655660b790b3e6110731f2c5c306f026a563f51336a0e3a7912661f'.decode('hex')

key = ord('b')

flag = ''

for c in cipher:
	flag += chr(ord(c)^key)
	key = (key-1)^((ord(c)^key)-1)

print '[*] flag :', 'b'+flag[1:]
