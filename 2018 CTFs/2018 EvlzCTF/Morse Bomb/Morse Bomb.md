# **Morse Bomb**

#### tag : reversing

-----------------------------------------------

#### Description

>>Let's play 8 bit
>>Enclose the flag in evlz{}ctf

>>https://goo.gl/bokc4X

-----------------------------------------------

#### Solution

~~~

$ file morseBomb
morseBomb: ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, not stripped

~~~

I open this file on IDA, and I can find morse string from .data ...

~~~

Address        Length   Type String                                                                             
-------        ------   ---- ------                                                                             
.data:0080010C 00000054 C    ..-. .-.. .- --. .. ... .--. .-. . - - -.-- -- --- .-. ... . -... .. -. .- .-. -.--

~~~

I generate morse code, and I can get flag text easily.

~~~

FLAGISPRETTYMORSEBINARY

~~~

**evlz{FLAGISPRETTYMORSEBINARY}ctf**
