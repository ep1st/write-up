# **Second**

#### tag : reversing

--------------------------------------------------------------------

#### Description

>2./usr/bin/sqlconnect 는 DB접속에 사용되는 실행파일로 보인다. 해당 파일에서 DB접속 패스워드를 찾아 입력하시오.

--------------------------------------------------------------------

#### Challenge

I have elf file from /usr/bin/download:

~~~

$ file sqlconnect
sqlconnect: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=602f3e82246c7978f2caf689d18805b278eb570e, not stripped

~~~

When I run this elf file:

~~~

$ ./sqlconnect
Password : aaaaaaaaaaaaaaaa
wrong password!!
Password :

~~~

Well, there is some verfication system in the program.

So I try to debug this program.


I have some informations about functions:

~~~

pwndbg> info functions
All defined functions:

Non-debugging symbols:
0x0804853c  _init
0x08048570  AES_set_encrypt_key@plt
0x08048580  __gmon_start__@plt
0x08048590  memset@plt
0x080485a0  __libc_start_main@plt
0x080485b0  memcpy@plt
0x080485c0  strlen@plt
0x080485d0  printf@plt
0x080485e0  __stack_chk_fail@plt
0x080485f0  sleep@plt
0x08048600  __isoc99_scanf@plt
0x08048610  AES_ctr128_encrypt@plt
0x08048620  puts@plt
0x08048630  strncmp@plt
0x08048640  strcmp@plt
0x08048650  _start
0x08048680  __x86.get_pc_thunk.bx
0x08048690  deregister_tm_clones
0x080486c0  register_tm_clones
0x08048700  __do_global_dtors_aux
0x08048720  frame_dummy
0x0804874d  init_ctr
0x080487b5  encrypt
0x0804894b  main
0x08048b50  __libc_csu_init
0x08048bc0  __libc_csu_fini
0x08048bc4  _fini

~~~

And I disassemble the main of the program:

~~~

