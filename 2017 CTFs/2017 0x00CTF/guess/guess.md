# **guessme**

#### tag : reversing

-----------------------------------------------

#### Description

>Hi there. Can you find the right key that unlocks the flag?

>Platform: 64 bit Linux (developed on Ubuntu)

-----------------------------------------------

#### Solution

This program is linux 64 bit ELF program.

~~~

$ file ./guessme
./guessme: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=92b1d84ee22b7c92dc80fac971bdc7f6cd0e3672, stripped

~~~

Here is disassembly code of routine about input password key. So, I focus code after 0x400f32 and find 2 check password key routine.

~~~

...
.text:0000000000400EFD                 lea     rax, [rbp+var_40]
.text:0000000000400F01                 mov     rdi, rax
.text:0000000000400F04                 call    __ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1Ev ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(void)
.text:0000000000400F09                 cmp     [rbp+var_94], 1
.text:0000000000400F10                 jg      short loc_400F34
.text:0000000000400F12                 mov     esi, offset aEnterAKey ; "Enter a key: "
.text:0000000000400F17                 mov     edi, offset _ZSt4cout ; std::cout
.text:0000000000400F1C                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::basic_ostream<char,std::char_traits<char>> &,char const*)
.text:0000000000400F21                 lea     rax, [rbp+var_40]
.text:0000000000400F25                 mov     rsi, rax
.text:0000000000400F28                 mov     edi, offset _ZSt3cin ; std::cin
.text:0000000000400F2D                 call    __ZStrsIcSt11char_traitsIcESaIcEERSt13basic_istreamIT_T0_ES7_RNSt7__cxx1112basic_stringIS4_S5_T1_EE ; std::operator>><char,std::char_traits<char>,std::allocator<char>>(std::basic_istream<char,std::char_traits<char>> &,std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>> &)
.text:0000000000400F32                 jmp     short loc_400F51
...

~~~

First, there is checking the key's length routine in:

~~~

.text:0000000000400F34                 mov     rax, [rbp+var_A0]
.text:0000000000400F3B                 add     rax, 8
.text:0000000000400F3F                 mov     rdx, [rax]
.text:0000000000400F42                 lea     rax, [rbp+var_40]
.text:0000000000400F46                 mov     rsi, rdx
.text:0000000000400F49                 mov     rdi, rax
.text:0000000000400F4C                 call    __ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEaSEPKc ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=(char const*)
.text:0000000000400F51
.text:0000000000400F51 loc_400F51:                             ; CODE XREF: main+14Cj
.text:0000000000400F51                 lea     rax, [rbp+var_40]
.text:0000000000400F55                 mov     rdi, rax
.text:0000000000400F58                 call    __ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(void)
.text:0000000000400F5D                 mov     rbx, rax
.text:0000000000400F60                 lea     rax, [rbp+var_60]
.text:0000000000400F64                 mov     rdi, rax
.text:0000000000400F67                 call    sub_401402
.text:0000000000400F6C                 cmp     rbx, rax
.text:0000000000400F6F                 setnz   al
.text:0000000000400F72                 test    al, al
.text:0000000000400F74                 jz      short loc_400F8F
.text:0000000000400F76                 mov     esi, offset aFail ; "FAIL\n"
.text:0000000000400F7B                 mov     edi, offset _ZSt4cout ; std::cout
.text:0000000000400F80                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::basic_ostream<char,std::char_traits<char>> &,char const*)
.text:0000000000400F85                 mov     ebx, 1
.text:0000000000400F8A                 jmp     loc_401060

~~~

I can guess this line compare length of key.

~~~
.text:0000000000400F6C                 cmp     rbx, rax
~~~

Second, there is checking the key's value routine in:

~~~

.text:0000000000400F99                 mov     eax, [rbp+var_84]
.text:0000000000400F9F                 movsxd  rbx, eax
.text:0000000000400FA2                 lea     rax, [rbp+var_40]
.text:0000000000400FA6                 mov     rdi, rax
.text:0000000000400FA9                 call    __ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(void)
.text:0000000000400FAE                 cmp     rbx, rax
.text:0000000000400FB1                 setb    al
.text:0000000000400FB4                 test    al, al
.text:0000000000400FB6                 jz      short loc_40101E
.text:0000000000400FB8                 mov     eax, [rbp+var_84]
.text:0000000000400FBE                 movsxd  rdx, eax
.text:0000000000400FC1                 lea     rax, [rbp+var_40]
.text:0000000000400FC5                 mov     rsi, rdx
.text:0000000000400FC8                 mov     rdi, rax
.text:0000000000400FCB                 call    __ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](ulong)
.text:0000000000400FD0                 movzx   eax, byte ptr [rax]
.text:0000000000400FD3                 movsx   eax, al
.text:0000000000400FD6                 lea     ebx, [rax-61h]
.text:0000000000400FD9                 mov     eax, [rbp+var_84]
.text:0000000000400FDF                 movsxd  rdx, eax
.text:0000000000400FE2                 lea     rax, [rbp+var_60]
.text:0000000000400FE6                 mov     rsi, rdx
.text:0000000000400FE9                 mov     rdi, rax
.text:0000000000400FEC                 call    sub_4012D8
.text:0000000000400FF1                 mov     eax, [rax]
.text:0000000000400FF3                 cmp     ebx, eax
.text:0000000000400FF5                 setnz   al
.text:0000000000400FF8                 test    al, al
.text:0000000000400FFA                 jz      short loc_401012
.text:0000000000400FFC                 mov     esi, offset aFail ; "FAIL\n"
.text:0000000000401001                 mov     edi, offset _ZSt4cout ; std::cout
.text:0000000000401006                 call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::basic_ostream<char,std::char_traits<char>> &,char const*)
.text:000000000040100B                 mov     ebx, 2
.text:0000000000401010                 jmp     short loc_401060

