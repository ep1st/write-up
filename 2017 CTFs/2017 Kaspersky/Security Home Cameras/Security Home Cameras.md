# **Security Home Cameras**

#### tag : crypto

--------------------------------------------------

#### Description

>The smart home system has the function of remote monitoring of what is happening in the home and every few minutes sends pictures of the surveillance cameras to the owner of the house. You successfully intercepted the network traffic of this system, however, its creators took care of the security of their users data and encrypted the pictures. Descrypt the provided image and you will find the flag.

--------------------------------------------------

#### Challenge

I get a png file named secret_encrypted from link. and find it isn't opened.

~~~

epist@epist-machine:~$ hexdump -C secret_encrypted.png
00000000  76 af b1 b8 f2 f5 e5 f5  ff ff ff f2 b6 b7 bb ad  |v...............|
00000010  ff ff fa e1 ff ff fe be  f7 fd ff ff ff 61 55 db  |.............aU.|
00000020  de ff ff ff fe 8c ad b8  bd ff 51 31 e3 16 ff ff  |..........Q1....|
00000030  ff fb 98 be b2 be ff ff  4e 70 f4 03 9e fa ff ff  |........Np......|
00000040  ff f6 8f b7 a6 8c ff ff  ed 8b ff ff ed 8b fe 21  |...............!|
00000050  99 e0 87 ff ff de f8 b6  bb be ab 87 a1 12 22 c4  |..............".|
00000060  91 dc 40 65 c8 1f ec f2  73 d0 97 73 7e f1 63 e7  |..@e....s..s~.c.|
...

~~~

I investigate this png file by hexdump. and find there is no png magic number. Well, I can figure out that all byte is calculated by XOR operand.

~~~

76 af b1 b8 magic number of encrypted file
89 50 4e 47 magic number of normal png

~~~

So, I have to XOR all byte of encrypted png file.

--------------------------------------------------

#### Solution

**solve.c**

~~~

#include <stdio.h>
#include <stdlib.h>

int main(void) {
	unsigned char byte;

	FILE* f_in 	= fopen("secret_encrypted.png","rb");
	FILE* f_out	= fopen("output.png","wb");

	while((byte = fgetc(f_in))!=EOF) {
		byte = ~byte;
		fputc(byte, f_out);
	}
	fclose(f_in);
	fclose(f_out);
	return 0;
}

~~~

![img1](./output.png)

**KLCTF{it_was_just_atbash_encryption}**