pwndbg> disassemble main
Dump of assembler code for function main:
   0x0804894b <+0>:	push   ebp
   0x0804894c <+1>:	mov    ebp,esp
   0x0804894e <+3>:	push   ebx
   0x0804894f <+4>:	and    esp,0xfffffff0
   0x08048952 <+7>:	sub    esp,0x240
   0x08048958 <+13>:	mov    eax,DWORD PTR [ebp+0xc]
   0x0804895b <+16>:	mov    DWORD PTR [esp+0xc],eax
   0x0804895f <+20>:	mov    eax,gs:0x14
   0x08048965 <+26>:	mov    DWORD PTR [esp+0x23c],eax
   0x0804896c <+33>:	xor    eax,eax
   0x0804896e <+35>:	mov    BYTE PTR [esp+0x2b],0x2f
   0x08048973 <+40>:	mov    BYTE PTR [esp+0x2c],0xfd
   0x08048978 <+45>:	mov    BYTE PTR [esp+0x2d],0x2a
   0x0804897d <+50>:	mov    BYTE PTR [esp+0x2e],0xb3
   0x08048982 <+55>:	mov    BYTE PTR [esp+0x2f],0x6
   0x08048987 <+60>:	mov    BYTE PTR [esp+0x30],0x92
   0x0804898c <+65>:	mov    BYTE PTR [esp+0x31],0xb7
   0x08048991 <+70>:	mov    BYTE PTR [esp+0x32],0x74
   0x08048996 <+75>:	mov    BYTE PTR [esp+0x33],0xc7
   0x0804899b <+80>:	mov    BYTE PTR [esp+0x34],0xe9
   0x080489a0 <+85>:	mov    BYTE PTR [esp+0x35],0x4
   0x080489a5 <+90>:	mov    BYTE PTR [esp+0x36],0x10
   0x080489aa <+95>:	mov    BYTE PTR [esp+0x37],0xdf
   0x080489af <+100>:	mov    BYTE PTR [esp+0x38],0x7e
   0x080489b4 <+105>:	mov    BYTE PTR [esp+0x39],0xf5
   0x080489b9 <+110>:	mov    BYTE PTR [esp+0x3a],0xf3
   0x080489be <+115>:	mov    BYTE PTR [esp+0x3b],0xcd
   0x080489c3 <+120>:	mov    DWORD PTR [esp+0x8],0x100
   0x080489cb <+128>:	mov    DWORD PTR [esp+0x4],0x0
   0x080489d3 <+136>:	lea    eax,[esp+0x3c]
   0x080489d7 <+140>:	mov    DWORD PTR [esp],eax
   0x080489da <+143>:	call   0x8048590 <memset@plt>
   0x080489df <+148>:	mov    DWORD PTR [esp+0x20],0x0
   0x080489e7 <+156>:	mov    DWORD PTR [esp+0x24],0x0
   0x080489ef <+164>:	jmp    0x8048a3c <main+241>
   0x080489f1 <+166>:	mov    eax,DWORD PTR [esp+0x20]
   0x080489f5 <+170>:	add    eax,0x804a054
   0x080489fa <+175>:	movzx  eax,BYTE PTR [eax]
   0x080489fd <+178>:	mov    BYTE PTR [esp+0x1f],al
   0x08048a01 <+182>:	mov    eax,DWORD PTR [esp+0x24]
   0x08048a05 <+186>:	lea    edx,[eax+0x1]
   0x08048a08 <+189>:	mov    DWORD PTR [esp+0x24],edx
   0x08048a0c <+193>:	movzx  eax,BYTE PTR [eax+0x804a04c]
   0x08048a13 <+200>:	xor    BYTE PTR [esp+0x1f],al
   0x08048a17 <+204>:	movzx  eax,BYTE PTR [esp+0x1f]
   0x08048a1c <+209>:	mov    edx,DWORD PTR [esp+0x20]
   0x08048a20 <+213>:	add    edx,0x804a054
   0x08048a26 <+219>:	mov    BYTE PTR [edx],al
   0x08048a28 <+221>:	cmp    DWORD PTR [esp+0x24],0x8
   0x08048a2d <+226>:	jne    0x8048a37 <main+236>
   0x08048a2f <+228>:	mov    DWORD PTR [esp+0x24],0x0
   0x08048a37 <+236>:	add    DWORD PTR [esp+0x20],0x1
   0x08048a3c <+241>:	mov    ebx,DWORD PTR [esp+0x20]
   0x08048a40 <+245>:	mov    DWORD PTR [esp],0x804a054
   0x08048a47 <+252>:	call   0x80485c0 <strlen@plt>
   0x08048a4c <+257>:	cmp    ebx,eax
   0x08048a4e <+259>:	jb     0x80489f1 <main+166>
   0x08048a50 <+261>:	mov    DWORD PTR [esp],0x8048be0
   0x08048a57 <+268>:	call   0x80485d0 <printf@plt>
   0x08048a5c <+273>:	lea    eax,[esp+0x3c]
   0x08048a60 <+277>:	mov    DWORD PTR [esp+0x4],eax
   0x08048a64 <+281>:	mov    DWORD PTR [esp],0x8048bec
   0x08048a6b <+288>:	call   0x8048600 <__isoc99_scanf@plt>
   0x08048a70 <+293>:	mov    DWORD PTR [esp],0x1
   0x08048a77 <+300>:	call   0x80485f0 <sleep@plt>
   0x08048a7c <+305>:	lea    eax,[esp+0x3c]
   0x08048a80 <+309>:	mov    DWORD PTR [esp],eax
   0x08048a83 <+312>:	call   0x80485c0 <strlen@plt>
   0x08048a88 <+317>:	mov    DWORD PTR [esp+0x8],eax
   0x08048a8c <+321>:	lea    eax,[esp+0x3c]
   0x08048a90 <+325>:	mov    DWORD PTR [esp+0x4],eax
   0x08048a94 <+329>:	lea    eax,[esp+0x3c]
   0x08048a98 <+333>:	mov    DWORD PTR [esp],eax
   0x08048a9b <+336>:	call   0x80487b5 <encrypt>
   0x08048aa0 <+341>:	mov    DWORD PTR [esp+0x8],0x11
   0x08048aa8 <+349>:	lea    eax,[esp+0x2b]
   0x08048aac <+353>:	mov    DWORD PTR [esp+0x4],eax
   0x08048ab0 <+357>:	lea    eax,[esp+0x3c]
   0x08048ab4 <+361>:	mov    DWORD PTR [esp],eax
   0x08048ab7 <+364>:	call   0x8048630 <strncmp@plt>
   0x08048abc <+369>:	test   eax,eax
   0x08048abe <+371>:	jne    0x8048adb <main+400>
   0x08048ac0 <+373>:	mov    DWORD PTR [esp],0x8048bef
   0x08048ac7 <+380>:	call   0x8048620 <puts@plt>
   0x08048acc <+385>:	nop
   0x08048acd <+386>:	mov    DWORD PTR [esp],0x8048c14
   0x08048ad4 <+393>:	call   0x8048620 <puts@plt>
   0x08048ad9 <+398>:	jmp    0x8048aec <main+417>
   0x08048adb <+400>:	mov    DWORD PTR [esp],0x8048c03
   0x08048ae2 <+407>:	call   0x8048620 <puts@plt>
   0x08048ae7 <+412>:	jmp    0x8048a50 <main+261>
   0x08048aec <+417>:	mov    DWORD PTR [esp],0x8048c29
   0x08048af3 <+424>:	call   0x80485d0 <printf@plt>
   0x08048af8 <+429>:	lea    eax,[esp+0x13c]
   0x08048aff <+436>:	mov    DWORD PTR [esp+0x4],eax
   0x08048b03 <+440>:	mov    DWORD PTR [esp],0x8048bec
   0x08048b0a <+447>:	call   0x8048600 <__isoc99_scanf@plt>
   0x08048b0f <+452>:	mov    DWORD PTR [esp+0x4],0x8048c31
   0x08048b17 <+460>:	lea    eax,[esp+0x13c]
   0x08048b1e <+467>:	mov    DWORD PTR [esp],eax
   0x08048b21 <+470>:	call   0x8048640 <strcmp@plt>
   0x08048b26 <+475>:	test   eax,eax
   0x08048b28 <+477>:	jne    0x8048b3d <main+498>
   0x08048b2a <+479>:	nop
   0x08048b2b <+480>:	mov    eax,DWORD PTR [esp+0x23c]
   0x08048b32 <+487>:	xor    eax,DWORD PTR gs:0x14
   0x08048b39 <+494>:	je     0x8048b44 <main+505>
   0x08048b3b <+496>:	jmp    0x8048b3f <main+500>
   0x08048b3d <+498>:	jmp    0x8048aec <main+417>
   0x08048b3f <+500>:	call   0x80485e0 <__stack_chk_fail@plt>
   0x08048b44 <+505>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x08048b47 <+508>:	leave  
   0x08048b48 <+509>:	ret

