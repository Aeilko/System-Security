# %% Imports and some static values
import numpy as np
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

# Useful utilities
sbox = (
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16)
hw = [bin(x).count("1") for x in range(256)]


def cov(x, y):
    return np.cov(x, y)[0][1]


# %% Import Data and some preparation
traces = np.load("../data_lab2/traces.npy")
pt = np.load("../data_lab2/plain.npy")
knownkey = np.load("../data_lab2/key.npy")

# Somehow an extra trace containing only 0s is loaded, remove it.
traces = np.delete(traces, 10000, 0)

# Split the data in train and attack data
a_traces = traces[9950:10000]
traces = np.delete(traces, range(9950, 10000), 0)
a_pt = pt[9950:10000]
pt = np.delete(pt, range(9950, 10000), 0)
a_knownkey = knownkey[9950:10000]
knownkey = np.delete(knownkey, range(9950, 10000), 0)


# print("Plaintext")
# print(pt)
# print(len(pt))
# print("Known Key")
# print(knownkey)
# print(len(knownkey))
# print("Traces")
# print(traces)
# print(len(traces))
# plt.plot(traces[0])
# plt.show()

# Note - we're only working with the first byte here
tempSbox = [sbox[pt[i][0] ^ knownkey[i][0]] for i in range(len(pt))]
tempHW = [hw[s] for s in tempSbox]

# Make 9 blank lists - one for each Hamming weight
tempTracesHW = [[] for _ in range(9)]

# Fill the lists
# print(len(tempHW))
for i in range(len(traces)):
    HW = tempHW[i]
    tempTracesHW[HW].append(traces[i])

# Switch to numpy arrays
tempTracesHW = [np.array(tempTracesHW[HW]) for HW in range(9)]

# print("Length TracesHW")
# print(len(tempTracesHW[8]))

# %% Find points of interest
tempMeans = np.zeros((9, len(traces[0])))
for i in range(9):
    tempMeans[i] = np.average(tempTracesHW[i], 0)

# plt.plot(tempMeans[2])
# plt.title("Averages")
# plt.grid()
# plt.show()


tempSumDiff = np.zeros(len(traces[0]))
for i in range(9):
    for j in range(i):
        tempSumDiff += np.abs(tempMeans[i] - tempMeans[j])

plt.plot(tempSumDiff)
plt.title("Sum of differences")
plt.grid()
plt.show()


POIs = []
numPOIs = 5
POIspacing = 5
for i in range(numPOIs):
    # Find the max
    nextPOI = tempSumDiff.argmax()
    POIs.append(nextPOI)

    # Make sure we don't pick a nearby value
    poiMin = max(0, nextPOI - POIspacing)
    poiMax = min(nextPOI + POIspacing, len(tempSumDiff))
    for j in range(poiMin, poiMax):
        tempSumDiff[j] = 0

print("POIs")
print(POIs)

# %% Covariance Matrices
meanMatrix = np.zeros((9, numPOIs))
covMatrix = np.zeros((9, numPOIs, numPOIs))
for HW in range(9):
    for i in range(numPOIs):
        # Fill in mean
        meanMatrix[HW][i] = tempMeans[HW][POIs[i]]
        for j in range(numPOIs):
            x = tempTracesHW[HW][:, POIs[i]]
            y = tempTracesHW[HW][:, POIs[j]]
            covMatrix[HW, i, j] = cov(x, y)

# print("meanMatrix")
# print(meanMatrix)
# print("covMatrix[0]")
# print(covMatrix[0])

# %% Perform the attack
# print("Attack traces")
# print(a_traces)
# print("Attack pt")
# print(a_pt)
# print("Attack knownkey")
# print(a_knownkey)

# Running total of log P_k
P_k = np.zeros(256)
for j in range(len(a_traces)):
    # Grab key points and put them in a small matrix
    a = [a_traces[j][POIs[i]] for i in range(len(POIs))]

    # Test each key
    for k in range(256):
        # Find HW coming out of sbox
        HW = hw[sbox[a_pt[j][0] ^ k]]

        # Find p_{k,j}
        rv = multivariate_normal(meanMatrix[HW], covMatrix[HW])
        p_kj = rv.pdf(a)

        # Add it to running total
        P_k[k] += np.log(p_kj)

    # Print our top 5 results so far
    # Best match on the right
    # print(P_k.argsort()[-5:])

print("Best guess")
print(P_k.argsort()[-5:][4])
print("Actual key")
print(a_knownkey[0])