#include "Substitution.h"
#include "Util.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


int main(int argc, char** argv)
{
	char text[] = "CIAO COME TI CHIAMI? RAFFAELE10";
	//morse_encoding(text);
	morse_decoding("-.-. .. .- --- | -.-. --- -- . | - .. | -.-. .... .. .- -- .. ..--.. | .-. .- .._. .._. .- . .-.. . .---- -----");
}

void ceaser_cypher_encoding(const char* text, int num_pos)
{
	printf("Creation of file encrypted through Ceaser Cypher");
	FILE *fp = fopen("Ceaser_encryption.txt", "w");

	int i = 0;
	printf("numero posizioni: %d\n", num_pos);	

	while (i < (strlen(text)-1))
	{
		
		int c = (char) text[i];
		int c1 = c+num_pos;	
		int c2 = (c=='\n')?'\n':((c1-BEGIN)%LENGTH)+BEGIN;		

		fprintf(fp, "%c", c2);
		i++;		
	}
}

void ceaser_cypher_decoding(const char* text, int num_pos)
{
	printf("Creation of file decrypted through Ceaser Cypher");
	FILE *fp = fopen("Ceaser_decryption.txt", "w");

	int i = 0;
	printf("numero posizioni: %d\n", num_pos);	

	while (i < (strlen(text)-1))
	{
		
		int c = (char) text[i];
		int c1 = c-num_pos;
		c1 = (c1>=BEGIN)? c1 : LENGTH+c1;
		int c2 = (c=='\n')?'\n':c1;		

		fprintf(fp, "%c", c2);
		i++;		
	}
}

void vigenere_cypher_encoding(const char* text, const char* word)
{
	printf("Creation of file encrypted through Vigenere Cypher");
	FILE *fp = fopen("Vigenere_encryption.txt", "w");

	int i = 0;
	int j = 0;
	int w_len = strlen(word);

	while (i < (strlen(text)-1))
	{	
		int c = (char) text[i];
		j = (c=='\n')? j : (j+1) % w_len;		

		int c1 = c+(word[j]-BEGIN);
		int c2 = (c=='\n')? '\n' : ((c1-BEGIN)%LENGTH)+BEGIN;		

		fprintf(fp, "%c", c2);
		i++;		
	}
}

void vigenere_cypher_decoding(const char* text, const char* word)
{
	printf("Creation of file encrypted through Vigenere Cypher");
	FILE *fp = fopen("Vigenere_decryption.txt", "w");

	int i = 0;
	int j = 0;
	int w_len = strlen(word);

	while (i < (strlen(text)-1))
	{	
		int c = (char) text[i];
		j = (c=='\n')? j : (j+1) % w_len;		

		int c1 = c-(word[j]-BEGIN);
		c1 = (c1>=BEGIN)? c1 : LENGTH+c1;
		int c2 = (c=='\n')? '\n' : ((c1-BEGIN)%LENGTH)+BEGIN;		

		fprintf(fp, "%c", c2);
		i++;		
	}
}

void morse_encoding(const char* text)
{
	FILE *fp = fopen(MORSE_TABLE, "r");
	morse table[MORSE_SIZE];

	int i=0;
	while(i<MORSE_SIZE)
	{	
		table[i].code = malloc(sizeof(char)*MAX_MORSE_SIZE);	
		fscanf(fp,"%c %s\n", &(table[i].meaning), table[i].code);
		printf("%c %s\n", table[i].meaning, table[i].code);
		i++;
	}

	fclose(fp);

	fp = fopen("Morse_encryption.txt", "a");
	
	i=0;
	
	while(i<strlen(text))
	{
		int flag = true;
		int h=0;
		while(h<MORSE_SIZE && flag)
		{
			if(text[i]==table[h].meaning)
			{
				fprintf(fp, "%s ", table[h].code);
				flag = false;
			}			
			else if(text[i]==' ')
			{	
				fprintf(fp, "| ");
				flag = false;
			}
			
			h++;		
		}

		i++;
	}
	
	fclose(fp);
}

void morse_decoding(char* text)
{
	FILE *fp = fopen(MORSE_TABLE, "r");
	morse table[MORSE_SIZE];	

	int i=0;
	while(i<MORSE_SIZE)
	{	
		table[i].code = malloc(sizeof(char)*MAX_MORSE_SIZE);	
		fscanf(fp,"%c %s\n", &(table[i].meaning), table[i].code);
		printf("%s\n", table[i].code);
		i++;
	}

	fclose(fp);

	i=0;
	char **morse_text = malloc(sizeof(char*)*SIZE);
	int size = SIZE;

	for (; i<SIZE; morse_text[i++]= malloc(sizeof(char)*(MAX_MORSE_SIZE+1)));

	int j=0;
	int k=0;	
	
	i=0;
	printf("\n\n %d \n\n", (int) strlen(text));
	while(j<strlen(text))
	{
		if(i==size)
		{
			size = size << 1;
			morse_text = realloc(morse_text, sizeof(char*)*size);
			
			int y=i;
			for(; y<size; morse_text[y++]= malloc(sizeof(char)*(MAX_MORSE_SIZE+1)));
		}	
			
		morse_text[i][k] = text[j];
		k++;
		j++;		
		
		if(morse_text[i][k-1]==' ')
		{
			morse_text[i][k-1]='\0';
			i++;
			k=0;
		}
		
		if(j==strlen(text))
		{			
			morse_text[i][k]='\0';
			i++;
		}			
		
	}

	size=i;
	morse_text = realloc(morse_text, sizeof(char*)*i);
	fp = fopen("Morse_decryption.txt", "a");
	
	i=0;
	while(i<size)
	{
		int flag = true;
		int h=0;
		
		while(h<MORSE_SIZE && flag)
		{
			if(strcmp(morse_text[i], table[h].code)==0)
			{
				fprintf(fp, "%c", table[h].meaning);
				flag = false;
			}			
			else if(strcmp(morse_text[i], "|")==0)
			{	
				fprintf(fp, " ");
				flag=false;
			}
			
			h++;		
		
		}

		i++;
		
	}
	
	fclose(fp);	
}

