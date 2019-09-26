#ifndef ENTROPY
#define ENTROPY

#define SIZE 20
#define SX 0
#define DX 1

struct huffman
{
	char letter;
    int frequency;
	int child_num;
    int code;
    int depth;
    struct huffman* dad;
};

void huffman_encoding(const char* text, const int mode);
void huffman_decoding(const char* text, const int mode);
void arithmetic_encoding(const char* text, const int mode);
void arithmetic_decoding(const char* text, const int mode);

#endif
