# **MD5 Games 1(50)**

#### tag : web

----------------------------------------------------------------------------

#### Description

>10 Years has passed since MD5 was broken, yet it is still frequently used in web applications, particularly PHP powered applications (maybe there's a function after it?). Break it again to prove the point!

-----------------------------------------------------------------

#### Challenge

~~~
<?php
if (isset([)$_GET['src']))
    highlight_file(__FILE__) and die();
if (isset($_GET['md5']))
{
    $md5=$_GET['md5'];
    if ($md5==md5($md5))
        echo "Wonderbubulous! Flag is ".require __DIR__."/flag.php";
    else
        echo "Nah... '",htmlspecialchars($md5),"' not the same as ",md5($md5);
}

?>
~~~

 I can see the php source in link of problem.

~~~
$md5=md5($md5)
~~~

 First, I try to find x = md5(x) which is called 'fixed point', but I can't find it because it's not exist in md5 hash.

 Second, I try to find another way to satisfy the condition and I can find some information about operator '=='' with '0e'.

<https://stackoverflow.com/questions/22140204/why-md5240610708-is-equal-to-md5qnkcdzo/>

 According to above site, 0e~ is eqaul to 0e~ when ~ is cosist of only digit.

----------------------------------------------------------------------------

#### Solution


~~~
#solve.py

#!/usr/bin/python
import sys
import hashlib

fix = "0e"

for x in xrange(1000,10000000000):
    fix += str(x)
    h = hashlib.md5()
    h.update(fix)
    if(str(h.hexdigest())[:2] == "0e"):
	if(str(h.hexdigest())[2:].isdigit()==True):
	    print fix + " is equal to " + h.hexdigest()
      print "flag is " + fix
	    sys.exit(1)
    fix = fix[:2]
~~~

~~~
0e215962017 is equal to 0e291242476940776845150308577824
flag is 0e215962017
~~~

### **flag 0e215962017**
