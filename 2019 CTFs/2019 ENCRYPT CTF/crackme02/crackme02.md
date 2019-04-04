# **crackme02**

#### tag : rev

-----------------------------------------------

#### Description

>quack me!
>
>author: Robyn12

-----------------------------------------------

#### Solution

This is main code. `buf` for username and `v7` for pass will be caluated by xor. And `v4` is accumulation of `v9` with index subtraction.

```c
  puts("Hey give username");
  read(0, buf, 8uLL);
  puts("Give pass:");
  read(0, v7, 8uLL);
  for ( i = 0; i <= 8; ++i )
    v9[i] = buf[i] ^ v7[i];
  for ( j = 0; j <= 8; ++j )
    v4 += v9[j] - 4 * j;
  sub_73A(v4);
```

This is `sub_73a`. `a1` is `v4` in main. In this case, I use bruteforce `a1` whatever.

```c
_int64 __fastcall sub_73A(int a1)
{
  signed int i; // [rsp+1Ch] [rbp-34h]
  __int64 v3; // [rsp+20h] [rbp-30h]
  __int64 v4; // [rsp+28h] [rbp-28h]
  __int64 v5; // [rsp+30h] [rbp-20h]
  int v6; // [rsp+38h] [rbp-18h]
  __int16 v7; // [rsp+3Ch] [rbp-14h]
  char v8; // [rsp+3Eh] [rbp-12h]
  unsigned __int64 v9; // [rsp+48h] [rbp-8h]

  v9 = __readfsqword(0x28u);
  v3 = 3321718172420014856LL;
  v4 = 2234359365280082745LL;
  v5 = 145030110599518468LL;
  v6 = 201867289;
  v7 = 5150;
  v8 = 16;
  for ( i = 0; i <= 30; ++i )
    putchar(a1 ^ *((char *)&v3 + i));
  return 0LL;
}
```
This is solution script.

```python
t = '08030e1f141d192e'.decode('hex')
t += '392b162c010a021f'.decode('hex')
t += '041905001e400302'.decode('hex')
t += '1940080c'.decode('hex')
t += '1e14'.decode('hex')
t += '10'.decode('hex')

for i in range(0, 256):
	flag = ''
	for j in t:
		flag += chr(ord(j) ^ i)
	if 'enc' in flag:
		print flag
```
**encryptCTF{Algorithms-not-easy}**
