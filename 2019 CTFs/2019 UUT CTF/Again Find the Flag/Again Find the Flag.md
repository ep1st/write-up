# **Again Find the Flag**

#### tag : reversing, agnr

-----------------------------------------------

#### Description

>> Run, enter correct password and capture the flag.
>>
>> Flag is MD5 of the correct password:
>>
>> UUTCTF{MD5(Correct Password)}

-----------------------------------------------

#### Solution

I'm really lazy so that I use automation.

```python
import angr
import claripy

proj = angr.Project("./chal_re_med.so", load_options={"auto_load_libs":False})
argv1 = claripy.BVS("argv1", 100*8)
initial_state = proj.factory.entry_state(args=["./chal_re_med.so", argv1])

pg = proj.factory.simgr(initial_state)
pg.explore(find=0xad5+0x400000, avoid=0xaa4+0x400000)
print pg.found[0].state.se.any_str(argv1)
```

Result of angr is here.

~~~
$ p solve.py 
WARNING | 2019-04-27 20:22:26,622 | angr.analyses.disassembly_utils | Your verison of capstone does not support MIPS instruction groups.
WARNING | 2019-04-27 20:22:26,693 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
Deprecation warning: Use eval(expr, cast_to=str) instead of any_str
1721_3222_8899_5634
~~~

~~~
$ ./chal_re_med.so 1721_3222_8899_5634

You entered it right! Congratulations
~~~

**UUTCTF{98fc3a42de98bde8eb894c05cea34bfb}**
