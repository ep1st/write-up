# **Assemble your way to the flag**

#### tag : reversing

-----------------------------------------------


#### Description

>My friend was trying out assembly for the first time, he has no clue what he's doing, help him out and procure your reward in the form of a flag :)

-----------------------------------------------

#### Solution

I find char table in main.

Disassembly of main:

~~~

int __cdecl main(int argc, const char **argv, const char **envp)
{
  printf(
    "Look for something else....\n",
    argv,
    envp,
    112LL,
    99LL,
    116LL,
    102LL,
    123LL,
    108LL,
    51LL,
    103LL,
    101LL,
    78LL,
    100LL,
    115LL,
    95LL,
    99LL,
    48LL,
    100LL,
    51LL,
    95LL,
    49LL,
    110LL,
    95LL,
    52LL,
    83LL,
    115LL,
    51LL,
    109LL,
    98LL,
    49LL,
    121LL,
    125LL);
  return 0;
}

~~~

This is solution script:

~~~

flag = [112,99,116,102,123,108,51,103,101,78,100,115,95,99,48,100,51,95,49,110,95,52,83,115,51,109,98,49,121,125]

print ''.join([chr(i) for i in flag])

~~~

~~~

$ python ./question.py
[*] flag is pctf{l3geNds_c0d3_1n_4Ss3mb1y}

~~~

**pctf{l3geNds_c0d3_1n_4Ss3mb1y}**
