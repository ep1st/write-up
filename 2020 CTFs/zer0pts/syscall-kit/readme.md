# **syscall kit**

#### tag : pwn, hard(671p)

-----------------------------------------------

#### Description

>It's a good tool to learn syscall, isn't it?

>nc 18.179.178.246 9006

-----------------------------------------------

#### TL;DR;

1. use brk syscall to leak heap address.
2. use readv and writev syscall to leak pie address.
3. use mprotect and overwite call exit in main to shellcode.

-----------------------------------------------

#### Solution

Solution script is [here](./solve.py).