# **Passport**

#### tag : junior, crypto, md5

-----------------------------------------------

#### Description

>Provide valid passport file in order to pass.
>
>Target: http://passport.dctfq18.def.camp
>
>Author: Lucian Nitescu

-----------------------------------------------

#### Solution

Ok, This is md5 hash collision problem. I have to find collsion pair for `cee9a457e790cf20d4bdaa6d69f01e41`.

```sh

$ xxd -ps -c 64 demo.bin
0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef

$ md5sum demo.bin
cee9a457e790cf20d4bdaa6d69f01e41  demo.bin

```

It's just simple work. I find pair in net - `0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef` is will be evil pair for this prob.

Ok, Just make raw data.


```python

evil = '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef'

open('payload.bin', 'w').write(evil.decode('hex'))

```

Here is `payload.bin`. Ok md5sum's result is same.


```sh

$ xxd -ps -c 64 payload.bin
0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef

$ md5sum payload.bin
cee9a457e790cf20d4bdaa6d69f01e41  payload.bin

```

And I can get flag from uploading payload.bin to checking server.

**DCTF{04c8d0052e3ffd8d21934e392c272a0494f23433901941c93fab82b50be27c1a}**
