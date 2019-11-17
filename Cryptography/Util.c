#include "Util.h"
#include <stdlib.h>
#include <time.h>
#include <math.h>
/**
    @param num number for which we want to know if it is an integer number
    @return 0 if num is not an integer power of a number
            1 if num is an integer power of a number
*/
int is_int_power(int);

/**
    @param num find the r number needed by AKS algorithm
    @return r found
*/
int find_r(int);

/**
    Euclidean Algorithm with iterative approach
    Greatest common divisor (GCD) of n and m
    @param n first number
    @param m second number
    @return GCD
*/
int ea(int, int);

/**
    Extended Euclidean Algorithm with iterative approach
    Greatest common divisor (GCD) of n and m + Bèzout multipliers
    @param n first number
    @param m second number
    @return array x (GCD = x[0], alpha = x[1], beta = x[2])
*/
int* eea(int, int);

/**
    Euclidean Algorithm with recursive approach
    Greatest common divisor (GCD) of n and m
    @param n first number
    @param m second number
    @return GCD
*/
int recursive_ea(int, int);

/**
    Extended Euclidean Algorithm with recursive approach
    Greatest common divisor (GCD) of n and m + Bèzout multipliers
    @param n first number
    @param m second number
    @return array x (GCD = x[0], alpha = x[1], beta = x[2])
*/
int* recursive_eea(int, int);

/**
    Primality test made by Miller and Rabin
    @param num number for which I want to check the Primality
    @param T number of random a for which Miller_Rabin test is repeated
    @return 1 if num is prime or pseudo-prime, 0 otherwise
*/
int miller_rabin_T(int, int);

/**
    Power
    @param a base
    @param d exponent
    @return (a^d)
*/
int power(int, int);

/**
    Modular power
    @param a base
    @param d exponent
    @param num defines the space the power return live {0, ... ,num-1}
    @return (a^d) mod num
*/
int mod_pow(int a, int d, int num);

int is_int_power(int num)
{
    int i=2;
    int length_num = ceil(log(num)/log(2));
    int is_no_power = 1;
    int m = 2;

    for(; m<length_num; m++)
    {
        int l;

        if(length_num%m>0)
            l = (length_num / m)+1;
        else
            l = length_num / m;

        //mask = 2^(l-1)
        int mask = 1<<(l-1);

        int x=0;
        int y=0;
        int j=0;
        int i=0;

        for(; i<l; i++)
        {
            y=x+(mask>>i);

            y=power(y,m);

            if(y>num)
                y=x;
        }

        if(y==num)
            return 1;
    }

    return 0;
}

int find_r(int num)
{
    double lg_num= log(num)/log(2); //lg2_num
    int max_r = ceil(pow(lg_num, 5));
    int max_exp = floor(pow(lg_num, 2));
    int r=2;

    for(; r<=max_r; r++)
    {
        int d = ea(num,r);

        if(d==1)
        {
            int i=2;
            int flag = 1; // represents n^i mod r != 1

            while(i<=max_exp && flag)
            {
                if(mod_pow(num, i, r)==1)
                {
                    flag = 0;
                }

                i++;
            }

            if(i==max_exp+1)
            {
                return r;
            }
        }
    }
}

int ea(int n, int m)
{
    int r1 = (n>m)?m:n;
    int r2 = (n+m)-r1;

    while(r2!=0)
    {
        int temp = r1%r2;
        r1 = r2;
        r2 = temp;
    }

    return r1;
}

int* eea(int n, int m)
{
    int r1 = (n>m)?m:n;
    int r2 = (n+m)-r1;
    int a1 = 1;
    int a2 = 0;
    int b1 = 0;
    int b2 = 1;

    while(r2!=0)
    {
        int temp_r = r1%r2;
        r1 = r2;
        r2 = temp_r;

        int temp_a = a1%a2;
        a1 = a2;
        a2 = temp_a;

        int temp_b = b1%b2;
        b1 = b2;
        b2 = temp_b;
    }

    int* eea = malloc(sizeof(int)*3);
    eea[0]=r1;
    eea[1]=a1;
    eea[2]=b1;

    return eea;
}

/**
    Euclidean Algorithm
    Greatest common divisor (GCD) of n and m
    @param n first number
    @param m second number
    @return GCD
*/
int recursive_ea(int n, int m)
{
    if(m==0)
        return m;

    return recursive_ea(n, n%m);
}

/**
    Extended Euclidean Algorithm
    Greatest common divisor (GCD) of n and m + Bèzout multipliers
    @param n first number
    @param m second number
    @return array x (GCD = x[0], alpha = x[1], beta = x[2])
*/
int* recursive_eea(int n, int m)
{
    int* eea = malloc(sizeof(int)*3);

    if(m==0)
    {
        eea[0]=n;
        eea[1]=1;
        eea[2]=0;
        return eea;
    }

    eea = recursive_eea(m, n % m);

    int y=eea[2];
    eea[2]=eea[1]-((m/n)*y);
    eea[1]=y;

    return eea;
}

/**
    Primality test made by Agraval Kayal Saxena
    param num number for which I want to check the Primality
    return 1 if num is prime, 0 otherwise
*/
int aks(int num)
{
    int check;

    check = is_int_power(num);

    if(!check)
        return 0;

    //Find
    return 0;
}

int miller_rabin_T(int num, int T)
{
    //Compute s,d such that n-1 = (2^s)*d
    int d = num-1;
    int s = 0;

    while(d&1==0)
    {
        s++;
        d>>=1;
    }

    while(T>0)
    {
        srand(time(NULL));
        int a = rand() % num;

        if(ea(a,num)>1)
            return 0;

        int b = mod_pow(a,d,num);

        if(b!=1 && b!=(num-1))
        {
            int e=0;

            while(b!=1 && b!=(num-1) && e<s-1)
            {
                b = (b*b) %num;
                e++;
            }

            if(b!=(num-1))
                return 0;
        }
    }

    return 1;
}

int miller_rabin(int num)
{
    int length_num = ceil(log(num)/log(2));
    int num_a = ceil(pow(length_num, 4));

    miller_rabin_T(num, num_a);
}

int mod_pow(int a, int d, int num)
{
    return power(a,d) % num;
}

int power(int a, int d)
{
    int j=1;

    while(j<d)
    {
        a*=a;
        j++;
    }

    return a;
}
