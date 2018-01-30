# **hello**

#### tag : reversing

-----------------------------------------------

#### Description

>No Description

-----------------------------------------------

#### Solution

This program is linux 64 bit ELF, but there is error warnning.

~~~

$ file hello
hello: ERROR: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=b8ccefeffb8978b2289ec31802396333def9dfad error reading (Invalid argument)

~~~

Well, Maybe there is some trick to anti-dubugging skill. I can't read section's header in correctly.

~~~

$ readelf -h hello
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x4006f0
  Start of program headers:          64 (bytes into file)
  Start of section headers:          8696 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         9
  Size of section headers:           64 (bytes)
  Number of section headers:         25901
  Section header string table index: 27
readelf: Error: Reading 0x194b40 bytes extends past end of file for section headers

~~~

~~~

pwndbg> file ./hello
"/home/epist/Desktop/0x00/reversing/./hello": not in executable format: File truncated
pwndbg> run
Starting program:  
No executable file specified.
Use the "file" or "exec-file" command.

~~~

Um.. So, What can I do? - there is two way to solve this problem. first one is edit section's header in correct. And another one is static debugging(which don't need section's information).

In this case, I use IDA debugger. When I open this program by IDA, I get message SHT table size or offset is invalid. Continue?- but that's not matter, I just click continue.

And I can get this pseudocode in `sub_40084E`:

~~~

if ( (off_602088 ^ *a1) == 48 )
  {
    if ( (BYTE1((*off_602088)[0]) ^ *(a1 + 1)) == 120 )
    {
      if ( (BYTE2((*off_602088)[0]) ^ *(a1 + 2)) == 48 )
      {
        if ( (BYTE3((*off_602088)[0]) ^ *(a1 + 3)) == 48 )
        {
          if ( (BYTE4((*off_602088)[0]) ^ *(a1 + 4)) == 67 )
          {
            if ( (BYTE5((*off_602088)[0]) ^ *(a1 + 5)) == 84 )
            {
              if ( (BYTE6((*off_602088)[0]) ^ *(a1 + 6)) == 70 )
              {
                if ( (BYTE7((*off_602088)[0]) ^ *(a1 + 7)) == 123 )
                {
                  for ( i = 0; i < dword_602080; ++i )
                  {
                    buf = *((((((i >> 32) >> 29) + i) & 7) - ((i >> 32) >> 29)) + a1) ^ *(off_602088 + i);
                    write(1, &buf, 1uLL);
                  }
                  exit(1);
                ...
~~~

Well, [120, 48, 48, 67, 84, 70, 123] is '0x00CTF{' in ascii. So, I can guess this code generate key of this program. I trace `off_602088` - instruct `dq offset qword_400C18`.

~~~

LOAD:0000000000602088 off_602088      dq offset qword_400C18

~~~

~~~

LOAD:0000000000400C18 qword_400C18    dq 5A12640444791601h, 16605372212F0C01h, 7B60623324162A02h

~~~

I make simple python script to generate key.

~~~

#!/usr/bin/env python

keyset = '5A12640444791601'
flag = '0x00CTF{'
password = ''

key = [keyset[i:i+2] for i in range(0, len(keyset), 2)]
key.reverse()

for x,y in enumerate(key):
	password += str(chr(int(ord(flag[x]))^int(y,16)))

print password

~~~

~~~

$ python ./hellokey.py
1nItG0T!

~~~

Yeah, key is `1nItG0T!`

~~~

$ ./hello
Welcome to the Twinlight Zone!!!
Password: 1nItG0T!
0x00CTF{0bfU5c473D_PtR4Z3}

~~~

**0x00CTF{0bfU5c473D_PtR4Z3}**
