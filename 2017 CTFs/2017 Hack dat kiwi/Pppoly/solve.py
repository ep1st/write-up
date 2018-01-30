import hashlib

solve = ['H','A','I','R','A','S','S']
password = ""

for y,x in enumerate(solve):
    for i in range(0,256):
        if((i+5+y**2)%256 == ord(x)):
	    password += chr(i+46)
	    break
print "passowrd is " + password
h = hashlib.md5()
h.update(password)
print "flag is " + h.hexdigest()
