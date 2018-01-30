f1 = open('./table.txt','r')
f2 = open('./result.txt','w')

xor = "010011100"

lines = f1.readlines()
for line in lines:
    f2.write(str(bin(int(line,2)^int(xor,2)))[2:]+'\n')

