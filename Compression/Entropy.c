#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "Entropy.h"

int compare_frequency(const void* a, const void* b);
int compare_letter(const void* a, const void* b);

void huffman_encoding(const char* text, const int mode)
{
    int i=0;

    struct huffman* huffman_tree = malloc(sizeof(struct huffman)*SIZE);
    int size = SIZE;
    int num_letters = 0;

    while (i < (strlen(text)-1))
	{
		char c = (char) text[i];

        int j=0;
        for(; j<num_letters; j++)
        {
            if(huffman_tree[j].letter == c)
            {
                huffman_tree[j].frequency ++;
                break;
            }
        }

        if(j==num_letters)
        {
            if(j==size)
            {
                size = size << 1;
                huffman_tree = realloc(huffman_tree, sizeof(struct huffman)*size);
            }

            huffman_tree[j].letter = c;
            huffman_tree[j].frequency = 1;
            num_letters++;
        }

    	i++;
	}

    huffman_tree = realloc(huffman_tree, sizeof(struct huffman)*num_letters);

    int num = num_letters;
    size = num_letters;
    i=0;

    while(num>1)
    {
        qsort((void *) &huffman_tree[2*i], num, sizeof(struct huffman), compare_frequency);
        size = num_letters+i+1;
        huffman_tree = realloc(huffman_tree, sizeof(struct huffman)*(num_letters+i+1));


        if(huffman_tree[2*i].frequency > huffman_tree[2*i+1].frequency)
        {
            huffman_tree[2*i].child_num = DX;
            huffman_tree[2*i+1].child_num = SX;
        }
        else
        {
            huffman_tree[2*i].child_num = SX;
            huffman_tree[2*i+1].child_num = DX;
        }

        huffman_tree[2*i].dad = &huffman_tree[num_letters+i];
        huffman_tree[2*i+1].dad = &huffman_tree[num_letters+i];;

        i++;
        num--;
    }

    huffman_tree[size-1].dad = NULL;
    huffman_tree[size-1].code = 0;
    huffman_tree[size-1].depth = 0;

    i=0;

    while(i<num_letters)
    {
        struct huffman * dad_node;

        do
        {
            dad_node = huffman_tree[i].dad;
            huffman_tree[i].code = ((dad_node->code)<<1) | huffman_tree[i].child_num;
            huffman_tree[i].depth = dad_node->depth + 1;
        }
        while(dad_node!=NULL);

        i++;
    }

    qsort((void *) &huffman_tree, num_letters, sizeof(struct huffman), compare_letter);

    i=0;

    FILE *fd = fopen("Huffman_encryption.txt", "w");
    while(i<strlen(text)-1)
    {
        struct huffman* found = bsearch((void *) &text[i], (void *) &huffman_tree, num_letters, sizeof(struct huffman), compare_letter);
        fwrite(&(found->code), sizeof(int), 1, fd);
    }
    fclose(fd);
}

int compare_frequency(const void* a, const void* b)
{
    return (((struct huffman*) a)->frequency)-(((struct huffman*) b)->frequency);
}

int compare_letter(const void* a, const void* b)
{
    return (((struct huffman*) a)->letter)==(((struct huffman*) b)->letter);
}

void huffman_decoding(const char* text, const int mode)
{

}

void arithmetic_encoding(const char* text, const int mode)
{

}

void arithmetic_decoding(const char* text, const int mode)
{

}
