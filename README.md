# System Security

## Lab: PUF & PRNG
### PRNG
For the PRNG we implemented LFSR, which can be found as a class in the [LFSR.py](assignments/prng/LFSR.py) file.

There is also a [test.py](assignments/prng/test.py) file, which is actually runnable.
Running this file will create a file called LFSRData, which contains 10 million bits from the LFSR.
This file can be used to perform randomness tests.

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

## Lab: Side Channel Attacks
The traces.npy file is missing from the data_lab2 folder since it is a very big file, so you have to place it there yourself.

### Pooled Template Attack
The pooled template attack can be performed by running the [AES_Pooled_Template.py](assignments/AES_Template/AES_Pooled_Template.py) file.
This will perform multiple pooled template attacks on different datasets en result in the guessing entropy.
The attack phaase always consists of 100 traces for consistency. 

### Countermeasurments
Run the file [RSA_attack.py](assignments/SC_countermeasures/RSA_attack.py) to create the timing graphs.