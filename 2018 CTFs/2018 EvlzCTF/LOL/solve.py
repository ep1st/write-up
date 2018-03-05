import re

flag = ''
	
with open('lol', 'r') as f:
	data = str(f.read(8)).encode('hex')

	while data != b'':
		data = re.sub('09', '1', data)
		data = re.sub('20', '0', data)
		flag += chr(int(data,2))
		data = str(f.read(8)).encode('hex')

print flag
