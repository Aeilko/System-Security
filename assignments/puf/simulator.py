import random

class PUF:
    def __init__(self, size):
        self.stages = [Stage() for _ in range(0, size)]       

    def run(self, challengeVector):
        d1 = 0
        d2 = 0
        isSwapped = False

        for index, stage in enumerate(self.stages):
            c = challengeVector[index]
            output = stage.run(c)

            d1 += output[int(isSwapped)]
            d2 += output[int(not isSwapped)]

            if c == 1:
                isSwapped = not isSwapped

        return 0 if d1 < d2 else 1

class Stage:
    def __init__(self):
        self.delayVector = [[random.uniform(0, 1), random.uniform(0, 1)], [random.uniform(0, 1), random.uniform(0, 1)]]

    def run(self, c):
        return (self.delayVector[0][c], self.delayVector[1][c])