~~~

I disassemble main of sqlconnect. and I get some informations to solve this prob.

Frist, I parse string to program at:

~~~

   0x08048a6b <+288>:	call   0x8048600 <__isoc99_scanf@plt>

~~~

And, the string encrypted by:

~~~

   0x08048a9b <+336>:	call   0x80487b5 <encrypt>

~~~

Then, encrypted string and another string is compared at:

~~~

   0x08048ab7 <+364>:	call   0x8048630 <strncmp@plt>

~~~


Let's trace step by step.

~~~

pwndbg> b* main+288
Breakpoint 1 at 0x8048a6b
pwndbg> b* main+336
Breakpoint 2 at 0x8048a9b
pwndbg> b* main+364
Breakpoint 3 at 0x8048ab7

~~~

I find my string is exist at 0xffffcc2c from:

~~~

pwndbg> r
Starting program: /home/epist/Desktop/sqlconnect

Breakpoint 1, 0x08048a6b in main ()

....

 ► 0x8048a6b <main+288>    call   __isoc99_scanf@plt            <0x8048600>
        format: 0x8048bec ◂— 0x63007325 /* '%s' */
        vararg: 0xffffcc2c ◂— 0x0

~~~

~~~

pwndbg> ni
Password : aaaaaaaaa

pwndbg> x/s 0xffffcc2c
0xffffcc2c:	"aaaaaaaaa"

~~~

I find that encrypt function have same two argument which is my string:

~~~

pwndbg> c
Continuing.

Breakpoint 2, 0x08048a9b in main ()