~~~

I can guess these line compare value of key. key value - 61h(which ascii code is 'a') is compared with eax(which is input key). this mean key's value is allocated by distacne from 'a' - alphabet order.

~~~

.text:0000000000400FD0                 movzx   eax, byte ptr [rax]
.text:0000000000400FD3                 movsx   eax, al
.text:0000000000400FD6                 lea     ebx, [rax-61h]
.text:0000000000400FD9                 mov     eax, [rbp+var_84]
.text:0000000000400FDF                 movsxd  rdx, eax
.text:0000000000400FE2                 lea     rax, [rbp+var_60]
.text:0000000000400FE6                 mov     rsi, rdx
.text:0000000000400FE9                 mov     rdi, rax
.text:0000000000400FEC                 call    sub_4012D8
.text:0000000000400FF1                 mov     eax, [rax]
.text:0000000000400FF3                 cmp     ebx, eax

~~~


I make breakpoint at `0x400f6c`. At `0x400f6c`, program compare input's key's length with real key's length. I can guess that key lenght is 14 byte from `*RAX  0xe`.

~~~

pwndbg> b* 0x400f6c
Breakpoint 1 at 0x400f6c
pwndbg> r
Starting program: /home/epist/Desktop/0x00/reversing/guessme
Enter a key: aaaa

Breakpoint 1, 0x0000000000400f6c in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[──────────────────────────────────REGISTERS───────────────────────────────────]
*RAX  0xe
*RBX  0x4
*RCX  0x7ffff75ec5a0 (_nl_C_LC_CTYPE_class+256) ◂— add    al, byte ptr [rax]
*RDX  0x38
*RDI  0x7fffffffde00 —▸ 0x615c20 ◂— 0x100000000
*RSI  0x7ffff783b790 (_IO_stdfile_0_lock) ◂— 0x0
*R8   0x7ffff78398e0 (_IO_2_1_stdin_) ◂— 0xfbad2288
*R9   0x7ffff783b790 (_IO_stdfile_0_lock) ◂— 0x0
*R10  0xde6
*R11  0x7ffff7b747c0 ◂— mov    rax, qword ptr [rdi + 8]
*R12  0x400cf0 ◂— xor    ebp, ebp
*R13  0x7fffffffdf40 ◂— 0x1
 R14  0x0
 R15  0x0
*RBP  0x7fffffffde60 —▸ 0x401af0 ◂— push   r15
*RSP  0x7fffffffddc0 —▸ 0x7fffffffdf48 —▸ 0x7fffffffe2b0 ◂— 0x70652f656d6f682f ('/home/ep')
*RIP  0x400f6c ◂— cmp    rbx, rax
[────────────────────────────────────DISASM────────────────────────────────────]
 ► 0x400f6c    cmp    rbx, rax
   0x400f6f    setne  al
   0x400f72    test   al, al
   0x400f74    je     0x400f8f

   0x400f76    mov    esi, 0x401c2e
   0x400f7b    mov    edi, std::cout                <0x6031e0>
   0x400f80    call   0x400c20

   0x400f85    mov    ebx, 1
   0x400f8a    jmp    0x401060
    ↓
   0x401060    lea    rax, [rbp - 0x40]
   0x401064    mov    rdi, rax
[────────────────────────────────────STACK─────────────────────────────────────]
00:0000│ rsp  0x7fffffffddc0 —▸ 0x7fffffffdf48 —▸ 0x7fffffffe2b0 ◂— 0x70652f656d6f682f ('/home/ep')
01:0008│      0x7fffffffddc8 ◂— 0x100400c10
02:0010│      0x7fffffffddd0 —▸ 0x6030b0 ◂— 0x0
03:0018│      0x7fffffffddd8 —▸ 0x7ffff74af299 (__cxa_atexit+25) ◂— test   rax, rax
04:0020│      0x7fffffffdde0 —▸ 0x615c20 ◂— 0x100000000
05:0028│      0x7fffffffdde8 —▸ 0x7fffffffde10 —▸ 0x615c58 ◂— 0x411
06:0030│      0x7fffffffddf0 —▸ 0x615c20 ◂— 0x100000000
07:0038│      0x7fffffffddf8 —▸ 0x4011e2 ◂— nop    
[──────────────────────────────────BACKTRACE───────────────────────────────────]
 ► f 0           400f6c
   f 1     7ffff7495830 __libc_start_main+240
