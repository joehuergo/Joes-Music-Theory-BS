def map_setup(v):
    v.pop()
    v.insert(0, 0)
    return v


class Filter:
    def __init__(self, _harmonics):
        self._modulus = _harmonics[-1]
        self.map = map_setup(_harmonics)

    def __call__(self, i):
        r = i % self.period()
        q = (i - r) / self.period()
        return q * self.modulus() + self.map[r]

    def __mul__(self, h):
        new_harmonics = []
        n = h.period() * self.period()
        for i in range(n):
            new_harmonics.append(h(i + 1))
        return Filter(new_harmonics)

    def period(self):
        return len(self.map)

    def modulus(self):
        return self._modulus


def mod(a, b):
    return ((a % b)+b) % b


tet12 = pow(2, 1.0 / 12.0)
