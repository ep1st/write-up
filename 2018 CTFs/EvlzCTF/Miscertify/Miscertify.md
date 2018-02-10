# **Miscertify**

#### tag : reversing

-----------------------------------------------

#### Description

>>https://goo.gl/bcaJFt

>>nc 35.200.197.38 8000
>>Go get flag

>>Europe: nc 35.231.8.67 8000

-----------------------------------------------

#### Solution

~~~

$ file miscertify
miscertify: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=eea559d062b08b1d8d0840277157222ea94f0bf0, stripped

~~~

Prob file have simple functions(create, read, sign).

~~~

$ ./miscertify
Hello User, Enter name:	guest
Choose your option
	1.Create file
	2.Read file
	3.Sign file
	>>>

~~~

Well, I can find flag is allocated in memory from flag file named `flag.flag`.

~~~

...
v0 = sub_401AF4(8LL, 4LL);
sub_42F700(&v13, "flag.flag", (unsigned int)v0);
sub_403220(&v13, &unk_78FDE0);
...

~~~

I know flag file's name, So I trying to read flag file from prob like this:

~~~

$ nc 35.200.197.38 8000
Hello User, Enter name:	guest
Choose your option
	1.Create file
	2.Read file
	3.Sign file
	>>>2
Enter filename:	flag.flag
evlz{intended_mistake}ctf
Choose your option
	1.Create file
	2.Read file
	3.Sign file
	>>>

~~~

**evlz{intended_mistake}ctf**
