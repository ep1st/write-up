# **GIF**

#### tag : misc

-----------------------------------------------

#### Description

>Making a gif is so hard.

-----------------------------------------------

#### Solution

There is 8 png images in gif file.

~~~

$ binwalk jiggs.gif

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
211           0xD3            Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
148050        0x24252         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
148261        0x24325         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
292577        0x476E1         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
292788        0x477B4         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
441489        0x6BC91         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
441700        0x6BD64         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
581765        0x8E085         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
581976        0x8E158         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
725461        0xB11D5         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
725672        0xB12A8         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
857131        0xD142B         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
857342        0xD14FE         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">
987856        0xF12D0         PNG image, 500 x 323, 8-bit/color RGB, non-interlaced
988067        0xF13A3         Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#">


~~~

I can find flag in 5'th png file.

![image](./5.png)

**actf{thats_not_how_you_make_gifs}**
