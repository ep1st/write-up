import base64

cipher ="""\
011000010110001101110100011001100111101100110000011011100110010101011111011101000111011100110000010111110110011000110000
165 162 137 145 151 147 150 164 137 163 151 170 164 63 63
6e5f7468317274797477305f733178
dHlmMHVyX25vX20wcmV9""".split('\n')

flag = ''

for i in range(0,len(cipher[0]),8):
	flag += chr(int(str(cipher[0])[i:i+8],2))

for i in cipher[1].split(' '):
	flag += chr(int(str(i),8))

flag += cipher[2].decode('hex')

flag += base64.b64decode(cipher[3])

print '[*] flag :', flag
