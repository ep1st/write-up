from UserString import MutableString

key = MutableString('a'*72)

k1 = open('key1').read().split('\n')[:-1]
k2 = open('key2').read().split('\n')[:-1]

for i,j in zip(k1,k2):
	key[int(j)] = chr(int(i))
	
print key
