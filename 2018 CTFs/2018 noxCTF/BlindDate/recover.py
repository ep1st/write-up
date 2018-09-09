d = open('BlindDate.jpeg', 'rb').read()

r = ''.join(x[::-1] for x in [d[i:i+4] for i in range(0, len(d), 4)])

open('BlindDate.recover.jpeg', 'wb').write(r)
