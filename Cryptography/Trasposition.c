#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "Trasposition.h"
#include "Util.h"

int dim_matrix(int length);

void fence_cypher(const char* text, int num_pos)
{
		
}

void path_cypher_encoding(const char* text, const int mode)
{
	int len = strlen(text);

	int dim = dim_matrix(len);

	char matrix[dim][dim];

	for(int i=0; i<dim; i++)
	{
		for(int j=0; j<dim; j++)
		{
			if((i*dim+j)<len)
				matrix[i][j]=text[i*dim+j];
			else
				matrix[i][j]='*';		
		}
	}
	
	FILE *fp = fopen("Trasposition_encryption.txt", "a");

	fprintf(fp, "%2d:  ",mode);
	switch(mode)
	{
		case PATH_COLOUMN_HSX:
		{
			for(int j=0; j<dim; j++)
			{
				for(int i=0; i<dim; i++)
				{		
					fprintf(fp, "%c", matrix[i][j]);
				}
			}

			fprintf(fp, "\n");
			break;
		}

		case PATH_COLOUMN_HDX:
		{
			for(int j=dim-1; j>=0; j--)
			{
				for(int i=0; i<dim; i++)
				{			
					fprintf(fp, "%c", matrix[i][j]);
				}
			}

			fprintf(fp, "\n");
			break;
		}

		case PATH_COLOUMN_BSX:
		{
			for(int j=0; j<dim; j++)
			{
				for(int i=dim-1; i>=0; i--)
				{			
					fprintf(fp, "%c", matrix[i][j]);
				}
			}

			fprintf(fp, "\n");
			break;
		}

		case PATH_COLOUMN_BDX:
		{
			for(int j=dim-1; j>=0; j--)
			{
				for(int i=dim-1; i>=0; i--)
				{			
					fprintf(fp, "%c", matrix[i][j]);
				}
			}

			fprintf(fp, "\n");
			break;
		}

		case PATH_SPIRAL_HOUR_HSX:
		{
			int i=0, j=dim-1;

			while(j>0)			
			{
				int k;

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[i][k]);
	
				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][j]);

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[j][k]);
	
				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][i]);
	
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_HOUR_HDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][j]);

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[j][k]);
	
				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][i]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[i][k]);

				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_HOUR_BDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[j][k]);
	
				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][i]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[i][k]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][j]);		
		
				i++;
				j--;
			}

			break;
		}		

		case PATH_SPIRAL_HOUR_BSX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][i]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[i][k]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][j]);

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[j][k]);
		
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_ANTI_HSX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][i]);
			
				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[j][k]);
	
				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][j]);

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[i][k]);
		
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_ANTI_HDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[i][k]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][i]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[j][k]);
	
				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][j]);
		
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_ANTI_BDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][j]);

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[i][k]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][i]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[j][k]);	
				
				i++;
				j--;
			}

			break;
		}		

		case PATH_SPIRAL_ANTI_BSX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[j][k]);
	
				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[k][j]);

				for(k=j; k>i; k--)
					fprintf(fp, "%c", matrix[i][k]);

				for(k=i; k<j; k++)
					fprintf(fp, "%c", matrix[k][i]);
		
				i++;
				j--;
			}

			break;
		}
	}

	if(dim%2 && mode>4)
	{
		int middle = (dim-1)/2;	
		fprintf(fp, "%c\n", matrix[middle][middle]);
	}
}

int dim_matrix(int length)
{
	int i=1;

	for(i=2; (i*i)<length; i++);
	
	return i;
}