...

 ► 0x8048a9b <main+336>    call   encrypt                       <0x80487b5>
        glibc_block: 0xffffcc2c ◂— 'aaaaaaaaa'
        edflag: 0xffffcc2c ◂— 'aaaaaaaaa'

~~~

After encryption, encrypted my string and another string at 0xffffcc1b is compared only 17 bytes:

~~~

pwndbg> c
Continuing.

Breakpoint 3, 0x08048ab7 in main ()

...

 ► 0x8048ab7 <main+364>    call   strncmp@plt                   <0x8048630>
        s1: 0xffffcc2c ◂— 0xb33cfd26
        s2: 0xffffcc1b ◂— 0xb32afd2f
        n: 0x11

~~~

And another string is at 0xffffcc1b:

~~~

pwndbg> x/17x 0xffffcc1b
0xffffcc1b:	0x2f	0xfd	0x2a	0xb3	0x06	0x92	0xb7	0x74
0xffffcc23:	0xc7	0xe9	0x04	0x10	0xdf	0x7e	0xf5	0xf3
0xffffcc2b:	0xcd

~~~

When allocated at 0x0804896e-0x080489be:

~~~

   0x0804896e <+35>:	mov    BYTE PTR [esp+0x2b],0x2f
   0x08048973 <+40>:	mov    BYTE PTR [esp+0x2c],0xfd
   0x08048978 <+45>:	mov    BYTE PTR [esp+0x2d],0x2a
   0x0804897d <+50>:	mov    BYTE PTR [esp+0x2e],0xb3
   0x08048982 <+55>:	mov    BYTE PTR [esp+0x2f],0x6
   0x08048987 <+60>:	mov    BYTE PTR [esp+0x30],0x92
   0x0804898c <+65>:	mov    BYTE PTR [esp+0x31],0xb7
   0x08048991 <+70>:	mov    BYTE PTR [esp+0x32],0x74
   0x08048996 <+75>:	mov    BYTE PTR [esp+0x33],0xc7
   0x0804899b <+80>:	mov    BYTE PTR [esp+0x34],0xe9
   0x080489a0 <+85>:	mov    BYTE PTR [esp+0x35],0x4
   0x080489a5 <+90>:	mov    BYTE PTR [esp+0x36],0x10
   0x080489aa <+95>:	mov    BYTE PTR [esp+0x37],0xdf
   0x080489af <+100>:	mov    BYTE PTR [esp+0x38],0x7e
   0x080489b4 <+105>:	mov    BYTE PTR [esp+0x39],0xf5
   0x080489b9 <+110>:	mov    BYTE PTR [esp+0x3a],0xf3
   0x080489be <+115>:	mov    BYTE PTR [esp+0x3b],0xcd

~~~

In conclusion, encrypted parsing string will be:

~~~

"\x2f\xfd\x2a\xb3\x06\x92\xb7\x74\xc7\xe9\x04\x10\xdf\x7e\xf5\xf3\xcd"

~~~

Now, let's make that string by encrypt function.

~~~

