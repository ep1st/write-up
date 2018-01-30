# **vuln-chat**

#### tag : pwnable

------------------------------------------------------

#### Description

>One of our informants goes by the handle djinn. He found some information while working undercover inside an organized crime ring. Although we've had trouble retrieving this information from him. He left us this chat client to talk with him. Let's see if he trusts you...

>nc vulnchat.tuctf.com 4141

>vuln-chat - md5: 5d081990e899864c9dc85b1cf255af6e

------------------------------------------------------

#### Solution

vuln-chat's main code from ida:

~~~

int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [sp+3h] [bp-2Dh]@1
  char v5; // [sp+17h] [bp-19h]@1
  int v6; // [sp+2Bh] [bp-5h]@1
  char v7; // [sp+2Fh] [bp-1h]@1

  setvbuf(stdout, 0, 2, 0x14u);
  puts("----------- Welcome to vuln-chat -------------");
  printf("Enter your username: ");
  v6 = 0x73303325;
  v7 = 0;
  __isoc99_scanf(&v6, &v5);
  printf("Welcome %s!\n", &v5);
  puts("Connecting to 'djinn'");
  sleep(1u);
  puts("--- 'djinn' has joined your chat ---");
  puts("djinn: I have the information. But how do I know I can trust you?");
  printf("%s: ", &v5);
  __isoc99_scanf(&v6, &v4);
  puts("djinn: Sorry. That's not good enough");
  fflush(stdout);
  return 0;
}

~~~

vuln-chat's printFlag code from ida:

~~~

int printFlag()
{
  system("/bin/cat ./flag.txt");
  return puts("Use it wisely");
}

~~~

In this case, To exploit this program, I overwrite main's ret address to printFlag's address.

There is two scanf in code. I have to use two scanf in correctly to overwrite ret address.

First scanf is for overwriting second scanf's format arguments where is bp-5h : 0x73303325 + 0x00 which mean "%30s". I can overwrite this value by parsing more than 20 byte in first scanf.

~~~

0xffffce20:	0x61616161	0x61616161	0x61616161	0x61616161
0xffffce30:	0x25616161	0x00733436

~~~

Second scanf is for overwriting ret of main. I find ret's offset is v4 + 0x36. I can overwrite ret address by parsing more than 54 byte in second scanf.

So, To parse more than 54 byte in second parsing, I have to modify format argument more bigger in first parsing.

I put 20 byte of dummy and format value 64 byte for overwriting ret in second parsing. And I put 54 byte of dummy and address of printFlag.

[Solution Script](./solve.py)
