# **That's not my name**

#### tag : misc

-----------------------------------------------

#### Description

>My friend sent me this copy of Lincoln's inspiring Gettysburg Address, but I can't seem to open it. Something about having the wrong name. Can you help me figure it out?

-----------------------------------------------

#### Solution

Simple extension changing solve this prob.

~~~

$ wget https://angstromctf.com/static/misc/not_my_name/gettysburg.pdf
--2018-03-22 01:43:08--  https://angstromctf.com/static/misc/not_my_name/gettysburg.pdf
Resolving angstromctf.com (angstromctf.com)... 45.55.83.114
Connecting to angstromctf.com (angstromctf.com)|45.55.83.114|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5210 (5.1K) [application/pdf]
Saving to: ‘gettysburg.pdf’

gettysburg.pdf      100%[===================>]   5.09K  --.-KB/s    in 0s      

2018-03-22 01:43:09 (1.47 GB/s) - ‘gettysburg.pdf’ saved [5210/5210]

$ file gettysburg.pdf
gettysburg.pdf: Microsoft OOXML

$ mv gettysburg.pdf gettysburg.docx

~~~

In docx file:

~~~

Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal.
...
actf{thanks_mr_lincoln_but_who_even_uses_word_anymore}

~~~

**actf{thanks_mr_lincoln_but_who_even_uses_word_anymore}**
