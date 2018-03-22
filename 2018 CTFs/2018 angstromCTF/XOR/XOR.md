# **XOR**

#### tag : crypto

-----------------------------------------------

#### Description

>We found these mysterious symbols hidden in ancient (1950s-era) ruins. We think a single byte may be key to unlocking the mystery. Can you help us figure out what they mean?

-----------------------------------------------

#### Solution

Cipher:

~~~

fbf9eefce1f2f5eaffc5e3f5efc5efe9fffec5fbc5e9f9e8f3eaeee7

~~~

Soltion Script:

~~~

cipher = 'fbf9eefce1f2f5eaffc5e3f5efc5efe9fffec5fbc5e9f9e8f3eaeee7'.decode('hex')

for i in range(0x00,0xff):
	res = ''
	for j in cipher:
		res += chr(i^ord(j))
	if 'actf' in res:
		print '[*] flag :', res

~~~

~~~

$ python ./XOR.py
[*] flag : actf{hope_you_used_a_script}

~~~

**actf{hope_you_used_a_script}**
