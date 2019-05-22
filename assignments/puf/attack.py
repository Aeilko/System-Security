import puf
import random
import functools
import operator
import tensorflow as tf
from tensorflow.keras import layers
from numpy import array

# The PUF size (number of stages)
PUF_SIZE = 32

# The amount of PUFs (arbiter output is XOR'd)
PUF_AMOUNT = 8

# The size of the training set
TRAINING_SET_SIZE = 30000

# The size of the test set
TEST_SET_SIZE = 70000

# Generates a random challenge vector
def generate_challenge_vector(size):
    return [random.randint(0, 1) for _ in range(0, size)]

# Generates a dataset
def generate_dataset(pufs, dataset_size, puf_size):
    input_list = []
    output_list = []

    # For XOR'ing outputs
    foldr = lambda func, acc, xs: functools.reduce(lambda x, y: func(y, x), xs[::-1], acc)

    for _ in range(0, dataset_size):
        challenge_vector = generate_challenge_vector(puf_size)

        outputs = []

        for puf in pufs:
            output = puf.run(challenge_vector)
            outputs.append(output)

        output = foldr(operator.xor, 0, outputs)

        input_list.append(challenge_vector)
        output_list.append(output)

    return array(input_list), array(output_list)

def main():
    # Create the PUFs
    pufs = []
    for _ in range(0, PUF_AMOUNT):
        pufs.append(puf.PUF(PUF_SIZE))

    model = tf.keras.Sequential()

    # Input layer
    model.add(layers.Dense(PUF_SIZE, activation='relu'))

    model.add(layers.Dense(PUF_SIZE, activation='relu'))

    # Output layer
    model.add(layers.Dense(1, activation='sigmoid'))

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    train_input, train_output = generate_dataset(pufs, TRAINING_SET_SIZE, PUF_SIZE)
    model.fit(train_input, train_output, epochs=30, batch_size=10)

    # Evaluate on a new test set
    test_input, test_output = generate_dataset(pufs, TEST_SET_SIZE, PUF_SIZE)
    scores = model.evaluate(test_input, test_output)

    # Print the test set accuracy
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

main()
