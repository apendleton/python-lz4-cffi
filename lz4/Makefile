UNAME := $(shell uname)

LIBTYPE=so

all: clean build

clean:
	rm -f *.so *.dylib *.gch

build:
	gcc -O3 -shared -fPIC -std=c99 -Wall -W -Wundef -Wno-implicit-function-declaration -o liblz4.$(LIBTYPE) lz4.h lz4hc.h lz4.c lz4hc.c lz4_offset_hack.c

debug:
	gcc -O3 -shared -fPIC -g -std=c99 -Wall -W -Wundef -Wno-implicit-function-declaration -o liblz4.$(LIBTYPE) lz4.h lz4hc.h lz4.c lz4hc.c lz4_offset_hack.c
