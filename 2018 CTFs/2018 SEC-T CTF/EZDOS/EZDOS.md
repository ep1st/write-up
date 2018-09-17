# **EZDOS**

#### tag : reversing, dos, emulating

-----------------------------------------------

#### Description

>They told me you were old-school, great! Have a look at this license-server as a warm-up
>
>Service: nc 142.93.38.98 7777 | nc rev.sect.ctf.rocks 7777
>
>Download: ezdos.tar.gz
>
>Author: likvidera

-----------------------------------------------

#### Solution

In `seg000:0112`, dx will be 0x0d. And then in `seg000:0121`, compare cx, dx. It means that serial key's length will be 0x0d.

~~~

seg000:0100                 public start
seg000:0100 start           proc near
seg000:0100                 mov     ah, 9
seg000:0102                 mov     dx, 1DDh
seg000:0105                 int     21h             ; DOS - PRINT STRING
seg000:0105                                         ; DS:DX -> string terminated by "$"
seg000:0107                 mov     dx, 214h
seg000:010A                 int     21h             ; DOS -
seg000:010C                 mov     cx, 0
seg000:010F                 mov     bx, 2000h
seg000:0112                 mov     dx, 0Dh

seg000:0115 readSerialKey:                          ; CODE XREF: start+23j
seg000:0115                 mov     ah, 1
seg000:0117                 int     21h             ; DOS - KEYBOARD INPUT
seg000:0117                                         ; Return: AL = character read
seg000:0119                 cmp     al, 0Ah
seg000:011B                 jz      short initReadData
seg000:011D                 mov     [bx], al
seg000:011F                 inc     bx
seg000:0120                 inc     cx
seg000:0121                 cmp     cx, dx
seg000:0123                 jnz     short readSerialKey

...

~~~

After reading 0x0d byte, Program set bx to 2000h which is input data's offset and set ax to 268h which is data's offset of `1337SHELL`.

~~~

seg000:0125 initReadData:                           ; CODE XREF: start+1Bj
seg000:0125                 mov     cx, 0
seg000:0128                 mov     bx, 2000h
seg000:012B                 mov     ax, 26Bh
seg000:012E                 mov     dx, 4

1000:0258  72 65 73 73 20 45 4E 54  45 52 20 74 6F 20 65 78  ress ENTER to ex
1000:0268  69 74 24 31 33 33 37 53  48 45 4C 4C              it$1337SHELL

~~~

Then, compare input data and `1337` in 4 loop. So, First 4 byte of serial will be `1337`.

~~~

seg000:0131 checkFrontSerial:                       ; CODE XREF: start+46j
seg000:0131                 push    cx
seg000:0132                 xor     cx, cx
seg000:0134                 mov     cl, [bx]
seg000:0136                 xchg    ax, bx
seg000:0137                 mov     ch, [bx]
seg000:0139                 xchg    ax, bx
seg000:013A                 cmp     cl, ch
seg000:013C                 jnz     serialFailed
seg000:0140                 pop     cx
seg000:0141                 inc     cx
seg000:0142                 inc     bx
seg000:0143                 inc     ax
seg000:0144                 cmp     cx, dx
seg000:0146                 jnz     short checkFrontSerial

~~~

Next step, just dl have to be 0x2d in char('-'). So serial will be `1337-`.

~~~

seg000:0148                 xor     dx, dx
seg000:014A                 mov     dl, [bx]
seg000:014C                 cmp     dl, 2Dh         
seg000:014F                 jnz     short serialFailed

~~~

Last step, this routine use xor calculating to check serial. Well, `SHELL` will be cl one byte by one byte in loop. So `0x66 ^ 'S' = Serial[5]` that serial[5] will be '5'. and serial[6] will be '1', serial[7] will be '1', serial[8] will be '5'.

Finally I can get serial that `1337-5115`.

*check) First, I talked serial key's length will be 0x0d but it's not. It just compare 9byte of serial.*

