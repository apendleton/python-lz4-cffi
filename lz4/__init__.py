import cffi, platform, os

libtype = "so"

ffi = cffi.FFI()

ffi.cdef("int LZ4_compress   (const char* source, char* dest, int isize);")
ffi.cdef("int LZ4_uncompress (const char* source, char* dest, int osize);")
ffi.cdef("int LZ4_compressHC (const char* source, char* dest, int isize);")
ffi.cdef("int LZ4_uncompress_offset (const char* source, char* dest, int osize, int offset);")

candidate_names = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "%s.%s" % (name, libtype)) for name in
    ['liblz4', 'liblz4.pypy-20']
]
existing_names = [name for name in candidate_names if os.path.exists(name)]
assert len(existing_names) >= 1, "Can't find compiled library."

liblz4 = ffi.dlopen(existing_names[0])

def LZ4_compressBound(isize):
    return isize + (isize / 255) + 16

def store_le32(c, x):
    c[0] = chr(x & 0xff);
    c[1] = chr((x >> 8) & 0xff);
    c[2] = chr((x >> 16) & 0xff);
    c[3] = chr((x >> 24) & 0xff);

def load_le32(c):
    return ord(c[0]) | (ord(c[1]) << 8) | (ord(c[2]) << 16) | (ord(c[3]) << 24)

HDR_SIZE = 4
INT_MAX = 2 ** 31

def _compress_with(compressor, source):
    source_size = len(source)
    
    dest_size = HDR_SIZE + LZ4_compressBound(source_size)
    dest = ffi.new("char[]", dest_size)
    actual_size = 0

    store_le32(dest, source_size)
    if source_size > 0:
        osize = compressor(source, dest + HDR_SIZE, source_size)
        actual_size = HDR_SIZE + osize
        # ideally we would resize the buffer now, but I don't know how to do that with cffi
        
    return (dest, actual_size)

def _compress(source):
    return _compress_with(liblz4.LZ4_compress, source)

def _compressHC(source):
    return _compress_with(liblz4.LZ4_compressHC, source)

def compress(source):
    data, size = _compress(source)
    return ffi.buffer(data, size)[:]

def compressHC(source):
    data, size = _compressHC(source)
    return ffi.buffer(data, size)[:]

def _uncompress(source):
    source_size = len(source)

    if source_size < HDR_SIZE:
        raise ValueError("input too short")
    
    dest_size = load_le32(source)
    if dest_size > INT_MAX:
        raise ValueError("invalid size in header: 0x%x" % dest_size)

    if dest_size > 0:
        dest = ffi.new("char[]", dest_size)
        osize = liblz4.LZ4_uncompress_offset(source, dest, dest_size, HDR_SIZE)

        if osize < 0:
            raise ValueError("corrupt input at byte %d" % -osize)
        elif osize < source_size - HDR_SIZE:
            raise ValueError("decompression incomplete")

    return (dest, dest_size)

def uncompress(source):
    data, size = _uncompress(source)
    return ffi.buffer(data, size)[:]