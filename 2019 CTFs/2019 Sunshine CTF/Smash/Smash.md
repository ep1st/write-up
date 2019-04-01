# **Smash**

#### tag : reversing

-----------------------------------------------

#### Description

>We discovered this old CD from the 90s in our attic. It looks like it used to register you to a WWE betting community back in the day, but we seem to have lost the access code. Can you get us in?
>
>WrestleOfMania
>
>Author: Winyl

-----------------------------------------------

#### Solution

```python
# stack variable, which will be stored in heap
v = [5,3,6,5,2,5,3,3,3,5,2,4,6,5,5,2,2,5,2,6,5,1,3,4,5,3,4,6,6,5]

# encrypted flag in .data
t = '60 0E 00 00 A8 03 00 00 80 1B 00 00 60 0F 00 00 20 01 00 00 A0 0E 00 00 88 01 00 00 58 03 00 00 A0 01 00 00 A0 09 00 00 84 01 00 00 E0 04 00 00 40 0C 00 00 20 0C 00 00 A0 05 00 00 C8 01 00 00 D4 01 00 00 C0 09 00 00 CC 01 00 00 40 0B 00 00 E0 0A 00 00 62 00 00 00 60 03 00 00 40 03 00 00 A0 05 00 00 80 01 00 00 E0 06 00 00 40 0B 00 00 40 15 00 00 A0 0F 00 00 '

# parsing encrypted flag in little endian, unpack
d = []
for x in [t[i:i+11] for i in range(0,len(t),12)]:
	d.append(int((''.join([y[::-1] for y in x.split(' ')]))[::-1],16))

# calculating
f = []
for i,j in zip(d,v):
	f.append((i/pow(2,j)))

flag = ''
for x in f:
	flag += chr(x)
print flag

```
**sun{Hu1k4MaN1a-ruNs-W1l4-0n-U}**
