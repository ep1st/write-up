t = '08030e1f141d192e'.decode('hex')
t += '392b162c010a021f'.decode('hex')
t += '041905001e400302'.decode('hex')
t += '1940080c'.decode('hex')
t += '1e14'.decode('hex')
t += '10'.decode('hex')

for i in range(0, 256):
	flag = ''
	for j in t:
		flag += chr(ord(j) ^ i)
	if 'enc' in flag:
		print flag
