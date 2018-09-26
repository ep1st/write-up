# **SimplePass**

#### tag : junior, reversing, debug, fibonacci

-----------------------------------------------

#### Description

>Can you guess what is wrong with the password

-----------------------------------------------

#### Solution

Ok, I can get `SimplePass` binary from link. And I can find this binary is C++ program. This binary just read password by `getline` and save that password to `v14`. And `v14` will be compared with `v15` which is password calculated in binary. And result of comparison will be `v9`. If `v9` is `True`, It will go to success routine.

To sum up, `DCTF{sha256(v15)}` is flag.

~~~

  LODWORD(v3) = std::operator<<<std::char_traits<char>>(&std::cout, "Password?");
  std::ostream::operator<<(v3, &std::endl<char,std::char_traits<char>>);
  std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v14);

  ...

  LOBYTE(v9) = std::operator==<char>(&v14, &v15);

  ...

  if ( (_BYTE)v9 )
    {
      LODWORD(v11) = std::operator<<<std::char_traits<char>>(&std::cout, "DONE! The flag is DCTF{sha256(your_number)}!");
      std::ostream::operator<<(v11, &std::endl<char,std::char_traits<char>>);
    }

~~~

This is `v15` calculating routine, In end, `v15` have result of calculation.

~~~

  v4 = Fibonacci(10);
  v5 = (unsigned __int64)Fibonacci(22) + v4;
  v6 = (signed int)Fibonacci(22) / 2 + v5;
  v7 = (unsigned __int64)Fibonacci(11) + v6;
  v8 = (unsigned __int64)Fibonacci(9) + v7;
  v9 = 400 * (v8 + 1337 * (unsigned __int64)Fibonacci(10));
  v10 = Fibonacci(17);
  std::__cxx11::to_string((std::__cxx11 *)&v15, v9 * v10)

~~~

I make the breakpoint at `to_string`, And I peek `v15`'s data from debugger. Ok, `v15` is `-366284240`.

~~~

 ► 0x55555555570e <main+216>    call   std::__cxx11::to_string(int)  <0x555555555843>
        rdi: 0x7fffffffde20 ◂— 0x2
        rsi: 0xea2af230
        rdx: 0xea2af230
        rcx: 0xa


pwndbg> x/gx 0x7fffffffde20
0x7fffffffde20:	0x00007fffffffde30

pwndbg> x/s 0x00007fffffffde30
0x7fffffffde30:	"-366284240

~~~

Nice.

```sh

$ ./SimplePass
Password?
-366284240
DONE! The flag is DCTF{sha256(your_number)}!

```

**DCTF{554A58CFAD51E0D7DF7E8287FA96223780A249B104DE60425908ABF0B83C69AA}**
