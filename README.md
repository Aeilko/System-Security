# System Security

## Lab: PUF & PRNG
### PRNG


### PUF
##### Running an attack
The attack utilizes the TensorFlow ML library and Numpy. Install the libraries using `pip`:
`pip3 install tensorflow && pip3 install numpy`

Then, set the following variables:
- `PUF_SIZE`: The amount of stages for each PUF.
- `PUF_AMOUNT`: The amount of PUFs used. The outputs are XOR'ed.
- `TRAINING_SET_SIZE`: The size (amount of input/output pairs) of the training set
- `TEST_SET_SIZE`: The size (amount of input/output pairs) of the test set

The resulting accuracy (for training and test set) will be printed to the console.