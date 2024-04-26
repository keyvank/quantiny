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


def swap_gate():
    return [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]


def not_on(i, bits):
    return kron(kron(identitiy(i), not_gate()), identitiy(bits - i - 1))


class ClassicalState:
    def __init__(self, bits):
        self.bits = bits
        self.value = [0] * (2**bits)
        self.value[0] = 1

    def apply(self, gate):
        res = []
        for row in gate:
            v = 0
            for i in range(len(self.value)):
                v += row[i] * self.value[i]
            res.append(v)
        self.value = res

    def to_bits(self):
        s = bin(self.value.index(1))[2:]
        while len(s) < self.bits:
            s = "0" + s
        return s


state = ClassicalState(3)

state.apply(not_on(2, 3))
state.apply(not_on(1, 3))
state.apply(not_on(0, 3))
state.apply(not_on(1, 3))

print(state.to_bits())
