# **decrypto-1**

#### tag : crypto, 101

-----------------------------------------------

#### Description

>[Kerckhoffs's principle](https://en.wikipedia.org/wiki/Kerckhoffs%27s_principle) states that \"A cryptosystem should be secure even if everything about the system, except the key, is public knowledge.\"  So here's our unbreakable cipher.

-----------------------------------------------

#### TL;DR

1. extract key from prefix(json format)
2. xor key with encrypted data

-----------------------------------------------

#### Solution

Here is challnge script.

```python
import sys
import json
import hashlib


class Crypto:

    def __init__(self, key):
        if not isinstance(key, bytes):
            raise TypeError('key must be of type bytes!')
        self.key = key
        self._buf = bytes()
        self._out = open("/dev/stdout", "wb")

    def _extend_buf(self):
        self._buf += self.key

    def get_bytes(self, nbytes):
        while len(self._buf) < nbytes:
            self._extend_buf()
        ret, self._buf = self._buf[:nbytes], self._buf[nbytes:]
        return ret

    def encrypt(self, buf):
        if not isinstance(buf, bytes):
            raise TypeError('buf must be of type bytes!')
        stream = self.get_bytes(len(buf))
        return bytes(a ^ b for a, b in zip(buf, stream))

    def set_outfile(self, fname):
        self._out = open(fname, "wb")

    def encrypt_file(self, fname):
        buf = open(fname, "rb").read()
        self._out.write(self.encrypt(buf))


class JSONCrypto(Crypto):

    def encrypt_file(self, fname):
        buf = open(fname, "r").read().strip()
        h = hashlib.sha256(buf.encode('utf-8')).hexdigest()
        data = {
                "filename": fname,
                "hash": h,
                "plaintext": buf,
        }
        outbuf = json.dumps(data, sort_keys=True, indent=4)
        self._out.write(self.encrypt(outbuf.encode("utf-8")))


def main(argv):
    if len(argv) not in (3, 4):
        print("%s <key> <infile> [outfile]" % sys.argv[0])
        return
    argv.pop(0)
    key = argv.pop(0)
    inf = argv.pop(0)
    crypter = JSONCrypto(key.encode("utf-8"))
    if sys.argv:
        crypter.set_outfile(argv.pop(0))
    crypter.encrypt_file(inf)


if __name__ == '__main__':
    main(sys.argv)
```

flag.txt is json format before encrypting.

```python
        outbuf = json.dumps(data, sort_keys=True, indent=4)
        self._out.write(self.encrypt(outbuf.encode("utf-8")))
```

So using that json fomrat's prefix is same, recover key.

```
prefix = '7b0a202020202266696c656e616d65223a2022'.decode('hex')
with open('flag.txt.enc', 'r') as f:
    d = (f.read()).decode('utf-8')
    x = []
    for a,b in zip(prefix,d[:len(prefix)]):
        x.append(chr(ord(a)^ord(b)))
    print bytearray(x)
```
```
$ p solve.py
n0t4=l4gn0t4=l4g...
```

Key is `n0t4=l4g`. Now just xor with flag.txt.enc. Here is [solution script](./solve.py).

```
$ p solve.py
{
    "filename": "flag.txt",
    "hash": "2f98b8afa014bf955533a3e72cee0417413ff744e25f2b5b5838f5741cd69547",
    "plaintext": "CTF{plz_dont_r0ll_ur_own_crypto}"
}
```
**CTF{plz_dont_r0ll_ur_own_crypto}**