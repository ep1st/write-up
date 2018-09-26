# **Xornigma**

#### tag : junior, crypto, xor, guess

-----------------------------------------------

#### Description

>Obtain the file from given file

-----------------------------------------------

#### Solution

I can get python script from link. This script is simple `xor` script. key will be cycled. So, I have to guess `flag_key`. I can have hint from result of xor calculation.

I know flag will be `DCTF{...}` because of flag format. I can find result of xor calculation's first 4 byte are `00000000`. Wow, This mean flag_key's first 4 byte are `DCTF`. And look at index of 4. `'{'(0x7b)` xor `'D'(0x44)` is `0x3f`.

Well, So key will be `DCTFDCTFDCTF...`.

```python

import itertools
def xor_two_str(s, key):
	key = key * (len(s) / len(key) + 1)
	return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in itertools.izip(s, key))

flag = ""
flag_key = ""
x = xor_two_str(flag, flag_key)
print x.encode("hex")
# 000000003f2537257777312725266c24207062777027307574706672217a67747374642577263077777a3725762067747173377326716371272165722122677522746327743e

```

This is solution script. Noting more just reverse script from original code.

```python

import itertools
def xor_two_str(s, key):
	key = key * (len(s) / len(key) + 1)
	return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in itertools.izip(s, key))

enc = '000000003f2537257777312725266c24207062777027307574706672217a67747374642577263077777a3725762067747173377326716371272165722122677522746327743e'.decode('hex')
flag_key = "DCTF"
flag = xor_two_str(enc, flag_key)

print flag

```

**DCTF{fcc34eaae8bd3614dd30324e932770c3ed139cc2c3250c5b277cb14ea33f77a0}**
