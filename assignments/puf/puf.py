import random

class PUF:
    def __init__(self, size):
        self.stages = [Stage() for _ in range(0, size)]       

    def run(self, challenge_vector):
        d1 = 0
        d2 = 0
        swap = False

        for index, stage in enumerate(self.stages):
            # Get the current challenge from the challenge vector
            c = challenge_vector[index]

            # Run the current stage
            output = stage.run(c)

            # Add the delays for each line
            d1 += output[int(swap)]
            d2 += output[int(not swap)]

            # Update the swap variable if the lines swapped
            if c == 1:
                swap = not swap

        # The arbiter
        return 0 if d1 < d2 else 1

class Stage:
    def __init__(self):
        self.delay_vector = [[random.uniform(0, 1), random.uniform(0, 1)], [random.uniform(0, 1), random.uniform(0, 1)]]

    def run(self, c):
        # Return the values from the delay vector
        return self.delay_vector[0][c], self.delay_vector[1][c]
