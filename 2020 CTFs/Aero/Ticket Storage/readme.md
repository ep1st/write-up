# **Ticket Storage**

#### tag : PWN(366p)

-----------------------------------------------

#### Description

Missing. Server dosen't up after ended.

-----------------------------------------------

### TL;DR

1. allocate 8 chunks for writting chunks addresss to bss
2. change `name` to set fake chunk and to use overflow and overwrite first chunk address to `name`
3. leak addresss by using view list menu
4. get flag from heap base adress + 144

-----------------------------------------------

#### Solution

[Solution script](./solve.py) is here.