void path_cypher_decoding(const char* text, const int mode)
{
	int len = strlen(text);
	
	printf("%d \n",len);

	int dim = dim_matrix(len);
	
	printf("%d \n",dim);

	char matrix[dim][dim];
	int h=0;	

	switch(mode)
	{
		case PATH_COLOUMN_HSX:
		{
			for(int j=0; j<dim; j++)
			{
				for(int i=0; i<dim; i++)
				{		
					matrix[i][j]=text[h++];
				}
			}

			break;
		}

		case PATH_COLOUMN_HDX:
		{
			for(int j=dim-1; j>=0; j--)
			{
				for(int i=0; i<dim; i++)
				{			
					matrix[i][j]=text[h++];
				}
			}

			break;
		}

		case PATH_COLOUMN_BSX:
		{
			for(int j=0; j<dim; j++)
			{
				for(int i=dim-1; i>=0; i--)
				{			
					matrix[i][j]=text[h++];
				}
			}

			break;
		}

		case PATH_COLOUMN_BDX:
		{
			for(int j=dim-1; j>=0; j--)
			{
				for(int i=dim-1; i>=0; i--)
				{			
					matrix[i][j]=text[h++];
				}
			}

			break;
		}

		case PATH_SPIRAL_HOUR_HSX:
		{
			int i=0, j=dim-1;

			while(j>0)			
			{
				int k;

				for(k=i; k<j; k++)
					matrix[i][k]=text[h++];
	
				for(k=i; k<j; k++)
					matrix[k][j]=text[h++];

				for(k=j; k>i; k--)
					matrix[j][k]=text[h++];
	
				for(k=j; k>i; k--)
					matrix[k][i]=text[h++];
	
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_HOUR_HDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=i; k<j; k++)
					matrix[k][j]=text[h++];

				for(k=j; k>i; k--)
					matrix[j][k]=text[h++];
					
				for(k=j; k>i; k--)
					matrix[k][i]=text[h++];

				for(k=i; k<j; k++)
					matrix[i][k]=text[h++];

				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_HOUR_BDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					matrix[j][k]=text[h++];
	
				for(k=j; k>i; k--)
					matrix[k][i]=text[h++];

				for(k=i; k<j; k++)
					matrix[i][k]=text[h++];

				for(k=i; k<j; k++)
					matrix[k][j]=text[h++];
		
				i++;
				j--;
			}

			break;
		}		

		case PATH_SPIRAL_HOUR_BSX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					matrix[k][i]=text[h++];

				for(k=i; k<j; k++)
					matrix[i][k]=text[h++];

				for(k=i; k<j; k++)
					matrix[k][j]=text[h++];

				for(k=j; k>i; k--)
					matrix[j][k]=text[h++];
		
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_ANTI_HSX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=i; k<j; k++)
					matrix[k][i]=text[h++];
			
				for(k=i; k<j; k++)
					matrix[j][k]=text[h++];
	
				for(k=j; k>i; k--)
					matrix[k][j]=text[h++];

				for(k=j; k>i; k--)
					matrix[i][k]=text[h++];
		
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_ANTI_HDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					matrix[i][k]=text[h++];

				for(k=i; k<j; k++)
					matrix[k][i]=text[h++];

				for(k=i; k<j; k++)
					matrix[j][k]=text[h++];

				for(k=j; k>i; k--)
					matrix[k][j]=text[h++];
		
				i++;
				j--;
			}

			break;
		}

		case PATH_SPIRAL_ANTI_BDX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=j; k>i; k--)
					matrix[k][j]=text[h++];

				for(k=j; k>i; k--)
					matrix[i][k]=text[h++];

				for(k=i; k<j; k++)
					matrix[k][i]=text[h++];

				for(k=i; k<j; k++)
					matrix[j][k]=text[h++];	
				
				i++;
				j--;
			}

			break;
		}		

		case PATH_SPIRAL_ANTI_BSX:
		{
			int i=0, j=dim-1;

			while(j>0)
			{
				int k;

				for(k=i; k<j; k++)
					matrix[j][k]=text[h++];
	
				for(k=j; k>i; k--)
					matrix[k][j]=text[h++];

				for(k=j; k>i; k--)
					matrix[i][k]=text[h++];

				for(k=i; k<j; k++)
					matrix[k][i]=text[h++];
		
				i++;
				j--;
			}

			break;
		}
	}

	if(dim%2 && mode>4)
	{
		int middle = (dim-1)/2;	
		matrix[middle][middle]=text[h];
	}

	FILE *fp = fopen("Trasposition_decryption.txt", "a");

	fprintf(fp, "%2d:  ",mode);

	for(int i=0; i<dim; i++)
	{
		for(int j=0; j<dim; j++)
		{
			if(matrix[i][j]!='*')
				fprintf(fp, "%c", matrix[i][j]);		
		}
	}

	fprintf(fp, "\n");
}

