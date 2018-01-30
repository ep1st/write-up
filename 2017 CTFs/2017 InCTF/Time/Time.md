# **Time**

#### tag : reversing

-----------------------------------------------

#### Description

>All of you want is time and all you have is time.

-----------------------------------------------

#### Solution

First, Time is 32-bit excutable elf file, but Time run on ARM system. To run or debug in dynamic this file on ARM, `qemu` is installed in linux.

~~~

$ file Time
Time: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.3, for GNU/Linux 2.6.16, stripped

~~~

Anyway, I open this file on IDA, and get this code:

~~~

void sub_8514()
{
  int v0; // [sp+0h] [bp-Ch]@1
  int i; // [sp+4h] [bp-8h]@2

  puts("Enter your Key");
  _isoc99_scanf("%ld", &v0);
  if ( dword_108D0 - dword_108DC == v0 )
  {
    puts("Seems you guessed it.");
    printf("Flag is ");
    for ( i = 0; i <= 33; ++i )
      putchar(dword_1084C[i] ^ 7);
    exit(0);
  }
  puts("Flag check failed");
  exit(-1);
}

~~~

In code, `putchar(dword_1084C[i] ^ 7);` is print flag to me. Well, there is no codes to affect `dword_1084C`. So, I just use values on `dword_1084C`.

~~~

.data:0001084C ; _DWORD dword_1084C[33]
.data:0001084C dword_1084C     DCD 0x6E, 0x69, 0x64, 0x73, 0x61, 0x7C, 0x53, 0x6F, 0x36
.data:0001084C                                         ; DATA XREF: sub_8514:loc_8574o
.data:0001084C                                         ; .text:off_85D4o
.data:0001084C                 DCD 0x74, 0x58, 0x26, 0x74, 0x58, 0x6D, 0x52, 0x74, 0x73
.data:0001084C                 DCD 0x58, 0x73, 0x6F, 0x34, 0x58, 0x45, 0x34, 0x60, 0x6E
.data:0001084C                 DCD 0x69, 0x49, 0x6E, 0x69, 0x60, 0x7A

~~~

I have to calculate this value ^ 7. So, I make simple python script.

~~~

key = [ 0x6E, 0x69, 0x64, 0x73, 0x61, 0x7C, 0x53, 0x6F, 0x36, 0x74, 0x58, 0x26, 0x74, 0x58, 0x6D, 0x52, 0x74, 0x73, 0x58, 0x73, 0x6F, 0x34, 0x58, 0x45, 0x34, 0x60, 0x6E, 0x69, 0x49, 0x6E, 0x69, 0x60, 0x7A ]

flag = ''

for i in key:
	flag += chr(i^7)

print flag

~~~

~~~

$ python ./key.py
inctf{Th1s_!s_jUst_th3_B3ginNing}

~~~

**inctf{Th1s_!s_jUst_th3_B3ginNing}**
