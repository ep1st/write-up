# **Band Aid**

#### tag : reversing

-----------------------------------------------

#### Description

>Sometimes all you need is a little change in life.

-----------------------------------------------

#### Solution

I can download 32-bit elf file from download link.

~~~

file e0dd79b3d9b05e80
e0dd79b3d9b05e80: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=f02443b763cd44685e80979efbfa7052624cabfe, not stripped

~~~

This is part of function list of this elf file.

~~~
pwndbg> info functions

...
0x08048aeb  f2()
0x08048cab  main
...

~~~

At `0x08048cf6`, main function call f2 function. But in `0x08048cf4`, if `ebp-0xc` is equal or less than `0x124b`, f2 won't called.

~~~

pwndbg> disassemble main
Dump of assembler code for function main:
   0x08048cab <+0>:	lea    ecx,[esp+0x4]
   0x08048caf <+4>:	and    esp,0xfffffff0
   0x08048cb2 <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048cb5 <+10>:	push   ebp
   0x08048cb6 <+11>:	mov    ebp,esp
   0x08048cb8 <+13>:	push   ecx
   0x08048cb9 <+14>:	sub    esp,0x14
   0x08048cbc <+17>:	sub    esp,0x8
   0x08048cbf <+20>:	push   0x804942d
   0x08048cc4 <+25>:	push   0x804d080
   0x08048cc9 <+30>:	call   0x80488f0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x08048cce <+35>:	add    esp,0x10
   0x08048cd1 <+38>:	sub    esp,0x8
   0x08048cd4 <+41>:	push   0x8048970
   0x08048cd9 <+46>:	push   eax
   0x08048cda <+47>:	call   0x8048950 <_ZNSolsEPFRSoS_E@plt>
   0x08048cdf <+52>:	add    esp,0x10
   0x08048ce2 <+55>:	mov    DWORD PTR [ebp-0xc],0xd6
   0x08048ce9 <+62>:	add    DWORD PTR [ebp-0xc],0x1
   0x08048ced <+66>:	cmp    DWORD PTR [ebp-0xc],0x124b
   0x08048cf4 <+73>:	jle    0x8048d02 <main+87>
   0x08048cf6 <+75>:	call   0x8048aeb <_Z2f2v>
   0x08048cfb <+80>:	mov    eax,0x0
   0x08048d00 <+85>:	jmp    0x8048d07 <main+92>
   0x08048d02 <+87>:	mov    eax,0x1
   0x08048d07 <+92>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x08048d0a <+95>:	leave  
   0x08048d0b <+96>:	lea    esp,[ecx-0x4]
   0x08048d0e <+99>:	ret    
End of assembler dump.

~~~

~~~

   0x08048ce2 <+55>:	mov    DWORD PTR [ebp-0xc],0xd6
   0x08048ce9 <+62>:	add    DWORD PTR [ebp-0xc],0x1
   0x08048ced <+66>:	cmp    DWORD PTR [ebp-0xc],0x124b
   0x08048cf4 <+73>:	jle    0x8048d02 <main+87>
   0x08048cf6 <+75>:	call   0x8048aeb <_Z2f2v>

~~~

Value in `ebp-0xc` is 0xd7. It's will satisfy comparing instruction, So f2 won't called.

~~~

pwndbg> b* main+66
Breakpoint 1 at 0x8048ced

pwndbg> r
Starting program: /home/epist/Workspace/Github/Write-up/2018 CTFs/2018 TAMUCTF/Band Aid/e0dd79b3d9b05e80
 this code needs a band aid

Breakpoint 1, 0x08048ced in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────────────────────────────────────────────[ REGISTERS ]──────────────────────────────────────────────────────
*EAX  0x804d080 (std::cout@@GLIBCXX_3.4) —▸ 0xf7fb1c68 —▸ 0xf7f359e0 ◂— push   ebx
 EBX  0x0
*ECX  0xf7e20870 (_IO_stdfile_1_lock) ◂— 0x0
 EDX  0x0
