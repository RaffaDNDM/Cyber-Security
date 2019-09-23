#include "Substitution.h"
#include "Util.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define SIZE 20

int main(int argc, char** argv)
{
	if (argc < 2)
	{
		printf("You need to specify the text to be encrypted \n");
	}

	int fp = open(argv[1], O_RDONLY);

	int flag = true;
	int check = true;

	int i = 0;
	int size_text = SIZE;
	char* text = malloc(sizeof(char)*size_text);

	while (check)
	{
		if (i == size_text)
		{
			size_text = size_text << 1;
			text = realloc(text, sizeof(char)*size_text);
		}

		check = read(fp, &text[i], sizeof(char));
		i++;
	}

	
	//Use of cyphers
	check = true;

	while(check)
	{
		printf("Decide which encryption method with substitution you want to use\n");
		printf("1: Ceaser Cyper\n");
		printf("2: Vigenere Cyper\n");
		printf("2: Path Cyper\n");
		printf("4: Exit\n");

		char word[MAX_LIMIT];	
		gets(&word);		
		
		int choice = atoi(word);

		switch(choice)
		{
			case 1:
			{
				printf("Write the number that will be used Ceaser Cypher\n");
				
				gets(&word);				
				int num_pos = atoi(word);		

				ceaser_cypher(text, num_pos);
				break;
			}
			
			case 2:
			{
				printf("Write the word that will be used by Veaser Cypher\n");

				gets(&word);				
				
				vigenere_cypher(text, word);
				break;
			}
			case 3:
			{				
				int flag = true;
				int mode = 0;

				while(flag)	
				{
					printf("        What type of encryption do you choose?\n");
					printf(" 1. Reading coloumns UP_BOTTOM (from left to right)\n");					
					printf(" 2. Reading coloumns UP_BOTTOM (from right to left)\n");
					printf(" 3. Reading coloumns BOTTOM_UP (from left to right)\n");					
					printf(" 4. Reading coloumns BOTTOM_UP (from right to left)\n");
					printf(" 5. Clockwise spiral reading (from element [0][0])\n");
					printf(" 6. Clockwise spiral reading (from element [0][dim-1])\n");
					printf(" 7. Clockwise spiral reading (from element [dim-1][dim-1])\n");
					printf(" 8. Clockwise spiral reading (from element [dim-1][0])\n");				
					printf(" 9. Counterclockwise spiral reading (from element [0][0])\n");
					printf("10. Counterclockwise spiral reading (from element [0][dim-1])\n");
					printf("11. Counterclockwise spiral reading (from element [dim-1][dim-1])\n");
					printf("12. Counterclockwise spiral reading (from element [dim-1][0])\n");

					gets(&word);	
					choice = atoi(word);				

					if(mode>0 && mode<13)
						flag = false;
				}
				
				path_cypher_encoding(text, mode);
				break;
			}

			case 4:
			{
				int flag = true;

				while(flag)	
				{
					printf("Are you sure? (yes/no) \n");
					
					gets(&word);				
				
					if(strcmp(word,"yes")==0)
					{
						flag = false;
						check = false;
					}					
					else if(strcmp(word,"no")==0)
						flag=false;
				}
				
				break;
			}
			default:
				printf("Invalid choice: write only one of the specified numbers\n");
		}
	}

	return 0;
}


