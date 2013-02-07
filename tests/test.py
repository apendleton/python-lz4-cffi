import lz4
import sys

DATA = open("/dev/urandom", "rb").read(128 * 1024)  # Read 128kb
sys.exit(DATA != lz4.uncompress(lz4.compress(DATA)) and 1 or 0)
