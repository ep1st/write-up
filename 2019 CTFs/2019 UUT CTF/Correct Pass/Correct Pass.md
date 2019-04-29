# **Correct Pass**

#### tag : reversing, angr

-----------------------------------------------

#### Description

>> Find the correct password in order to access the flag.

-----------------------------------------------

#### Solution

I'm really lazy so that I use automation.

```python
import angr

proj = angr.Project("./pass", load_options={"auto_load_libs":False})
pg = proj.factory.simgr()
pg.explore(find=0x8048A99, avoid=[0x08048A5F,0x08048A23,0x080489E7,0x080489AB,0x0804896F,0x08048AC4])

print pg.found[0].state.posix.dumps(0)
```

Result of angr is here.

~~~
$ p solve.py 
WARNING | 2019-04-29 12:49:14,586 | angr.analyses.disassembly_utils | Your verison of capstone does not support MIPS instruction groups.
Awesome_M0v!!;-)
~~~

~~~
$ ./pass 
[*] Enter the flag:Awesome_M0v!!;-)
[*] Flag: UUTCTF{MD5(Awesome_M0v!!;-))}
~~~

**UUTCTF{7e7d9d8d6a7ad4a2b3d0f0b4abc1d9bf}**
