import simulator
import random
import tensorflow as tf
from tensorflow.keras import layers
from numpy import array

# Constants
pufSize = 32
trainingSetSize = 30000
testSetSize = 70000

puf = simulator.PUF(pufSize)

def generateChallengeVector(size):
    return [random.randint(0, 1) for _ in range(0, size)]

def generateDataset(size, pufSize):
    x = []
    y = []

    for _ in range(0, size):
        currentChallengeVector = generateChallengeVector(pufSize)
        output = puf.run(currentChallengeVector)

        x.append(currentChallengeVector)
        y.append(output)

    return array(x), array(y)

model = tf.keras.Sequential()

# Input layer
model.add(layers.Dense(pufSize, activation='relu'))

model.add(layers.Dense(pufSize, activation='relu'))

# Output layer
model.add(layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
xTrain, yTrain = generateDataset(trainingSetSize, pufSize)
model.fit(xTrain, yTrain, epochs=30, batch_size=10)

# Evaluate on a new test set
xTest, yTest = generateDataset(testSetSize, pufSize)
scores = model.evaluate(xTest, yTest)

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
