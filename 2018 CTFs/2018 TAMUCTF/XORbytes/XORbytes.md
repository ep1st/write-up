# **XORbytes**

#### tag : crypto

-----------------------------------------------

#### Description

>Looks like there is a flag here...if only you could run the binary.

-----------------------------------------------

#### Solution

I can get just data binary from prob.

~~~

$ file hexxy
hexxy: data

~~~

First, I guess this file is elf file. But this file is encrypted by xor.

Key is `QB1g3l4B5uzPjjD4` for xor encryption. 

~~~

$ xxd hexxy
00000000: 2e07 7d21 316d 3542 3575 7a50 6a6a 4434  ..}!1m5B5uzPjjD4
00000010: 5242 0f67 326c 3442 5570 7a50 6a6a 4434  RB.g2l4BUpzPjjD4
00000020: 1142 3167 336c 3442 b56c 7a50 6a6a 4434  .B1g3l4B.lzPjjD4
00000030: 5142 3167 736c 0c42 3c75 3a50 776a 5834  QB1gsl.B<u:PwjX4
00000040: 5742 3167 366c 3442 7575 7a50 6a6a 4434  WB1g6l4BuuzPjjD4
00000050: 1142 3167 336c 3442 7575 7a50 6a6a 4434  .B1g3l4BuuzPjjD4
00000060: a943 3167 336c 3442 cd74 7a50 6a6a 4434  .C1g3l4B.tzPjjD4
00000070: 5942 3167 336c 3442 3675 7a50 6e6a 4434  YB1g3l4B6uzPnjD4
00000080: 6940 3167 336c 3442 0d77 7a50 6a6a 4434  i@1g3l4B.wzPjjD4
00000090: 6940 3167 336c 3442 2975 7a50 6a6a 4434  i@1g3l4B)uzPjjD4
000000a0: 4d42 3167 336c 3442 3475 7a50 6a6a 4434  MB1g3l4B4uzPjjD4
000000b0: 5042 3167 366c 3442 3575 7a50 6a6a 4434  PB1g6l4B5uzPjjD4
000000c0: 5142 3167 336c 3442 3575 7a50 6a6a 4434  QB1g3l4B5uzPjjD4
000000d0: 294a 3167 336c 3442 4d7d 7a50 6a6a 4434  )J1g3l4BM}zPjjD4
000000e0: 5142 1167 336c 3442 3475 7a50 6c6a 4434  QB.g3l4B4uzPljD4
...

~~~

Here is decryption code.

~~~

key = 'QB1g3l4B5uzPjjD4'

f1 = open('hexxy', 'rb')
f2 = open('hexyy', 'wb')

enc = f1.read(16)

while enc != ''	:
	for i, j  in zip(enc,key):
		f2.write(chr(ord(i) ^ ord(j)))
	enc = f1.read(16)
			
f1.close()
f2.close()

~~~

Now, I can get normal elf file from encrypted data.

~~~

$ xxd ./hexyy
00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
00000010: 0300 3e00 0100 0000 6005 0000 0000 0000  ..>.....`.......
00000020: 4000 0000 0000 0000 8019 0000 0000 0000  @...............
00000030: 0000 0000 4000 3800 0900 4000 1d00 1c00  ....@.8...@.....
00000040: 0600 0000 0500 0000 4000 0000 0000 0000  ........@.......
00000050: 4000 0000 0000 0000 4000 0000 0000 0000  @.......@.......
00000060: f801 0000 0000 0000 f801 0000 0000 0000  ................
00000070: 0800 0000 0000 0000 0300 0000 0400 0000  ................
00000080: 3802 0000 0000 0000 3802 0000 0000 0000  8.......8.......
00000090: 3802 0000 0000 0000 1c00 0000 0000 0000  8...............
000000a0: 1c00 0000 0000 0000 0100 0000 0000 0000  ................
000000b0: 0100 0000 0500 0000 0000 0000 0000 0000  ................
000000c0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000000d0: 7808 0000 0000 0000 7808 0000 0000 0000  x.......x.......
000000e0: 0000 2000 0000 0000 0100 0000 0600 0000  .. .............
...

~~~

~~~

$ hexyy 
Congrats! You found the flag!
GigEm{NibblerEatsNibbles}

~~~

**GigEm{NibblerEatsNibbles}**
