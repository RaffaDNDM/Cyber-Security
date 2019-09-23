#ifndef TRASPOSITION
#define TRASPOSITION

#define PATH_COLOUMN_HSX 1
#define PATH_COLOUMN_HDX 2
#define PATH_COLOUMN_BSX 3
#define PATH_COLOUMN_BDX 4
#define PATH_SPIRAL_HOUR_HSX 5
#define PATH_SPIRAL_HOUR_HDX 6
#define PATH_SPIRAL_HOUR_BDX 7
#define PATH_SPIRAL_HOUR_BSX 8
#define PATH_SPIRAL_ANTI_HSX 9
#define PATH_SPIRAL_ANTI_HDX 10
#define PATH_SPIRAL_ANTI_BDX 11
#define PATH_SPIRAL_ANTI_BSX 12

void fence_cypher(const char* text, int num_pos);
void path_cypher_encoding(const char* text, const int mode);
void path_cypher_decoding(const char* text, const int mode);

#endif

