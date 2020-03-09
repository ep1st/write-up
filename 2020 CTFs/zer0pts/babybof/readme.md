# **babybof**

#### tag : pwn, lunatic(590p)

-----------------------------------------------

#### Description

>Simple BOF with PIE/SSP disabled and libc disclosed. Who can't solve it?

>nc 18.179.178.246 9002

-----------------------------------------------

#### TL;DR;

1. use leave;ret gadget to set rsp to bss.
2. overwrite stderr's 3byte to oneshot gadget - it will be 20bit bruteforce.
3. use ret to call oneshot gagdet.

-----------------------------------------------

#### Solution

Solution script is [here](./solve.py).