pwndbg> disassemble encrypt
Dump of assembler code for function encrypt:
   0x080487b5 <+0>:	push   ebp
   0x080487b6 <+1>:	mov    ebp,esp
   0x080487b8 <+3>:	sub    esp,0x68
   0x080487bb <+6>:	mov    eax,DWORD PTR [ebp+0x8]
   0x080487be <+9>:	mov    DWORD PTR [ebp-0x3c],eax
   0x080487c1 <+12>:	mov    eax,DWORD PTR [ebp+0xc]
   0x080487c4 <+15>:	mov    DWORD PTR [ebp-0x40],eax
   0x080487c7 <+18>:	mov    eax,gs:0x14
   0x080487cd <+24>:	mov    DWORD PTR [ebp-0xc],eax
   0x080487d0 <+27>:	xor    eax,eax
   0x080487d2 <+29>:	mov    DWORD PTR [ebp-0x38],0x0
   0x080487d9 <+36>:	mov    DWORD PTR [ebp-0x34],0x0
   0x080487e0 <+43>:	mov    DWORD PTR [esp+0x8],0x804a0a0
   0x080487e8 <+51>:	mov    DWORD PTR [esp+0x4],0x80
   0x080487f0 <+59>:	mov    DWORD PTR [esp],0x804a054
   0x080487f7 <+66>:	call   0x8048570 <AES_set_encrypt_key@plt>
   0x080487fc <+71>:	cmp    DWORD PTR [ebp+0x10],0x3ff
   0x08048803 <+78>:	jg     0x804885a <encrypt+165>
   0x08048805 <+80>:	mov    DWORD PTR [esp+0x4],0x804a060
   0x0804880d <+88>:	lea    eax,[ebp-0x30]
   0x08048810 <+91>:	mov    DWORD PTR [esp],eax
   0x08048813 <+94>:	call   0x804874d <init_ctr>
   0x08048818 <+99>:	mov    eax,DWORD PTR [ebp+0x10]
   0x0804881b <+102>:	lea    edx,[ebp-0x30]
   0x0804881e <+105>:	add    edx,0x10
   0x08048821 <+108>:	mov    DWORD PTR [esp+0x18],edx
   0x08048825 <+112>:	lea    edx,[ebp-0x30]
   0x08048828 <+115>:	add    edx,0x14
   0x0804882b <+118>:	mov    DWORD PTR [esp+0x14],edx
   0x0804882f <+122>:	lea    edx,[ebp-0x30]
   0x08048832 <+125>:	mov    DWORD PTR [esp+0x10],edx
   0x08048836 <+129>:	mov    DWORD PTR [esp+0xc],0x804a0a0
   0x0804883e <+137>:	mov    DWORD PTR [esp+0x8],eax
   0x08048842 <+141>:	mov    eax,DWORD PTR [ebp-0x40]
   0x08048845 <+144>:	mov    DWORD PTR [esp+0x4],eax
   0x08048849 <+148>:	mov    eax,DWORD PTR [ebp-0x3c]
   0x0804884c <+151>:	mov    DWORD PTR [esp],eax
   0x0804884f <+154>:	call   0x8048610 <AES_ctr128_encrypt@plt>
   0x08048854 <+159>:	nop
   0x08048855 <+160>:	jmp    0x8048938 <encrypt+387>
   0x0804885a <+165>:	mov    DWORD PTR [ebp-0x38],0x400
   0x08048861 <+172>:	jmp    0x80488c8 <encrypt+275>
   0x08048863 <+174>:	mov    DWORD PTR [esp+0x4],0x804a060
   0x0804886b <+182>:	lea    eax,[ebp-0x30]
   0x0804886e <+185>:	mov    DWORD PTR [esp],eax
   0x08048871 <+188>:	call   0x804874d <init_ctr>
   0x08048876 <+193>:	lea    eax,[ebp-0x30]
   0x08048879 <+196>:	add    eax,0x10
   0x0804887c <+199>:	mov    DWORD PTR [esp+0x18],eax
   0x08048880 <+203>:	lea    eax,[ebp-0x30]
   0x08048883 <+206>:	add    eax,0x14
   0x08048886 <+209>:	mov    DWORD PTR [esp+0x14],eax
   0x0804888a <+213>:	lea    eax,[ebp-0x30]
   0x0804888d <+216>:	mov    DWORD PTR [esp+0x10],eax
   0x08048891 <+220>:	mov    DWORD PTR [esp+0xc],0x804a0a0
   0x08048899 <+228>:	mov    DWORD PTR [esp+0x8],0x400
   0x080488a1 <+236>:	mov    eax,DWORD PTR [ebp-0x40]
   0x080488a4 <+239>:	mov    DWORD PTR [esp+0x4],eax
   0x080488a8 <+243>:	mov    eax,DWORD PTR [ebp-0x3c]
   0x080488ab <+246>:	mov    DWORD PTR [esp],eax
   0x080488ae <+249>:	call   0x8048610 <AES_ctr128_encrypt@plt>
   0x080488b3 <+254>:	add    DWORD PTR [ebp-0x3c],0x400
   0x080488ba <+261>:	add    DWORD PTR [ebp-0x40],0x400
   0x080488c1 <+268>:	add    DWORD PTR [ebp-0x38],0x400
   0x080488c8 <+275>:	mov    eax,DWORD PTR [ebp-0x38]
   0x080488cb <+278>:	cmp    eax,DWORD PTR [ebp+0x10]
   0x080488ce <+281>:	jle    0x8048863 <encrypt+174>
   0x080488d0 <+283>:	mov    eax,DWORD PTR [ebp+0x10]
   0x080488d3 <+286>:	cdq    
   0x080488d4 <+287>:	shr    edx,0x16
   0x080488d7 <+290>:	add    eax,edx
   0x080488d9 <+292>:	and    eax,0x3ff
   0x080488de <+297>:	sub    eax,edx
   0x080488e0 <+299>:	mov    DWORD PTR [ebp-0x34],eax
   0x080488e3 <+302>:	cmp    DWORD PTR [ebp-0x34],0x0
   0x080488e7 <+306>:	je     0x8048938 <encrypt+387>
   0x080488e9 <+308>:	mov    DWORD PTR [esp+0x4],0x804a060
   0x080488f1 <+316>:	lea    eax,[ebp-0x30]
   0x080488f4 <+319>:	mov    DWORD PTR [esp],eax
   0x080488f7 <+322>:	call   0x804874d <init_ctr>
   0x080488fc <+327>:	mov    eax,DWORD PTR [ebp-0x34]
   0x080488ff <+330>:	lea    edx,[ebp-0x30]
   0x08048902 <+333>:	add    edx,0x10
   0x08048905 <+336>:	mov    DWORD PTR [esp+0x18],edx
   0x08048909 <+340>:	lea    edx,[ebp-0x30]
   0x0804890c <+343>:	add    edx,0x14
   0x0804890f <+346>:	mov    DWORD PTR [esp+0x14],edx
   0x08048913 <+350>:	lea    edx,[ebp-0x30]
   0x08048916 <+353>:	mov    DWORD PTR [esp+0x10],edx
   0x0804891a <+357>:	mov    DWORD PTR [esp+0xc],0x804a0a0
   0x08048922 <+365>:	mov    DWORD PTR [esp+0x8],eax
   0x08048926 <+369>:	mov    eax,DWORD PTR [ebp-0x40]
   0x08048929 <+372>:	mov    DWORD PTR [esp+0x4],eax
   0x0804892d <+376>:	mov    eax,DWORD PTR [ebp-0x3c]
   0x08048930 <+379>:	mov    DWORD PTR [esp],eax
   0x08048933 <+382>:	call   0x8048610 <AES_ctr128_encrypt@plt>
   0x08048938 <+387>:	mov    eax,DWORD PTR [ebp-0xc]
   0x0804893b <+390>:	xor    eax,DWORD PTR gs:0x14
   0x08048942 <+397>:	je     0x8048949 <encrypt+404>
   0x08048944 <+399>:	call   0x80485e0 <__stack_chk_fail@plt>
   0x08048949 <+404>:	leave  
   0x0804894a <+405>:	ret    