Breakpoint * 0x400f6c

~~~

And I make breakpoint at `0x400fec`. At `0x400fec`, program compare key's value with real key's value. And I can find key's alphabet order is in `0x615c20`.

~~~

pwndbg> b* 0x400fec
Breakpoint 1 at 0x400fec
pwndbg> r
Starting program: /home/epist/Desktop/0x00/reversing/guessme
Enter a key: aaaaaaaaaaaaaa

Breakpoint 1, 0x400fec in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
[───────────────────────────────────────────────────────────────────────────────REGISTERS───────────────────────────────────────────────────────────────────────────────]
*RAX  0x7fffffffddf0 —▸ 0x615c20 ◂— 0x100000000
 RBX  0x0
*RCX  0x7ffff75ec5a0 (_nl_C_LC_CTYPE_class+256) ◂— add    al, byte ptr [rax]
 RDX  0x0
*RDI  0x7fffffffddf0 —▸ 0x615c20 ◂— 0x100000000
 RSI  0x0
*R8   0x7ffff78398e0 (_IO_2_1_stdin_) ◂— 0xfbad2288
*R9   0x7ffff783b790 (_IO_stdfile_0_lock) ◂— 0x0
*R10  0xd57
*R11  0x7ffff7b74990 ◂— mov    rax, rsi
*R12  0x400cf0 ◂— xor    ebp, ebp
*R13  0x7fffffffdf30 ◂— 0x1
 R14  0x0
 R15  0x0
*RBP  0x7fffffffde50 —▸ 0x401af0 ◂— push   r15
*RSP  0x7fffffffddb0 —▸ 0x7fffffffdf38 —▸ 0x7fffffffe2af ◂— 0x70652f656d6f682f ('/home/ep')
*RIP  0x400fec ◂— call   0x4012d8
[────────────────────────────────────────────────────────────────────────────────DISASM─────────────────────────────────────────────────────────────────────────────────]
 ► 0x400fec    call   0x4012d8

   0x400ff1    mov    eax, dword ptr [rax]
   0x400ff3    cmp    ebx, eax
   0x400ff5    setne  al
   0x400ff8    test   al, al
   0x400ffa    je     0x401012

   0x400ffc    mov    esi, 0x401c2e
   0x401001    mov    edi, std::cout                <0x6031e0>
   0x401006    call   0x400c20

   0x40100b    mov    ebx, 2
   0x401010    jmp    0x401060
[─────────────────────────────────────────────────────────────────────────────────STACK─────────────────────────────────────────────────────────────────────────────────]
00:0000│ rsp  0x7fffffffddb0 —▸ 0x7fffffffdf38 —▸ 0x7fffffffe2af ◂— 0x70652f656d6f682f ('/home/ep')
01:0008│      0x7fffffffddb8 ◂— 0x100400c10
02:0010│      0x7fffffffddc0 —▸ 0x6030b0 ◂— 0x0
03:0018│      0x7fffffffddc8 ◂— 0xf74af299
04:0020│      0x7fffffffddd0 —▸ 0x615c20 ◂— 0x100000000
05:0028│      0x7fffffffddd8 —▸ 0x7fffffffde00 —▸ 0x615c58 ◂— 0x411
06:0030│      0x7fffffffdde0 —▸ 0x615c20 ◂— 0x100000000
07:0038│      0x7fffffffdde8 —▸ 0x4011e2 ◂— nop    
[───────────────────────────────────────────────────────────────────────────────BACKTRACE───────────────────────────────────────────────────────────────────────────────]
 ► f 0           400fec
   f 1     7ffff7495830 __libc_start_main+240
Breakpoint * 0x400fec

~~~

There is key's alphabet order at `0x615c20`:

~~~

pwndbg> x/14wx 0x615c20
0x615c20:	0x00000000	0x00000001	0x00000001	0x00000002
0x615c30:	0x00000003	0x00000005	0x00000008	0x0000000d
0x615c40:	0x00000015	0x00000008	0x00000003	0x0000000b
0x615c50:	0x0000000e	0x00000019

~~~

So, I make simple python script generate key.

~~~

keyset =  [0,0x1,0x1,0x2,0x3,0x5,0x8,0xd,0x15,0x8,0x3,0xb,0xe,0x19]

key = []

for x in keyset:
	key.append(chr(x+ord('a')))

print ''.join(key)

~~~

Yeah, Key is `abbcdfinvidloz`.

~~~

$ python ./key.py
abbcdfinvidloz

~~~

~~~

$ ./guessme
Enter a key: abbcdfinvidloz
Good key!
The flag is: 0x00CTF{abbcdfinvidloz}

~~~

**0x00CTF{abbcdfinvidloz}**
