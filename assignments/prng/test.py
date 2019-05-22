from LFSR import LFSR
from utils import to_binary_string

taps = (16, 14, 13, 11)
state = [True, False, False, True, True, True, False, True, False, True, True, False, False, True, True, True]

l = LFSR(taps, state)

print(to_binary_string(l.next_n(32)))