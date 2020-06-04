from itertools import permutations
import math


a = [
    [0, 2, 4, 9],
    [0, 2, 4, 9],
    [-3, 0, 4, 7],
    [21, 4, 8, 4],
    [4, 4, 8, 21]
]


def note_name(mpv):
    return mdict[mpv % 12] + str(math.floor(mpv / 12) - 1)


mdict = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B"
}


# works on any-dimensional list
def prune_copies(inp):
    list_len = len(inp)
    i = 0
    while i < list_len:
        val1 = inp[i]
        j = i + 1
        while j < list_len:
            val2 = inp[j]
            if val1 == val2:
                inp.reverse()
                inp.remove(val2)
                inp.reverse()
                list_len -= 1
                j -= 1
            j += 1
        i += 1
    return inp


# counts the depth of a list
def depth_count(x):
    return int(isinstance(x, list)) and len(x) and 1 + max(map(depth_count, x))


# operates on list of pitch sets
def sort_psets(psets):
    return sorted({tuple(x): x for x in psets}.values())


# operates on a 1-dimensional list
def normalize_set(pset):
    if min(pset) < 0 or min(pset) > 11:
        sub = math.floor(min(pset) / 12) * 12
        for i in range(len(pset)):
            pset[i] = pset[i] - sub
    return pset


def get_voicings(pset):
    voicings = [list(x) for x in permutations(pset)]
    for i in range(len(voicings)):
        for b in range(len(voicings[i]) - 1):
            while voicings[i][b] >= voicings[i][b + 1]:
                voicings[i][b + 1] += 12
    return voicings


def get_intervals(pset):
    big_iset = []
    for i in range(1, len(pset)):
        lil_iset = []
        for j in range(len(pset) - i):
            lil_iset.append(pset[i + j] - pset[j])
        big_iset.append(lil_iset)
    return big_iset


def get_permuted_intervals(iset):
    perm_iset = []
    for i in permutations(iset):
        if list(i) not in perm_iset:
            perm_iset.append(list(i))
    return perm_iset


def get_pitches_from_intervals(iset):
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
