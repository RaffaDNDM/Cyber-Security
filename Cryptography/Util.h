#ifndef UTIL
#define UTIL

//Definition of boolean values
#define true 1
#define false 0
#define SIZE 20

//Max length of a string read by input line
#define MAX_LIMIT 20

//Circular set of maius char (from BEGIN=A to END=Z)
#define BEGIN 65
#define LENGTH 26

/**
    Primality test made by Agraval, Kayal and Saxena
    @param num number for which I want to check the Primality
    @return 1 if num is prime, 0 otherwise
*/
int aks(int);

/**
    Primality test made by Miller and Rabin
    @param num number for which I want to check the Primality
    @return 1 if num is prime or pseudo-prime, 0 otherwise
*/
int miller_rabin(int);
#endif
