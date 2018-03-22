# **Flags**

#### tag : reversing

-----------------------------------------------

#### Description

>Flags everywhere, which one do you want?
>
>https://drive.google.com/open?id=1onuCTmkzJhN8s8wvbioB0fEx70hVYEQ8
>
>Author :DreadedLama

-----------------------------------------------

#### Solution

~~~

$ binwalk Flags.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
51934         0xCADE          ELF, 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)

~~~

~~~

$ dd if=Flags.jpg of=Flags bs=1 skip=51934
10320+0 records in
10320+0 records out
10320 bytes (10 kB, 10 KiB) copied, 0.0184781 s, 559 kB/s

$ file Flags
Flags: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=c36046431a5abeeeab8e26b07645a00dc82cfcc2, stripped

~~~

~~~

qword_202060[0] = (__int64)sub_745;
qword_202068 = (__int64)sub_6A0;
qword_202070 = (__int64)sub_7F5;
qword_202078 = (__int64)sub_7BE;
qword_202080 = (__int64)sub_6AB;

...

qword_202188 = (__int64)sub_816;
qword_202190 = (__int64)sub_787;
qword_202198 = (__int64)sub_82C;
qword_2021A0 = (__int64)sub_6E2;
puts("The flag is");
for ( i = 0; i <= 40; ++i )
{
  if ( i != 33 )
    v3 = (char)((int (*)(void))qword_202060[i])();
}

~~~

~~~

import re

flag = ''

seq = ('745,6A0,7F5,7BE,6AB,837,6C1,75B,695,6CC,6D7,766,6ED,6B6,821,68A,703,72F,800,73A,724,7D4,771,77C,6F8,842,750,792,79D,7A8,70E,7B3,7C9,7DF,7EA,719,80B,816,787,82C,6E2').lower().split(',')

with open('table', 'r') as f:
	table = ''.join(f.readlines())

	for idx in seq:
		res = table.find('$', table.find(str(idx)))
		flag += chr(int(table[res+3:res+5],16))

print '[*] flag :', flag[:33]+flag[34:]

~~~

~~~

$ python Flags.py
[*] flag : b00t2root{4_s1mpl3_r3turned_v4lu3_fl4g!}

~~~

**b00t2root{4_s1mpl3_r3turned_v4lu3_fl4g!}**
