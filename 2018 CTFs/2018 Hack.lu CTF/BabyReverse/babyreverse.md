# **BabyReverse**

#### tag : reversing, writeup, Hack.lu-CTF-2018

-----------------------------------------------

#### Description

>Hey there!
>
>Disclaimer: This chall is intended for new gamers only ;-)! You veterans got plenty of other Challenges which will keep you busy, so please pass this Challenge to someone, who never or rarely reversed before! We encourage everyone who never reversed anything to try this challenge. We believe in you and your future reversing skills =). You CAN do it!
>
>The task is to find the correct input which will be the flag. See the challenge files for more instructions.

-----------------------------------------------

#### Solution

I can download chall binary(.elf) with commented notes. In notes, some tips to solve this challenge.

~~~

Hey there, future Reverser!

We created this small challenge to introduce you to reversing. This task might _still_ take quite some time, but trust us, it will be very rewarding!
We sadly can't spoonfeed you, but we created a set of questions which you might want to answer yourself. We expect you to google on your own and find resources.

...

There is a lot of work ahead of you, and maybe some sleepless nights with a lot of googling - but it will be worth it;-)!
We are certain that with a dedicated mind you can solve this task and from there on you'll be ready for a bright future!
Don't give up, we all have been there. Stick to it and you'll be rewarded =)

~~~

Let's see binary. It's 64bit elf file, and it requires key string.   

~~~

$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped

$ ./chall
Welcome to this Chall!
Enter the Key to win: epist

~~~

Ok, Let's analyze binary. In `start`, it jumps to `0x4000D2`, and in `0x4000D2`, it calls `sub_400082` function which is main routine.

~~~

.text:0000000000400080     public start
.text:0000000000400080     start proc near
.text:0000000000400080 000 jmp     short loc_4

...

.text:00000000004000D2     loc_4000D2:
.text:00000000004000D2 000 call    sub_400082

~~~

First in `sub_400082`, it write welcome and read key. Well, `rsi` will be `0x4000d7` which is pushed when `call sub_400082`. And at offset:`0x4000d7`, "Welcome to..." is found. And it will be re-written by sys_read.

~~~

.text:0000000000400082     sub_400082 proc near
.text:0000000000400082 000 xor     rax, rax
.text:0000000000400085 000 inc     al
.text:0000000000400087 000 xor     rdi, rdi
.text:000000000040008A 000 inc     rdi             ; fd(1)
.text:000000000040008D 000 pop     rsi             ; buf(0x4000d2)
.text:000000000040008E -08 mov     dl, 2Eh         ; count(0x2e)
.text:0000000000400090 -08 syscall                 ; LINUX - sys_write(1)
.text:0000000000400092 -08 sub     al, 2Eh
.text:0000000000400094 -08 dec     edi             ; fd(0)
.text:0000000000400096 -08 syscall                 ; LINUX - sys_read(0)


00000000004000D0  EB 34 E8 AB FF FF FF 57  65 6C 63 6F 6D 65 20 74  .......Welcome t
00000000004000E0  6F 20 74 68 69 73 20 43  68 61 6C 6C 21 20 0A 45  o this Chall! .E
00000000004000F0  6E 74 65 72 20 74 68 65  20 4B 65 79 20 74 6F 20  nter the Key to
0000000000400100  77 69 6E 3A 20 00 31 C0  B0 3C 0F 05 0A 0D 06 1C  win: .1..<......

~~~

After reading key, It calculates `xor input[i], input[i+1]`. So, at offset:`0x4000d7`, key string computed by xor.

~~~

.text:0000000000400098     loc_400098:
.text:0000000000400098 -08 movzx   rdi, byte ptr [rsi+1]
.text:000000000040009D -08 xor     [rsi], rdi
.text:00000000004000A0 -08 inc     rsi
.text:00000000004000A3 -08 dec     rdx
.text:00000000004000A6 -08 jnz     short loc_

~~~

After xor routine, It compares `0x40010c(rdi) : 0x4000d7(buf)+0x2e(key_length)+7`, `0x4000d7(rsi) : 0x40010c(rdi)-0x35`. And if not same, it calls exit in `loc_400106`.

~~~

.text:00000000004000A8 -08 and     ecx, 2Eh
.text:00000000004000AB -08 add     cl, 26h
.text:00000000004000AE -08 lea     rdi, [rsi+7]
.text:00000000004000B2 -08 lea     rsi, [rdi-35h]
.text:00000000004000B6 -08 repe cmpsb
.text:00000000004000B8 -08 test    rcx, rcx
.text:00000000004000BB -08 jnz     short near ptr loc_400105+1

Breakpoint *0x4000b6            ; Well, in gdb, I can check rdi, rsi easily.
pwndbg> i r rip rdi rsi
rip            0x4000b6	0x4000b6
rdi            0x40010c	4194572
rsi            0x4000d7	4194519

~~~

After, checking comparing. If key is corret, It'll print 'Yay!'.

~~~

.text:00000000004000BD -08 xor     al, 2Fh
.text:00000000004000BF -08 push    '!yaY'
.text:00000000004000C4 000 mov     rsi, rsp        
.text:00000000004000C7 000 mov     dl, 4
.text:00000000004000C9 000 mov     edi, 1          
.text:00000000004000CE 000 syscall                 
.text:00000000004000D0 000 jmp     short near ptr loc_40

~~~

Ok, binary analyzing is done. Let's solve this.

Here is data in `0x40010c`. It have to be key string computed by xor.

~~~
pwndbg> x/46bx 0x40010c
0x40010c:	0x0a	0x0d	0x06	0x1c	0x22	0x38	0x18	0x26
0x400114:	0x36	0x0f	0x39	0x2b	0x1c	0x59	0x42	0x2c
0x40011c:	0x36	0x1a	0x2c	0x26	0x1c	0x17	0x2d	0x39
0x400124:	0x57	0x43	0x01	0x07	0x2b	0x38	0x09	0x07
0x40012c:	0x1a	0x01	0x17	0x13	0x13	0x17	0x2d	0x39
0x400134:	0x0a	0x0d	0x06	0x46	0x5c	0x7d
~~~

It's my solution script.

```python
# Data in 0x40010c. Encrypted key.
key = [\
0x0a,0x0d,0x06,0x1c,0x22,0x38,0x18,0x26,\
0x36,0x0f,0x39,0x2b,0x1c,0x59,0x42,0x2c,\
0x36,0x1a,0x2c,0x26,0x1c,0x17,0x2d,0x39,\
0x57,0x43,0x01,0x07,0x2b,0x38,0x09,0x07,\
0x1a,0x01,0x17,0x13,0x13,0x17,0x2d,0x39,\
0x0a,0x0d,0x06,0x46,0x5c,0x7d]

# In description, correct key is will be flag. So, key will be printable.
possible = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Xor key[i], key[i+1] routine.
for x in possible:
    r = [ord(x)]
    for k in key:
        r += [r[-1] ^ k]
    r = ''.join([chr(i) for i in r])

    # Find flag format.
    if 'flag' in r:
        print r
        break

# flag{Yay_if_th1s_is_yer_f1rst_gnisrever_flag!}\x00

```

**flag{Yay_if_th1s_is_yer_f1rst_gnisrever_flag!}**
