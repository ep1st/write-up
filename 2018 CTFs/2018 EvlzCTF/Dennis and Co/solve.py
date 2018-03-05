import base64

res = '*'

with open('result', 'r') as f:
	for line in f.readlines():
		if chr(int(line[2:4],16)) != res[-1]:
			res += chr(int(line[2:4],16))

print base64.b64decode(res[1:])
