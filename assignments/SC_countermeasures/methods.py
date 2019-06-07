import time

import matplotlib.pyplot as plt


def current_time():
    return time.perf_counter()


def square_and_multiply_graph(m, n, d):
    t = [0]*len(d)

    a = 1
    for i in range(len(d)-1, 0-1, -1):
        t1 = current_time()

        a = (a*a) % n
        if d[i]:
            a = (a*m) % n
        t2 = current_time()

        t[i] = t2-t1

    plt.plot(t)
    plt.title("Square and Multiply")
    plt.xticks(range(0, len(t)))
    plt.grid()
    plt.show()

    return a


def square_and_multiply_always_graph(m, n, d):
    time = []

    R0 = 1
    R1 = m
    i = len(d)-1
    t = False
    while i >= 0:
        t1 = current_time()

        R0 = (R0*R1) % n
        t = t ^ d[i]
        i = i-1 + (1 if t else 0)

        t2 = current_time()
        time.append(t2-t1)

    plt.plot(time)
    plt.title("Square and Multiply Always")
    plt.xticks(range(0, len(time)))
    plt.grid()
    plt.show()

    return R0


def montgomery_ladder_graph(m, n, d):
    t = [0]*len(d)

    R0 = 1
    R1 = m
    for i in range(len(d)-1, 0-1, -1):
        t1 = current_time()

        if d[i]:
            R0 = (R0*R1) % n
            R1 = (R1*R1) % n
        else:
            R1 = (R0*R1) % n
            R0 = (R0*R0) % n

        t2 = current_time()
        t[i] = t2-t1

    plt.plot(t)
    plt.title("Montgomery Ladder")
    plt.xticks(range(0, len(t)))
    plt.grid()
    plt.show()

    return R0


# Converts a number to a boolean array binary representation (index 0 is MSB)
def to_base2(n):
    x = bin(n)[2:]
    r = [False]*len(x)
    for i in range(0, len(x)):
        if x[i] == '1':
            r[i] = True
    return r