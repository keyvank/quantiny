def scale(mat, s):
    return [[v * s for v in row] for row in mat]


def kron(a, b):
    res = []
    for a_row in a:
        res_row = []
        for v in a_row:
            res_row.append(scale(b, v))
        res.append(res_row)

    final = []
    for row in res:
        rows = [list() for _ in range(len(row[0]))]
        for mat in row:
            for ind, mat_row in enumerate(mat):
                rows[ind].extend(mat_row)
        final.extend(rows)
    return final


def identitiy(bits):
    return [[1 if j == i else 0 for j in range(2**bits)] for i in range(2**bits)]


def not_gate():
    return [[0, 1], [1, 0]]


def cnot_gate():
    return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]


def swap_gate():
    return [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]


import math


def hadamard_gate():
    sqrt2inv = 1 / math.sqrt(2)
    return [[sqrt2inv, sqrt2inv], [sqrt2inv, -sqrt2inv]]


def not_on(i, bits):
    return kron(kron(identitiy(i), not_gate()), identitiy(bits - i - 1))


def hadamard_on(i, bits):
    return kron(kron(identitiy(i), hadamard_gate()), identitiy(bits - i - 1))


import math
import random


class QuantumState:
    def __init__(self, bits):
        self.bits = bits
        self.values = [0 + 0j] * (2**bits)
        self.values[0] = 1 + 0j

    def is_unitary(self):
        return math.isclose(abs(sum(map(lambda v: v * v, self.values))), 1)

    def apply(self, gate):
        res = []
        for row in gate:
            res.append(sum([row[i] * self.values[i] for i in range(len(self.values))]))
        self.values = res

    def observe(self):
        dice = random.random()
        accum = 0
        for i, p in enumerate(self.values):
            accum += abs(p * p)
            if dice < accum:
                s = bin(i)[2:]
                while len(s) < self.bits:
                    s = "0" + s
                return s
        raise Exception()

    def sample(self, times=1000):
        states = {}
        for _ in range(times):
            v = self.observe()
            if v not in states:
                states[v] = 0
            states[v] += 1
        return states


s = QuantumState(3)
print(s.sample())
exit(0)
state = QuantumState(2)
print(state.is_unitary())
state.apply(hadamard_on(0, 2))
print(state.is_unitary())
state.apply(cnot_gate())
print(state.is_unitary())

samples = 1000
states = {}
for _ in range(samples):
    v = state.observe()
    if v not in states:
        states[v] = 0
    states[v] += 1
print(states)
