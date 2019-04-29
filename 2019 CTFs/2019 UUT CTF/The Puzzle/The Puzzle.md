# **The Puzzle**

#### tag : reversing, .net

-----------------------------------------------

#### Description

>> Solve the puzzle!

-----------------------------------------------

#### Solution

There are 2 stage slide puzzle. First stage is made of images numbers (range for 8). And second stage is made of qr code parts. First stage is resolvable. But second stage is unresolvable bacause qr images' complexity difference is 1 that mean unresolvable in slide puzzle game. And there is no success routine in program. So I extract images of qr.

```python
from os import system

'''
12762         0x31DA          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
14209         0x3781          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
16047         0x3EAF          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
17995         0x464B          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
19524         0x4C44          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
21315         0x5343          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
23306         0x5B0A          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
25032         0x61C8          PNG image, 154 x 154, 8-bit/color RGBA, non-interlaced
27787         0x6C8B          PNG image, 78 x 78, 8-bit/color RGBA, non-interlaced
28558         0x6F8E          PNG image, 78 x 78, 1-bit colormap, non-interlaced
28984         0x7138          PNG image, 78 x 78, 8-bit/color RGBA, non-interlaced
29790         0x745E          PNG image, 78 x 78, 1-bit colormap, non-interlaced
30213         0x7605          PNG image, 78 x 78, 1-bit colormap, non-interlaced
30635         0x77AB          PNG image, 78 x 78, 1-bit colormap, non-interlaced
31051         0x794B          PNG image, 78 x 78, 8-bit/color RGBA, non-interlaced
31822         0x7C4E          PNG image, 78 x 78, 1-bit colormap, non-interlaced
32238         0x7DEE          PNG image, 78 x 78, 1-bit colormap, non-interlaced
'''

offset = [12762,14209,16047,17995,19524,21315,23306,25032,27787,28558,28984,29790,30213,30635,31051,31822,32238]

for i in range(len(offset)):
	cmd = 'dd if=ThePuzzle.exe of=' + str(i) + '.png bs=1 skip=' + str(offset[i])
	system(cmd)
```

There are 8 png file for first stage and 9 png file for second stage which are qr code.

~~~
$ ls *.png
0.png  10.png  11.png  12.png  13.png  14.png  15.png  16.png  1.png  2.png  3.png  4.png  5.png  6.png  7.png  8.png  9.png
~~~

In qr code, `VVVUQ1RGe21kNShJX2wwVjNfcEw0eTFOZ19QdVp6MWVTKX0=` is stored. And this will be `UUTCTF{md5(I_l0V3_pL4y1Ng_PuZz1eS)}` as `UUTCTF{9ad589e4c948c9ecd46bf2c55c3049b5}`.

**UUTCTF{9ad589e4c948c9ecd46bf2c55c3049b5}**
