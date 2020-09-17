from Filter import *


def mod(a, b):
    return ((a % b)+b) % b


tet12 = pow(2, 1.0 / 12.0)


class Field:

    def __init__(self, _multipliers, _fundamental):
        self.multipliers = _multipliers
        self.fundamental = _fundamental

    def __call__(self, i):
        return self.multiplier(i) * self.fundamental

    def multiplier(self, i):
        note = int(mod(i, self.modulus()))
        octave = (i - note) / self.modulus()
        return pow(2, octave) * self.multipliers[note]

    def modulus(self):
        return len(self.multipliers)

    def filter(self, fil):
        f = Filter(fil)
        new_multipliers = []
        n = f.period()
        for i in range(n):
            new_multipliers.append(self.multiplier(f(i)))
        return Field(new_multipliers, self.fundamental)


def n_tet(n, fundamental):
    r = pow(2, 1.0 / n)
    multipliers = []
    for i in range(n):
        multipliers.append(pow(r, i))
    return Field(multipliers, fundamental)


Chromatic = n_tet(12, 440)
Lydian = Chromatic.filter([2, 4, 6, 7, 9, 11, 12])
Ionian = Chromatic.filter([2, 4, 5, 7, 9, 11, 12])
Mixolydian = Chromatic.filter([2, 4, 5, 7, 9, 10, 12])
Dorian = Chromatic.filter([2, 3, 5, 7, 9, 10, 12])
Aeolian = Chromatic.filter([2, 3, 5, 7, 8, 10, 12])
Phrygian = Chromatic.filter([1, 3, 5, 7, 8, 10, 12])
Locrian = Chromatic.filter([1, 3, 5, 6, 8, 10, 12])
