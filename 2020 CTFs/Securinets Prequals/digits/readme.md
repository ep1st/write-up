# **digits**

#### tag : pwn(968p)

-----------------------------------------------

#### Description

>Just another pwnable...

>nc 54.225.38.91 1027

>Authors : KERRO && Anis_Boss

-----------------------------------------------

#### TL;DR;

1. use significant bit trick to read more bytes.
2. use rop to leak libc base and fuzz for finding offset that return `\x7fELF`.
3. use `DynELF` to find `system` in libc.
4. use `csu` gadget to read `/bin/sh` and call `system` with `/bin/sh`.

-----------------------------------------------

#### Solution

I used `libc-2.11.1.so` but it's not correct libc, prob use own's libc so you can't find it in libc-databse.

Solution script is [here](./solve.py).