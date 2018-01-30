# **Suffled Love**

#### tag : reversing

-----------------------------------------------

#### Description

>Find out if you and your computer are twin souls

-----------------------------------------------

#### Solution

~~~

$ file c1
c1: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=e38feffad25c4dbbd869b52a2587dd5605b1c61d, stripped

~~~

Here is main code. I can find return value of sub_40069D is way to get flag.

~~~

__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  int v4; // [sp+4h] [bp-Ch]@1
  int v5; // [sp+8h] [bp-8h]@1
  int v6; // [sp+Ch] [bp-4h]@1

  v4 = 0;
  v6 = 0;
  puts("Shuffled Love");
  puts("by p1c0\n");
  v5 = 371173;
  printf("My PIN is %d\nYour PIN:", 371173LL);
  __isoc99_scanf("%d", &v4);
  v6 = sub_40069D(v5, v4);
  if ( v6 )
    puts("Oh. You are not the one :(.");
  else
    printf("You read my mind!!!. We are twin souls\n--> 0x00CTF{Y0uR_th3_0n3_%x} <--\n\n", (unsigned int)v4);
  return 0LL;
}

~~~

In sub_40069D, There is algorithm that generate pincode. First, Divide 371173 to each digit. and this values and byte_601060 is generate key.

~~~

__int64 __fastcall sub_40069D(signed int a1, int a2)
{
  __int64 result; // rax@7
  __int64 v3; // rbx@7
  signed int v4; // [sp+Ch] [bp-44h]@1
  signed int i; // [sp+14h] [bp-3Ch]@1
  signed int j; // [sp+14h] [bp-3Ch]@4
  signed int v7; // [sp+18h] [bp-38h]@1
  signed int v8; // [sp+18h] [bp-38h]@4
  unsigned int v9; // [sp+1Ch] [bp-34h]@1
  char v10[16]; // [sp+20h] [bp-30h]@2
  char v11[8]; // [sp+30h] [bp-20h]@5
  __int64 v12; // [sp+38h] [bp-18h]@1

  v4 = a1;
  v12 = *MK_FP(__FS__, 40LL);
  v7 = 100000;
  v9 = 0;
  for ( i = 0; i <= 5; ++i )
  {
    v10[i] = v4 / v7;
    v4 -= v7 * v10[i];
    v7 /= 10;
  }
  putchar(10);
  v8 = 1;
  for ( j = 0; j <= 5; ++j )
  {
    v11[j] = byte_601060[((j + 3) ^ 6)] * v10[(j + 2) % 6] ^ v10[j];
    v9 += v8 * v11[j];
    v8 *= 10;
  }
  result = a2 ^ v9;
  v3 = *MK_FP(__FS__, 40LL) ^ v12;
  return result;
}

~~~

Well, I can follow byte_601060.

~~~

.data:0000000000601060 ; char byte_601060[]
.data:0000000000601060 byte_601060     db 1                    ; DATA XREF: sub_40069D+DEr
.data:0000000000601061                 db    2
.data:0000000000601062                 db    1
.data:0000000000601063                 db    3
.data:0000000000601064                 db    2
.data:0000000000601065                 db    5

~~~

I make simple python script to generate pincode. But in this code, keyset is not 6 byte. In algorithm of generate code, (i+3)^6 will be 14 when i is 5. So, to handle error, I expand keyset to 14 byte.

~~~

#!/usr/bin/env python

