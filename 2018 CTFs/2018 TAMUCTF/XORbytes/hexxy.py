key = 'QB1g3l4B5uzPjjD4'

f1 = open('hexxy', 'rb')
f2 = open('hexyy', 'wb')

enc = f1.read(16)

while enc != ''	:
	for i, j  in zip(enc,key):
		f2.write(chr(ord(i) ^ ord(j)))
	enc = f1.read(16)
			
f1.close()
f2.close()