~~~

seg000:0151                 inc     bx
seg000:0152                 xor     cx, cx
seg000:0154                 mov     cl, [bx]
seg000:0156                 xchg    ax, bx
seg000:0157                 mov     ch, [bx]
seg000:0159                 xchg    ax, bx
seg000:015A                 xor     cl, ch
seg000:015C                 cmp     cl, 66h
seg000:015F                 jnz     short serialFailed

... (repeat)

seg000:016D                 cmp     cl, 79h
seg000:0170                 jnz     short serialFailed

... (repeat)

seg000:017E                 cmp     cl, 74h
seg000:0181                 jnz     short serialFailed

... (repeat)

seg000:018F                 cmp     cl, 79h
seg000:0192                 jnz     short serialFailed

~~~

Well, After checking serial, It will read flag in server, and then print to me!

~~~

seg000:0194                 mov     ah, 9
seg000:0196                 mov     dx, 236h
seg000:0199                 int     21h             ; DOS - PRINT STRING
seg000:0199                                         ; DS:DX -> string terminated by "$"
seg000:019B                 mov     word ptr [bp+0], 6C66h
seg000:01A0                 mov     word ptr [bp+2], 6761h
seg000:01A5                 mov     word ptr [bp+4], 0
seg000:01AA                 mov     ax, 3D00h
seg000:01AD                 mov     dx, bp
seg000:01AF                 int     21h             ; DOS - 2+ - OPEN DISK FILE WITH HANDLE
seg000:01AF                                         ; DS:DX -> ASCIZ filename
seg000:01AF                                         ; AL = access mode
seg000:01AF                                         ; 0 - read
seg000:01B1                 mov     bx, ax
seg000:01B3                 mov     ah, 3Fh
seg000:01B5                 mov     cx, 18h
seg000:01B8                 int     21h             ; DOS - 2+ - READ FROM FILE WITH HANDLE
seg000:01B8                                         ; BX = file handle, CX = number of bytes to read
seg000:01B8                                         ; DS:DX -> buffer
seg000:01BA
seg000:01BA printFlag:                              ; CODE XREF: start+C3j
seg000:01BA                 mov     ah, 2
seg000:01BC                 mov     dl, [bp+0]
seg000:01BF                 int     21h             ; DOS - DISPLAY OUTPUT
seg000:01BF                                         ; DL = character to send to standard output
seg000:01C1                 inc     bp
seg000:01C2                 dec     cx
seg000:01C3                 jnz     short printFlag
seg000:01C5                 jmp     short exitProgram

~~~

~~~

$ nc rev.sect.ctf.rocks 7777
PRESS ENTER TWICE TO START THE LICENSE-SERVICE!!!
Note that DOS needs 25 lines. You might want to enlarge your
window before continuing.

Now type ENTER to start DOSEMU or <Ctrl>C to cancel




[dosemu cdrom driver installed (V0.2)]


Access to cdrom denied.
Installation aborted.

Kernel: allocated 41 Diskbuffers = 21812 Bytes in HMA
Z: = LINUX\FS\ attrib = READ ONLY

FreeCom version 0.84-pre2 XMS_Swap [Aug 28 2006 00:29:00]
Sound on: SB at 0x220-0x22f, IRQ=5, DMA8=1, DMA16=5. MPU-401 at 0x330-0x331.
D: = LINUX\FS/HOME/CTF attrib = READ/WRITE
Error 35 (network name not found)
while redirecting drive E: to LINUX\FS/MEDIA/CDROM
"Welcome to dosemu 1.4.0.8!"
About to Execute : CHALL.COM
######################
EZ DOS
######################
Enter license: 1337-5115
1337-5115

Correct! Here is your flag: SECT{K3YG3N_MU51C_R0CK5}
Press ENTER to exit

~~~

**SECT{K3YG3N_MU51C_R0CK5}**
