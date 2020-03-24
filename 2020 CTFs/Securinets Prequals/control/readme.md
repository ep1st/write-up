# **control**

#### tag : pwn(930p)

-----------------------------------------------

#### Description

>Everything, Everything ...

>nc 54.225.38.91 1026

>Authors : KERRO & Anis_Boss

-----------------------------------------------

#### TL;DR;

1. use fsb to overwrite `v1` and `v2` in bss.
2. use fsb to leak libc base and fuzz for finding offset that return `\x7fELF`.
3. use `DynELF` to find `system` in libc.
4. use stack-pivot and call `system` with `/bin/sh`.

-----------------------------------------------

#### Solution

Solution script is [here](./solve.py).