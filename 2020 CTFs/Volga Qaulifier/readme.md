# **Notepad—**

#### tag : pwn

-----------------------------------------------

#### Description

>Notepad-- is the app to store your most private notes, with an extremely lightweight UI. Check it out!

>notepad

>nc notepad.q.2020.volgactf.ru 45678

-----------------------------------------------

#### TL;DR;

1. allocate tab - big size chunk and free size to leak libc
2. allocate note - with fake chunk(fake tab) by name of note
3. overwrite __free_hook and call one_gadget

-----------------------------------------------

#### Solution

Solution script is [here](./solve.py).