*EDI  0xf7e1f000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1b1db0
*ESI  0xf7e1f000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1b1db0
*EBP  0xffffce98 ◂— 0x0
*ESP  0xffffce80 ◂— 0x1
*EIP  0x8048ced (main+66) ◂— cmp    dword ptr [ebp - 0xc], 0x124b
───────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────
 ► 0x8048ced  <main+66>                  cmp    dword ptr [ebp - 0xc], 0x124b
   0x8048cf4  <main+73>                  jle    main+87 <0x8048d02>
    ↓
   0x8048d02  <main+87>                  mov    eax, 1
   0x8048d07  <main+92>                  mov    ecx, dword ptr [ebp - 4]
   0x8048d0a  <main+95>                  leave  
   0x8048d0b  <main+96>                  lea    esp, [ecx - 4]
   0x8048d0e  <main+99>                  ret    
    ↓
   0xf7c85637 <__libc_start_main+247>    add    esp, 0x10
   0xf7c8563a <__libc_start_main+250>    sub    esp, 0xc
   0xf7c8563d <__libc_start_main+253>    push   eax
   0xf7c8563e <__libc_start_main+254>    call   exit <0xf7c9b9d0>
───────────────────────────────────────────────────────[ STACK ]────────────────────────────────────────────────────────
00:0000│ esp  0xffffce80 ◂— 0x1
01:0004│      0xffffce84 —▸ 0xffffcf44 —▸ 0xffffd133 ◂— 0x6d6f682f ('/hom')
02:0008│      0xffffce88 —▸ 0xffffcf4c —▸ 0xffffd18a ◂— 0x505f434c ('LC_P')
03:000c│      0xffffce8c ◂— 0xd7
04:0010│      0xffffce90 —▸ 0xf7e1f3dc (__exit_funcs) —▸ 0xf7e201e0 (initial) ◂— 0x0
05:0014│      0xffffce94 —▸ 0xffffceb0 ◂— 0x1
06:0018│ ebp  0xffffce98 ◂— 0x0
07:001c│      0xffffce9c —▸ 0xf7c85637 (__libc_start_main+247) ◂— add    esp, 0x10
─────────────────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────────────────
 ► f 0  8048ced main+66
   f 1 f7c85637 __libc_start_main+247
Breakpoint * main+66

pwndbg> x/wx $ebp-0xc
0xffffce8c:	0x000000d7

~~~

Well, I change value of `ebp-0xc` to 0x124b in `main+62` on purpose to use set command of gdb:

~~~

pwndbg> b* main+62
Breakpoint 1 at 0x8048ce9

pwndbg> r

...

pwndbg> set {int}($ebp-0xc) = 0x124b
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────────────────────────────────────────────[ REGISTERS ]──────────────────────────────────────────────────────
*EAX  0x804d080 (std::cout@@GLIBCXX_3.4) —▸ 0xf7fb1c68 —▸ 0xf7f359e0 ◂— push   ebx
 EBX  0x0
*ECX  0xf7e20870 (_IO_stdfile_1_lock) ◂— 0x0
 EDX  0x0
*EDI  0xf7e1f000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1b1db0
*ESI  0xf7e1f000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1b1db0
*EBP  0xffffce98 ◂— 0x0
*ESP  0xffffce80 ◂— 0x1
*EIP  0x8048ce9 (main+62) ◂— add    dword ptr [ebp - 0xc], 1
───────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────
 ► 0x8048ce9 <main+62>    add    dword ptr [ebp - 0xc], 1
   0x8048ced <main+66>    cmp    dword ptr [ebp - 0xc], 0x124b
   0x8048cf4 <main+73>    jle    main+87 <0x8048d02>

   0x8048cf6 <main+75>    call   f2() <0x8048aeb>

   0x8048cfb <main+80>    mov    eax, 0
   0x8048d00 <main+85>    jmp    main+92 <0x8048d07>
    ↓
   0x8048d07 <main+92>    mov    ecx, dword ptr [ebp - 4]
   0x8048d0a <main+95>    leave  
   0x8048d0b <main+96>    lea    esp, [ecx - 4]
   0x8048d0e <main+99>    ret    

   0x8048d0f              push   ebp
