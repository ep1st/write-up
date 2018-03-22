# **Hexer**

#### tag : reversing

-----------------------------------------------

#### Description

>An ultimate ninja looks beyond deceptions, are you one?
>
>https://drive.google.com/open?id=1YKteQhwoWsXa4TfZ5DbjeodSgGS8apQm
>
>Author :DreadedLama


-----------------------------------------------

#### Solution

Little-endian bytes. I can guess these bytes mean elf binary.

~~~

$ cat Hexer.txt

7f45 4c46 0201 0100 0000 0000 0000 0000 0300 3e00 0100 0000 8005 0000 0000 0000 4000 0000 0000 0000 5011 0000 0000 0000 0000 0000 4000 3800 0900 4000 1c00 1b00 0600 0000 0500 0000  ...

~~~

I make elf file.

~~~

with open('Hexer.txt', 'r') as a:
	with open('Hexer', 'w') as b:
		b.write((''.join((a.readlines()[0]).split(' ')[:-1])).decode('hex'))

~~~

There is one hash in elf file.

~~~

s = "21133d5763137e11671a7b2655660b790b3e6110731f2c5c306f026a563f51336a0e3a7912661f";

~~~

There is no processing that encrypt or decrypt something in program. But there is algorithm in program at 0x724:

~~~

__int64 __fastcall sub_724(char a1, const char *a2)
{
  ...

  v3 = a1;
  v4 = strlen(a2);
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( i >= v4 )
      break;
    a2[i] ^= v3;
    v3 = (v3 - 1) ^ (a2[i] - 1);
  }
  return result;
}

~~~

Well, I can decrypt the hash by this algorithm.

~~~

cipher = '21133d5763137e11671a7b2655660b790b3e6110731f2c5c306f026a563f51336a0e3a7912661f'.decode('hex')

key = ord('b')

flag = ''

for c in cipher:
	flag += chr(ord(c)^key)
	key = (key-1)^((ord(c)^key)-1)

print '[*] flag :', 'b'+flag[1:]

~~~

~~~

$ python ./Hexer.py
[*] flag : b00t2root{a_s1mpl3_scr1pt_sh0uld_d0_it}

~~~

**b00t2root{a_s1mpl3_scr1pt_sh0uld_d0_it}**
