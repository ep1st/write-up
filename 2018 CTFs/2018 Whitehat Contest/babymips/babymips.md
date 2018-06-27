# **babymips**

#### tag : reversing

-----------------------------------------------

#### Description

>Description is missing.

-----------------------------------------------

#### Solution

Well, Challenge file is elf on MIPS architecture.

~~~
$ file babymips
babymips: ELF 32-bit MSB executable, MIPS, MIPS32 rel2 version 1 (SYSV), dynamically linked, interpreter /lib/ld.so.1, for GNU/Linux 3.2.0, BuildID[sha1]=42ba8792cceb2538e504856310967a89c35e7681, not stripped
~~~

First, I make environment running MIPS by qemu-system. I put the binary to MIPS and attempt to run this. And then I notice that segmentation fault occur when there is no arguments.

~~~
root@debian-mips:~# ./babymips
Segmentation fault
root@debian-mips:~# ./babymips aaaa
~~~

Ok, Let's analyze code of binary. This is first checking section. In `.text:00400A2C`, $v0 will be 0x460+var_438($fp) which is offset of argv[1]. And $v0 increase by 0x34 in `.text:00400A30`. And $v1 will be $v0 in `.text:00400A34 `. And then $v0 will be 0x61 in `.text:00400A38`.

Finally, $v1 will be offset of argv[1]+0x34 and $v0 will be 0x61. And these values compared in `.text:00400A3C`. When two value is not same, loc_4028F8(exit routine) will run.

So, argv[1][0x34] have to be 0x61(a).

~~~
...
.text:004009D4                 lw      $v0, 4($v0)
.text:004009D8                 sw      $v0, 0x460+var_438($fp)
.text:004009DC                 la      $v0, rand
.text:004009E0                 move    $t9, $v0
.text:004009E4                 jalr    $t9 ; rand
.text:004009E8                 nop
.text:004009EC                 lw      $gp, 0x460+var_450($fp)
.text:004009F0                 move    $a0, $v0
.text:004009F4                 li      $v0, 0x66666667
.text:004009FC                 mult    $a0, $v0
.text:00400A00                 mfhi    $v0
.text:00400A04                 sra     $v1, $v0, 1
.text:00400A08                 sra     $v0, $a0, 31
.text:00400A0C                 subu    $v1, $v0
.text:00400A10                 move    $v0, $v1
.text:00400A14                 sll     $v0, 2
.text:00400A18                 addu    $v0, $v1
.text:00400A1C                 subu    $v1, $a0, $v0
.text:00400A20                 li      $v0, 3
.text:00400A24                 beq     $v1, $v0, loc_400A44
.text:00400A28                 nop
.text:00400A2C                 lw      $v0, 0x460+var_438($fp)
.text:00400A30                 addiu   $v0, 0x34
.text:00400A34                 lbu     $v1, 0($v0)
.text:00400A38                 li      $v0, 0x61
.text:00400A3C                 bne     $v1, $v0, loc_4028F8
~~~

Well, There are 72 same routines that check argv[x]. This mean length of argument is 72.

~~~
.text:00400A44 loc_400A44:                              # CODE XREF: main+124j
.text:00400A44                 lw      $v1, 0x460+arg_0($fp)
.text:00400A48                 li      $v0, 2
.text:00400A4C                 bne     $v1, $v0, loc_4028F8
.text:00400A50                 nop
.text:00400A54                 la      $v0, rand
.text:00400A58                 move    $t9, $v0
.text:00400A5C                 jalr    $t9 ; rand
.text:00400A60                 nop
.text:00400A64                 lw      $gp, 0x460+var_450($fp)
.text:00400A68                 move    $a0, $v0
.text:00400A6C                 li      $v0, 0x66666667
.text:00400A74                 mult    $a0, $v0
.text:00400A78                 mfhi    $v0
.text:00400A7C                 sra     $v1, $v0, 1
.text:00400A80                 sra     $v0, $a0, 31
.text:00400A84                 subu    $v1, $v0
.text:00400A88                 move    $v0, $v1
.text:00400A8C                 sll     $v0, 2
.text:00400A90                 addu    $v0, $v1
.text:00400A94                 subu    $v1, $a0, $v0
.text:00400A98                 li      $v0, 2
.text:00400A9C                 beq     $v1, $v0, loc_400ABC
.text:00400AA0                 nop
.text:00400AA4                 lw      $v0, 0x460+var_438($fp)
.text:00400AA8                 addiu   $v0, 0x22
.text:00400AAC                 lbu     $v1, 0($v0)
.text:00400AB0                 li      $v0, 0x78
.text:00400AB4                 bne     $v1, $v0, loc_4028F8
.text:00400AB8                 nop
~~~

I use some command to extract all the values. key1 file will contain ascii data of argument, key2 file will contain index data of argument.

~~~
$ mips-linux-gnu-objdump -d babymips | grep li | grep v0 | awk -F, '{print $2}' | egrep '[0-9][0-9]' > key1

$ mips-linux-gnu-objdump -d babymips | grep addiu | grep 400a30 -A 70 | awk -F, {'print $3'} > key2
~~~

But, There is no addiu instruction in checking argument of index 0. So I have to add 0 index in manually.

~~~
.text:0040105C loc_40105C:                              # CODE XREF: main+73Cj
.text:0040105C                 la      $v0, rand
.text:00401060                 move    $t9, $v0
.text:00401064                 jalr    $t9 ; rand
.text:00401068                 nop
.text:0040106C                 lw      $gp, 0x460+var_450($fp)
.text:00401070                 move    $a0, $v0
.text:00401074                 li      $v0, 0x66666667
.text:0040107C                 mult    $a0, $v0
.text:00401080                 mfhi    $v0
.text:00401084                 sra     $v1, $v0, 1
.text:00401088                 sra     $v0, $a0, 31
.text:0040108C                 subu    $v1, $v0
.text:00401090                 move    $v0, $v1
.text:00401094                 sll     $v0, 2
.text:00401098                 addu    $v0, $v1
.text:0040109C                 subu    $v1, $a0, $v0
.text:004010A0                 li      $v0, 2
.text:004010A4                 beq     $v1, $v0, loc_4010C0
.text:004010A8                 nop
.text:004010AC                 lw      $v0, 0x460+var_438($fp)
.text:004010B0                 lbu     $v1, 0($v0)
.text:004010B4                 li      $v0, 0x54
.text:004010B8                 bne     $v1, $v0, loc_4028F8
.text:004010BC                 nop
~~~

I put 0 index to key2 file.

~~~
...
40
0
41
...
~~~

And then, I make some script to generate key.

~~~
from UserString import MutableString

key = MutableString('a'*72)

k1 = open('key1').read().split('\n')[:-1]
k2 = open('key2').read().split('\n')[:-1]

for i,j in zip(k1,k2):
	key[int(j)] = chr(int(i))

print key
~~~

Ok, Key is `Th1s_1s_k3y_f1foasdjfp1j234joxjpcvxcvjapsdforjqwpejoajfsdpjfaaa3gjqi4938`

~~~
$ python solve.py
Th1s_1s_k3y_f1foasdjfp1j234joxjpcvxcvjapsdforjqwpejoajfsdpjfaaa3gjqi4938
~~~

~~~
root@debian-mips:~# ./babymips Th1s_1s_k3y_f1foasdjfp1j234joxjpcvxcvjapsdforjqwpejoajfsdpjfaaa3gjqi4938
WoW Flag is
flag{B6by_MipS_h4T3_asA}
~~~

**flag{B6by_MipS_h4T3_asA}**