───────────────────────────────────────────────────────[ STACK ]────────────────────────────────────────────────────────
00:0000│ esp  0xffffce80 ◂— 0x1
01:0004│      0xffffce84 —▸ 0xffffcf44 —▸ 0xffffd133 ◂— 0x6d6f682f ('/hom')
02:0008│      0xffffce88 —▸ 0xffffcf4c —▸ 0xffffd18a ◂— 0x505f434c ('LC_P')
03:000c│      0xffffce8c ◂— 0x124b
04:0010│      0xffffce90 —▸ 0xf7e1f3dc (__exit_funcs) —▸ 0xf7e201e0 (initial) ◂— 0x0
05:0014│      0xffffce94 —▸ 0xffffceb0 ◂— 0x1
06:0018│ ebp  0xffffce98 ◂— 0x0
07:001c│      0xffffce9c —▸ 0xf7c85637 (__libc_start_main+247) ◂— add    esp, 0x10
─────────────────────────────────────────────────────[ BACKTRACE ]──────────────────────────────────────────────────────
 ► f 0  8048ce9 main+62
   f 1 f7c85637 __libc_start_main+247
Breakpoint * main+62

~~~

Ok, Program's flow is changed, It will call f2 function. And When continuing, I can get these messages encoded by base64 from program.

~~~

pwndbg> c
Continuing.
result
L/R8ejlvVP4+JvgvsSI+JaLn6YCArf5fTAIfUwMNCrJ8HkRkQLEB5RH5COF1+9mSQoGY8wG23AtDyM0OEgm+zFCTibFOgieixjrv5OHAIB+akOahMWoyt/qAGnK9ZsLsv20apyzlH0llafbfQ0MkurU/c8O3Xj3m0VL1GOjHk14=
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDV3dJQkFBS0JnUUNjVDRaalluR2lNWXRFZDcrL1l0RmdHRTNlZ1RrV0Jpd2hXQ240MUxQU1lzdXErNE9RCnBuQk1ZUjVZdExiOTRXTzdpNnZHYU9PTnNzSE5kWUFkblJETThpTFN2L3JUMHVPdGdTd2RaTmlMQzduNmdILzgKOFJqRlFFTGptSldRemdzWDhDVXFkWm80SnJNZkJTbXd3RFlBNUJtMGI3Nmd6bXFoK3lMWGErdW5PUUlEQVFBQgpBb0dBYWNhUy9adzNvM2Q5Yy9iSkpqMDd6SmlGMFdXRytQVnlWWm93eFBkRFBNS29hbXRMYTg2RnZkb1d6QloyCm9yVXNaVlN1Q0ZVZ2I5b2d0ZVdtcmVPRTR1d0FQK0RGKzJpU1h0MlZxTEdJZ29ieDZib0YrTktjMXNvUUFEaFQKNkw2emZNSzFNVzZwSDVYUGNVNUg4QU1TWUREYVFxeEVtWEp0azg4OUxJTVpVUUVDUVFDNDRYVjRqdEwwcjFkcQpjY1ByTlIrTEp4UjExMkJPMEhXLzduRVEwQUtUbUhIZ2EvbmV1ejMycHF1TVNRM2xodXRTNW5kanNzdmJ3dHJuCjNWdVhKRUJaQWtFQTJIQ1E0bE12MHI5Y3B2b2lCTVR0cDlYS2dIeU5Vbmd3dE1SODZ6VE0vK1dudlhTWjlDZk8KWXhyMlVvd2daMTlPNXpCZDFrVGRZQnNMbFVoL2syekI0UUpBWWtMeVBIRXNqZi9qWmgreEVZSGFrZ3JqUlA2RApvV0FLTlVoMXI0bmUxTE5oVXZZUWgrRGN2Z3MzZ2dnUjZyd2F0cVRuTDRZSDgzVk5BNDhTN3ZIRmdRSkFkeFZvCkFiNDNQOExkM1ZrZVFuVi9OS3FpSWhObFJneXU3Nlp6L0kwdWhWVDc5M2NpQlgycFJrbmRZUW1NQXBRanUzdVgKQlg4YU5maHJaUlZnYStLWXdRSkFYY1RKemE3ODNFeVk1YmxTZWIvWlJGYzZjdnFERDlRSDRXRVQ1b000ZjFnWgprZlI3Ti9qcEc4b09sZkl5d2o1RStaaHJaSTlEY1RmQjVnQWlFRHFrQmc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ==
LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDY1Q0WmpZbkdpTVl0RWQ3Ky9ZdEZnR0UzZQpnVGtXQml3aFdDbjQxTFBTWXN1cSs0T1FwbkJNWVI1WXRMYjk0V083aTZ2R2FPT05zc0hOZFlBZG5SRE04aUxTCnYvclQwdU90Z1N3ZFpOaUxDN242Z0gvODhSakZRRUxqbUpXUXpnc1g4Q1VxZFpvNEpyTWZCU213d0RZQTVCbTAKYjc2Z3ptcWgreUxYYSt1bk9RSURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ==
[Inferior 1 (process 30373) exited normally]

