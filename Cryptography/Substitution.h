#ifndef SUBSTITUTION
#define SUBSTITUTION

#define MORSE_TABLE "MorseTable.txt"
#define MORSE_SIZE 45
#define MAX_MORSE_SIZE 6
typedef struct morse_match
{
	char meaning;
	char *code;
}morse;


void ceaser_cypher_encoding(const char* text, int num_pos);
void ceaser_cypher_decoding(const char* text, int num_pos);
void vigenere_cypher_encoding(const char* text, const char* word);
void vigenere_cypher_decoding(const char* text, const char* word);
void morse_encoding(const char* text);
void morse_decoding(char* text);

#endif

