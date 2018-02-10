# **LOL**

#### tag : misc

-----------------------------------------------

#### Description

>>LOL LMAO

>>https://evlzctf.in/files/fa2b38bf9b18b3e8c1bd30ace4765e57/lol

-----------------------------------------------

#### Solution

~~~

$ file lol
lol: ASCII text, with no line terminators

~~~

Well, prob file contain only 0x20 or 0x09. And I can guess they are substitutions from 0 or 1.

~~~

$ xxd lol
00000000: 2009 0920 2009 2009 2009 0909 2009 0920   ..  . . ... ..
00000010: 2009 0920 0909 2020 2009 0909 0920 0920   .. ..   .... .
00000020: 2009 0909 0920 0909 2009 0920 0920 2009   .... .. .. .  .
00000030: 2009 2009 0909 0909 2009 0920 2009 2020   . ..... ..  .  
00000040: 2009 0920 0909 0909 2009 0920 0909 0920   .. .... .. ...
00000050: 2009 0909 2009 2020 2009 2009 0909 0909   ... .   . .....
00000060: 2009 0920 0909 2020 2009 0920 0920 2009   .. ..   .. .  .
00000070: 2009 0920 0920 0909 2009 0920 2009 2009   .. . .. ..  . .
00000080: 2009 2009 0909 0909 2009 0909 2009 0909   . ..... ... ...
00000090: 2009 0909 2009 0909 2009 0920 2009 2009   ... ... ..  . .
000000a0: 2009 0909 0909 2009 2009 0920 2020 0909   ..... . ..   ..
000000b0: 2009 0909 2009 2020 2009 0920 2009 0920   ... .   ..  ..

~~~

So, I attempt to map each 8 bytes to one character.

This is my simple code to get flag:

~~~

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

~~~

~~~

$ python solve.py
evlz{i_dont_like_wwe}ctf

~~~

**evlz{i_dont_like_wwe}ctf**