~~~

I make simple script to decode:

~~~

import base64

enc1 = "L/R8ejlvVP4+JvgvsSI+JaLn6YCArf5fTAIfUwMNCrJ8HkRkQLEB5RH5COF1+9mSQoGY8wG23AtDyM0OEgm+zFCTibFOgieixjrv5OHAIB+akOahMWoyt/qAGnK9ZsLsv20apyzlH0llafbfQ0MkurU/c8O3Xj3m0VL1GOjHk14="

enc2 = 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDV3dJQkFBS0JnUUNjVDRaalluR2lNWXRFZDcrL1l0RmdHRTNlZ1RrV0Jpd2hXQ240MUxQU1lzdXErNE9RCnBuQk1ZUjVZdExiOTRXTzdpNnZHYU9PTnNzSE5kWUFkblJETThpTFN2L3JUMHVPdGdTd2RaTmlMQzduNmdILzgKOFJqRlFFTGptSldRemdzWDhDVXFkWm80SnJNZkJTbXd3RFlBNUJtMGI3Nmd6bXFoK3lMWGErdW5PUUlEQVFBQgpBb0dBYWNhUy9adzNvM2Q5Yy9iSkpqMDd6SmlGMFdXRytQVnlWWm93eFBkRFBNS29hbXRMYTg2RnZkb1d6QloyCm9yVXNaVlN1Q0ZVZ2I5b2d0ZVdtcmVPRTR1d0FQK0RGKzJpU1h0MlZxTEdJZ29ieDZib0YrTktjMXNvUUFEaFQKNkw2emZNSzFNVzZwSDVYUGNVNUg4QU1TWUREYVFxeEVtWEp0azg4OUxJTVpVUUVDUVFDNDRYVjRqdEwwcjFkcQpjY1ByTlIrTEp4UjExMkJPMEhXLzduRVEwQUtUbUhIZ2EvbmV1ejMycHF1TVNRM2xodXRTNW5kanNzdmJ3dHJuCjNWdVhKRUJaQWtFQTJIQ1E0bE12MHI5Y3B2b2lCTVR0cDlYS2dIeU5Vbmd3dE1SODZ6VE0vK1dudlhTWjlDZk8KWXhyMlVvd2daMTlPNXpCZDFrVGRZQnNMbFVoL2syekI0UUpBWWtMeVBIRXNqZi9qWmgreEVZSGFrZ3JqUlA2RApvV0FLTlVoMXI0bmUxTE5oVXZZUWgrRGN2Z3MzZ2dnUjZyd2F0cVRuTDRZSDgzVk5BNDhTN3ZIRmdRSkFkeFZvCkFiNDNQOExkM1ZrZVFuVi9OS3FpSWhObFJneXU3Nlp6L0kwdWhWVDc5M2NpQlgycFJrbmRZUW1NQXBRanUzdVgKQlg4YU5maHJaUlZnYStLWXdRSkFYY1RKemE3ODNFeVk1YmxTZWIvWlJGYzZjdnFERDlRSDRXRVQ1b000ZjFnWgprZlI3Ti9qcEc4b09sZkl5d2o1RStaaHJaSTlEY1RmQjVnQWlFRHFrQmc9PQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ=='

