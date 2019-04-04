# **crackme03**

#### tag : rev

-----------------------------------------------

#### Description

>tik-tok tik-tok can you defuse the bomb?
>
>author: codacker
>nc 104.154.106.182 7777

-----------------------------------------------

#### Solution

Here is main code. There are 5 challenges as `sub_1286, sub_12BD, sub_12E6, sub_1392, sub_1410`. If passed challenges, In `sub_122D`, flag will be given.

```c
int __cdecl sub_1502(int a1)
{
  int v1; // ecx
  int result; // eax
  int v3; // edx
  unsigned int v4; // et1
  signed int i; // [esp+0h] [ebp-68h]
  int (__cdecl *v6)(char *); // [esp+8h] [ebp-60h]
  int (__cdecl *v7)(int *); // [esp+Ch] [ebp-5Ch]
  int (__cdecl *v8)(int); // [esp+10h] [ebp-58h]
  int (__cdecl *v9)(char *); // [esp+14h] [ebp-54h]
  int (__cdecl *v10)(const char *); // [esp+18h] [ebp-50h]
  char v11; // [esp+1Ch] [ebp-4Ch]
  unsigned int v12; // [esp+5Ch] [ebp-Ch]
  int *v13; // [esp+60h] [ebp-8h]

  v13 = &a1;
  v12 = __readgsdword(0x14u);
  v6 = sub_1286;
  v7 = sub_12BD;
  v8 = sub_12E6;
  v9 = sub_1392;
  v10 = sub_1410;
  setvbuf(stdout, 0, 2, 0);
  puts("Hi!, i am a BOMB!\nI will go boom if you don't give me right inputs");
  for ( i = 0; i <= 4; ++i )
  {
    printf("Enter input #%d: ", i);
    __isoc99_scanf("%s", &v11);
    (*(&v6 + i))(&v11);
  }
  sub_122D();
  result = 0;
  v4 = __readgsdword(0x14u);
  v3 = v4 ^ v12;
  if ( v4 != v12 )
    sub_1670(v1, v3);
  return result;
}
```

First string : `CRACKME02`.

```c
int __cdecl sub_1286(char *s1)
{
  int result; // eax

  result = strcmp(s1, "CRACKME02");
  if ( result )
    sub_1258();
  return result;
}
```

Second string : `\xef\xbe\xad\xde`.

```c
int __cdecl sub_12BD(int *a1)
{
  int result; // eax

  result = *a1;
  if ( *a1 != 0xDEADBEEF )
    sub_1258();
  return result;
}
```

Thrid string : `ZXytUb9fl78evgJy3KJN`.

```c
unsigned int __cdecl sub_12E6(int a1)
{
  size_t v1; // edx
  int v2; // ecx
  unsigned int result; // eax
  unsigned int v4; // et1
  size_t i; // [esp+10h] [ebp-28h]
  char s[4]; // [esp+17h] [ebp-21h]
  unsigned int v7; // [esp+2Ch] [ebp-Ch]

  v7 = __readgsdword(0x14u);
  strcpy(s, "ZXytUb9fl78evgJy3KJN");
  for ( i = 0; ; ++i )
  {
    v1 = strlen(s);
    if ( v1 <= i )
      break;
    if ( s[i] != *(_BYTE *)(i + a1) )
      sub_1258();
  }
  v4 = __readgsdword(0x14u);
  result = v4 ^ v7;
  if ( v4 != v7 )
    sub_1670(v2, v1);
  return result;
}
```

Forth string : `1`. Because a is 1 in equation `a^3 + 4a^2 - 2a - 3 = 0`.

```c
int __cdecl sub_1392(char *s)
{
  int v1; // ST1C_4

  if ( strlen(s) > 3 )
    sub_1258();
  v1 = atoi(s);
  if ( v1 * v1 * v1 + 2 * (2 * v1 * v1 - v1) - 3 )
    sub_1258();
  return puts("SUBSCRIBE TO PEWDIEPIE");
}
```

Fifth string : `127, 127, 127, 127, 105, (201-127), (231-127), (206-127), (213-127)`. Focus data type is char, So It need to be lesser than `80h`.

```
d int __cdecl sub_1410(const char *a1)
{
  int v1; // ecx
  int v2; // edx
  unsigned int result; // eax
  unsigned int v4; // et1
  char dest; // [esp+12h] [ebp-16h]
  char v6; // [esp+13h] [ebp-15h]
  char v7; // [esp+14h] [ebp-14h]
  char v8; // [esp+15h] [ebp-13h]
  char v9; // [esp+16h] [ebp-12h]
  char v10; // [esp+17h] [ebp-11h]
  char v11; // [esp+18h] [ebp-10h]
  char v12; // [esp+19h] [ebp-Fh]
  char v13; // [esp+1Ah] [ebp-Eh]
  unsigned int v14; // [esp+1Ch] [ebp-Ch]

  v14 = __readgsdword(0x14u);
  strncpy(&dest, a1, 0xAu);
  puts("Validating Input 4");
  if ( dest + v13 != 213 )
    sub_1258();
  if ( v6 + v12 != 206 )
    sub_1258();
  if ( v7 + v11 != 231 )
    sub_1258();
  v2 = v8;
  if ( v8 + v10 != 201 )
    sub_1258();
  if ( v9 == 105 )
    puts("you earned it");
  v4 = __readgsdword(0x14u);
  result = v4 ^ v14;
  if ( v4 != v14 )
    sub_1670(v1, v2);
  return result;
}
```
This is solution script.

```python
from pwn import *

context.log_level = 'debug'
r = remote('104.154.106.182', 7777)

rr = lambda x: r.recvuntil(str(x))
ss = lambda x: r.sendline(str(x))

s1 = 'CRACKME02'
s2 = 0xdeadbeef
s3 = 'ZXytUb9fl78evgJy3KJN'
s4 = 1
s5 = [chr(i) for i in [ 127, 127, 127, 127, 105, (201-127), (231-127), (206-127), (213-127)]]

rr(': ')
ss(s1)
rr(': ')
ss(p32(s2))
rr(': ')
ss(s3)
rr(': ')
ss(s4)
rr(': ')
ss(''.join(s5))

r.interactive()
```
**encryptCTF{B0mB_D!ffu53d}**
