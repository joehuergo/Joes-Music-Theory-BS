from itertools import permutations
import math
import numpy as np


# class for individual pitch sets
class PSet:
    def __init__(self, pset):
        # pset is the pitch set. wow
        self.pset = pset
        # iseqset is a list of interval sequences derived from the pitch set
        # contains all intervals, from intervals between adjacent notes
        # to the interval between the top and bottom note
        self.iseqset = get_intervals(pset)

    def get_voicings(self):
        psets = [list(x) for x in permutations(self.pset)]
        for i in range(len(psets)):
            for b in range(len(psets[i]) - 1):
                while psets[i][b] >= psets[i][b + 1]:
                    psets[i][b + 1] += 12
        return PSetList([PSet(i) for i in psets])

    # wraps around negative pitches to wrap_octave, 0 wraps to first octave, 1 wraps to second, etc
    def apply_moveset(self, move_set, iterations, wrap_octave):
        if any(len(i) != len(self.pset) for i in move_set):
            print("Move sets must be same size as pitch set.")
            return self
        psets = [self.pset]
        for x in range(iterations):
            for i in range(len(move_set)):
                index = x * len(move_set) + i
                psets.append([])
                for j in range(len(move_set[i])):
                    psets[index + 1].append(psets[index][j] + move_set[i][j])
        psets = [normalize_negatives(i, wrap_octave) for i in psets]
        return PSetList([PSet(i) for i in psets])

    def permute_intervals(self):  # permutes set of intervals between adjacent notes
        iseq_permutations = [intervals_to_pitches(i) for i in permute_distinct(self.iseqset[0])]
        return PSetList([PSet(i) for i in iseq_permutations])

    def transpose(self, trans):
        self.pset = transpose_pitches(self.pset, trans)
        return self


# class for operations on list of PSet objects
class PSetList:
    def __init__(self, pset_list):
        self.pset_list = pset_list
        # moveset is a list of lists, as the name suggests these lists describe the difference
        # between successive pitch sets - think of this as a mathy way of representing a chord progression
        self.moveset = get_moveset([i.pset for i in self.pset_list])

    def filter_intervals(self, filt):
        if type(filt) != list:
            filt = [filt]
        pset_list = []
        intervals = [[i % 12 for i in flatten_list(j.iseqset)] for j in self.pset_list]
        for i in range(len(self.pset_list)):
            if not common_data(filt, intervals[i]):
                pset_list.append(self.pset_list[i])
        self.pset_list = pset_list
        return self

    def filter_interval_span(self, filt):
        pset_list = []
        iseq = [i.iseqset[0] for i in self.pset_list]
        for i in range(len(self.pset_list)):
            if not any(x > filt for x in iseq[i]):
                pset_list.append(self.pset_list[i])
        self.pset_list = pset_list
        return self

    def filter_pset_span(self, filt):
        pset_list = []
        for i in self.pset_list:
            if max(i.pset) - min(i.pset) <= filt:
                pset_list.append(PSet(i.pset))
        self.pset_list = pset_list
        return self

    def transpose(self, trans):
        for x in self.pset_list:
            x.pset = transpose_pitches(x.pset, trans)

    def sort(self):
        self.pset_list = sorted({tuple(x): x for x in self.pset_list}.values())
        return self

    def prune_copies(self):
        self.pset_list = prune_copies(self.pset_list)
        return self

    def normalize(self):
        self.pset_list = [PSet(normalize(i.pset)) for i in self.pset_list]
        return self

    def crop(self, start, end):
        self.pset_list = self.pset_list[start:end + 1]
        self.moveset = get_moveset([i.pset for i in self.pset_list])
        return self


# general use functions
def normalize(pset):
    if min(pset) < 0 or min(pset) > 11:
        sub = math.floor(min(pset) / 12) * 12
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


# wraps around negative pitches to wrap_octave, 0 wraps to first octave, 1 wraps to second, etc
def normalize_negatives(pset, wrap_octave):
    if min(pset) < 0:
        sub = math.floor(min(pset) / 12) * (wrap_octave * 12)
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


def permute_distinct(pset):
    perm_iseq = []
    for i in permutations(pset):
        if list(i) not in perm_iseq:
            perm_iseq.append(list(i))
    return perm_iseq


def intervals_to_pitches(iseq):
    perm_pset = []
    p = 0
    perm_pset.append(0)
    for j in iseq:
        p += j
        perm_pset.append(p)
    return perm_pset


def get_intervals(pset):
    iseqset = []
    for i in range(1, len(pset)):
        iseq = []
        for j in range(len(pset) - i):
            iseq.append(pset[i + j] - pset[j])
        iseqset.append(iseq)
    return iseqset


def get_moveset(pset_list):
    moveset = []
    for i in range(len(pset_list) - 1):
        difference = list(np.array(pset_list[i + 1]) - np.array(pset_list[i]))
        moveset.append(difference)
    return moveset


def transpose_pitches(pset, trans):
    trans_pset = []
    for i in pset:
        trans_pset.append(i + trans)
    return trans_pset


def common_data(list1, list2):
    result = False
    # traverse in the 1st list
    for x in list1:
        # traverse in the 2nd list
        for y in list2:
            # if one common
            if x == y:
                result = True
                return result
    return result


def flatten_list(inp):
    output = []
    for i in inp:
        if type(i) == list:
            output.extend(flatten_list(i))
        else:
            output.append(i)
    return output


def prune_copies(inp):
    list_len = len(inp)
    i = 0
    while i < list_len:
        j = i + 1
        while j < list_len:
            if inp[i] == inp[j]:
                inp.reverse()
                inp.remove(inp[j])
                inp.reverse()
                list_len -= 1
                j -= 1
            j += 1
        i += 1
    return inp


def depth_count(x):
    return int(isinstance(x, list)) and len(x) and 1 + max(map(depth_count, x))
