# **BlindDate**

#### tag : misc

-----------------------------------------------

#### Description

>My mom got me a date with someone! she sent me an image but i cannot open it. I don't want it to be a blind date. Can you help me?

-----------------------------------------------

#### Solution

First, I find `BlindDate.jpeg` file is not opened in viewer, I use xxd and I can get file's magic byte is `e0 ff d8 ff`. Well, normal jpeg file's magic byte must be `ff d8 ff e0`. So, I think file's bytes are revered in each 4 bytes.

~~~

$ xxd BlindDate.jpeg | head
00000000: e0ff d8ff 464a 1000 0100 4649 6000 0101  ....FJ....FI`...
00000010: 0000 6000 2200 e1ff 6669 7845 4d4d 0000  ..`."...fixEMM..
00000020: 0000 2a00 0100 0800 0300 1201 0100 0000  ..*.............
00000030: 0000 0100 0000 0000 1100 ecff 6b63 7544  ............kcuD
00000040: 0001 0079 0000 0004 ff00 004b 687e 03e1  ...y.......Kh~..
00000050: 3a70 7474 736e 2f2f 6f64 612e 632e 6562  :pttsn//oda.c.eb
00000060: 782f 6d6f 312f 7061 002f 302e 7078 3f3c  x/mo1/pa./0.px?<
00000070: 656b 6361 6562 2074 3d6e 6967 bfbb ef22  ekcaeb t=nig..."
00000080: 6469 2022 3557 223d 704d 304d 6968 6543  di "5W"=pM0MiheC
00000090: 6572 7a48 544e 7a53 636b 7a63 3f22 6439  erzHTNzSckzc?"d9

~~~

I can recover the jpeg file by below code.

~~~

#recover.py

d = open('BlindDate.jpeg', 'rb').read()

r = ''.join(x[::-1] for x in [d[i:i+4] for i in range(0, len(d), 4)])

open('BlindDate.recover.jpeg', 'wb').write(r)

~~~

Ok, I can get correct jpeg image, But there is no valuable data on image, but there is zip file in image. And I extract hidden zip file from image.

~~~

$ binwalk -e BlindDate.recover.jpeg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
30            0x1E            TIFF image data, big-endian, offset of first image directory: 8
301           0x12D           Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
393           0x189           Unix path: /ns.adobe.com/xap/1.0/mm/" xmlns:stRef="http://ns.adobe.com/xap/1.0/sType/ResourceRef#" xmlns:xmp="http://ns.adobe.com/xap/1.0/"
38618         0x96DA          Zip archive data, encrypted at least v2.0 to extract, compressed size: 131, uncompressed size: 412, name: flag.txt
38915         0x9803          End of Zip archive

~~~

Good, There is flag.txt in zip file. But this zip file is locked. Actually I first tried to use john with fcrackzip, but that way is incorrect.

~~~

$ zipinfo 96DA.zip
Archive:  96DA.zip
Zip file size: 319 bytes, number of entries: 1
-rw-a--     3.1 fat      412 BX u099 18-Jul-10 21:43 flag.txt
1 file, 412 bytes uncompressed, 119 bytes compressed:  71.1%

~~~

Well, I go back to image, I find some base64 string before PK header start.

~~~

$ strings BlindDate.recover.jpeg | tail
\TMn
Z{F/fU
NL9H
v#U-
lj9B
Li4gICAuICAuLiAgLi4gICAuICAuLiAgLi4gICAuICAuLiAgLiAgLi4NCi4gICAgLiAgIC4gICAgICAgLiAgICAgIC4gICAgLiAgIC4gIC4gIA0KICAgIC4uICAgICAgICAgIC4uICAgICAgLiAgIC4uICAgICAgLiAgLgPK
flag.txt
K,S8
X: t
flag.txt

~~~

I can get `English Braille` from base64 string. I use [Braille Decode Site](https://www.dcode.fr/braille-alphabet) to read this code. And It mean `F4C3P4LM` will be password for zip.

~~~
$ python pass.py
..   .  ..  ..   .  ..  ..   .  ..  .  ..
.    .   .       .      .    .   .  .  
    ..          ..      .   ..      .  .
~~~

I can get another fucking encrypted code in flag.txt. It's brainfuck code, I use [Brainfuck Decode Site](https://www.dcode.fr/brainfuck-language) to get flag. And I can get flag!

~~~

++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++++++++++.+.+++++++++.<---.+++++++++++++++++.--------------.>+++.<+++++++++++++++++.<++++++++++++++++++.>>------.---------.--------.-----.++++++++++++++++++++++++++.<<.>>----.<++++++++.+++.>---------.<<+.>>++.<++.-----.+++++.<+++.>>++++++.<<-.>-----.<+.>.+++.>--------.<<---.>>++.<++.-----.+++++.<+++.>>++++++.<<-.++++++++++++.>>+++++++++.<<<++++++++++++++++++++++.

~~~

**noxCTF{W0uld_y0u_bl1nd_d4t3_4_bl1nd_d4t3?}**
