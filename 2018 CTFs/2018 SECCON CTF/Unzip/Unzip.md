# **Unzip**

#### tag : forensic, writeup, SECCON-2018-Online-CTF

-----------------------------------------------

#### Description

>Unzip flag.zip.


-----------------------------------------------

#### Solution

I can get shell script and encrypted zip file. And shell script encrypt flag.txt to zip file by password which is local time.

~~~

echo 'SECCON{'`cat key`'}' > flag.txt
zip -e --password=`perl -e "print time()"` flag.zip flag.txt

~~~

Well, zipinfo tell me when flag.zip is compressed. `18-Oct-26 08:10` is time when compressed. So, I change my system local time to it and location to Tokyo. (I tried to set 08:08's time because of any mistake)

~~~

$ zipinfo flag.zip
Archive:  flag.zip
Zip file size: 225 bytes, number of entries: 1
-rw-r--r--  3.0 unx       32 TX defN 18-Oct-26 08:10 flag.txt
1 file, 32 bytes uncompressed, 31 bytes compressed:  3.1%

~~~

~~~

$ date
Fri Oct 26 20:08:00 JST 2018

~~~

And I can get time()'s result when `08:08`. Ok, let's bruteforce. I use `fcrackzip` to bruteforce. And I set first number to `1540552143`, so It tried all number in range of `1540552143~`.

~~~

$ echo `perl -e "print time()"`
1540552143

~~~

~~~

$ fcrackzip -u -p 1540552143 -c 1 ./flag.zip


PASSWORD FOUND!!!!: pw == 1540566641

~~~

Good, I can get password `1540566641`.

~~~

$ unzip flag.zip
Archive:  flag.zip
[flag.zip] flag.txt password:

$ cat flag.txt
SECCON{We1c0me_2_SECCONCTF2o18}

~~~

**SECCON{We1c0me_2_SECCONCTF2o18}**
