from itertools import permutations
import math


class PSetList:
    def __init__(self, pset_list):
        self.pset_list = pset_list

    def filter_intervals(self, filt):
        if type(filt) != list:
            filt = [filt]
        pset_list = []
        intervals = [[i % 12 for i in flatten_list(i.isets)] for i in self.pset_list]
        for i in range(len(self.pset_list)):
            if not common_data(filt, intervals[i]):
                pset_list.append(self.pset_list[i])
        self.pset_list = pset_list
        return self

    def filter_interval_span(self, filt):
        pset_list = []
        iset = [i.isets[0] for i in self.pset_list]
        for i in range(len(self.pset_list)):
            if not any(x > filt for x in iset[i]):
                pset_list.append(self.pset_list[i])
        self.pset_list = pset_list
        return self

    def filter_pset_span(self, filt):
        pset_list = []
        for i in self.pset:
            if max(i) - min(i) <= filt:
                pset_list.append(i)
        self.pset_list = pset_list
        return self

    def sort(self):
        self.pset_list = sorted({tuple(x): x for x in self.pset_list}.values())
        return self

    def prune_copies(self):
        self.pset_list = prune_copies(self.pset_list)
        return self


# class for individual pitch sets
class PSet:
    def __init__(self, pset):
        # pset is the pitch set. wow
        self.pset = pset

        # isets is a list of interval sets derived from the pitch set
        # contains all intervals, from intervals between adjacent notes
        # to the interval between the top and bottom note
        isets = []
        for i in range(1, len(self.pset)):
            iset = []
            for j in range(len(self.pset) - i):
                iset.append(self.pset[i + j] - self.pset[j])
            isets.append(iset)
        self.isets = isets

    def get_voicings(self):
        psets = [list(x) for x in permutations(self.pset)]
        for i in range(len(self.pset)):
            for b in range(len(self.pset[i]) - 1):
                while self.pset[i][b] >= self.pset[i][b + 1]:
                    self.pset[i][b + 1] += 12
        return PSetList(psets)

    def permute_intervals(self):  # permutes set of intervals between adjacent notes
        iset_permutationss = [intervals_to_pitches(i) for i in permute(self.isets[0])]
        return PSetList(iset_permutationss)


def normalize_set(pset):
    if min(pset) < 0 or min(pset) > 11:
        sub = math.floor(min(pset) / 12) * 12
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


def permute(pset):
    perm_iset = []
    for i in permutations(pset):
        if list(i) not in perm_iset:
            perm_iset.append(list(i))
    return perm_iset


def intervals_to_pitches(iset):
    perm_pset = []
    p = 0
    perm_pset.append(0)
    for j in iset:
        p += j
        perm_pset.append(p)
    return perm_pset


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


# some chord naming stuff
def note_name(mpv):
    mdict = {
        0: "C",
        1: "Db",
        2: "D",
        3: "Eb",
        4: "E",
        5: "F",
        6: "F#",
        7: "G",
        8: "Ab",
        9: "A",
        10: "Bb",
        11: "B"
    }
    return mdict[mpv % 12] + str(math.floor(mpv / 12) - 1)