pinset = [ 3, 7, 1, 1, 7, 3 ]
keyset = [ 1, 2, 1, 3, 2, 5 , 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
password = 0

for i in range(0,6):
	password += int((keyset[((i+3)^6)] * pinset[(i+2)%6] ^ pinset[i])*pow(10,i))

print password

~~~

~~~

$ python ./key.py
314066

~~~

Pincode is 314066.

~~~

$ ./c1
Shuffled Love
by p1c0

My PIN is 371173
Your PIN:314066

You read my mind!!!. We are twin souls
--> 0x00CTF{Y0uR_th3_0n3_4cad2} <--

~~~

There is another way to find key. at 0x00000000004007C8, xor operand compare key with input value.

~~~

.text:00000000004007C8                 xor     [rbp+var_34], eax
.text:00000000004007CB                 mov     eax, [rbp+var_34]
.text:00000000004007CE                 mov     rbx, [rbp+var_18]
.text:00000000004007D2                 xor     rbx, fs:28h
.text:00000000004007DB                 jz      short loc_4007E2
.text:00000000004007DD                 call    ___stack_chk_fail
.text:00000000004007E2 ; ---------------------------------------------------------------------------
.text:00000000004007E2
.text:00000000004007E2 loc_4007E2:                             ; CODE XREF: sub_40069D+13Ej
.text:00000000004007E2                 add     rsp, 48h
.text:00000000004007E6                 pop     rbx
.text:00000000004007E7                 pop     rbp
.text:00000000004007E8                 retn

~~~

I make breakpoint at 0x00000000004007C8, and find $rbp-0x34 is 0x0004cad2(314066).

~~~

pwndbg> b* 0x00000000004007C8
Breakpoint 1 at 0x4007c8
pwndbg> r
Starting program: /home/epist/Desktop/0x00/reversing/c1
Shuffled Love
by p1c0

My PIN is 371173
Your PIN:123456


Breakpoint 1, 0x00000000004007c8 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[──────────────────────────────────REGISTERS───────────────────────────────────]
*RAX  0x1e240
 RBX  0x0
*RCX  0x7
*RDX  0x186a0
*RDI  0x1
*RSI  0x3
*R8   0x7ffff7dd3780 (_IO_stdfile_1_lock) ◂— 0x0
*R9   0x7ffff7fda700 ◂— 0x7ffff7fda700
*R10  0x1d6
*R11  0x246
*R12  0x4005b0 ◂— xor    ebp, ebp
*R13  0x7fffffffdf40 ◂— 0x1
 R14  0x0
 R15  0x0
*RBP  0x7fffffffde40 —▸ 0x7fffffffde60 —▸ 0x400890 ◂— push   r15
*RSP  0x7fffffffddf0 —▸ 0x7ffff7dd3780 (_IO_stdfile_1_lock) ◂— 0x0
*RIP  0x4007c8 ◂— xor    dword ptr [rbp - 0x34], eax
[────────────────────────────────────DISASM────────────────────────────────────]
 ► 0x4007c8    xor    dword ptr [rbp - 0x34], eax
   0x4007cb    mov    eax, dword ptr [rbp - 0x34]
   0x4007ce    mov    rbx, qword ptr [rbp - 0x18]
   0x4007d2    xor    rbx, qword ptr fs:[0x28]
   0x4007db    je     0x4007e2
    ↓
   0x4007e2    add    rsp, 0x48
   0x4007e6    pop    rbx
   0x4007e7    pop    rbp
   0x4007e8    ret    

   0x4007e9    push   rbp
   0x4007ea    mov    rbp, rsp
[────────────────────────────────────STACK─────────────────────────────────────]
00:0000│ rsp  0x7fffffffddf0 —▸ 0x7ffff7dd3780 (_IO_stdfile_1_lock) ◂— 0x0
01:0008│      0x7fffffffddf8 ◂— 0x1e240
02:0010│      0x7fffffffde00 ◂— 0x600400946 /* 'F\t@' */
03:0018│      0x7fffffffde08 ◂— 0x4cad2000f4240
04:0020│      0x7fffffffde10 ◂— 0x30701010703
05:0028│      0x7fffffffde18 —▸ 0x7ffff7dd2620 (_IO_2_1_stdout_) ◂— 0xfbad2a84
06:0030│      0x7fffffffde20 ◂— 0x30102140606
07:0038│      0x7fffffffde28 ◂— 0xd4e2a72b94a2b200
[──────────────────────────────────BACKTRACE───────────────────────────────────]
 ► f 0           4007c8
   f 1           40085a
   f 2     7ffff7a2d830 __libc_start_main+240
Breakpoint * 0x00000000004007C8

pwndbg> x/wx $rbp-0x34
0x7fffffffde0c:	0x0004cad2

~~~

**0x00CTF{Y0uR_th3_0n3_4cad2}**