End of assembler dump.

~~~

And I can figure out that encryption algorithm is AES_CTR128 from:

~~~

   0x080487f7 <+66>:	call   0x8048570 <AES_set_encrypt_key@plt>
   ...
   0x08048813 <+94>:	call   0x804874d <init_ctr>
   ...
   0x08048933 <+382>:	call   0x8048610 <AES_ctr128_encrypt@plt>

~~~

In this case, I use AES_CTR128 double encrypted cipher string is eqaul to decrypted string.

And this mean:

~~~

  encrypt(encrypted cipher string) = decrypted cipher string

~~~

Well, I put "\x2f\xfd\x2a\xb3\x06\x92\xb7\x74\xc7\xe9\x04\x10\xdf\x7e\xf5\xf3\xcd" to encrypted cipher string and then I can get decrypted string.


--------------------------------------------------------------------

#### Solution

~~~

$ xxd password
00000000: 2ffd 2ab3 0692 b774 c7e9 0410 df7e f5f3  /.*....t.....~..
00000010: cd0a
                                    ..
~~~

~~~

pwndbg> r < password

...

pwndbg> x/2s 0xffffcc2c
0xffffcc2c:	"hawaiianchocola"...
0xffffcc3b:	"te"

~~~

Yeah! I can get plain text of 0xffffcc1b. Password is hawaiianchocolate!

~~~

$ ./sqlconnect
Password : hawaiianchocolate
connect db success.
[Enter exit to exit]
mysql>

~~~

Success to login mysql system.


**flag hawaiianchocolate**
