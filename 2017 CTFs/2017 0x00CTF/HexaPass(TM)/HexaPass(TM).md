# **HexaPass(TM)**

#### tag : reversing

-----------------------------------------------

#### Description

>The new and revolutionary HexaPass protection system is unbeatable... Can you break it?

-----------------------------------------------

#### Solution

~~~

$ file c4
c4: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=bb4cb471badbe69e05e1a4f2448edf72d9ef9c28, stripped

~~~

Here is main code. I can find return value of sub_4006FD is way to get flag.

~~~

__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  __int64 result; // rax@3
  __int64 v4; // rcx@3
  char s[1032]; // [sp+10h] [bp-410h]@1
  __int64 v6; // [sp+418h] [bp-8h]@1

  v6 = *MK_FP(__FS__, 40LL);
  memset(s, 0, 0x400uLL);
  puts("Program protected by HexaPass(TM)\n");
  printf("Enter key: ", 0LL);
  fgets(s, 1024, stdin);
  s[(signed int)(strlen(s) - 1)] = 0;
  if ( sub_4006FD(s, 1024LL) )
    puts("Wrong Key!\n");
  puts("--\nCrackme by pico\n  Greetings to the 0x00sec.org Community");
  result = 0LL;
  v4 = *MK_FP(__FS__, 40LL) ^ v6;
  return result;
}

~~~

In sub_4006FD, input string data transfered to hex data.

~~~

signed __int64 __fastcall sub_4006FD(_BYTE *a1)
{
  char v2; // [sp+12h] [bp-Eh]@2
  char v3; // [sp+14h] [bp-Ch]@1
  _BYTE *v4; // [sp+18h] [bp-8h]@1
  _BYTE *v5; // [sp+18h] [bp-8h]@8

  v4 = a1;
  v3 = 0;
  while ( *v4 )
  {
    v2 = 0;
    if ( *v4 <= 47 || *v4 > 57 )
    {
      if ( *v4 > 96 && *v4 <= 102 )
        v2 = 16 * (*v4 - 87);
    }
    else
    {
      v2 = 16 * (*v4 - 48);
    }
    v5 = v4 + 1;
    if ( !*v5 )
      return 0xFFFFFFFFLL;
    if ( *v5 <= 47 || *v5 > 57 )
    {
      if ( *v5 > 96 && *v5 <= 102 )
        v2 |= *v5 - 87;
    }
    else
    {
      v2 |= *v5 - 48;
    }
    if ( byte_601080[(unsigned __int64)(v3 & 3)] != v2 )
      return 1LL;
    ++v3;
    v4 = v5 + 1;
  }
  printf("**********************\n**  0x00CTF{H3x4p4sS_SucK5!-%s-R0cK5!}\n**********************\n", a1);
  puts("Greetings to:");
  printf("%s", &unk_6010A0);
  return 0LL;
}

~~~

I follow byte_601080 to get hex data of key.

~~~

.data:0000000000601080 ; char byte_601080[]
.data:0000000000601080 byte_601080     db 0BAh                 ; DATA XREF: sub_4006FD+28r
.data:0000000000601081                 db 0BEh ;
.data:0000000000601082                 db 0CAh ;
.data:0000000000601083                 db 0B1h ;

~~~

Well, 0xba, 0xbe, 0xca, 0xb1 is key. In this case, I put babecab1 to get flag.

~~~

$ ./c4
Program protected by HexaPass(TM)

Enter key: babecab1
**********************
**  0x00CTF{H3x4p4sS_SucK5!-babecab1-R0cK5!}
**********************
Greetings to:

  .:xKOo'              ,dKKd;.   'd0Kx:.   :ddddddddd: 'dddddddd:   :dddddddd;  
 kMMMMMMMN.          'NMMMMMMWo.NMMMMMMWd  OMMMMMMMMMO lMMMMMMMM0 :NMMMMMMMMMk  
 0MW00MMMM'          ,MMXkXMMMk.MMNkOMMMk  OMMMx''KMMO lMMMK''''. OMMMx''xMMMk  
 d:. lMMMW...      . 'x'  OMMMx.O'  lMMMk  OMMMK:..''. lMMM0....  OMMMl  :XXXd  
 ONO:dMMMM'kWOc.'lOW',WOl'OMMMk'W0o,dMMMk  .dKMMMWO;   lMMMMMMMMl OMMMl         
 0MMMo'lON'kMMMMMMX: ,MMMM;:xNk'MMMMd;dXk     'dNMMMNc lMMMNdddd' OMMMl         
 0MMMl .:O..lNMMMMMW.,MMMM' ,xd.WMMMl 'dd  ,:::. dMMMO lMMMO      OMMMl  .:::'  
 0MMMKKMMM':KW0dxKMM',MMMM0NMMk'MMMMXNMMk  OMMMO:xMMMO lMMMX::::: OMMMO::OMMMk  
 dWMMMMMM0.;:.    .c..XMMMMMMX:.0MMMMMMNo  OMMMMMMMMMO lMMMMMMMMM.OMMMMMMMMWx.  
   'dOx:.              'lkOo'    .ckOd'    ,:::::::::, .::::::::: ,::::::::.    

--
Crackme by pico
  Greetings to the 0x00sec.org Community

~~~

**0x00CTF{H3x4p4sS_SucK5!-babecab1-R0cK5!}**