enc3 = 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHZk1BMEdDU3FHU0liM0RRRUJBUVVBQTRHTkFEQ0JpUUtCZ1FDY1Q0WmpZbkdpTVl0RWQ3Ky9ZdEZnR0UzZQpnVGtXQml3aFdDbjQxTFBTWXN1cSs0T1FwbkJNWVI1WXRMYjk0V083aTZ2R2FPT05zc0hOZFlBZG5SRE04aUxTCnYvclQwdU90Z1N3ZFpOaUxDN242Z0gvODhSakZRRUxqbUpXUXpnc1g4Q1VxZFpvNEpyTWZCU213d0RZQTVCbTAKYjc2Z3ptcWgreUxYYSt1bk9RSURBUUFCCi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ=='

f1 = open('enc1', 'w')
f1.write(base64.b64decode(enc1))

f2 = open('enc2', 'w')
f2.write(base64.b64decode(enc2))

f3 = open('enc3', 'w')
f3.write(base64.b64decode(enc3))

~~~

Well, Let's see files. `enc1` is encrypted file, `enc2` is private.pem file, `enc3` is public.pem file. Encryption method is RSA.

~~~

$ python ./Band\ Aid.py

$ cat enc1
/�|z9oT�>&�/�">%��退��_LS
�|Dd@���u�ْB�����
                    C��	��P���N�'��:���� ����1j2���r�f���m�,�Iei��CC$��?s÷^=��R��Ǔ^

$ cat enc2
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCcT4ZjYnGiMYtEd7+/YtFgGE3egTkWBiwhWCn41LPSYsuq+4OQ
pnBMYR5YtLb94WO7i6vGaOONssHNdYAdnRDM8iLSv/rT0uOtgSwdZNiLC7n6gH/8
8RjFQELjmJWQzgsX8CUqdZo4JrMfBSmwwDYA5Bm0b76gzmqh+yLXa+unOQIDAQAB
AoGAacaS/Zw3o3d9c/bJJj07zJiF0WWG+PVyVZowxPdDPMKoamtLa86FvdoWzBZ2
orUsZVSuCFUgb9ogteWmreOE4uwAP+DF+2iSXt2VqLGIgobx6boF+NKc1soQADhT
6L6zfMK1MW6pH5XPcU5H8AMSYDDaQqxEmXJtk889LIMZUQECQQC44XV4jtL0r1dq
ccPrNR+LJxR112BO0HW/7nEQ0AKTmHHga/neuz32pquMSQ3lhutS5ndjssvbwtrn
3VuXJEBZAkEA2HCQ4lMv0r9cpvoiBMTtp9XKgHyNUngwtMR86zTM/+WnvXSZ9CfO
Yxr2UowgZ19O5zBd1kTdYBsLlUh/k2zB4QJAYkLyPHEsjf/jZh+xEYHakgrjRP6D
oWAKNUh1r4ne1LNhUvYQh+Dcvgs3gggR6rwatqTnL4YH83VNA48S7vHFgQJAdxVo
Ab43P8Ld3VkeQnV/NKqiIhNlRgyu76Zz/I0uhVT793ciBX2pRkndYQmMApQju3uX
BX8aNfhrZRVga+KYwQJAXcTJza783EyY5blSeb/ZRFc6cvqDD9QH4WET5oM4f1gZ
kfR7N/jpG8oOlfIywj5E+ZhrZI9DcTfB5gAiEDqkBg==
-----END RSA PRIVATE KEY-----

$ cat enc3
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCcT4ZjYnGiMYtEd7+/YtFgGE3e
gTkWBiwhWCn41LPSYsuq+4OQpnBMYR5YtLb94WO7i6vGaOONssHNdYAdnRDM8iLS
v/rT0uOtgSwdZNiLC7n6gH/88RjFQELjmJWQzgsX8CUqdZo4JrMfBSmwwDYA5Bm0
b76gzmqh+yLXa+unOQIDAQAB
-----END PUBLIC KEY-----

~~~

To decode this rsa-encrypted file, I use openssl command.

~~~

$ openssl rsautl -in enc1 -out /dev/tty -inkey enc2 -decrypt -oaep -raw
gigem{pirate_iter_v2_660c6b7aed3b905b}

~~~

**gigem{pirate_iter_v2_660c6b7aed3b905b}**
