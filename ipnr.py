from itertools import permutations
from dataclasses import dataclass
from collections import deque


def findPartitionsUtil(arr, index, number, reducedNum, partition_set):
    if reducedNum < 0:
        return
    if reducedNum == 0:
        partition_set.append(arr[:index])
        return
    prev = 1 if (index == 0) else arr[index - 1]
    for k in range(prev, number + 1):
        arr[index] = k
        findPartitionsUtil(arr, index + 1, number, reducedNum - k, partition_set)


def partition(n):
    partition_set = []
    arr = [0] * n
    findPartitionsUtil(arr, 0, n, n, partition_set)
    return partition_set


def permute_distinct(pset):
    perm_iset = []
    for i in permutations(pset):
        if list(i) not in perm_iset:
            perm_iset.append(list(i))
    return perm_iset


def count_elements(lst):
    output = []
    for i in set(lst):
        output.append(lst.count(i))
    return output


@dataclass
class Cell:
    next: int
    prev: int


class Sawada:
    def __init__(self, combination):
        self.necklaces = []
        if not combination:
            return
        self.head = 0
        self.key = {}
        combo_set = list(sorted(set(combination)))
        for i in range(len(combo_set)):
            self.key[i] = combo_set[i]
        lst_count = count_elements(combination)
        self.num_map = [i for i in range(len(set(combination)) + 1)]
        self.K = len(set(combination))
        self.N = len(combination)
        self.avail = [Cell(0, 0) for i in range(self.K + 2)]
        self.a = [0] * (self.N + 1)
        self.run = [0] * (self.N + 1)
        self.num = [lst_count[i - 1] for i in range(1, len(set(combination)) + 1)]
        self.num.insert(0, 0)
        self.begin()
        self.necklaces = [[self.key[x] for x in y] for y in self.necklaces]
        self.necklaces.reverse()

    def remove(self, i):
        if i == self.head:
            self.head = self.avail[i].next
        p = self.avail[i].prev
        n = self.avail[i].next
        self.avail[p].next = n
        self.avail[n].prev = p
        return self

    def add(self, i):
        p = self.avail[i].prev
        n = self.avail[i].next
        self.avail[p].next = i
        self.avail[n].prev = i
        if self.avail[i].prev == self.K + 1:
            self.head = i
        return self

    def result(self):
        h = []
        for j in range(1, self.N + 1):
            h.append(self.num_map[self.a[j]] - 1)
        self.necklaces.append(h)
        return self

    def gen(self, t, p, s):
        if self.num[self.K] == self.N - t + 1:
            if (self.num[self.K] == self.run[t - p]) & (self.N % p == 0):
                self.result()
            elif (self.num[self.K] == self.run[t - p]) & (self.N == p):
                self.result()
            elif self.num[self.K] > self.run[t - p]:
                self.result()
        elif self.num[1] != self.N - t + 1:
            j = self.head
            s2 = s
            while j >= self.a[t - p]:
                self.run[s] = t - s
                self.a[t] = j

                self.num[j] -= 1
                if self.num[j] == 0:
                    self.remove(j)

                if j != self.K:
                    s2 = t + 1
                if j == self.a[t - p]:
                    self.gen(t + 1, p, s2)
                else:
                    self.gen(t + 1, t, s2)

                if self.num[j] == 0:
                    self.add(j)
                self.num[j] += 1

                j = self.avail[j].next
            self.a[t] = self.K
        return self

    def begin(self):
        for j in range(self.K + 1, -1, -1):
            self.avail[j].next = j - 1
            self.avail[j].prev = j + 1
        self.head = self.K

        for j in range(1, self.N + 1):
            self.a[j] = self.K
            self.run[j] = 0

        self.a[1] = 1
        self.num[1] -= 1
        if self.num[1] == 0:
            self.remove(1)

        self.gen(2, 1, 2)
        return self


def get_necklaces(a):
    return Sawada(a).necklaces


def get_rotations(a):
    if len(set(a)) == 1 or not a:
        return [a]
    rots = []
    a_deque = deque(a)
    for i in a:
        rots.append(list(a_deque))
        a_deque.rotate(-1)
    return rots


key_map = {
    1: 'm2',
    2: 'M2',
    3: 'm3',
    4: 'M4',
    5: 'P4',
    6: 'TT',
    7: 'P5',
    8: 'm6',
    9: 'M6',
    10: 'm7',
    11: 'M7',
    12: 'Octave'
}


def get_partition_set(n):
    # partition_set = [[key_map[x] for x in i] for i in partition(n)]
    partition_set = partition(n)
    pset = []
    for i in partition_set:
        necklaces = get_necklaces(i)
        neck_set = []
        for j in necklaces:
            neck_set.append(get_rotations(j))
        pset.append(neck_set)
    return pset


def print_partition_set(partition_set, n):
    print("Partitions of " + str(n) + ":")
    for i in range(len(partition_set)):
        print("\tPartition " + str(i+1) + ":")
        for j in range(len(partition_set[i])):
            print("\t\tNecklace " + str(j+1) + ": ")
            for h in partition_set[i][j]:
                print("\t\t\t" + str(h))
    return


num = 12

part_set = get_partition_set(num)

print_partition_set(part_set, num)
