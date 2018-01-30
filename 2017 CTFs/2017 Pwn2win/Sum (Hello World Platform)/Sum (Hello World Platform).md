# **Sum (Hello World Platform)**

#### tag : PPC-M

----------------------------------------------------------------------

#### Description

>This problem is an example on how to connect to our server to read inputs and send the outputs for the programming challenges. Given a set of numbers greater than zero, followed by zero and a line break, compute the sum of these numbers. All you need to do in order to obtain the flag is to execute the implementation you see more fit!

----------------------------------------------------------------------

#### Challenge

I can get 3 items in zip downloaded in link.

~~~

#!/usr/bin/python2
import ssl, socket

class Connect(object):
    def __init__(self, host, port):
        self.context = ssl.create_default_context()
        self.conn = self.context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=host)
        self.conn.connect((host, port))
        self.f = self.conn.makefile('rwb', 0)
    def __enter__(self):
        return self.f
    def __exit__(self, type, value, traceback):
        self.f.close()

with Connect('programming.pwn2win.party', 9000) as f:
    for line in f:
        line = line.strip()
        print('received: %s' % line)

        if line.startswith(b'CTF-BR{') or \
           line == b'WRONG ANSWER': break

        numbers = map(int, line.split())
        s = sum(numbers)

        f.write(('%d\n' % s).encode('utf-8'))
        print('sent: %d' % s)  # for debugging purposes

~~~

One of them is python script. And I can just run this script with python to get flag.

----------------------------------------------------------------------

#### Solution

~~~

epist@epist-machine:~$ python ./solve_sum.py
received: 1 5 6 8 3 3 9 1 1 1 4 6 1 9 2 9 5 0
sent: 74
...
received: 6 6 6 1 2 8 3 7 9 2 1 5 5 9 9 0
sent: 79
received: CTF-BR{Congrats!_you_know_how_to_sum!}

~~~

**CTF-BR{Congrats!_you_know_how_to_sum!}**
