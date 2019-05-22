from LFSR import LFSR
from utils import to_binary_string

taps = (16, 14, 13, 11)
state = [True, False, False, True, True, True, False, True, False, True, True, False, False, True, True, True]

l = LFSR(taps, state)

# Generate random bits
bin_string = to_binary_string(l.next_n(10000000))

# Write bits to file for testing
f = open("LFSRData", "w")
f.write(bin_string)
f.close()