#include "lz4.h"

int LZ4_uncompress_offset (const char* source, char* dest, int osize, int offset) {
    return LZ4_uncompress(source + offset, dest, osize);
}