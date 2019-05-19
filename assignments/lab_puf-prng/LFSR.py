from utils import to_binary_string, print_as_binary_string

class LFSR:

    # Create a new LFSR
    # taps should be a tuple containing the the locations of the taps, example: x^16 + x^14 + x^13 + x^11 + 1 => (16, 14, 13, 11)
    # Make sure the highest polynomial is the first one in the tuple
    def __init__(self, taps):
        self.taps = taps
        self.length = taps[0]
        self.state = [False] * taps[0]

    # Create a new LFSR
    # taps should be a tuple containing the the locations of the taps, example: x^16 + x^14 + x^13 + x^11 + 1 => (16, 14, 13, 11)
    # Make sure the highest polynomial is the first one in the tuple
    # seed should be an boolean array of length taps[0] with the current state of the bits (index 0 = left bit, max index is right bit)
    def __init__(self, taps, seed):
        self.taps = taps
        self.length = taps[0]
        self.state = seed

    # Returns the rightmost bit of this LFSR
    def next(self):
        out = self.state[self.length-1]
        new_bit = out

        for x in range(self.length-2, -1, -1):
            # Shift right
            self.state[x+1] = self.state[x]

            # Increase index by 1 because index starts at 0
            if x+1 in self.taps:
                # XOR the new bit
                new_bit = new_bit ^ self.state[x]

        self.state[0] = new_bit
        return out

    # Returns the next N bits from this LFSR
    def next_n(self, n):
        result = [False] * n

        for x in range(0, n):
            result[x] = self.next()

        return result
